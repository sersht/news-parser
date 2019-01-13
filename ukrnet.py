# -*- coding: utf-8 -*-
import helper
import db_interactor


def get_categories_list(parsed_categories_page):
    categories = parsed_categories_page.findAll(
        name="a", attrs={"class": "n-m_li_a ps-h", "href": True})

    titles_and_links = list()
    for category in categories:
        titles_and_links.append(
            (category.get_text(strip=True), category["href"]))

    return titles_and_links


def get_news_from_category(category, parsed_category_page):
    news_list = parsed_category_page.findAll(
        name="a", attrs={"class": "im-tl_a", "href": True})

    # news_from_category = list()
    for news in news_list:
        # First value - title, second value - link
        # news_from_category.append(
        #     (news.get_text(strip=True), news["href"]))
        source = "ukrnet"
        title = news.get_text(strip=True)
        link = news["href"]
        db_interactor.insert_news((source, category, title, "", link))

    # return news_from_category


def get_news_from_categories(parsed_main_page):
    # news_by_categories = list()
    
    categories_list = get_categories_list(parsed_main_page)
    for category in categories_list:
        parsed_category_page = helper.get_parsed_data(
            "https:" + category[1], to_scroll=True)
        # news_by_category = get_news_from_category(parsed_category_page)
        get_news_from_category(category[0], parsed_category_page)

        # news_by_categories.append((category[0], news_by_category))
        # helper.write_news_by_category_in_file(news_by_category, category[0], "ukrnet")
    
    # return news_by_categories


def get_news_from_main(parsed_main_page):
    # news_from_main = list()

    sections = list(parsed_main_page.select(".feed__section"))
    for section in sections:
        category = section.select(
            ".feed__section--title")[0].select("a")[0].get_text(strip=True)

        # titles_and_links = list()

        # Parse "Головне" section.
        # It has a different html-code structure from other sections.
        source = "ukrnet"
        for subsection in section.findAll(attrs={"class": "feed__section--top"}):
            for news in subsection.findAll(name="a", attrs={"href": True}):
                # titles_and_links.append(
                #     (news.get_text(strip=True), news["href"]))
                title = news.get_text(strip=True)
                link = news["href"]
                db_interactor.insert_news((source, category, title, "", link))

        # Parse all other sections.
        for subsection in section.findAll(attrs={"class": "feed__item"}):
            for news in subsection.findAll(name="a", attrs={"href": True}):
                # titles_and_links.append(
                #     (news.get_text(strip=True), news["href"]))
                title = news.get_text(strip=True)
                link = news["href"]
                db_interactor.insert_news((source, category, title, "", link))

        # news_from_main.append((category, titles_and_links))

    # return news_from_main


def parse():
    all_news = list()
    
    main_page_url = "https://www.ukr.net/ua/"
    parsed_main_page = helper.get_parsed_data(main_page_url)
    get_news_from_main(parsed_main_page)
    # news_from_main = get_news_from_main(parsed_main_page)
    # helper.write_news_in_file(source="ukrnet", news=news_from_main, file_name="UKRNET-main")
    # all_news.extend(news_from_main)

    categories = "https://www.ukr.net/news/main.html"
    parsed_categories = helper.get_parsed_data(categories)
    get_news_from_categories(parsed_categories)
    # news_by_categories = get_news_from_categories(parsed_categories)
    # helper.write_news_in_file(source="ukrnet", news=news_by_categories, file_name="UKRNET-categories")
    # all_news.extend(news_by_categories)

    # return all_news