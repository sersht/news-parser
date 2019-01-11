# -*- coding: utf-8 -*-
import time
import psycopg2

import helper
import ukrnet
import tsnua


DB_CONNECTION_CONFIG = {
    "user": "postgres",
    "password": "123456",
    "host": "127.0.0.1",
    "port": "5432",
    "db_name": "news"}


def delete_all_news():
    connection = psycopg2.connect(
        user=DB_CONNECTION_CONFIG["user"],
        password=DB_CONNECTION_CONFIG["password"],
        host=DB_CONNECTION_CONFIG["host"],
        port=DB_CONNECTION_CONFIG["port"],
        database=DB_CONNECTION_CONFIG["db_name"])

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
    connection = psycopg2.connect(
        user=DB_CONNECTION_CONFIG["user"],
        password=DB_CONNECTION_CONFIG["password"],
        host=DB_CONNECTION_CONFIG["host"],
        port=DB_CONNECTION_CONFIG["port"],
        database=DB_CONNECTION_CONFIG["db_name"])

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
    connection = psycopg2.connect(
        user=DB_CONNECTION_CONFIG["user"],
        password=DB_CONNECTION_CONFIG["password"],
        host=DB_CONNECTION_CONFIG["host"],
        port=DB_CONNECTION_CONFIG["port"],
        database=DB_CONNECTION_CONFIG["db_name"])

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
    connection = psycopg2.connect(
        user=DB_CONNECTION_CONFIG["user"],
        password=DB_CONNECTION_CONFIG["password"],
        host=DB_CONNECTION_CONFIG["host"],
        port=DB_CONNECTION_CONFIG["port"],
        database=DB_CONNECTION_CONFIG["db_name"])

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
    connection = psycopg2.connect(
        user=DB_CONNECTION_CONFIG["user"],
        password=DB_CONNECTION_CONFIG["password"],
        host=DB_CONNECTION_CONFIG["host"],
        port=DB_CONNECTION_CONFIG["port"],
        database=DB_CONNECTION_CONFIG["db_name"])

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
    connection = psycopg2.connect(
        user=DB_CONNECTION_CONFIG["user"],
        password=DB_CONNECTION_CONFIG["password"],
        host=DB_CONNECTION_CONFIG["host"],
        port=DB_CONNECTION_CONFIG["port"],
        database=DB_CONNECTION_CONFIG["db_name"])

    cursor = connection.cursor()
    query = "select count(*) from news"

    cursor.execute(query)
    found = cursor.fetchall()

    cursor.close()
    connection.close()

    return int(found[0][0])


# Needed speed up
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


# # delete_all_news()

# beg = time.time()
# a = tsnua.parse()
# #b = ukrnet.parse()
# end = time.time()

# print("parsing is over...", end=" ")
# print("estimated " + str(int((end - beg) / 60)) + "min " + str(int((end - beg)) % 60) + "sec")

# source = "tsnua"
# content = ""

# beg = time.time()
# for i in a:
#     category = helper.format_for_db(i[0])
#     for j in i[1]:
#         title = helper.format_for_db(j[0])
#         link = helper.format_for_db(j[1])

#         beg = time.time()
#         try:
#             raw_content = tsnua.get_content(link)[1]
#             #content = helper.format_for_db(raw_content)
#             content = " "
#             insert_news((source, category, title, content, link))
#         except:
#             pass
#         end = time.time()
#         print(end - beg)
#         exit()
        
# end = time.time()
# print("estimated " + str(int((end - beg) / 60)) + "min " + str(int((end - beg)) % 60) + "sec")

# source = "ukrnet"
# content = ""

# beg = time.time()
# for i in b:
#     category = helper.format_for_db(i[0])
#     for j in i[1]:
#         title = helper.format_for_db(j[0])
#         link = helper.format_for_db(j[1])
#         insert_news((source, category, title, content, link))
# end = time.time()

# print("estimated " + str(int((end - beg) / 60)) + "min " + str(int((end - beg)) % 60) + "sec")
# #print(len(a[0][1]))