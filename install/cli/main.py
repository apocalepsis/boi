import sys

from cli.commands import users

def display_help():
    print("""
Usage:
    boi-cli.py [options]

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
    [users]
        Access to users operations like create, read, update, delete.
    """)

def run(args):

    if len(args) == 0:
        display_help()
        sys.exit(0)

    option = None

    try:
        option = args.pop(0)
    except:
        print("[ERROR] Unable to read option. Please use -h or -help for more information")
        sys.exit(1)

    if option in ["-h","-help"]:
        display_help()

    elif option in ["users"]:
        users.main.run(args)

    else:
        print("[ERROR] Invalid option <{}>. Please use -h or -help for more information".format(option))
        sys.exit(1)
