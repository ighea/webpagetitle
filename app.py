#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import abort 

from lib.title import Title

import logging, sys, os

logging_level = logging.DEBUG
if os.environ['FLASK_ENV'] == "production":
    logging_level = logging.ERROR
logging.basicConfig(stream=sys.stderr, level=logging_level)

app = Flask(__name__)

# POST url param, get title as reponse
@app.route('/', methods=['POST'])
def title():

    timeout = 30

    url = request.form.get('url')
    logging.debug("URL:" + url);
    
    if url is None:
        abort(400)
    
    title = Title(url)
    title.fetch()
    
    method = title.get_method()
    title = title.get_title()
    if title is None:
        abort(500)
    
    if method is "requests":
        title = title + " (F)"

    logging.debug("Final title: " + title);
    
    return title
