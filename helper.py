# -*- coding: utf-8 -*-
import time
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# <<<<< BAD >>>>>
def write_news_by_category_in_file(news, file_name, source):
    file_ = open(file_name + ".txt", "w", encoding="utf-8")
    for i in news:
        if (source == "tsnua"):
            file_.write("# " + i["title"] + "\n")
            file_.write("@ " + i["link"] + "\n\n")
        else:
            file_.write("# " + i[0] + "\n")
            file_.write("@ " + i[1] + "\n\n")
    file_.close()


# <<<<< BAD >>>>>
def write_news_in_file(news, file_name, source):
    file_ = open(file_name + ".txt", "w", encoding="utf-8")
    for category in news:
        for i in category[1]:
            file_.write("> " + category[0] + "\n")
            if (source == "tsnua"):
                file_.write("# " + i["title"] + "\n")
                file_.write("@ " + i["link"] + "\n\n")
            else:
                file_.write("# " + i[0] + "\n")
                file_.write("@ " + i[1] + "\n\n")
        #file_.write("\n\n")
    file_.close()


PATH_TO_GECKODRIVER = r"C:\Python37\geckodriver.exe"

def get_html(url, to_scroll=False):
    # Standard version
    # browser = webdriver.Firefox()

    # Headless version
    options = Options()
    options.set_headless(True)
    # options.add_argument("window-size=1920,1080")
    browser = webdriver.Firefox(
        options=options, executable_path=PATH_TO_GECKODRIVER)

    # Get html-code from url
    browser.get(url)
    if to_scroll:
        scroll_down(browser)
    html = browser.page_source

    browser.quit()

    return html


def scroll_down(browser):
    PAUSE_TIME = 1.0

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

    # Use lxml parser
    parsed_data = BeautifulSoup(html, "lxml")

    return parsed_data


def save_image(url, file_name):
    urllib.request.urlretrieve(url, file_name)