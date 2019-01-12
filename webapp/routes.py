# -*- coding: utf-8 -*-
from flask import Flask,  render_template, redirect, url_for, request
from webapp import app
import db_interactor, tsnua


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    search_text = request.form["fts"]
    categories_list = [x.strip() for x in request.form["category"].split(",")]
    # Check if categories form is empty
    if len(categories_list) == 1 and categories_list[0] == '':
        categories_list.clear()
    sources_list = request.form.getlist("select")

    search_results = db_interactor.find(
        pattern=search_text, categories=categories_list, sources=sources_list)

    news_list = list()
    for index in search_results:
        news_list.append(db_interactor.get_row(index))

    return render_template("search-results.html", news=news_list)


@app.route("/content/<index>")
def content(index):
    text = db_interactor.get_row(int(index))[4]
    return render_template("content.html", TEXT=text)


@app.route("/images/<index>")
def imgs(index):
    url = db_interactor.get_row(int(index))[5]
    lst = tsnua.get_images(url)
    return render_template("images.html", img=lst)