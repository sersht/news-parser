# -*- coding: utf-8 -*-
import helper


# Get news content by url
def get_content(url):
    parsed_page = helper.get_parsed_data(url, True)

    # In some articles title saved in different class
    title = parsed_page.find(
        attrs={"class": "p-name c-post-title u-uppercase"})
    if title is None:
        title = parsed_page.find(
            attrs={"class": "p-name c-post-title u-uppercase js-si-title"})
    title = title.get_text(strip=True)

    # Save all images links (by tag <img>)
    images = list()
    for image in parsed_page.find(name="div", attrs={"class": "h-entry c-main"}).findAll(name="img"):
        images.append(image["src"])

    article = parsed_page.find(
        name="article", attrs={"class": "o-cmr u-content-read"})

    # Get unformated text directly from <article> tag
    # print(article.get_text(strip=True))

    # Get text iterating article tag-by-tag
    text = str()
    for tag in article.findAll(name="p"):
        for string in tag.stripped_strings:
            text += (string + " ")

    return {"title": title, "text": text, "images": images}


def parse_news_page(articles):
    news = list()

    for article in articles:
        news_data_tag = article.find(name="div")
        post_meta_tag = news_data_tag.find(attrs={"class": "c-post-meta"})

        # Check if news-block is valid
        if post_meta_tag is None:
            continue

        title = post_meta_tag.find(name="a").get_text(strip=True)
        link = news_data_tag.find(name="a")["href"]
        image_url = article.find(name="img")["src"]

        news.append({"title": title, "link": link, "image_url": image_url})

    return news


def get_categories_list(parsed_main_page):
    categories = parsed_main_page.find(
        attrs={"class": "container u-px-0 c-app-nav js-si-nav"}).findAll(name="li", attrs={"class": True})

    titles_and_links = list()
    for category in categories:
        title = category.find(name="a").get_text(strip=True)
        link = category.find(name="a")["href"]

        titles_and_links.append({"title": title, "link": link})

    # Delete "Main-page" category
    del titles_and_links[0]

    return titles_and_links


def get_news_from_category(parsed_category_page):
    articles = parsed_category_page.findAll(
        name="article", attrs={"class": ["h-entry", "c-entry"]})
    return parse_news_page(articles)


def get_news_from_categories(categories):
    # parsed_page = helper.get_parsed_data(url, True)
    news = list()

    i = 0
    for category in categories:
        i += 1
        
        parsed_category_page = helper.get_parsed_data(category["link"])
        news_list_from_category = get_news_from_category(parsed_category_page)
        news.append((category["title"], news_list_from_category))

        if (i == 2): break 
        # helper.write_news_by_category_in_file(news_list_from_category, category["title"])

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

        news.append({"title": title, "link": link, "image_url": "None"})

    return news


def parse():
    main_page_url = "https://tsn.ua/"
    parsed_main_page = helper.get_parsed_data(main_page_url)
    news_from_main = get_news_from_main(parsed_main_page)
    helper.write_news_by_category_in_file(news_from_main, "TSN-main", "tsnua")

    categories_list = get_categories_list(parsed_main_page)
    news_by_categories = get_news_from_categories(categories_list)
    helper.write_news_in_file(news_by_categories, "TSN-categories", "tsnua")