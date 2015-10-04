import os
from time import time
try:
   import cPickle as pickle
except:
   import pickle

class Lazy:
    def __init__(self, func, timestamp_arg=None, func_name='html'):
        self.timestamp_arg = timestamp_arg
        self.func_name     = func_name
        self.func = func # get_html_content(url)
        if os.path.isfile('buffer_%s.dat' %self.func_name): # If buffer exist, load it
            try:
                self.buffer = pickle.load(open('buffer_%s.dat' %self.func_name, 'rb'))
            except:
                self.buffer = {} # If something wrong with buffer, get new data
        else:
            self.buffer = {}

    def __call__(self, arg):
        timestamp_at_call = int(round( time() )) # Seconds since epoch
        if arg in self.buffer: # If in buffer, return this
            timestamp_when_buffered = self.buffer[arg][0]
            seconds = 10
            if timestamp_at_call < timestamp_when_buffered + seconds:
                #print "time at call:", timestamp_at_call, "time when bufferde", timestamp_when_buffered
                #print "found current url in buffer:", arg
                return self.buffer[arg][1]
            else:
                del self.buffer[arg] # Remove old weather data

        # If buffer is out-of-date or non-exsisting, get new data (and save to buffer file)
        retval = self.func(arg) #
        self.buffer[arg] = (timestamp_at_call, retval)
        pickle.dump(self.buffer, open('buffer_%s.dat' %self.func_name, 'wb'))
        return retval
