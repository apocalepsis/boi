import sys

from config import properties

from lib.users.model.linux import Implementation as LinuxUser
from lib.users.model.zeppelin import Implementation as ZeppelinUser

from lib.users.dao.linux import Implementation as LinuxDAO
from lib.users.dao.zeppelin import Implementation as ZeppelinDAO

from lib.users.validator.linux import Implementation as LinuxValidator
from lib.utils import cipher

params = {
    "username" : None,
    "password" : None,
    "uid" : None,
    "gid" : None
}

def display_help():
    print("""
Usage:
    boi-cli.py users create-user [options]

Available Options:
    [parameter]
        Is an immediate action

Available Parameters:
    [-h | -help]
        Type: bool
        Required: no
    [-username <value>]
        Type: string
        Required: yes
        Notes:
            * Must be between <8-20> characters length.
            * Only alphanumeric and underscore characters are accepted.
    [-password <value>]
        Type: string
        Required: yes
        Notes:
            * Must be between <8-20> characters length.
            * Must include at least one of the special characters #$@!%&*?
            * Must include at least one upper and lower case letters
            * Must include at least one digit
    [-uid <value>]
        Type: integer
        Required: yes
        Notes:
            * Must be between <4-8> digits length.
    [-gid <value>]
        Type: integer
        Required: yes
        Notes:
            * Must be between <4-8> digits length.
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
            print("[ERROR] Unable to read option.")
            sys.exit(1)

        if p in ["-h","-help"]:
            display_help()
            sys.exit(0)

        elif p in ["-username"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["username"] = v

        elif p in ["-password"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["password"] = v

        elif p in ["-uid"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["uid"] = v

        elif p in ["-gid"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["gid"] = v

        else:
            print("[ERROR] Invalid parameter <{0}>".format(p))
            sys.exit(1)

    validator = LinuxValidator()

    p = params["username"]
    if not validator.is_valid_username(p):
        print("[ERROR] Invalid value <{}> for parameter <username>".format(p))
        sys.exit(1)

    p = params["password"]
    if not validator.is_valid_password(p):
        print("[ERROR] Invalid value <{}> for parameter <password>".format(p))
        sys.exit(1)

    p = params["uid"]
    if not validator.is_valid_uid(p):
        print("[ERROR] Invalid value <{}> for parameter <uid>".format(p))
        sys.exit(1)

    p = params["gid"]
    if not validator.is_valid_gid(p):
        print("[ERROR] Invalid value <{}> for parameter <gid>".format(p))
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

    try:
        user = LinuxUser(params["username"],cipher.aes.encrypt(params["password"]).decode("utf-8"),params["uid"],params["gid"])
        linux_user_dao.save(user)
    except Exception as e:
        print("[ERROR] {}".format(e))
    else:
        try:
            user = ZeppelinUser(params["username"],cipher.shiro.hasher.hash(params["password"]),"")
            zeppelin_user_dao.save(user)
        except Exception as e:
            print("[ERROR] {}".format(e))
            try:
                linux_user_dao.delete_by_attr("username",params["username"])
            except Exception as e:
                print("[ERROR] Unable to rollback user from linux database, please connect to the database, check if user exists and delete him manually")
