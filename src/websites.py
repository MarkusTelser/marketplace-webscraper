from main import save_latest_entry, write_data
from sys import maxsize
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

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
                    conv_price = int(price.replace('.', '').split("€")[0].split(' ')[0])
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
                        write_data("second_hand", title, conv_price, location, date, link)
            except TimeoutException as e:
                if j == 1:
                    noMoreElements = True
                break

def subito(driver, first_page=1, last_page=20, min_price=0, max_price=10000):
    driver.get("https://www.subito.it")

    # accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button'))).click()

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
                        write_data("subito", title, conv_price, location, date, link)
            except TimeoutException as e:
                if j == 1:
                    noMoreElements = True
                break

def facebook_marketplace(driver, first_element=1, last_element=40, min_price=0, max_price=10000):
    driver.get("https://www.facebook.com/marketplace")

    # accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="facebook"]/body/div[2]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div[3]/div/div[1]/div[1]'))).click()
    sleep(0.5)

    driver.get(f"https://www.facebook.com/marketplace/109939089035498/vehicles?minPrice={min_price}&maxPrice={max_price}&exact=true")
    for i in range(first_element, last_element):
        elements = driver.find_elements_by_class_name('_1oem')
        
        for element in elements:
            print(element.text)