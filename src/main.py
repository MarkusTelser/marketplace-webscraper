import websites as web

from genericpath import isfile
from time import sleep
from json import load, dump
from os.path import isfile
from os import stat, getcwd, listdir
from os.path import join, isdir

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException

def save_latest_entry(website, link):
    oldEntry = ""
    # get saved data
    data = {}
    if not isfile("history.json") or stat("history.json").st_size == 0:
        with open("history.json", 'w'):
            pass
    else:
        with open("history.json") as f:
            data = load(f)
    if website in data:
        oldEntry = data[website]
    # add/update entry for latest item on website
    new_data = {website : link}
    data.update(new_data)
    # append new data
    with open("../data/history.json", "w") as f:
        dump(data, f)
    return oldEntry
    

def gen_website():
    html = '<!DOCTYPE html><html>'
    html += '<head><meta charset="utf-16"><title>New Items</title></head>'
    html += """
            <style>
            table{
                width: 100%;
            }
            table, th, td{
                border: 2px solid green;
            }
            </style>
            """
    html += '<body><h1>New Items</h1>'
    if isdir(".newitems"):
        html += '<table id="table">'
        for i in range(len(listdir(".newitems"))):
            html += '<tr><th colspan="4">'+ listdir(".newitems")[i].strip() +'</th></tr>'
            with open(join(".newitems",listdir(".newitems")[i]), "r") as f:
                lines = f.readlines()
                html += f'<tr><td style="width:25%">Titel</a></td>'
                html += f'<td style="width:25%">Price</td>'
                html += f'<td style="width:25%">Location</td>'
                html += f'<td style="width:25%">Date</td></tr>'
                # add all items
                for line in lines:
                    items = line.split("||")
                    html += f'<tr><td style="width:25%"><a href="{items[4]}">{items[0]}</a></td>'
                    html += f'<td style="width:25%">{items[1]}</td>'
                    html += f'<td style="width:25%">{items[2]}</td>'
                    html += f'<td style="width:25%">{items[3]}</td></tr>'
    html += '</body></html>'

    with open("index.html", "w") as f:
        f.write(html)

def open_website(driver):
    path = join(getcwd(),"index.html")
    driver.get("file:///" + path)
    sleep(100)

def main():
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging']) # disable logging

        driver = webdriver.Chrome(options=options)

        # fetch new data from websites
        #web.second_hand(driver)
        #web.subito(driver, min_price=3000, last_page=2)
        web.facebook_marketplace(driver)
        sleep(100)
        # generate showcase website, open
        gen_website()
        open_website(driver)

        driver.quit()
    except (KeyboardInterrupt, NoSuchWindowException):
        print()

if __name__ == "__main__":
    main()
