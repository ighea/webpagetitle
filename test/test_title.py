from lib.title import Title

import logging, sys, os
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

import werkzeug

def test_request_fallback_works(httpserver):
    
    data = "<html><head><title>Hello to you!!</title></head></html>"
    
    def callback(req):
        callback.counter += 1
        logging.debug("Request attempt #" + str(callback.counter))
        logging.debug(req)
        if(callback.counter > 1):
            logging.debug("Request fails....")
            r = werkzeug.wrappers.Response(status=200, content_type="text", response=data)
        else:
            logging.debug("Request succeeds!")
            r = werkzeug.wrappers.Response(status=511, content_type="text")
        return r
    callback.counter = 0
    
    httpserver.expect_request("/get_title").respond_with_handler(callback)

    t = Title(httpserver.url_for("/get_title"))
    t.fetch()
    title = t.get_title()

    assert title == "Hello to you!!"

def test_request(httpserver):
    
    data = '<!DOCTYPE html><head><title>Hello to you!!</title></head><body><h1>Woo</h1></body></html>'
    
    httpserver.expect_request("/get_title").respond_with_data(data, content_type="html")

    t = Title(httpserver.url_for("/get_title"))
    t.fetch()
    title = t.get_title()
    logging.debug("TITLE IS: " + title)

    assert title == "Hello to you!!"
