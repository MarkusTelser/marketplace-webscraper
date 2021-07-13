from data import save_latest_entry, write_data

from sys import maxsize
from time import sleep
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def second_hand(driver, first_page=1, last_page=50, max_elements=100, min_price=500, max_price=10000):
    driver.get("https://www.second-hand.it")

    # accept cookies
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath('//*[@id="sp_message_iframe_511960"]')))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="notice"]/div[3]/div[2]/button'))).click()
    driver.switch_to.default_content()

    stack = []  # save data to write to file

    # run through all pages
    noMoreElements = False
    elements = 0
    for i in range(first_page, last_page):
        # stop if there are no more items
        if noMoreElements:
            break
        # fetch only max count of elements
        if elements >= max_elements:
            break
        driver.get(f"https://www.second-hand.it/c/auto-motorrad?page={i}")
        # run through all items
        for j in range(1, maxsize):
            if elements >= max_elements:
                break
            try:
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div[2]/div[2]/div[4]/div/ul/li[{j}]')))
                if element.text != "":
                    title = element.find_elements_by_class_name('list-item-title')[0].text
                    location = element.find_elements_by_class_name('list-item-location')[0].text.split(' ')[1]
                    price = element.find_elements_by_class_name('list-item-price')[0].text
                    date = element.find_elements_by_class_name('uk-text')[0].text
                    link = element.find_elements_by_class_name('uk-cover-container.list-image')[0].get_attribute("href")

                    # add real date and not "today"
                    if ":" in date:
                        date += " " + datetime.today().strftime('%d.%m.%Y')
                    else:
                        date += datetime.today().strftime('%Y')

                    # print out fetched data, save latest entry/all entrys after that
                    conv_price = int(price.replace('.', '').split("€")[0].split(' ')[0])
                    if min_price <= conv_price <= max_price:
                        if elements == 0:
                            oldEntry = save_latest_entry("second_hand", link)
                            print("---New Second Hand Items---")
                        # stop if oldEntry is equal to current entry
                        if oldEntry == link:
                            noMoreElements = True
                            break
                        print(f"{title} || {price} || {location} || {date} || {link}")
                        stack.append([title, price, location, date, link])
                        elements += 1
            except TimeoutException as e:
                if j == 1:
                    noMoreElements = True
                break

    # write them all to file
    write_data(stack, "second_hand")


def subito(driver, first_page=1, last_page=50, max_elements=100, min_price=500, max_price=10000, min_mileage=0, max_mileage=100000):
    driver.get("https://www.subito.it")

    # accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button'))).click()

    stack = []  # save data to write to file

    # run through all pages
    noMoreElements = False
    elements = 0
    for i in range(first_page, last_page):
        # stop if there are no more items
        if noMoreElements:
            break
        # fetch only max count of elements
        if elements >= max_elements:
            break
        driver.get(f'https://www.subito.it/annunci-italia/vendita/auto/?o={i}')
        for j in range(1, maxsize):
            if elements >= max_elements:
                break
            try:
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="layout"]/main/div[2]/div[6]/div[2]/div[1]/div[4]/div[{j}]')))
                if "BigCard" in element.get_attribute("class"):
                    title = element.find_element_by_tag_name("h2").text
                    price = element.find_element_by_tag_name("p").text
                    location = element.find_elements_by_tag_name("span")[1].text
                    date = element.text.split('\n')[2].split(')')[-1]
                    link = element.find_element_by_tag_name("a").get_attribute("href")
                    mileage = element.find_elements_by_tag_name("p")[3].text

                    # add real date and not "today"
                    if "Oggi" in date:
                        date += " " + datetime.today().strftime('%d.%m.%Y')

                    # print out fetched data, save latest entry/all entrys after that
                    conv_price = int(price.replace('.', '').split("€")[0])
                    conv_mileage = int(mileage.split(' ')[0]) if "-" not in mileage else 0
                    if min_price <= conv_price <= max_price and min_mileage <= conv_mileage <= max_mileage:
                        if elements == 0:
                            oldEntry = save_latest_entry("subito", link)
                            print("---New Subito Items---")
                        # stop if oldEntry is equal to current entry
                        if oldEntry == link:
                            noMoreElements = True
                            break
                        print(f"{title} || {price} || {location} || {date} || {link} || {mileage}")
                        stack.append([title, price, location, date, link, mileage])
                        elements += 1
            except TimeoutException as e:
                if j == 1:
                    noMoreElements = True
                break

    # write them all to file
    write_data(stack, "subito")


def auto_suedtirol(driver, first_page=1, last_page=50, max_elements=100, min_price=500, max_price=10000, min_mileage=0, max_mileage=100000):
    driver.get("https://auto-suedtirol.com")

    # accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'catapultCookie'))).click()

    stack = []  # save data to write to file

    # run through all pages
    noMoreElements = False
    elements = 0
    for i in range(first_page, last_page):
        # stop if there are no more items
        if noMoreElements:
            break
        # fetch only max count of elements
        if elements >= max_elements:
            break
        driver.get(f'https://auto-suedtirol.com/autos/page/{i}/?filter&keyword&from-year&to-year&min-price={min_price}&max-price={max_price}')
        for j in range(1, maxsize):
            if elements >= max_elements:
                break
            try:
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="post-1120"]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div[{j}]')))

                title = element.find_element_by_class_name("item-title").text
                price = element.find_element_by_class_name("iw-meta-price").text
                try:
                    location = element.find_element_by_class_name("location-town").text
                except NoSuchElementException:
                    location = "no location"
                date = "no date"
                link = element.find_element_by_class_name("iw-property-title").find_element_by_tag_name("a").get_attribute("href")
                mileage = element.find_element_by_class_name("iw-meta-beds").text

                # add real date and not "today"
                if "Oggi" in date:
                    date += " " + datetime.today().strftime('%d.%m.%Y')

                # print out fetched data, save latest entry/all entrys after that
                conv_price = int(price.replace('.', '').split(" ")[-1])
                conv_mileage = int(mileage.split(' ')[0]) if "-" not in mileage else 0
                if min_price <= conv_price <= max_price and min_mileage <= conv_mileage <= max_mileage:
                    if elements == 0:
                        oldEntry = save_latest_entry("auto_suedtirol", link)
                        print("---New Auto-Suedtirol Items---")
                    # stop if oldEntry is equal to current entry
                    if oldEntry == link:
                        noMoreElements = True
                        break
                    print(f"{title} || {price} || {location} || {date} || {link} || {mileage}")
                    stack.append([title, price, location, date, link, mileage])
                    elements += 1
            except TimeoutException as e:
                if j == 1:
                    noMoreElements = True
                break

    # write them all to file
    write_data(stack, "subito")


def facebook_marketplace(driver, first_element=1, last_element=40, max_elements=50, min_price=0, max_price=10000):
    """
    facebook marketplace is the biggest bullshit platform of all and wants to lose customers without any mercy
    just to fuck around they change the css classes and everything that would be definable, so nobody can scrape anything
    but they themself steal everything that isn't nailed onto the ground, i am not trying to finish this fucking method
    """
    driver.get("https://www.facebook.com/marketplace")

    # accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="facebook"]/body/div[2]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div[3]/div/div[1]/div[1]'))).click()
    sleep(0.5)

    driver.get(f"https://www.facebook.com/marketplace/109939089035498/vehicles?minPrice={min_price}&maxPrice={max_price}&exact=true")
    for i in range(first_element, last_element):
        elements = driver.find_elements_by_class_name('_1oem')

        for element in elements:
            print(element.text)
