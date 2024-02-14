import os
import sqlite3
import util

base_url = "www.crucial.com"

with open("missing_models_logged.txt", 'w') as together_f, open("missing_models.txt", 'r') as f:
    with sqlite3.connect("Crucial_PC_SSDs.sqlite") as conn:
        cur = conn.cursor()

        # os.chdir("models")
        # for model_f in os.listdir():
        for model in f:
            split = model.split(",")
            model_f = split[0].removeprefix("models\\")
            # prod_models = util.read_file(model_f)
            # for model in prod_models:
            if len(split) <= 2:
                continue
            model = ",".join(split[1:])
            model_name = model[:model.find("/compatible-upgrade-for/") - 1]
            man = model_f.split("_")[0]
            product = model_f.split("_")[1].replace(".txt", "")
            url = base_url + model[model.find("/compatible-upgrade-for/"):].replace("\n", "")
            cur.execute("""
            INSERT INTO Models (Manufacturer, Product, Model, Recommend_URL)
            VALUES (?, ?, ?, ?)""", (man, product, model_name, url))
            cur.execute("SELECT ID FROM Models WHERE Recommend_URL=?", (url,))
            mid = cur.fetchone()[0]
            together_f.write(f"{mid},{man},{product},{model_name},{url}\n")
