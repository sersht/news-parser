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

    for news in news_list:
        # First value - title, second value - link
        source = "ukrnet"
        title = helper.format_for_db(news.get_text(strip=True))
        link = helper.format_for_db(news["href"])
        db_interactor.insert_news((source, helper.format_for_db(category), title, "", link))


def get_news_from_categories(parsed_main_page):
    categories_list = get_categories_list(parsed_main_page)
    for category in categories_list:
        parsed_category_page = helper.get_parsed_data(
            "https:" + category[1], to_scroll=True)
        get_news_from_category(category[0], parsed_category_page)


def get_news_from_main(parsed_main_page):
    sections = list(parsed_main_page.select(".feed__section"))
    for section in sections:
        category = section.select(
            ".feed__section--title")[0].select("a")[0].get_text(strip=True)

        # Parse "Головне" section.
        # It has a different html-code structure from other sections.
        source = "ukrnet"
        for subsection in section.findAll(attrs={"class": "feed__section--top"}):
            for news in subsection.findAll(name="a", attrs={"href": True}):
                title = helper.format_for_db(news.get_text(strip=True))
                link = helper.format_for_db(news["href"])
                db_interactor.insert_news((source, helper.format_for_db(category), title, "", link))

        # Parse all other sections.
        for subsection in section.findAll(attrs={"class": "feed__item"}):
            for news in subsection.findAll(name="a", attrs={"href": True}):
                title = helper.format_for_db(news.get_text(strip=True))
                link = helper.format_for_db(news["href"])
                db_interactor.insert_news((source, helper.format_for_db(category), title, "", link))


def parse():
    main_page_url = "https://www.ukr.net/ua/"
    parsed_main_page = helper.get_parsed_data(main_page_url)
    get_news_from_main(parsed_main_page)

    categories = "https://www.ukr.net/news/main.html"
    parsed_categories = helper.get_parsed_data(categories)
    get_news_from_categories(parsed_categories)