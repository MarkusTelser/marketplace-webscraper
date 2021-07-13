import codecs as cd
from genericpath import isfile
from time import sleep
from json import load, dump
from os import stat, remove, listdir
from os.path import join, dirname, isfile
from sys import modules

ROOT_DIR = dirname(dirname(modules['__main__'].__file__))


def remove_data():
    # remove site data
    for file in listdir(join(ROOT_DIR, "data", "websites")):
        remove(join(ROOT_DIR, "data", "websites", file))


def write_data(dataset, website):
    # read old content of file and save
    data_path = join(ROOT_DIR, "data", "websites", website + ".txt")
    old_data = ""
    if isfile(data_path):
        with cd.open(data_path, "r", "utf-8") as f:
            old_data = f.readlines()
    # write new content
    with cd.open(data_path, "w", "utf-8") as f:
        for data in dataset:
            if len(data) == 5:
                title, price, location, date, link = data
                f.write(f"{title} || {price} || {location} || {date} || {link}\n")
            elif len(data) == 6:
                title, price, location, date, link, mileage = data
                f.write(f"{title} || {price} || {location} || {date} || {link} || {mileage}\n")
    # append old content of file
    with cd.open(data_path, "a", "utf-8") as f:
        for d in old_data:
            f.write(d)


def save_latest_entry(website, link):
    history_path = join(ROOT_DIR, "data", "history.json")
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
    new_data = {website: link}
    data.update(new_data)

    # append new data
    with open(history_path, "w") as f:
        dump(data, f)

    return oldEntry


def open_website(driver):
    path = join(ROOT_DIR, "page", "index.html")
    driver.get("file:///" + path)