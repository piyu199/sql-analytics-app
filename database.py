from psycopg2 import pool

class Database:

    __connection_pool = None

    @staticmethod
    def initialise(**kwargs):
        Database.__connection_pool=pool.SimpleConnectionPool(1, 10, **kwargs)

    @staticmethod
    def get_connection():
        return Database.__connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        Database.__connection_pool.putconn(connection)

    @staticmethod
    def close_all_connection():
        Database.__connection_pool.closeall()



class CursorFromConnectionFromPool:

    def __init__(self):
        self.connection=None
        self.cursor=None

    def __enter__(self):
        self.connection= Database.get_connection()
        self.cursor= self.connection.cursor()
        return self.cursor

    def __exit__(self,exception_type,exception_value,exception_traceback):
        if exception_value is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)
