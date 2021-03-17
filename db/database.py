import sqlite3


class DataBase:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect("requests.db")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(
                "CREATE TABLE request_url ("
                "id_request INTEGER PRIMARY KEY AUTOINCREMENT, "
                "status INTEGER, "
                "message TEXT, "
                "url TEXT);"
            )
            self.conn.commit()
        except sqlite3.OperationalError:
            pass
        return self

    def fetchone(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

    def insert_request(self, data):
        url = data['url']
        status_code = data['status_code']
        message = data['message']
        r = f"Insert into request_url (status, message, url) values ({status_code}, '{message}', '{url}')"
        self.cursor.execute(r)
        self.conn.commit()
