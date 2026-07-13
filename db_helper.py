import pymysql

class MySqlHelper:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = None
        self.cursor = None

    def _get_conn(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            charset="utf8mb4"
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def query_all(self, sql, args=None):
        try:
            self._get_conn()
            self.cursor.execute(sql, args or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"查询出错：{e}")
            return []
        finally:
            self._close()

    def query_one(self, sql, args=None):
        try:
            self._get_conn()
            self.cursor.execute(sql, args or ())
            return self.cursor.fetchone()
        except Exception as e:
            print(f"查询出错：{e}")
            return None
        finally:
            self._close()

    def execute(self, sql, args=None):
        try:
            self._get_conn()
            row = self.cursor.execute(sql, args or ())
            self.conn.commit()
            return row
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"执行SQL出错，已回滚：{e}")
            return 0
        finally:
            self._close()

    def _close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    db = MySqlHelper(
        host="localhost",
        user="root",
        password="leo20200303",  #密码
        database="student_db"
    )

    insert_sql = "INSERT INTO student(name, height) VALUES (%s, %s)"
    db.execute(insert_sql, ("小明", 172.3))

    print("所有学生：", db.query_all("SELECT * FROM student"))

    print("id=1学生：", db.query_one("SELECT * FROM student WHERE id=%s", (1,)))

    db.execute("UPDATE student SET height=%s WHERE id=%s", (177, 1))

    db.execute("DELETE FROM student WHERE name=%s", ("小明",))