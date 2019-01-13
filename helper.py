# -*- coding: utf-8 -*-
import time
import urllib.request
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# <<<<< BAD >>>>>
def write_news_by_category_in_file(news, file_name, source):
    file_ = open(file_name + ".txt", "w", encoding="utf-8")
    for i in news:
        file_.write("# " + i[0] + "\n")
        file_.write("@ " + i[1] + "\n\n")
    file_.close()


# <<<<< BAD >>>>>
def write_news_in_file(news, file_name, source):
    file_ = open(file_name + ".txt", "w", encoding="utf-8")
    for category in news:
        for i in category[1]:
            file_.write("> " + category[0] + "\n")
            file_.write("# " + i[0] + "\n")
            file_.write("@ " + i[1] + "\n\n")
        file_.write("\n\n")
    file_.close()


# PATH_TO_GECKODRIVER = r"C:\Python37\geckodriver.exe"
PATH_TO_GECKODRIVER = os.path.join(os.path.dirname(__file__), "geckodriver.exe")


def get_html(url, to_scroll=False):
    # Standard version
    # browser = webdriver.Firefox()

    # Headless version
    options = ChromeOptions()
    options.headless = True
    options.binary_location = "/app/.apt/usr/bin/google-chrome-stable"
    browser = webdriver.Chrome(chrome_options=options)
    # options.set_headless(True)
    # options.add_argument("window-size=1920,1080")
    # browser = webdriver.Firefox(options=options, executable_path=PATH_TO_GECKODRIVER)

    # Get html-code from url
    browser.get(url)
    if to_scroll: 
        scroll_down(browser)
    html = browser.page_source

    browser.quit()

    return html


def scroll_down(browser):
    PAUSE_TIME = 1.5

    # Get scroll height
    prev_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to next possible scroll
        time.sleep(PAUSE_TIME)

        # Calculate current scroll height and compare with previous one
        curr_height = browser.execute_script(
            "return document.body.scrollHeight")
        if curr_height == prev_height:
            break
        prev_height = curr_height


def get_parsed_data(url, to_scroll=False):
    html = get_html(url, to_scroll)
    return BeautifulSoup(html, "lxml")


def save_image(url, file_name):
    urllib.request.urlretrieve(url, file_name)


def format_for_db(string):
    formated = string
    
    # Cure "//http..."
    if len(formated) > 1 and formated[0] == formated[1] == "/":
        formated = formated.replace("//", "", 1)
    
    # Replace quotes for correctness of queries
    formated = formated.replace("'", "''")
    formated = formated.replace('"', '""')

    return formated

if __name__ == "__main__":
    parsed = get_parsed_data("https://stackoverflow.com/questions/918154/relative-paths-in-python")
    print(parsed.find("img")["src"])