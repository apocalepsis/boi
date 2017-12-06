import sys

from config import properties

from lib.users.dao.linux import Implementation as LinuxDAO
from lib.users.dao.zeppelin import Implementation as ZeppelinDAO

from lib.users.validator.linux import Implementation as LinuxValidator

params = {
    "attr-name" : None,
    "attr-value" : None
}

def display_help():
    print("""
Usage:
    boi-cli.py users delete-user [options]

Available Options:
    [parameter]
        Is an immediate action

Available Parameters:
    [-h | -help]
        Type: bool
        Required: no
    [-attr-name <username|uid|gid>]
        Type: choice
        Required: yes
    [-attr-value <value>]
        Type: string
        Required: yes
    """)

def run(args):

    if len(args) == 0:
        display_help()
        sys.exit(0)

    # MAPPINGS

    while len(args) > 0:

        p = None

        try:
            p = args.pop(0)
        except:
            print("[ERROR] Unable to read parameter.")
            sys.exit(1)

        if p in ["-h","-help"]:
            display_help()
            sys.exit(0)

        elif p in ["-attr-name"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["attr-name"] = v

        elif p in ["-attr-value"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["attr-value"] = v

        else:
            print("[ERROR] Invalid parameter <{0}>".format(p))
            sys.exit(1)

    validator = LinuxValidator()

    p = params["attr-name"]
    if not validator.is_valid_attr_name(p):
        print("[ERROR] Invalid value <{}> for parameter <attr-name>".format(p))
        sys.exit(1)

    p = params["attr-value"]
    if not validator.is_valid_attr_value(p):
        print("[ERROR] Invalid value <{}> for parameter <attr-value>".format(p))
        sys.exit(1)

    linux_user_dao = LinuxDAO(
        properties.boi_linux_db_host,
        properties.boi_linux_db_name,
        properties.boi_linux_db_user,
        properties.boi_linux_db_password
    )

    zeppelin_user_dao = ZeppelinDAO(
        properties.boi_zeppelin_db_host,
        properties.boi_zeppelin_db_name,
        properties.boi_zeppelin_db_user,
        properties.boi_zeppelin_db_password
    )

    dao_response = linux_user_dao.get_by_attr(params["attr-name"],params["attr-value"])

    for user in dao_response["users"]:

        try:
            zeppelin_user_dao.delete_by_attr("username",user.get_username())
        except Exception as e:
            print("[ERROR] {}".format(e))

        try:
            linux_user_dao.delete_by_attr("username",user.get_username())
        except Exception as e:
            print("[ERROR] {}".format(e))
