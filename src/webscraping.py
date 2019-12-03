from selenium import webdriver
import numpy as np
import time
import glob
from bs4 import BeautifulSoup
import pandas as pd

DRIVER_PATH = "../chromedriver"
PARLAMENT_CH = "https://www.parlament.ch"


def download_councillor_info(start=0, end=355):
    link = "https://www.parlament.ch/de/ratsmitglieder#k=#s="
    pages = np.arange(start, end)
    driver = webdriver.Chrome(DRIVER_PATH)

    for page in pages:
        driver.get(link + str(page * 10 + 1))
        time.sleep(3)
        with open(f"../ratsmitglieder/file_{page:0>3}.html", "w+") as file:
            file.write(driver.page_source)

    driver.close()


def download_business_items(start=0, end=4593):
    link = "https://www.parlament.ch/en/ratsbetrieb/suche-curia-vista#k=#s="
    pages = np.arange(start, end)
    driver = webdriver.Chrome(DRIVER_PATH)

    for page in pages:
        driver.get(link + str(page * 10 + 1))
        time.sleep(3)
        with open(f"../business_items/file_{page:0>3}.html", "w+") as file:
            file.write(driver.page_source)

    driver.close()


def read_html(path):
    with open(path, "r") as file:
        return BeautifulSoup(file.read(), "html.parser")


def councillor_info_df():
    def person_items(html):
        return html.find_all("div", class_="person-item")

    def image(person):
        return PARLAMENT_CH + person.find("img")["src"]

    def name(person):
        return person.find("img")["alt"].strip()

    def status(person):
        return person.find("span", class_="pd-status").text

    paths = glob.glob(("../ratsmitglieder/*"))
    info = []
    for path in paths:
        html = read_html(path)
        for person in person_items(html):
            info.append(
                {
                    "FullName": name(person),
                    "Image": image(person),
                    "Status": status(person),
                }
            )

    # sorting by status ensures that more recent members are preferred over older members in name conflics
    df = pd.DataFrame(info).drop_duplicates().sort_values(["FullName", "Status"])
    df = df.groupby("FullName").last().reset_index()
    return df
