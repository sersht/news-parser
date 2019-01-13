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

    # In some articles title saved in different class
    # title = parsed_page.find(
    #     attrs={"class": "p-name c-post-title u-uppercase"})
    # if title is None:
    #     title = parsed_page.find(
    #         attrs={"class": "p-name c-post-title u-uppercase js-si-title"})
    # title = title.get_text(strip=True)

    article = parsed_page.find(
        name="article", attrs={"class": "o-cmr u-content-read"})

    if article is None:
        raise ValueError("Didn't recognise as article")

    # Get unformated text directly from <article> tag
    # text = article.get_text(strip=True)

    # Get text iterating article tag-by-tag
    text = str()
    for tag in article.findAll(name="p"):
        for string in tag.stripped_strings:
            text += (string + " ")

    return ("title", text, "images")


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
    # news = list()
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CATEGORY")
    for article in articles:
        news_data_tag = article.find(name="div")
        post_meta_tag = news_data_tag.find(attrs={"class": "c-post-meta"})

        # Check if news-block is valid
        if post_meta_tag is None:
            continue

        source = "tsnua"
        title = post_meta_tag.find(name="a").get_text(strip=True)
        link = news_data_tag.find(name="a")["href"]
        # image_url = article.find(name="img")["src"]

        # news.append((title, link, image_url))

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> TRY ADD")
        try:
            raw_content = tsnua.get_content(link)[1]
            content = helper.format_for_db(raw_content)
            db_interactor.insert_news((source, category, title, content, link))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ADDED NEWS")
        except Exception as e:
            print("@@@@@@@@@@@@@@@@@@@@@@@@", end="")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

    # return news


def get_news_from_category(category, parsed_category_page):
    articles = parsed_category_page.findAll(
        name="article", attrs={"class": ["h-entry", "c-entry"]})
    # return parse_news_page(articles)
    parse_news_page(category, articles)


def get_news_from_categories(categories):
    news = list()
    
    for category in categories:
        parsed_category_page = helper.get_parsed_data(category[1])
        # news_list_from_category = get_news_from_category(parsed_category_page)
        # news.append((category[0], news_list_from_category))
        # helper.write_news_by_category_in_file(news_list_from_category, category[0], "tsnua")

        get_news_from_category(category[0], parsed_category_page)
        
    return news


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
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PARSE")
    # all_news = list()

    main_page_url = "https://tsn.ua/"
    
    parsed_main_page = helper.get_parsed_data(main_page_url)
    # news_from_main = get_news_from_main(parsed_main_page)
    # helper.write_news_by_category_in_file(news_from_main, "TSN-main", "tsnua")
    # all_news.extend(news_from_main)

    categories_list = get_categories_list(parsed_main_page)
    get_news_from_categories(categories_list)
    # news_by_categories = get_news_from_categories(categories_list)
    # helper.write_news_in_file(news_by_categories, "TSN-categories", "tsnua")
    # all_news.extend(news_by_categories)

    # return all_news