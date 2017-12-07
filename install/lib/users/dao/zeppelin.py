import mysql.connector as mysql

from config import properties
from lib.users.model.zeppelin import Implementation as ZeppelinUser
from lib.exceptions.dao import Implementation as DAOException

class Implementation:

    def __init__(self,db_host,db_name,db_user,db_password):
        self.__db_host = db_host
        self.__db_name = db_name
        self.__db_user = db_user
        self.__db_password = db_password

    def save(self,user):

        dao_response = self.get_by_attr("username",user.get_username())

        if len(dao_response["users"]) > 0:
            raise DAOException("User already exists")

        conn = None
        cursor = None

        try:

            conn = mysql.connect(
                host = self.__db_host,
                database = self.__db_name,
                user = self.__db_user,
                password = self.__db_password
            )

            sql = "INSERT INTO users VALUES ('%s','%s','%s')" % (
                user.get_username(),user.get_password(),user.get_salt())

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
                host = self.__db_host,
                database = self.__db_name,
                user = self.__db_user,
                password = self.__db_password
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
                host = self.__db_host,
                database = self.__db_name,
                user = self.__db_user,
                password = self.__db_password
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
                host = self.__db_host,
                database = self.__db_name,
                user = self.__db_user,
                password = self.__db_password
            )

            sql = "SELECT * FROM users WHERE %s='%s'" % (attr_name,attr_value)

            cursor = conn.cursor(buffered = True)
            cursor.execute(sql)

            for row in cursor:
                user = ZeppelinUser(row[0],row[1],row[2])
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
                host = self.__db_host,
                database = self.__db_name,
                user = self.__db_user,
                password = self.__db_password
            )

            sql = "SELECT * FROM users ORDER BY username"

            cursor = conn.cursor(buffered = True)
            cursor.execute(sql)

            for row in cursor:
                user = ZeppelinUser(row[0],row[1],row[2])
                response["users"].append(user)

        except Exception as e:
            raise DAOException(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return response
