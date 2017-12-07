import sys
import re
import time
import boto3
import logging

from time import strftime
from config import properties

logger = logging.getLogger("boi")
logger.setLevel(logging.INFO)

logging_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
logging_filename = "boi-undeploy_{}.log".format(strftime("%Y-%m-%d_%H-%M-%S"))

logging_file_handler = logging.FileHandler("{}/{}".format(properties.undeploy_logging_dir,logging_filename))
logging_file_handler.setFormatter(logging_formatter)
logger.addHandler(logging_file_handler)

logging_stdout_handler = logging.StreamHandler(sys.stdout)
logging_stdout_handler.setFormatter(logging_formatter)
logger.addHandler(logging_stdout_handler)

do_terminate_cluster = False
do_set_dns_to_none = False
do_change_website = False
do_send_email_notification = False

def terminate_cluster():

    response = {
        "status_code" : 0,
        "payload" : None
    }

    emr_client = boto3.client("emr",region_name=properties.aws_region)
    emr_response = None

    job_flow_id = None

    try:

        emr_response = emr_client.list_clusters(
            ClusterStates = ["WAITING"]
        )
    except Exception as e:
        response["status_code"] = 1
        response["payload"] = e
        logger.error(e)
    else:
        for emr_cluster in emr_response["Clusters"]:
            if emr_cluster["Name"] == properties.emr_name:
                job_flow_id = emr_cluster["Id"]

    if job_flow_id:

        try:

            emr_client.terminate_job_flows(
                JobFlowIds = [job_flow_id]
            )
        except Exception as e:
            response["status_code"] = 1
            response["payload"] = e
            logger.error(e)
        else:
            while True:
                time.sleep(5)
                emr_response = emr_client.describe_cluster(ClusterId = job_flow_id)
                state = emr_response["Cluster"]["Status"]["State"]
                logger.info("EMR Cluster {} is {}".format(job_flow_id,state))
                response["payload"] = emr_response["Cluster"]
                if state == "TERMINATED":
                    break
                if state == "TERMINATED_WITH_ERRORS":
                    response["status_code"] = 1
                    break

    return response

def set_dns_to_none(emr_cluster):

    response = {
        "status_code" : 0,
        "payload" : None
    }

    emr_cluster_ip = None

    if emr_cluster:
        m = re.search("^ec2-(\d+)-(\d+)-(\d+)-(\d+).*\.amazonaws\.com$",
            emr_cluster["MasterPublicDnsName"])
        if m:
            emr_cluster_ip = m.group(1) + "." + m.group(2) + "." + m.group(3) + "." + m.group(4)

    if emr_cluster_ip:
        r53_client = boto3.client('route53',region_name=properties.aws_region)
        r53_response = None
        try:
            r53_response = r53_client.change_resource_record_sets(
                HostedZoneId = properties.r53_hosted_zone_id,
                ChangeBatch = {
                    "Changes" : [
                        {
                            "Action" : "DELETE",
                            "ResourceRecordSet" : {
                                "Name" : properties.r53_resource_record_set_name,
                                "Type" : "A",
                                "TTL" : 60,
                                "ResourceRecords" : [
                                    {"Value" : emr_cluster_ip}
                                ]
                            }
                        }
                    ]
                }
            )
            print("R53 RESPONSE: {}".format(r53_response))
        except Exception as e:
            response["status_code"] = 1
            response["payload"] = e
            logger.error(e)
        else:
            change_info = r53_response["ChangeInfo"]
            while True:
                time.sleep(5)
                try:
                    r53_response = r53_client.get_change(
                        Id = change_info["Id"]
                    )
                    status = r53_response["ChangeInfo"]["Status"]
                    logger.info("Change Status {} is {}".format(change_info["Id"],status))
                    if status == "INSYNC":
                        response["payload"] = r53_response
                        break
                except Exception as e:
                    response["status_code"] = 1
                    response["payload"] = e
                    logger.error(e)
                    break

    return response

def change_website():

    response = {
        "status_code" : 0,
        "payload" : None
    }

    s3_client = boto3.resource('s3',region_name=properties.aws_region)

    tgt_bucket_name = properties.boi_s3_website_bucket_name
    tgt_obj_key = "index.html"

    src_bucket_name = properties.boi_s3_bucket_name
    src_obj_key = "deploy/html/unavailable.html"

    try:
        s3_client.Object(tgt_bucket_name,tgt_obj_key).copy_from(CopySource = src_bucket_name+'/'+src_obj_key)
    except Exception as e:
        response["status_code"] = 1
        response["payload"] = e
        logger.error(e)
    else:
        response["payload"] = "UNAVAILABLE"

    return response

def send_email(body_text,body_html):

    response = {
        "status_code" : 0,
        "payload" : None
    }

    ses_client = boto3.client("ses",region_name=properties.aws_region)

    ses_response = None

    try:

        ses_response = ses_client.send_email(
            Source = properties.ses_email_from,
            Destination = {
                "ToAddresses" : properties.ses_email_to
            },
            Message = {
                "Body" : {
                    "Html" : {
                        "Charset" : "utf-8",
                        "Data" : body_html
                    },
                    "Text" : {
                        "Charset" : "utf-8",
                        "Data" : body_text
                    }
                },
                "Subject" : {
                    "Charset" : "utf-8",
                    "Data" : properties.ses_email_subject
                }
            }
        )

    except Exception as e:
        response["status_code"] = 1
        response["payload"] = e
        logger.error(e)
    else:
        response["payload"] = ses_response

    return response

# :: MAIN ::

do_terminate_cluster = True

emr_response = None
if do_terminate_cluster:
    logger.info(">>> Terminating cluster ...")
    emr_response = terminate_cluster()
    if emr_response["status_code"] == 0:
        logger.info(emr_response)
        do_set_dns_to_none = True
    else:
        logger.error(emr_response)
    logger.info("<<< Done.")

dns_response = None
if do_set_dns_to_none:
    logger.info(">>> Setting up DNS ...")
    dns_response = set_dns_to_none(emr_response["payload"])
    if dns_response["status_code"] == 0:
        logger.info(dns_response)
        do_change_website = True
    else:
        logger.error(dns_response)
    logger.info("<<< Done.")

website_response = None
if do_change_website:
    logger.info(">>> Setting up website ...")
    website_response = change_website()
    if website_response["status_code"] == 0:
        logger.info(website_response)
        do_send_email_notification = True
    else:
        logger.error(website_response)
    logger.info("<<< Done.")

if do_send_email_notification:
    logger.info(">>> Sending notification email ...")
    email_body_text = "EMR Response:\n{}\n\nR53 Response:\n{}\n\n".format(emr_response,dns_response)
    email_body_html = "EMR Response:<br/>{}<br/><br/>R53 Response:<br/>{}<br/><br/>".format(emr_response,dns_response)
    ses_response = send_email(email_body_text,email_body_html)
    logger.info("<<< Done.")
