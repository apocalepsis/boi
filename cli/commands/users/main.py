import sys

from cli.commands.users import subcommands

def display_help():
    print("""
Usage:
    boi-cli.py users [options]

Available Options:
    [parameter]
        Is an immediate action
    [command]
        Can have command(s) and/or parameter(s)

Available Parameters:
    [-h | -help]
        Type: bool
        Required: No

Available Commands:
    [create-user]
        Creates a new user
    [get-all]
        Get all users
    [get-user]
        Get user(s) that match a specific attribute
    [delete-all]
        Delete all users
    [delete-user]
        Deletes a specific user
    [sync]
        Sync environments of all users that currently exists on the database.
        WARNING: If a user doesn't exists anymore, his environment will be deleted and all data,
        that was not backed up, will be lost
    """)

def run(args):

    if len(args) == 0:
        display_help()
        sys.exit(0)

    option = None

    try:
        option = args.pop(0)
    except:
        print("[ERROR] Unable to read option.")
        sys.exit(1)

    if option in ["-h","-help"]:
        display_help()

    elif option in ["create-user"]:
        subcommands.create_user.run(args)

    elif option in ["get-all"]:
        subcommands.get_all.run(args)

    elif option in ["get-user"]:
        subcommands.get_user.run(args)

    elif option in ["delete-all"]:
        subcommands.delete_all.run(args)

    elif option in ["delete-user"]:
        subcommands.delete_user.run(args)

    elif option in ["sync"]:
        pass
        #subcommands.sync.run(args)

    else:
        print("[ERROR] Invalid option <{}>. Please use -h or -help for more information".format(option))
        sys.exit(1)
