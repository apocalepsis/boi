import sys
import os

from config import properties

from lib.utils import shell
from lib.utils import cipher

from lib.users.dao.linux import Implementation as LinuxDAO

def setup_user_group(user):

    response = {
        "status_code" : 0,
        "out" : None,
        "err" : None
    }

    user_group_exists = False

    shell_response = shell.run(["getent","group",str(user.get_gid())])
    print("getent: " + str(shell_response))

    if shell_response["status_code"] not in [0,2]:
        response["err"] = shell_response["err"]
        response["status_code"] = 1
    elif shell_response["out"]:
        user_group_exists = True

    if not user_group_exists:
        print("Creating user group with name <{}> and gid <{}>".format(user.get_username(),str(user.get_gid())))
        shell_response = shell.run(["groupadd","--gid",str(user.get_gid()),user.get_username()])
        print("groupadd: " + str(shell_response))
        if shell_response["status_code"] != 0:
            response["err"] = shell_response["err"]
            response["status_code"] = 1

    if response["status_code"] == 0:
        response["out"] = "SUCCESS"
    else:
        response["err"] = "An error occurred during user group setup"

    return response

def setup_user(user):

    response = {
        "status_code" : 0,
        "out" : None,
        "err" : None
    }

    user_exists = False

    if not user_exists:
        shell_response = shell.run(["getent","passwd",str(user.get_uid())])
        print("getent[uid]: " + str(shell_response))

        if shell_response["status_code"] not in [0,2]:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        elif shell_response["out"]:
            user_exists = True

    if not user_exists:
        shell_response = shell.run(["getent","passwd",user.get_username()])
        print("getent[username]: " + str(shell_response))

        if shell_response["status_code"] not in [0,2]:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        elif shell_response["out"]:
            user_exists = True

    if not user_exists:
        print("Creating user with username <{}> and uid <{}>".format(user.get_username(),str(user.get_uid())))
        shell_response = shell.run(["useradd","--uid",str(user.get_uid()),"--gid",str(user.get_gid()),user.get_username()])
        print("useradd: " + str(shell_response))
        if shell_response["status_code"] != 0:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        else:
            # password setup
            user_password = cipher.aes.decrypt(user.get_password()).decode("utf-8")
            print("Creating password for user <{}>".format(user.get_username()))
            cmd = "echo '{}' | passwd {} --stdin".format(user_password,user.get_username())
            shell_response = shell.run(cmd,pshell=True)
            print("passwd: " + str(shell_response))
            if shell_response["status_code"] != 0:
                response["err"] = shell_response["err"]
                response["status_code"] = 1
            

    if response["status_code"] == 0:
        response["out"] = "SUCCESS"
    else:
        response["err"] = "An error occurred during user setup"

    return response

def setup_dirs(user):

    response = {
        "status_code" : 0,
        "out" : None,
        "err" : None
    }

    create_user_jupyter_dir = False
    create_user_rstudio_dir = False
    create_user_outputs_dir = False

    user_dir = properties.jerhz_users_dir + "/" + user.get_username()
    user_dir_exists = os.path.isdir(user_dir)

    if not user_dir_exists:
        print("Creating user dir <{}>".format(user_dir))
        shell_response = shell.run(["mkdir","-p",user_dir])
        print("mkdir: " + str(shell_response))
        if shell_response["status_code"] != 0:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        else:
            shell_response = shell.run(["chown","{}:{}".format(user.get_username(),user.get_username()),user_dir])
            print("chown: " + str(shell_response))
            if shell_response["status_code"] != 0:
                response["err"] = shell_response["err"]
                response["status_code"] = 1
            else:
                create_user_jupyter_dir = True
                create_user_rstudio_dir = True
                create_user_outputs_dir = True

    if create_user_jupyter_dir:
        user_dir = properties.jerhz_users_dir + "/" + user.get_username() + "/jupyter"
        print("Creating user jupyter dir <{}>".format(user_dir))
        shell_response = shell.run(["mkdir","-p",user_dir])
        print("mkdir: " + str(shell_response))
        if shell_response["status_code"] != 0:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        else:
            shell_response = shell.run(["chown","{}:{}".format(user.get_username(),user.get_username()),user_dir])
            print("chown: " + str(shell_response))
            if shell_response["status_code"] != 0:
                response["err"] = shell_response["err"]
                response["status_code"] = 1

    if create_user_rstudio_dir:
        user_dir = properties.jerhz_users_dir + "/" + user.get_username() + "/rstudio"
        print("Creating user rstudio dir <{}>".format(user_dir))
        shell_response = shell.run(["mkdir","-p",user_dir])
        print("mkdir: " + str(shell_response))
        if shell_response["status_code"] != 0:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        else:
            shell_response = shell.run(["chown","{}:{}".format(user.get_username(),user.get_username()),user_dir])
            print("chown: " + str(shell_response))
            if shell_response["status_code"] != 0:
                response["err"] = shell_response["err"]
                response["status_code"] = 1

    if create_user_outputs_dir:
        user_dir = properties.jerhz_users_dir + "/" + user.get_username() + "/outputs"
        print("Creating user outputs dir <{}>".format(user_dir))
        shell_response = shell.run(["mkdir","-p",user_dir])
        print("mkdir: " + str(shell_response))
        if shell_response["status_code"] != 0:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        else:
            shell_response = shell.run(["chown","{}:{}".format(user.get_username(),user.get_username()),user_dir])
            print("chown: " + str(shell_response))
            if shell_response["status_code"] != 0:
                response["err"] = shell_response["err"]
                response["status_code"] = 1

    if response["status_code"] == 0:
        response["out"] = "SUCCESS"
    else:
        response["err"] = "An error occurred during directories setup"

    return response

