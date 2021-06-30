from genericpath import isfile
from sys import maxsize
from time import sleep
from json import load, dump
from os.path import isfile
from os import stat, getcwd, listdir
from os.path import join, isdir

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchWindowException

from airium import Airium

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
    with open("history.json", "w") as f:
        dump(data, f)
    return oldEntry
    

def gen_website():
    a = Airium()
    html = '<!DOCTYPE html><html>'
    html += '<head><meta charset="utf-8"><title>New Items</title></head>'
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
                for line in lines:
                    items = line.split("||").encode('UTF-8')
                    html += f'<tr><td style="width:25%"><a href="{items[4]}">{items[0]}</a></td>'
                    html += f'<td style="width:25%">{items[1]}</td>'
                    html += f'<td style="width:25%">{items[2]}</td>'
                    html += f'<td style="width:25%">{items[3]}</td></tr>'
    html += '</body></html>'

    with open("index.html", "w") as f:
        f.write(html)

def second_hand(driver, first_page=1, last_page=20, min_price=0, max_price=10000):
    driver.get("https://www.second-hand.it")

    # accept cookies
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath('//*[@id="sp_message_iframe_511960"]')))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="notice"]/div[3]/div[2]/button'))).click()        
    driver.switch_to.default_content()

    # run through all pages
    noMoreElements = False
    for i in range(first_page, last_page):
        first = True
        # stop if there are no more items
        if noMoreElements:
            break
        driver.get(f"https://www.second-hand.it/c/auto-motorrad?page={i}")
        # run through all items
        for j in range(1, maxsize):
            try:
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH , f'//*[@id="app"]/div[2]/div[2]/div[4]/div/ul/li[{j}]')))
                if element.text != "":
                    title = element.find_elements_by_class_name('list-item-title')[0].text
                    location = element.find_elements_by_class_name('list-item-location')[0].text
                    price = element.find_elements_by_class_name('list-item-price')[0].text
                    date = element.find_elements_by_class_name('uk-text')[0].text
                    link = element.find_elements_by_class_name('uk-cover-container.list-image')[0].get_attribute("href")
                    
                    # print out fetched data, save latest entry/all entrys after that
                    conv_price = int(price.replace('.', '').split("€")[0])
                    if conv_price >= min_price and conv_price <= max_price:
                        if i == first_page and first:
                            oldEntry = save_latest_entry("second_hand", link)
                            print("---New Second Hand Items---")
                            first = False
                        # stop if oldEntry is equal to current entry
                        if oldEntry == link:
                            noMoreElements = True
                            break
                        print(f"{title} || {price} || {location} || {date} || {link}")
                        with open(".newitems/second_hand.txt", "a") as f:
                            f.write(f"{title} || {price} || {location} || {date} || {link}\n")
            except TimeoutException as e:
                if j == 1:
                    noMoreElements = True
                break

def subito(driver, first_page=1, last_page=20, min_price=0, max_price=10000):
    driver.get("https://www.subito.it")

    # accept cookies
    driver.find_element_by_id("didomi-notice-agree-button").click()

    # run through all pages
    noMoreElements = False
    for i in range(first_page, last_page):
        first = True
        # stop if there are no more items
        if noMoreElements:
            break
        driver.get(f'https://www.subito.it/annunci-italia/vendita/auto/?o={i}')
        for j in range(1, maxsize):
            try:
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH , f'//*[@id="layout"]/main/div[2]/div[6]/div[2]/div[1]/div[4]/div[{j}]')))
                if "BigCard" in element.get_attribute("class"):
                    title = element.find_element_by_tag_name("h2").text
                    price = element.find_element_by_tag_name("p").text
                    location = element.find_elements_by_tag_name("span")[1].text
                    date = element.text.split('\n')[2].split(')')[-1]
                    link = element.find_element_by_tag_name("a").get_attribute("href")
                    
                    # print out fetched data, save latest entry/all entrys after that
                    conv_price = int(price.replace('.', '').split("€")[0])
                    if conv_price >= min_price and conv_price <= max_price:
                        if i == first_page and first:
                            oldEntry = save_latest_entry("subito", link)
                            print("---New Subito Items---")
                            first = False
                        # stop if oldEntry is equal to current entry
                        if oldEntry == link:
                            noMoreElements = True
                            break
                        print(f"{title} || {price} || {location} || {date} || {link}")
                        with open("subito.txt", "a") as f:
                            f.write(f"{title} || {price} || {location} || {date} || {link}\n")
            except TimeoutException as e:
                if j == 1:
                    noMoreElements = True
                break
            
def facebook_marketplace(driver, first_page=1, last_page=20, min_price=0, max_price=10000):
    driver.get("https://www.facebook.com/marketplace")

def main():
    try:
        driver = webdriver.Chrome()

        # fetch new data from websites
        second_hand(driver)
        subito(driver)
        #facebook_marketplace(driver)

        # generate showcase website, open
        gen_website()
        path = join(getcwd(),"index.html")
        driver.get("file:///" + path)
        sleep(10)

        driver.close()
    except (KeyboardInterrupt, NoSuchWindowException):
        print()

if __name__ == "__main__":
    main()
