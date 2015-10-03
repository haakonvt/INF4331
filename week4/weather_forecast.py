#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, urllib, re, codecs, time

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

    return list_of_results


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
            #print "Currently retrieving weather forecast from url:\n -", index+1,',', current_url,'\n'
            current_html  = get_html_content(current_url)
            regex_place   = '\<location\>.*?\<name\>(.*?)<\/name\>'
            regex_weather = '\<tabular\>(.*?\<time\sfrom.*?\<\/time\>.*?\<\/time\>.*?\<\/time\>.*?\<\/time\>.*?\<\/time\>)'

            p_place   = re.compile(regex_place, re.DOTALL)
            p_weather = re.compile(regex_weather, re.DOTALL)

            html_place.append(re.search(p_place, current_html).group(1))
            html_weather.append(re.search(p_weather, current_html).group(1))

    return html_place, html_weather


def weather_update(place,hour,minute):
    # Step 1) Find the urls with regex matching
    list_of_urls = get_list_of_results(place)
    #print '\nNumber of found urls: ', len(list_of_urls)

    # Step 2) Follow these urls and retrieve weather info for next 24 hrs
    list_place, html_weather = retrieve_weather_forecast(list_of_urls)

    # Step 3) Retrieve the specific weather data and strip everything else
    for i,raw_weather in enumerate(html_weather):
        # Find all the specific weather data and save them as a list of tuples,
        # where each tuple (i.e. list element) correspond to one time intercal
        regular_expr = '<time\sfrom="(\d{4})-(\d{2})-(\d{2})T(\d{2}):00:00"\sto="(\d{4})-(\d{2})-(\d{2})T(\d{2}):00:00.*?\<symbol\snumber=".*?name="(.*?)".*?\<precipitation\svalue="(.*?)".*?\<windSpeed\smps="(.*?)".*?\<temperature\sunit.*?value="(.*?)"'
        key_weather_data = re.findall(regular_expr, raw_weather, re.DOTALL)

        # Find the weather data for the correct time interval specified by the user in [hour:minute]
        for j,kwd in enumerate(key_weather_data):
            start_hour = int(kwd[3])
            end_hour   = int(kwd[7])
            if start_hour <= hour and end_hour > hour:
                k = j
                break

        if i == 0: # Print out the time stamp (with date) just one time
            year  = int(key_weather_data[k][0])
            month = int(key_weather_data[k][1])
            day   = int(key_weather_data[k][2])
            date_stamp = "%i-%.2i-%.2i  %.2i:%.2i" %(year, month, day, hour, minute)
            #print date_stamp

        summary  =   key_weather_data[k][8]
        rain = float(key_weather_data[k][9])
        wind = float(key_weather_data[k][10])
        temp = float(key_weather_data[k][11])

        # Print out nicely formatted weather update
        formatted_weather_data = "%s: %s, rain:%.0f  mm, wind:%.1f mps, temp:%.0f deg C" \
                            %(list_place[i], summary, rain, wind, temp)
        #print formatted_weather_data
        return date_stamp + '\n' + formatted_weather_data


#----MAIN----#
if __name__ == '__main__':

    place  = raw_input('\nPlease input a location to find weather forecast: ')
    print '\nPlease specify what time in the future you want a weather update for:'
    try:
        hour   = int('0' + raw_input('- At what hour [0-23]? ')) # Adding zero infront if user doesn't input anything
    except:
        print "[hour] should be a INTEGER in range between [0-23]. Try again!"; sys.exit(1)
    try:
        minute = int('0' + raw_input('- At what minute [0-59]? '))
    except:
        print "[minute] should be a INTEGER in range between [0-59]. Try again!"; sys.exit(1)

    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        print "Hour or minute not in valid range, [0-23] and [0-59]\nExiting..."
        import sys; sys.exit(1)

    # One call to rule them all i.e. find news about the weather
    print weather_update(place,hour,minute)
