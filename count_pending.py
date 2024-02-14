import sqlite3

con = sqlite3.connect("Crucial_PC_SSDs.sqlite")
cur = con.cursor()
cur.execute("""SELECT * FROM Models WHERE NOT EXISTS(SELECT * FROM Recommendations WHERE Model_ID=ID)""")

fetched = cur.fetchall()
models = set([model[0] for model in fetched])

models_from_txt = set()
with open("models_spaces.txt", 'r') as f:
    for line in f.readlines():
        models_from_txt.add(int(line.split(',')[0]))

missing = models.intersection(models_from_txt)
print(len(missing))
# dump missing

with open("missing_models.txt", 'w') as f:
    for model in missing:
        cur.execute("select * from Models where ID=?", (model,))
        f.write(",".join((str(item) for item in cur.fetchone())))
        f.write("\n")
