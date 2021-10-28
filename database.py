import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS weight (id INTEGER PRIMARY KEY, city TEXT, time TEXT")
        self.conn.commit()

    def insert(self, id, city, time):
        self.cur.execute("INSERT INTO users VALUES (?,?,?)", (id, city, time))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def search(self, id="", city="", time=""):
        self.cur.execute("SELECT * FROM users WHERE id=? OR city=? OR time=?",
                         (id, city, time))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM users WHERE id=?", id)
        self.conn.commit()

    def update(self, id, city, time):
        self.cur.execute("UPDATE users SET city=?, time=? WHERE id=?",
                         (city, time, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
