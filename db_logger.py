import sqlite3
import time

done = False


class DBLogger:
    path = 'Crucial_PC_SSDs.sqlite'
    instance = None

    def __init__(self):
        if DBLogger.instance is None:
            DBLogger.instance = self
        self.queue = []

    @staticmethod
    def get_instance():
        if DBLogger.instance is None:
            DBLogger.instance = DBLogger()
        return DBLogger.instance

    def save_rec_to_db(self, model_id, drive_cn, cur):
        try:
            cur.execute("""INSERT INTO Recommendations (Model_ID, Drive_CN) VALUES (?, ?)""", (model_id, drive_cn))
        except:
            pass

    def save_drive_to_db(self, drive_cn, drive_name, cur):
        cur.execute("""SELECT * FROM Drives WHERE catalog_number = ?""", (drive_cn,))
        if cur.fetchone() is None:
            try:
                cur.execute("""INSERT INTO Drives (catalog_number, name) VALUES (?, ?)""", (drive_cn, drive_name))
            except:
                pass

    def log(self, model_id, drive_cn, drive_name):
        self.queue.append((model_id, drive_cn, drive_name))


def log(con, db, model_id, drive_cn, drive_name):
    cur = con.cursor()
    db.save_drive_to_db(drive_cn, drive_name, cur)
    db.save_rec_to_db(model_id, drive_cn, cur)


def main_loop():
    db = DBLogger.get_instance()
    completed = 0
    with sqlite3.connect(DBLogger.path) as con:
        while True:
            if len(db.queue) > 0:
                popped = db.queue.pop()
                log(con, db, popped[0], popped[1], popped[2])
                completed += 1
                if completed % 10 == 0:
                    print(f'committing... completed {completed} recommendations.')
                    con.commit()
            else:
                time.sleep(1)
