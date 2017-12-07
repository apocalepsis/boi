import sys
import cli

args = sys.argv.copy()
args.pop(0)

cli.main.run(args)
