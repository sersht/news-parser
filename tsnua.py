# -*- coding: utf-8 -*-
import helper
import db_interactor


def get_images(url):
    try:
        parsed_page = helper.get_parsed_data(url)

        # Save all images links (by tag <img>)
        images = list()
        for image in parsed_page.find(name="div", attrs={"class": "h-entry c-main"}).findAll(name="img"):
            images.append(image["src"])

        return images
    except:
        return list()


def get_content(url):
    parsed_page = helper.get_parsed_data(url)

    article = parsed_page.find(
        name="article", attrs={"class": "o-cmr u-content-read"})

    if article is None:
        raise ValueError("Didn't recognise as article")

    # Get text iterating article tag-by-tag
    text = str()
    for tag in article.findAll(name="p"):
        for string in tag.stripped_strings:
            text += (string + " ")

    return ("pseudo_title", text, "pseudo_images")


def get_categories_list(parsed_main_page):
    categories = parsed_main_page.find(
        attrs={"class": "container u-px-0 c-app-nav js-si-nav"}).findAll(name="li", attrs={"class": True})

    titles_and_links = list()
    for category in categories:
        title = category.find(name="a").get_text(strip=True)
        link = category.find(name="a")["href"]

        titles_and_links.append((title, link))

    # Delete "Main-page" category
    del titles_and_links[0]

    return titles_and_links


def parse_news_page(category, articles):
    for article in articles:
        news_data_tag = article.find(name="div")
        post_meta_tag = news_data_tag.find(attrs={"class": "c-post-meta"})

        # Check if news-block is valid
        if post_meta_tag is None:
            continue

        source = "tsnua"
        title = helper.format_for_db(post_meta_tag.find(name="a").get_text(strip=True))
        link = helper.format_for_db(news_data_tag.find(name="a")["href"])

        try:
            raw_content = get_content(link)[1]
            content = helper.format_for_db(raw_content)
            db_interactor.insert_news((source, helper.format_for_db(category), title, content, link))
        except Exception as e:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(e)


def get_news_from_category(category, parsed_category_page):
    articles = parsed_category_page.findAll(
        name="article", attrs={"class": ["h-entry", "c-entry"]})
    parse_news_page(category, articles)


def get_news_from_categories(categories):
    for category in categories:
        parsed_category_page = helper.get_parsed_data(category[1])
        get_news_from_category(category[0], parsed_category_page)
        break


def get_news_from_main(parsed_main_page):
    # Parse central part
    articles = parsed_main_page.find(name="div", attrs={"class": "c-main"}).findAll(
        name="article", attrs={"class": ["h-entry", "c-entry"], "data-vr-contentbox": True})

    # Get news from central part
    news = parse_news_page(articles)

    # Parse side-bar
    articles = parsed_main_page.find(
        attrs={"class": "c-sidebar-box"}).findAll(name="article")

    # Get news from side-bar
    for article in articles:
        news_tag = article.find(name="a", attrs={"class": "u-url u-uid"})

        title = news_tag.get_text(strip=True)
        link = news_tag["href"]

        # Third value - head-image url 
        news.append((title, link, ""))

    return news


def parse():
    main_page_url = "https://tsn.ua/"
    parsed_main_page = helper.get_parsed_data(main_page_url)

    categories_list = get_categories_list(parsed_main_page)
    get_news_from_categories(categories_list)