# BOI Properties
# ======================================
aws_region="us-west-2"

boi_s3_bucket_name="aws.boi"
boi_s3_website_bucket_name="awsome.website"

# R53 Properties
# ======================================
r53_hosted_zone_id="Z1NTB46Y263HW7"
r53_resource_record_set_name="boi.awsome.website"

# SES Properties
# ======================================
ses_email_from="meet.falej@gmail.com"
ses_email_to=["alejandro.x.flores@gmail.com"]
ses_email_subject="[BOI] EMR Cluster Deploy Notification"

# LOGGING Properties
# ======================================
deploy_logging_dir="/var/log/boi"
undeploy_logging_dir="/var/log/boi"

# EMR Properties
# ======================================
emr_name="emr_boi"
emr_s3_logging_uri="s3://aws.boi.logs/emr"
emr_slave_instance_count=2
emr_ec2_key_name="Oregon"
emr_keep_job_flow_alive_when_no_steps=True
emr_termination_protected=False
emr_release_label="emr-5.9.0"
emr_subnet_id="subnet-49b9a212"
emr_master_instance_type="m3.xlarge"
emr_master_instance_security_group="sg-3089284c"
emr_master_instance_additional_security_groups=["sg-5c862720"]
emr_slave_instance_type="m3.xlarge"
emr_slave_instance_security_group="sg-7a8a2b06"
emr_slave_instance_additional_security_groups=["sg-5c862720"]
emr_visible_to_all_users=True
emr_job_flow_role="EMR_EC2_DefaultRole"
emr_service_role="EMR_DefaultRole"
emr_steps=[
    {
        "Name" : "boi-install",
        "ActionOnFailure" : "CONTINUE",
        "HadoopJarStep" : {
            "Jar" : "s3://us-east-1.elasticmapreduce/libs/script-runner/script-runner.jar",
            "Args" : [
                "s3://aws.boi/install/boi-install.sh",
                "-s3uri","s3://aws.boi/install",
                "-new"
            ]
        }
    }
]
emr_bootstrap_actions=[
    {
        "Name" : "jupyter-install",
        "ScriptBootstrapAction" : {
            "Path" : "s3://aws.boi/install/3p/jupyter/install-jupyter-emr5.sh",
            "Args" : [
                "--ds-packages",
                "--ml-packages",
                "--python-packages",
                "ggplot nilearn",
                "--port","8585",
                "--user","oddjupy",
                "--password","boi2017",
                "--jupyterhub",
                "--jupyterhub-port","8686",
                "--cached-install",
                "--python3"
            ]
        }
    },
    {
        "Name" : "rstudio-install",
        "ScriptBootstrapAction" : {
            "Path" : "s3://aws.boi/install/3p/rstudio/rstudio_sparklyr_emr5.sh",
            "Args" : [
                "--sparklyr",
                "--rstudio",
                "--shiny",
                "--sparkr",
                "--rexamples",
                "--plyrmr",
                "--cloudyr",
                "--user","oddstudio",
                "--user-pw","boi2017"
            ]
        }
    }
]
