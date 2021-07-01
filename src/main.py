import websites as web

from genericpath import isfile
from time import sleep
from json import load, dump
from os.path import isfile
from os import stat, getcwd, listdir
from os.path import join, isdir, dirname
from sys import modules

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException

ROOT_DIR = dirname(dirname(modules['__main__'].__file__))

def write_data(website, title, price, location, date, link):
    data_path = join(ROOT_DIR, "data", website + ".txt")
    with open(data_path, "a") as f:
        f.write(f"{title} || {price} || {location} || {date} || {link}\n")


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
    
def gen_html():
    html = '<!DOCTYPE html><html>'
    html += '<head><meta charset="utf-16"><title>New Items</title></head>'
    html += '<link rel="stylesheet" href="style.css">'
    html += '<script src="script.js"></script>'
    html += '<body><h1>New Marketplace Items</h1>'
    if isdir("data"):
        
        websites = listdir(join(ROOT_DIR, "data", "websites"))
        for i in range(len(websites)):
            html += '<table class="section">'
            html += '<tr class="site"><th colspan="4">'+ websites[i].split('.')[0] +'</th></tr>'
            with open(join(ROOT_DIR, "data", "websites", websites[i]), "r") as f:
                lines = f.readlines()
                html += f'<tr><td class="type">Titel</a></td>'
                html += f'<td class="type">Price</td>'
                html += f'<td class="type">Location</td>'
                html += f'<td class="type">Date</td></tr>'
                # add all items
                for line in lines:
                    items = line.split("||")
                    html += f'<tr><td class="items"><a href="{items[4]}">{items[0]}</a></td>'
                    html += f'<td class="items">{items[1]}</td>'
                    html += f'<td class="items">{items[2]}</td>'
                    html += f'<td class="items">{items[3]}</td>'
                    html += '<td><input type="button" value="Delete" onclick="deleteRow(this)"/></td></tr>'
            html += '</table>'
    html += '</body></html>'
    return html

def gen_js():
    js = """
    function deleteRow(btn) {
        var row = btn.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }
    """
    return js

def gen_css():
    css = """
    body{
        background-color: #E1E8ED;
    }
    h1{
        font-size: 30pt;
        font-color: #292F33;
        justify-content: center;
        text-align: center;
    }
    table{
        margin-left: auto;
        margin-right: auto;
        width: 80%;
    }
    th, td{
        border: 2px solid  #66757F;
        font-color: #CCD6DD;
    }
    th{
        font-size: 22pt;
        padding: 5px;
    }
    a {
        color: #66757F;
    }
    td{
        width: 25%;
        font-size: 16pt;
    }
    .section{
        margin-top: 30px;
    }
    .type{
        font-size: 20pt;
        font-weight: bold;
    }
    .items{
        width: 20%;
    }
    """
    return css

def gen_website():
    # write html file
    with open(join(ROOT_DIR, "page", "index.html"), "w") as f:
        f.write(gen_html())
    
    # write css file
    with open(join(ROOT_DIR, "page", "style.css"), "w") as f:
        f.write(gen_css())

    # write js file
    with open(join(ROOT_DIR, "page", "script.js"), "w") as f:
        f.write(gen_js())
    
    
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
        #web.second_hand(driver)
        #web.subito(driver, last_page=2)
        #web.facebook_marketplace(driver)

        # generate showcase website, open
        gen_website()
        open_website(driver)

        driver.quit()
    except (KeyboardInterrupt, NoSuchWindowException):
        print()

if __name__ == "__main__":
    main()
