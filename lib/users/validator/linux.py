import re

class Implementation:

    def is_valid_username(self,username):
        if not username:
            return False
        else:
            m = re.compile("^[0-9a-zA-Z_]{8,20}$")
            return m.match(username)

    def is_valid_password(self,password):
        if password:
            m = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$@!%&*?])[A-Za-z\d#$@!%&*?]{8,20}$")
            return m.match(password)
        else:
            return True

    def is_valid_uid(self,uid):
        if not uid:
            return False
        else:
            m = re.compile("^\d{4,8}$")
            return m.match(uid)

    def is_valid_gid(self,gid):
        if not gid:
            return False
        else:
            m = re.compile("^\d{4,8}$")
            return m.match(gid)

    def is_valid_attr_name(self,attr_name):
        if not attr_name:
            return False
        elif attr_name not in ["username","password","uid","gid"]:
            return False
        else:
            return True

    def is_valid_attr_value(self,attr_value):
        if not attr_value:
            return False
        return True
