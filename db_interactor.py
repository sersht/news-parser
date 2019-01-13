# -*- coding: utf-8 -*-
import os
import psycopg2

import helper


DATABASE_URL = os.environ['DATABASE_URL']

def delete_all_news():
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = connection.cursor()

    query = "DELETE FROM news;"
    cursor.execute(query)
    # connection.commit()

    query = "ALTER SEQUENCE news_id_seq RESTART WITH 1"
    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


# record is tuple (source, category, title, content, link)
def insert_news(record):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = connection.cursor()

    insert_query = '''
        DO
        $do$
        BEGIN
        IF NOT EXISTS (SELECT 1 FROM news WHERE link = '{url}') THEN
            INSERT INTO news (source, category, title, content, link)
            VALUES ('{}', '{}', '{}', '{}', '{}');
        END IF;
        END
        $do$
    '''.format(url=record[4], *record)

    cursor.execute(insert_query)
    connection.commit()

    cursor.close()
    connection.close()


# selected is tuple, len(selected) > 0
def search_by_source(selected):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = connection.cursor()

    query = """
            select id
            from news
            where news.source in {set}
        """.format(set=selected)

    # Cut unnecessary comma in sql-query
    if len(selected) == 1:
        query = query[:-11] + query[-10:]

    cursor.execute(query)

    found = list()
    for i in cursor.fetchall():
        found.append(i[0])

    cursor.close()
    connection.close()

    return set(found)


def search_by_category(selected):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = connection.cursor()

    query = """
            select id
            from news
            where news.category in {set}
        """.format(set=selected)

    # Cut unnecessary comma in sql-query
    if len(selected) == 1:
        query = query[:-11] + query[-10:]

    cursor.execute(query)

    found = list()
    for i in cursor.fetchall():
        found.append(i[0])

    cursor.close()
    connection.close()

    return set(found)


def search_by_content(pattern):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = connection.cursor()

    query = """
            select id
            from news
            where (news.title ilike '%{p}%') or (news.content ilike '%{p}%') 
        """.format(p=pattern)

    cursor.execute(query)

    found = list()
    for i in cursor.fetchall():
        found.append(i[0])

    cursor.close()
    connection.close()

    return set(found)


def get_news_count_in_db():
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = connection.cursor()
    query = "select count(*) from news"

    cursor.execute(query)
    found = cursor.fetchall()

    cursor.close()
    connection.close()

    return int(found[0][0])


def find(sources=[], categories=[], pattern=""):
    if len(sources) == 0 and len(categories) == 0 and len(pattern) == 0:
        return list()

    result = set(range(1, get_news_count_in_db() + 1))

    if len(sources) > 0 and ("all" not in sources):
        for i in range(len(sources)):
            sources[i] = helper.format_for_db(sources[i])
        found_by_sources = search_by_source(tuple(sources))
        result.intersection_update(found_by_sources)

    if len(categories) > 0:
        for i in range(len(categories)):
            categories[i] = helper.format_for_db(categories[i])
        found_by_categories = search_by_category(tuple(categories))
        result.intersection_update(found_by_categories)

    if len(pattern) > 0:
        found_by_pattern = search_by_content(helper.format_for_db(pattern))
        result.intersection_update(found_by_pattern)

    return list(result)


def get_row(index):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = connection.cursor()
    query = "select * from news where news.id = {}".format(index)

    cursor.execute(query)
    found = cursor.fetchone()

    cursor.close()
    connection.close()

    return found