# UKR.net version
from bs4 import BeautifulSoup
from selenium import webdriver
import time


""" <<<<< BAD >>>>> """
def write_news_by_category_in_file(news, file_name):
    fl = open(file_name + ".txt", "w", encoding="utf-8")
    for p in news:
        fl.write("# Заголовок: " + p[0] + "\n")
        fl.write("@ Ссылка: " + p[1] + "\n\n")
    fl.write("\n\n")

""" <<<<< BAD >>>>> """
def write_news_in_file(news, file_name):
    fl = open(file_name + ".txt", "w", encoding="utf-8")
    for cat in news:
        fl.write(">>>>> Категория: " + cat[0] + "\n")
        for p in cat[1]:
            fl.write("# Заголовок: " + p[0] + "\n")
            fl.write("@ Ссылка: " + p[1] + "\n\n")
        fl.write("\n\n")


def get_html(url, to_scroll=False):
    browser = webdriver.Firefox()
    
    # Get html-code from url
    browser.get(url)
    if to_scroll:
       scroll_down(browser)
    html = browser.page_source
    
    browser.quit()
    
    return html


def scroll_down(driver):
    SCROLL_PAUSE_TIME = 1.0

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_parsed_data(url, to_scroll=False):
    html = get_html(url, to_scroll)
    parsed_data = BeautifulSoup(html, "lxml")
    return parsed_data


""" Memory """
def ukr_net_parse_main_page(parsed_main):
    news_from_main = list()

    sections = list(parsed_main.select(".feed__section"))
    for section in sections:
        category = section.select(
            ".feed__section--title")[0].select("a")[0].get_text(strip=True)

        titles_and_links = list()

        # Parsing "Головне" section.
        # It has a different html-code structure from other sections.
        for subsection in section.findAll(attrs={"class": "feed__section--top"}):
            for news in subsection.findAll(name="a", attrs={"href": True}):
                titles_and_links.append(
                    (news.get_text(strip=True), news["href"]))

        # Parsing all other sections.
        for subsection in section.findAll(attrs={"class": "feed__item"}):
            for news in subsection.findAll(name="a", attrs={"href": True}):
                titles_and_links.append(
                    (news.get_text(strip=True), news["href"]))

        news_from_main.append((category, titles_and_links))

    return news_from_main

""" Memory """
def get_categories_list(parsed_categories_page):
    names_and_links = list()
    for category in parsed_categories_page.findAll(name="a", attrs={"class": "n-m_li_a ps-h", "href": True}):
        names_and_links.append(
            (category.get_text(strip=True), category["href"]))
    return names_and_links

""" Memory """
def get_news_by_category(category_page):
    news_list = list()
    for news in category_page.findAll(name="a", attrs={"class": "im-tl_a", "href": True}):
        news_list.append((news.get_text(strip=True), news["href"]))
    return news_list


def ukr_net_parse_categories(parsed_categories):
    news_by_categories = list()
    
    categories_list = get_categories_list(parsed_categories)
    for category in categories_list:
        parsed_category_page = get_parsed_data("https:" + category[1], True)
        news_by_category = get_news_by_category(parsed_category_page)
        
        news_by_categories.append((category[0], news_by_category))
        
        write_news_by_category_in_file(news_by_category, category[0])

    return news_by_categories


def ukr_net():
    main = "https://www.ukr.net/ua/"
    parsed_main = get_parsed_data(main)
    news_from_main = ukr_net_parse_main_page(parsed_main)
    write_news_in_file(news_from_main, "news from main")

    categories = "https://www.ukr.net/news/main.html"
    parsed_categories = get_parsed_data(categories)
    news_by_categories = ukr_net_parse_categories(parsed_categories)
    # write_news_in_file(news_by_categories, "news by categories")


def main():
    # html = open("saved.html", "r", encoding="utf-8").read()
    # open("saved.html", "w", encoding="utf-8").write(parsed_data.prettify())
    ukr_net()


if __name__ == "__main__":
    main()
