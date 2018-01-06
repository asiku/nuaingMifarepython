import MySQLdb

class ConError(Exception):
    pass
class UsernameLogErr(Exception):
    pass
class DatabaseErr(Exception):
    pass
class SQLError(Exception):
    pass

class UseDatabase:
    def __init__(self,conf):
        self.config=conf
    def __enter__(self):
        try:
            self.conn=MySQLdb.connect(**self.config)
            self.cursor=self.conn.cursor()
            return self.cursor
        except MySQLdb.InterfaceError as err:
            raise ConError(err)
        except MySQLdb.OperationalError as err:
            raise UsernameLogErr(err)
        # except MySQLdb.err.DatabaseError as err:
        #     raise DatabaseErr(err)
        # except pymysql.err.ProgrammingError as err:
        #     raise SQLError(err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is MySQLdb.ProgrammingError:
            raise SQLError(exc_val)
        elif exc_type:
            exc_type(exc_val)





