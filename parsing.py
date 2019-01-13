# -*- coding: utf-8 -*-
import ukrnet
import tsnua
import db_interactor
import helper


def do():
    tsnua.parse()
    # ukrnet.parse()

def second_do():
    source = "ukrnet"
    content = ""
    print("PARSING >>>>>>>>>>>>>>>>>>>>>>>>> Begin parsing UKRNET")
    ukrnet_news = ukrnet.parse()

    print("PARSING >>>>>>>>>>>>>>>>>>>>>>>>> Begin process UKRNET")
    for pair in ukrnet_news:
        category = helper.format_for_db(pair[0])
        for news in pair[1]:
            title = helper.format_for_db(news[0])
            link = helper.format_for_db(news[1])

            db_interactor.insert_news((source, category, title, content, link))
    print("PARSING >>>>>>>>>>>>>>>>>>>>>>>>> Finished UKRNET")

    source = "tsnua"
    print("PARSING >>>>>>>>>>>>>>>>>>>>>>>>> Begin parsing TSNUA")
    tsnua_news = tsnua.parse()

    print("PARSING >>>>>>>>>>>>>>>>>>>>>>>>> Begin process TSNUA")
    for pair in tsnua_news:
        category = helper.format_for_db(pair[0])
        for news in pair[1]:
            title = helper.format_for_db(news[0])
            link = helper.format_for_db(news[1])

            try:
                raw_content = tsnua.get_content(link)[1]
                content = helper.format_for_db(raw_content)
                insert_news((source, category, title, content, link))
            except:
                pass
    print("PARSING >>>>>>>>>>>>>>>>>>>>>>>>> Finished TSNUA")