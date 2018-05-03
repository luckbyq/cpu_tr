#!/usr/bin/python
#coding=utf-8
import urllib
import urllib2

url = '<sms api url>'

def post(content, tos):
    d = {
        'content': content,
        'tos': tos,
    }
    data = urllib.urlencode(d)
    req = urllib2.Request(url, data)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req)
    return response.read()

if __name__ == "__main__":
    pass