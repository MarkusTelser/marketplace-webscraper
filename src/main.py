import websites as web
from page import gen_website

from genericpath import isfile
from time import sleep
from json import load, dump
from os.path import isfile
from os import stat
from os.path import join, dirname
from sys import modules

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException

ROOT_DIR = dirname(dirname(modules['__main__'].__file__))

def write_data(website, title, price, location, date, link):
    data_path = join(ROOT_DIR, "data", "websites", website + ".txt")
    with open(data_path, "r") as f:
        data = f.read()
    with open(data_path, "w") as f:
        f.write(f"{title} || {price} || {location} || {date} || {link}\n")
    with open(data_path, "a") as f:
        f.write(data)


def save_latest_entry(website, link):
    history_path = join(ROOT_DIR, "data","history.json")
    oldEntry = ""
    # get saved data
    data = {}
    if not isfile(history_path) or stat(history_path).st_size == 0:
        with open(history_path, 'w'):
            pass
    else:
        with open(history_path) as f:
            data = load(f)
    if website in data:
        oldEntry = data[website]
    # add/update entry for latest item on website
    new_data = {website : link}
    data.update(new_data)
    # append new data
    
    with open(history_path, "w") as f:
        dump(data, f)
    return oldEntry
    
def open_website(driver):
    path = join(ROOT_DIR, "page", "index.html")
    driver.get("file:///" + path)
    sleep(100)

def main():
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True) # stop closing
        options.add_experimental_option('excludeSwitches', ['enable-logging']) # disable logging

        driver = webdriver.Chrome(options=options)

        # fetch new data from websites
        web.second_hand(driver, max_elements=10)
        web.subito(driver, max_elements=10)
        #web.facebook_marketplace(driver)

        # generate showcase website, open
        gen_website()
        open_website(driver)

        driver.quit()
    except (KeyboardInterrupt, NoSuchWindowException):
        print()

if __name__ == "__main__":
    main()
