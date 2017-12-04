import mysql.connector as mysql

from config import properties
from lib.users.model.linux import LinuxUser
from lib.exceptions.dao import DAOException

class LinuxDAO:

    db_host = properties.boi_linux_users_db_host
    db_name = properties.boi_linux_users_db_name
    db_user = properties.boi_linux_users_db_user
    db_password = properties.boi_linux_users_db_password


    def save(self,user):

        dao_response = self.get_by_attr("username",user.get_username())

        if len(dao_response["users"]) > 0:
            raise DAOException("User already exists")

        dao_response = self.get_by_attr("uid",user.get_uid())

        if len(dao_response["users"]) > 0:
            raise DAOException("User already exists")

        conn = None
        cursor = None

        try:

            conn = mysql.connect(
                host = self.db_host,
                database = self.db_name,
                user = self.db_user,
                password = self.db_password
            )

            sql = "INSERT INTO users VALUES ('%s','%s','%s',%s,%s)" % (
                user.get_username(),user.get_password(),user.get_type(),user.get_uid(),user.get_gid())

            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            raise DAOException(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_by_attr(self,attr_name,attr_value):

        conn = None
        cursor = None

        try:

            conn = mysql.connect(
                host = self.db_host,
                database = self.db_name,
                user = self.db_user,
                password = self.db_password
            )

            sql = "DELETE FROM users WHERE %s='%s'" % (attr_name,attr_value)

            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            raise DAOException(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_all(self):

        conn = None
        cursor = None

        try:

            conn = mysql.connect(
                host = self.db_host,
                database = self.db_name,
                user = self.db_user,
                password = self.db_password
            )

            sql = "DELETE FROM users"

            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            raise DAOException(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_attr(self,attr_name,attr_value):

        response = {
            "users" : []
        }

        conn = None
        cursor = None

        try:

            conn = mysql.connect(
                host = self.db_host,
                database = self.db_name,
                user = self.db_user,
                password = self.db_password
            )

            sql = "SELECT * FROM users WHERE %s='%s'" % (attr_name,attr_value)

            cursor = conn.cursor(buffered = True)
            cursor.execute(sql)

            for row in cursor:
                user = LinuxUser(row[0],row[1],row[2],row[3],row[4])
                response["users"].append(user)

        except Exception as e:
            raise DAOException(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return response

    def get_all(self):

        response = {
            "users" : []
        }

        conn = None
        cursor = None

        try:

            conn = mysql.connect(
                host = self.db_host,
                database = self.db_name,
                user = self.db_user,
                password = self.db_password
            )

            sql = "SELECT * FROM users ORDER BY username"

            cursor = conn.cursor(buffered = True)
            cursor.execute(sql)

            for row in cursor:
                user = LinuxUser(row[0],row[1],row[2],row[3],row[4])
                response["users"].append(user)

        except Exception as e:
            raise DAOException(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return response
