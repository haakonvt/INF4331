import os
from time import time
try:
   import cPickle as pickle
except:
   import pickle

class Lazy:
    """
    This class takes a function as argument and stores the results of calls
    to a separate buffer file. When a argument is not unique, the buffered
    results will be used.
    """
    def __init__(self, func, buffer_is_valid=3600*6, func_name='html'):
        """
        Initiate and check if buffer exist. If not, create a new empty dict.
        """
        self.buffer_is_valid = buffer_is_valid
        self.func_name       = func_name
        self.func = func # get_html_content(url)
        if os.path.isfile('buffer_%s.dat' %self.func_name): # If buffer exist, load it
            try:
                self.buffer = pickle.load(open('buffer_%s.dat' %self.func_name, 'rb'))
            except:
                self.buffer = {} # If something wrong with buffer, get new data
        else:
            self.buffer = {}

    def __call__(self, arg):
        """
        When called, checks if arg is a key in the buffered dictionary. If true,
        and not outdated, return from buffer. Else, call the original function
        self.func(arg) and save the return to buffer.
        """
        timestamp_at_call = time() # Seconds since epoch

        if arg in self.buffer: # If in buffer, return this
            timestamp_when_buffered = self.buffer[arg][0] # Dict saves a tuple of timestamp and html

            if timestamp_at_call < timestamp_when_buffered + self.buffer_is_valid:
                if self.func_name == 'dummy': # Tell the world that buffer was used (if tested)
                    print "Buffer used!"
                buffered_result = self.buffer[arg][1]
                return buffered_result
            else:
                del self.buffer[arg] # Remove old weather data

        # If buffer is out-of-date or non-exsisting, get new data (and save to buffer file)
        retval = self.func(arg) #
        self.buffer[arg] = (timestamp_at_call, retval)
        pickle.dump(self.buffer, open('buffer_%s.dat' %self.func_name, 'wb'))
        return retval
