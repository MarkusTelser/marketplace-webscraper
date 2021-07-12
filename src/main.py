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

def write_data(dataset, website):
    # read old content of file and save
    data_path = join(ROOT_DIR, "data", "websites", website + ".txt")
    with open(data_path, "r") as f:
            old_data = f.readlines()
    # write new content
    with open(data_path, "w") as f:
        for data in dataset:
            title, price, location, date, link = data
            f.write(f"{title} || {price} || {location} || {date} || {link}\n")
    # append old content of file
    with open(data_path, "a") as f:
        print(old_data)
        for d in old_data:
            f.write(d)


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


def main():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito") # open in incognito mode
        chrome_options.add_argument("--start-maximized") # opens window max dimensions
        chrome_options.add_experimental_option("detach", True) # stop closing
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # disable logging

        driver = webdriver.Chrome(options=chrome_options)

        # fetch new data from websites
        #web.second_hand(driver, max_elements=10)
        #web.subito(driver, max_elements=10)
        #web.facebook_marketplace(driver)

        # generate showcase website, open
        gen_website()
        open_website(driver)

    except (KeyboardInterrupt, NoSuchWindowException):
        print()

if __name__ == "__main__":
    main()