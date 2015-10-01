#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
import urllib, re

def get_html_content(url):
    response = urllib.urlopen(url)
    html     = response.read()
    return html


def get_list_of_results():
    url  = 'http://fil.nrk.no/yr/viktigestader/noreg.txt'
    html = get_html_content(url)

    #html = open('small_noreg.txt', 'r').read()
    #html_file = open('noreg.txt', 'r')
    #html      = html_file.read(); html_file.close()
    location  = raw_input('Please input a location to find wheather forecast: ')

    t0 = time() # Time the computations

    # If user input one/more wildcard, add a dot-character right before for regex-support
    location = re.sub('\*', '.*', location)

    regular_expr = 'http://www\.yr\.no/place/Norway/[^/]*/[^/]*/' + location + '/forecast.xml'
    list_of_results = re.findall(regular_expr, html, re.I) # First search after 'stadnamn' (Location name)

    if len(list_of_results) == 0:                    #If no results, search 'kommune'
        print "Trying to search 'kommune'"
        regular_expr = 'http://www\.yr\.no/place/Norway/[^/]*/' + location + '/[^/]*/forecast.xml'
        list_of_results = re.findall(regular_expr, html, re.I)

    if len(list_of_results) == 0:                    # If still no results, search 'fylke'
        print "Trying to search 'fylke'"
        regular_expr = 'http://www\.yr\.no/place/Norway/' + location + '/[^/]*/[^/]*/forecast.xml'
        list_of_results = re.findall(regular_expr, html, re.I)

    # Remove duplicates while keeping the ordering of elements (i.e. urls)
    list_of_results = [i for n, i in enumerate(list_of_results) if i not in list_of_results[:n]]

    t1 = time(); cpu_time = t1-t0
    return list_of_results, cpu_time


#----MAIN----#
if __name__ == '__main__':
    list_of_urls, cpu_time = get_list_of_results()
    print '\n',list_of_urls,'\n', 'Number of found urls: ', len(list_of_urls), '\n', 'Time taken [sec]: %.3f' %cpu_time
