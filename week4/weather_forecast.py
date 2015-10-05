#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, urllib, re, codecs, os, glob
from random import sample
from time import *
from lazy import Lazy

def get_html_content(url):
    """
    Function takes exactly one argument: an url (string) and returns the html of that url.
    """
    if not isinstance(url, basestring):
        "The url must be a string! Exiting!"; sys.exit(1)
    try:
        response = urllib.urlopen(url)
    except:
        print "\nError! Make sure you are connected to the internet, and try again!"; sys.exit(1)
    html     = response.read()
    response.close()
    return html


def get_list_of_results(place):
    """
    By using regular expressions, we search through 'http://fil.nrk.no/yr/viktigestader/noreg.txt'
    for urls [english] matching either 'stadnamn', 'kommune' or 'fylke'.
    Function takes exactly one argument: the name of a place to look for [string].
    Argument can contain multiple wildcards i.e. "*kirke*" to return a bunch of urls
    """
    url  = 'http://fil.nrk.no/yr/viktigestader/noreg.txt'
    buffer_is_valid = time() + 86400 # Buffer is valid for 24 hours
    lazyhtml = Lazy(get_html_content,buffer_is_valid,'yrtxt') # Will put yr.no txt-file in buffer
    html     = lazyhtml(url)

    #html_file = open('noreg.txt', 'r')
    #html      = html_file.read(); html_file.close()
    location  = place

    # If empty string is provided, return links for all entries in list
    if location == '':
        location = '.*'
    else:
        # If user input one/more wildcard, add a dot-character right before for regex-support
        location = re.sub('\*', '.*', location)

    # Fix that norwegian special characters dosnt work with regex case insensitivity
    # for the most relevant cases ('place' starts with a capital letter)
    location = re.sub('^æ', 'Æ', location)
    location = re.sub('^ø', 'Ø', location)
    location = re.sub('^å', 'Å', location)

    regular_expr = 'http://www\.yr\.no/place/Norway/[^/]*/[^/]*/' + location + '/forecast.xml'
    list_of_results = re.findall(regular_expr, html, re.I) # First search after 'stadnamn' (Location name)

    if len(list_of_results) == 0:                    #If no results, search 'kommune'
        print "No 'stadnamn' found. Trying to search 'kommune'"
        regular_expr = 'http://www\.yr\.no/place/Norway/[^/]*/' + location + '/[^/]*/forecast.xml'
        list_of_results = re.findall(regular_expr, html, re.I)

    if len(list_of_results) == 0:                    # If still no results, search 'fylke'
        print "No 'kommune ' found. Trying to search 'fylke'"
        regular_expr = 'http://www\.yr\.no/place/Norway/' + location + '/[^/]*/[^/]*/forecast.xml'
        list_of_results = re.findall(regular_expr, html, re.I)

    if len(list_of_results) == 0:
        print "No 'fylke   ' found. Returning empty list"

    # Remove duplicates while keeping the ordering of elements (i.e. urls)
    list_of_results = [i for n, i in enumerate(list_of_results) if i not in list_of_results[:n]]

    return list_of_results


def retrieve_weather_raw_data(list_of_urls,shuffle_urls=False,limit=100):
    """
    Returns two list of maximum 100 entries with places and raw weather data.
    The selection is by default ordered and limited.
    """
    warning = False; skip_html_weather_append = False
    actual_number_of_urls = len(list_of_urls)
    number_of_urls        = len(list_of_urls) # Will be set to 100 (if more than 100)

    if number_of_urls > 10: # Print out a progress bar if we got more than just a few urls to fetch..
        print_progress_bar = True
    else:
        print_progress_bar = False
    if number_of_urls > 100:
        print "\nWarning: Too many urls given. \nWill show weather forecast for the first 100 locations. May take some time"
        warning = True; number_of_urls = 100

    html_place = []; html_weather = [] # Will contain location and raw weather data
    buffer_is_valid = time() + 3600*6  # Buffer is valid for 6 hours
    lazy_get_html = Lazy(get_html_content,buffer_is_valid) # Improve speed with buffering. Valid for 6 hours

    if shuffle_urls:
        if actual_number_of_urls >= 110:
            list_of_urls = sample(list_of_urls, 110) # Assuming some very few urls are bad, we might need more than 100 to search from
        else:
            list_of_urls = sample(list_of_urls, number_of_urls)

    for index, current_url in enumerate(list_of_urls):
        if print_progress_bar:
            percent_fix_for_bad_urls = limit - 100 # If we need to skip some urls, make sure we still end at 100 % [if you think, really?!?, I strongly agree]
            percent = int(round(float(index)/(number_of_urls+percent_fix_for_bad_urls)*100))
            sys.stdout.write("\rFetching data... %d%% " % percent) # Print out a simple "progress bar" showing percent
            sys.stdout.flush()

        if index+1 > limit: # Breaks loop after limit is reached
            break
        else:
            #current_html  = get_html_content(current_url) # NO BUFFERING
            current_html  = lazy_get_html(current_url) # WITH BUFFERING
            regex_place   = '\<location\>.*?\<name\>(.*?)<\/name\>'
            regex_weather = '\<tabular\>(.*?\<time\sfrom.*?\<\/time\>.*?\<\/time\>.*?\<\/time\>.*?\<\/time\>.*?\<\/time\>)'

            p_place   = re.compile(regex_place, re.DOTALL)
            p_weather = re.compile(regex_weather, re.DOTALL)

            try:
                html_place.append(re.search(p_place, current_html).group(1))
            except AttributeError:
                print "The current url is broken. Will skip and continue..."
                skip_html_weather_append = True

                # If urls>100 and some urls are bad, we still want 100 results, not 99 nor 98 so we add 1 new for each bad url
                # HOWEVER: If we dont have any more links, we must return just (i.e.) 99 or 98
                if number_of_urls == 100 and actual_number_of_urls > limit:
                        limit += 1
            if skip_html_weather_append == False: # Do this only if previous test "try/except" worked
                html_weather.append(re.search(p_weather, current_html).group(1))
                skip_html_weather_append = False  # Update for next iteration
    # Make sure output looks nice:
    print ' ';
    if print_progress_bar:
        print ' ' # Purely estetical reasons ;)
    return html_place, html_weather


