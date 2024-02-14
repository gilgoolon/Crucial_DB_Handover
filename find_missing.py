from glob import glob
import sqlite3
from tqdm import tqdm

base_url = "www.crucial.com"

con = sqlite3.connect("Crucial_PC_SSDs.sqlite")
cur = con.cursor()

missing = []

for product_f in glob("models/*"):
    with open(product_f, 'r') as f:
        for model in tqdm(f):
            url = base_url + model[model.find("/compatible-upgrade-for/"):].replace("\n", "")
            cur.execute(f"select * from Models where Recommend_URL='{url}'")
            res = cur.fetchone()
            if not res:
                print(model)
                missing.append(f"{product_f},{model}")

with open("missing_models.txt", 'w') as f:
    for m in missing:
        f.write(f"{m}\n")
con.close()