def setup_links(user):

    response = {
        "status_code" : 0,
        "out" : None,
        "err" : None
    }

    setup_jupyter_link = False
    setup_rstudio_link = False
    setup_outputs_link = False

    user_home_dir = "/home/" + user.get_username()
    user_jerhz_dir = properties.jerhz_users_dir + "/" + user.get_username()

    user_home_dir_exists = os.path.isdir(user_home_dir)
    user_jerhz_dir_exists = os.path.isdir(user_jerhz_dir)

    user_home_jupyter = user_home_dir + "/jupyter"
    user_home_rstudio = user_home_dir + "/rstudio"
    user_home_outputs = user_home_dir + "/outputs"

    user_jerhz_jupyter = user_jerhz_dir + "/jupyter"
    user_jerhz_rstudio = user_jerhz_dir + "/rstudio"
    user_jerhz_outputs = user_jerhz_dir + "/outputs"

    if user_home_dir_exists and user_jerhz_dir_exists:
        setup_jupyter_link = True
        setup_rstudio_link = True
        setup_outputs_link = True

    if setup_jupyter_link:
        shell_response = shell.run(["find",user_home_dir,"-name","jupyter"])
        print("find[jupyter]: " + str(shell_response))
        if shell_response["status_code"] != 0:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        elif not shell_response["out"]:
            shell_response = shell.run(["ln","-s",user_jerhz_jupyter,user_home_jupyter])
            print("ln[jupyter]: " + str(shell_response))
            if shell_response["status_code"] != 0:
                response["err"] = shell_response["err"]
                response["status_code"] = 1

    if setup_rstudio_link:
        shell_response = shell.run(["find",user_home_dir,"-name","rstudio"])
        print("find[rstudio]: " + str(shell_response))
        if shell_response["status_code"] != 0:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        elif not shell_response["out"]:
            shell_response = shell.run(["ln","-s",user_jerhz_rstudio,user_home_rstudio])
            print("ln[rstudio]: " + str(shell_response))
            if shell_response["status_code"] != 0:
                response["err"] = shell_response["err"]
                response["status_code"] = 1

    if setup_outputs_link:
        shell_response = shell.run(["find",user_home_dir,"-name","outputs"])
        print("find[outputs]: " + str(shell_response))
        if shell_response["status_code"] != 0:
            response["err"] = shell_response["err"]
            response["status_code"] = 1
        elif not shell_response["out"]:
            shell_response = shell.run(["ln","-s",user_jerhz_outputs,user_home_outputs])
            print("ln[rstudio]: " + str(shell_response))
            if shell_response["status_code"] != 0:
                response["err"] = shell_response["err"]
                response["status_code"] = 1

    if response["status_code"] == 0:
        response["out"] = "SUCCESS"
    else:
        response["err"] = "An error occurred during links setup"

    return response

def run(args):

    print(">>> Sync in progress, please wait ... \n")

    print("Checking jerhz users dir <{}>\n".format(properties.jerhz_users_dir))
    if not os.path.isdir(properties.jerhz_users_dir):
        print("[ERROR]: Dir not found or invalid")
        sys.exit(1)

    user_dao_linux = LinuxDAO()

    user_list = user_dao_linux.get_all()

    for user in user_list:

        response = None

        print("User <{}>".format(user.get_username()))

        print("Setup user group ...")
        response = setup_user_group(user)
        print(response)

        if response["status_code"] != 0:
            continue

        print("Setup user ...")
        response = setup_user(user)
        print(response)

        if response["status_code"] != 0:
            continue

        print("Setup directories ...")
        response = setup_dirs(user)
        print(response)

        if response["status_code"] != 0:
            continue

        print("Setup links ...")
        response = setup_links(user)
        print(response)

        print("")

    print("<<< Done.")