def weather_update(place,hour=0,minute=0,shuffle_urls=False,return_extreme=False,ignore_print=False):
    """
    This function takes at least three arguments 'place', 'hour' and 'minute' and returns the weather
    forecast at the first incident that hour:minute occurs (i.e. max 24 hours) for a multiple of
    locations matching the argument 'place'.
    Optional arguemnts include 'shuffe urls', return the max/min temp (will override ordinary output)
    and the ability to ignore print (for teseting purposes)
    """
    # Step 0) If main isnt run, must check that [hour] and [minute] are acceptable
    if not isinstance(hour, (int, long)) or not isinstance(minute, (int, long)):
        print "[Hour] and/or [minute] not INTEGER(S). Please specify hour [0-23] and minute [0-59]\nExiting..."; sys.exit(1)
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        print "Hour or minute not in valid range, [0-23] and [0-59]\nExiting..."; sys.exit(1)

    # Step 1) Find the urls with regex matching
    list_of_urls = get_list_of_results(place)
    #print '\nNumber of found urls: ', len(list_of_urls)

    # Step 2) Follow these urls and retrieve weather info for next 24 hrs
    list_place, html_weather = retrieve_weather_raw_data(list_of_urls,shuffle_urls)

    # Step 3) Retrieve the specific weather data and strip everything else
    date_stamp = ''                       # This string might be returned from this function
    formatted_weather_data_to_return = '' # This string might be returned from this function
    max_T_string, min_T_string = '', ''   # These strings might be returned from this function

    for i,raw_weather in enumerate(html_weather):
        # Find all the specific weather data and save them as a list of tuples,
        # where each tuple (i.e. list element) correspond to one time interval at yr.no/../../..
        regular_expr = '<time\sfrom="(\d{4})-(\d{2})-(\d{2})T(\d{2}):00:00"\sto="(\d{4})-(\d{2})-(\d{2})T(\d{2}):00:00.*?\<symbol\snumber=".*?name="(.*?)".*?\<precipitation\svalue="(.*?)".*?\<windSpeed\smps="(.*?)".*?\<temperature\sunit.*?value="(.*?)"'
        key_weather_data = re.findall(regular_expr, raw_weather, re.DOTALL)

        # Find the weather data for the correct time interval specified by the user in [hour:minute]
        for j,kwd in enumerate(key_weather_data):
            start_hour = int(kwd[3])
            end_hour   = int(kwd[7])
            if start_hour > end_hour:
                end_hour = 24 # Fix interval [18:00 -> 00:00] so that: end_hour > start_hour is always true
            if start_hour <= hour and end_hour > hour:
                k = j
                break

        if i == 0: # Print out the time stamp (with date) just one time
            year  = int(key_weather_data[k][0])
            month = int(key_weather_data[k][1])
            day   = int(key_weather_data[k][2])
            date_stamp = "%i-%.2i-%.2i  %.2i:%.2i" %(year, month, day, hour, minute)
            if return_extreme and not ignore_print:
                print date_stamp

        summary  =   key_weather_data[k][8]
        rain = float(key_weather_data[k][9])
        wind = float(key_weather_data[k][10])
        temp = float(key_weather_data[k][11])

        # Print out nicely formatted weather update
        formatted_weather_data = "%s: %s, rain:%.0f  mm, wind:%.1f mps, temp:%.0f deg C" \
                            %(list_place[i], summary, rain, wind, temp)
        formatted_weather_data_to_return += formatted_weather_data + '\n'

        # Find extreme temperatures
        if return_extreme:
            if i == 0:
                max_T_value = temp; min_T_value = temp
                max_T_string = formatted_weather_data
                min_T_string = formatted_weather_data
            else:
                if max_T_value < temp:
                    max_T_value  = temp
                    max_T_string = formatted_weather_data
                if min_T_value > temp:
                    min_T_value  = temp
                    min_T_string = formatted_weather_data

    final_weather_update = date_stamp + '\n' + formatted_weather_data_to_return[:-2] # [:-2] --> Remove that last newline i.e. '\n'
    if return_extreme:
        return max_T_value, max_T_string, min_T_value, min_T_string
    else:
        return final_weather_update


