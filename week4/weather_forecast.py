#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
import urllib, re, codecs

def get_html_content(url):
    response = urllib.urlopen(url)
    html     = response.read()
    response.close()
    return html


def get_list_of_results(place):
    url  = 'http://fil.nrk.no/yr/viktigestader/noreg.txt'
    #html = get_html_content(url)

    #html = open('small_noreg.txt', 'r').read()
    html_file = open('noreg.txt', 'r')
    html      = html_file.read(); html_file.close()
    location  = place

    t0 = time() # Time the computations

    # If user input one/more wildcard, add a dot-character right before for regex-support
    location = re.sub('\*', '.*', location)

    regular_expr = 'http://www\.yr\.no/place/Norway/[^/]*/[^/]*/' + location + '/forecast.xml'
    list_of_results = re.findall(regular_expr, html, re.I) # First search after 'stadnamn' (Location name)

    if len(list_of_results) == 0:                    #If no results, search 'kommune'
        print "No 'stadnamn' found. Trying to search 'kommune'"
        regular_expr = 'http://www\.yr\.no/place/Norway/[^/]*/' + location + '/[^/]*/forecast.xml'
        list_of_results = re.findall(regular_expr, html, re.I)

    if len(list_of_results) == 0:                    # If still no results, search 'fylke'
        print "No 'kommune' found. Trying to search 'fylke'"
        regular_expr = 'http://www\.yr\.no/place/Norway/' + location + '/[^/]*/[^/]*/forecast.xml'
        list_of_results = re.findall(regular_expr, html, re.I)

    # Remove duplicates while keeping the ordering of elements (i.e. urls)
    list_of_results = [i for n, i in enumerate(list_of_results) if i not in list_of_results[:n]]

    t1 = time(); cpu_time = t1-t0
    return list_of_results, cpu_time


def retrieve_weather_forecast(list_of_urls,limit=100):
    """Returns two list of maximum 100 entries with places and raw weather data"""

    if len(list_of_urls) > 100:
        print "\nWarning: Too many urls given. \nProceeding to show weather forecast for the first 100 locations. This may take some time."
        raw_input('Press Enter to continue..')

    html_place   = []; html_weather = [] # Will contain location and raw weather data

    for index, current_url in enumerate(list_of_urls):
        if index+1 > 100:
            break
        else:
            print "Currently retrieving weather forecast from url:\n -", index+1,',', current_url,'\n'
            current_html  = get_html_content(current_url)
            regex_place   = '\<location\>.*?\<name\>(.*?)<\/name\>'
            regex_weather = '\<tabular\>(.*?\<time\sfrom.*?\<\/time\>.*?\<\/time\>.*?\<\/time\>.*?\<\/time\>.*?\<\/time\>)'

            p_place   = re.compile(regex_place, re.DOTALL)
            p_weather = re.compile(regex_weather, re.DOTALL)

            html_place.append(re.search(p_place, current_html).group(1))
            html_weather.append(re.search(p_weather, current_html).group(1))

    return html_place, html_weather


def weather_update(place,hour,minute):
    list_of_urls, cpu_time = get_list_of_results(place)
    print 'Number of found urls: ', len(list_of_urls), '\n', 'Time taken [sec]: %.3f' %cpu_time

    list_place, html_weather = retrieve_weather_forecast(list_of_urls)



#----MAIN----#
if __name__ == '__main__':

    place  = raw_input('Please input a location to find weather forecast: ')
    print '\nPlease specify what time in the future you want a weather update for:'
    hour   = int(raw_input('At what hour [0-23]? '))
    minute = int(raw_input('At what minute [0-59]? '))
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        print "Hour or minute not in valid range, [0-23] and [0-59]\nExiting..."
        import sys; sys.exit(1)

    # One call to rule them all i.e. find news about the weather
    weather_update(place,hour,minute)

    for i in range(len(list_place)):
        print html_weather[i]
        print i+1, list_place[i]

"""
The data contains a tag group <forecast>
and sub-group <tabular>.  The tabular data are 6 hour weather
summary going back in time.
Create a function that retrieve weather information using regular expression.

- name of place
- weather summary (symbol name)
- amount of rain (precipitation value)
- wind speed (winSpeed mps)
- temperature (temperature value)
- time stamp (time from)
- time stamp (time to)

\<location\>\<name>(.*?)\</name\>.*?\<forecast\>.*\<tabular\>.*?<time\sfrom="(.*?T.*?)"\sto="(.*?)".*?\<symbol\snumber=".*?name="(.*?)".*?\<precipitation\svalue="(.*?)".*?\<windSpeed\smps="(.*?)".*?\<temperature\sunit.*?value="(.*?)"
"""
