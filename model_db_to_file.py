import sqlite3


if __name__ == '__main__':
    with open("models.txt", "w") as f:
        with sqlite3.connect('Crucial_PC_SSDs.sqlite') as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM Models""")
            while True:
                row = cur.fetchone()
                if not row:
                    break
                f.write(f'{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n')