def find_extreme_temps():
    """
    Get highest and lowest temp at upcoming time 13:00 in a set of 100 (default=random) locations in Norway
    """
    max_T, max_T_str, min_T, min_T_str = weather_update('',13,0,shuffle_urls=True,return_extreme=True)
    print "Maximum temperature of %.0f deg C, found here:\n" %max_T, max_T_str
    print "Minimum temperature of %.0f deg C, found here:\n" %min_T, min_T_str


def test_4_1():
    """
    Test that urllib correctly copies html from websites
    """
    url      = 'http://www.islostarepeat.com/'
    html     = get_html_content(url)

    ref_page = open('IsLostaRepeat.html','r') # Downloaded from web
    ref_read = ref_page.read(); ref_page.close()

    html     = re.sub('\s+', '', html)      # Strip all whitespaces
    ref_read = re.sub('\s+', '', ref_read)

    assert html == ref_read


def test_4_2():
    """
    Test that regex correctly matches 'Hannestad' to the right url
    """
    exact_url = 'http://www.yr.no/place/Norway/Østfold/Sarpsborg/Hannestad/forecast.xml'
    place     = 'Hannestad'
    url_list  = get_list_of_results(place)
    assert len(url_list) == 1
    assert url_list[0] == exact_url


def test_4_3():
    """
    Test that temperature at 'Hannestad' is in an acceptable range [-50, 50] deg C
    """
    time_now = localtime()
    place    = 'Hannestad'
    hour     = time_now[3] + 1 # Get the tm_hour and add '1' to get the earliest time interval at yr
    if hour == 24:
        hour = 0
    temp, a, b, c = weather_update(place, hour, 0, return_extreme=True,ignore_print=True)
    assert temp < 50 and temp > -50


def test_4_4():
    """
    Test that Lazy class correctly buffers a dummy function.
    Easiest verified by call in program (prints out 'buffer used / not used')

    >>> test_4_4()
    Buffer NOT used!
    Buffer used!
    """
    # Need to remove buffer-file if it exist!
    buffer_file = glob.glob("buffer_dummy.dat")[0]
    os.remove(buffer_file)

    def dummy(x):
        print 'Buffer NOT used!'
        return x+1
    lazytest = Lazy(dummy,func_name='dummy')

    t1 = lazytest(3)
    t2 = lazytest(3)
    assert t2 == 4


def test_4_4_2():
    """
    1) Creates a dummy file with expired time stamp and ensures that it is replaced.
    2) Creates a dummy file with unexpired time stamp and ensures that it isn't replaced.

    >>> test_4_4_2()
    Buffer NOT used!
    Buffer NOT used!
    ----------------
    Buffer NOT used!
    Buffer used!
    """
    for buffer_is_valid in [-10,10]:
        # Need to remove buffer-files if they already exist!
        buffer_file = glob.glob("buffer_dummy.dat")[0]
        os.remove(buffer_file)

        def dummy(x):
            print 'Buffer NOT used!'
            return x+1

        lazytest = Lazy(dummy,buffer_is_valid,func_name='dummy')
        t1 = lazytest(3) # Creates the dummy file
        t2 = lazytest(3) # Replaces only if expired
        assert t1 == t2
        if buffer_is_valid < 0:
            print '----------------'


#----MAIN----#
if __name__ == '__main__':
    """---------------
    Run all tests:
    - Can be run directly or via i.e.:
    >> nosetests weather_forecast.py
    (or some with doctest or/and py.test)
    ---------------"""
    #test_4_1(); test_4_2(); test_4_3(); test_4_4()

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

    ### One call to rule them all i.e. find news about the weather ###
    print weather_update(place,hour,minute)

    ### Find max/min temperatures ###
    #print "When searcing 100 random places in Norway:"
    #find_extreme_temps()
