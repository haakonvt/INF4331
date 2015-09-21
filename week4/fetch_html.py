#!/usr/bin/env python
# encoding: utf-8
import urllib
import codecs

def get_html_content(url):
    #response = urllib.urlopen(url)
    #response = codecs.open('short_noreg.txt','r','utf-8') #Speed things up BEFORE delivery...
    response = open('short_noreg.txt', 'r')
    return response#.read()

if __name__ == '__main__':
    url = 'http://folk.uio.no/haakonvt/'
    data = get_html_content(url)
    print data
