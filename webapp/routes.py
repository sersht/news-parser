# -*- coding: utf-8 -*-
from flask import Flask,  render_template, redirect, url_for, request
from webapp import app
import db_interactor


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# просмотреть содержимое - кнопка, перейти на новость - кнопка,
# просмотреть изображения и скачать (если нужно) - конопка и отдельная страница
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("msg.html")

    search_text = request.form["fts"]
    categories_list = [x.strip() for x in request.form["category"].split(",")]
    if len(categories_list) == 1 and categories_list[0] == '':
        categories_list.clear()
    sources_list = request.form.getlist("select")

    search_results = db_interactor.find(
        pattern=search_text, categories=categories_list, sources=sources_list)

    s = str()
    for x in search_results:
        s += str(x) + "\n"

    return s
