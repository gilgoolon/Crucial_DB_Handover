import sqlite3
import threading

import db_logger

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup

import util

completed_lock = threading.Lock()
completed = 0
active = 0


def scrape_recommends(model):
    global completed, active
    driver = None
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--silent")
        driver = webdriver.Chrome('C:/Program Files/ChromeDriver/chromedriver.exe', options=chrome_options)

        driver.get(f'http://{model[-1]}')
        # response = requests.get(f'https://{model[-1]}')

        # wait for page load - passive wait
        wait = WebDriverWait(driver, 15)

        ssd_tab_btn = wait.until(EC.presence_of_element_located((By.ID, "ssd-label")))

        try:
            # close the cookie banner
            driver.find_element_by_class_name("banner-close-button").click()
            time.sleep(1)
        except:
            pass

        # scroll down to the ssd tab button
        driver.execute_script("arguments[0].scrollIntoView();", ssd_tab_btn)
        driver.execute_script("window.scrollBy(0, -150);")

        time.sleep(1)
        # click on the "SSD" tab
        ssd_tab_btn.click()

        names = []
        cns = []

        while True:
            time.sleep(1)

            html = driver.page_source

            soup = BeautifulSoup(html, "html.parser")
            ssds = soup.find("div", {"id": "ssd"})

            for div in ssds.find_all("h4", class_="base-part-number"):
                cns.append(div.text)

            for div in ssds.find_all("a", class_="product-title"):
                names.append(div.text)

            try:
                next_button = driver.find_element_by_id("ssd")\
                    .find_element_by_class_name("pagination-next")\
                    .find_element_by_tag_name("a")
            except:
                break

            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            driver.execute_script("window.scrollBy(0, -150);")
            next_button.click()

        db = db_logger.DBLogger.get_instance()
        for i in range(len(names)):
            db.log(model[0], cns[i], names[i])

    except Exception as e:
        print(str(e))
        if driver is not None:
            driver.quit()
        with open("missing.txt", 'a') as f:
            f.write(model[-1] + '\n')

    completed_lock.acquire()
    completed += 1
    active -= 1
    completed_lock.release()


def fetch_generator(cur):
    while True:
        row = cur.fetchone()
        if not row:
            break
        yield row


con = sqlite3.connect("Crucial_PC_SSDs.sqlite")
cur = con.cursor()
cur.execute("""SELECT * FROM Models WHERE NOT EXISTS(SELECT * FROM Recommendations WHERE Model_ID=ID)""")

models = set([model[0] for model in cur.fetchall()])

with open('missing_models_logged.txt') as models_f:
    threading.Thread(target=db_logger.main_loop).start()

    line_number = 1
    while line_number <= len(models):
        m = models_f.readline()
        # m = models[line_number - 1]
        if m == '\n':
            break
        tok = m.split(',')
        if m.count(',') > 4:
            m = (tok[0], tok[1], tok[2], ",".join(tok[3:-1]), tok[-1])
        else:
            m = m[:-1].split(',')
        if int(m[0]) not in models:
            continue

        line_number += 1

        while active >= 8:
            print(f'completed: {completed}, active: {active} time_passed: {util.time_passed()}')
            time.sleep(1)
        print(m)
        threading.Thread(target=scrape_recommends, args=(m,)).start()
        completed_lock.acquire()
        active += 1
        completed_lock.release()
    # scrape_recommends(('212182', 'hp - compaq', 'Pavilion - 15 - Series', 'Pavilion 15 - bc202nt', 'www.crucial.com/compatible-upgrade-for/hp-compaq/pavilion-15-bc202nt'))
    # 212182, hp - compaq, Pavilion - 15 - Series, Pavilion
    # 15 - bc202nt,

    done = True
