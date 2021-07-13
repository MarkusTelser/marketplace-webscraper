import websites as web
from page import gen_website
from data import remove_data, open_website

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException


def main():
    try:
        remove_data()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")  # open in incognito mode
        chrome_options.add_argument("--start-maximized")  # opens window max dimensions
        chrome_options.add_experimental_option("detach", True)  # stop closing
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # disable logging

        driver = webdriver.Chrome(options=chrome_options)

        # fetch new data from websites
        web.second_hand(driver, max_elements=20)
        web.subito(driver, max_elements=20)
        web.auto_suedtirol(driver, max_elements=20)

        # generate showcase website, open
        gen_website()
        open_website(driver)
    except (KeyboardInterrupt, NoSuchWindowException):
        print()


if __name__ == "__main__":
    main()
