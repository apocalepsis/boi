import sys

from config import properties

from lib.users.dao.linux import Implementation as LinuxDAO
from lib.users.dao.zeppelin import Implementation as ZeppelinDAO

def run(args):

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
        linux_user_dao.delete_all()
    except Exception as e:
        print("[ERROR] {}".format(e))

    try:
        zeppelin_user_dao.delete_all()
    except Exception as e:
        print("[ERROR] {}".format(e))
