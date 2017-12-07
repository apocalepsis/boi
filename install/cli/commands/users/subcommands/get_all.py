import sys

from config import properties

from lib.users.dao.linux import Implementation as LinuxDAO
from lib.utils import cipher

def run(args):

    linux_user_dao = LinuxDAO(
        properties.boi_linux_db_host,
        properties.boi_linux_db_name,
        properties.boi_linux_db_user,
        properties.boi_linux_db_password
    )

    try:

        dao_response = linux_user_dao.get_all()

        for user in dao_response["users"]:
            user.set_password(cipher.aes.decrypt(user.get_password()).decode("utf-8"))
            print(user.str())

    except Exception as e:
        print("[ERROR] {}".format(e))
