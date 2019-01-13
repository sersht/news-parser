# -*- coding: utf-8 -*-
import time
import urllib.request
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_html(url, to_scroll=False):
    # Headless version
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.binary_location = "/app/.apt/usr/bin/google-chrome-stable"
    
    browser = webdriver.Chrome(chrome_options=options)
    
    # Get html-code from url
    browser.get(url)
    if to_scroll: 
        scroll_down(browser)
    html = browser.page_source

    browser.quit()

    return html


def scroll_down(browser):
    PAUSE_TIME = 2

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