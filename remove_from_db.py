import sqlite3


with sqlite3.connect("Crucial_PC_SSDs.sqlite") as conn, open("missing_models_logged.txt", 'r') as f:
    cur = conn.cursor()
    for line in f:
        mid = line.split(",")[0]
        cur.execute(f"delete from Models where ID={mid}")
