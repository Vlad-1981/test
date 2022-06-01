import mysql.connector


class ConnectionError(Exception):
    pass


class UserDatabase:
    def __init__(self, config: dict) -> None:
        self.configuration = config

    try:

        def __enter__(self) -> 'cursor':
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor

    except mysql.connector.errors.InterfaceError as err:
        raise ConnectionError(err)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
