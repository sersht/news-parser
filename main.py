# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver


def get_html(url):
    browser = webdriver.Firefox()
    browser.get(url)
    html = browser.page_source
    browser.quit()
    return html

# UKR.net version


def main():
    url = "https://www.ukr.net/"
    #html = open("saved.html", "r", encoding="utf-8").read()
    html = get_html(url)

    soup = BeautifulSoup(html, "lxml")
    #open("saved.html", "w", encoding="utf-8").write(soup.prettify())

    news_by_categories = list()

    sections_list = list(soup.select(".feed__section"))
    for section in sections_list:
        category = section.select(".feed__section--title")[0].select("a")[0].get_text(strip=True)
        #print("!!!" + category + "!!!\n")
        #title = section.findAll(name="a", attrs={"href" : True})[1].get_text(strip=True)

        PAIRS = list()
        # Parsing "Головне" section. It has a different structure from other sections
        for subsection in section.findAll(attrs={"class": "feed__section--top"}):
            for news in subsection.findAll(name="a", attrs={"href": True}):
                #print(news.get_text(strip=True))
                #print(news["href"])
                #print("\n")
                PAIRS.append((news.get_text(strip=True), news["href"]))
        # Parsing all other sections
        for subsection in section.findAll(attrs={"class": "feed__item"}):
            for news in subsection.findAll(name="a", attrs={"href": True}):
                PAIRS.append((news.get_text(strip=True), news["href"]))
        
        news_by_categories.append((category, PAIRS))
        #print("<<<<<<<<<<<<<<<<<END>>>>>>>>>>>>>>>>>>\n")
    
    fl = open("results.txt", "w", encoding="utf-8")

    for cat in news_by_categories:
        fl.write(">>>>> Категория: " + cat[0] + "\n")
        for p in cat[1]:
            fl.write("# Заголовок: " + p[0] + "\n")
            fl.write("@ Ссылка: " + p[1] + "\n\n")
        fl.write("\n")


if __name__ == "__main__":
    main()
