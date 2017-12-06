import re
import os

from subprocess import Popen, PIPE, STDOUT

def hash(password):

    self_cwd = os.path.dirname(os.path.realpath(__file__))

    p = Popen(["java","-cp","shiro-tools-hasher-1.3.2-cli.jar:jerhz-shiro-tools-hasher-1.0.0.jar",
        "aws.falej.shiro.tools.hasher.ShiroHasher","-p",password],
        stdout=PIPE, stdin=PIPE, stderr=STDOUT,cwd=self_cwd)

    output, err = p.communicate()

    if output:
        return output.decode("utf-8").strip()

    if err:
        return err.decode("utf-8").strip()

    return None
