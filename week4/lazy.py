import os
try:
   import cPickle as pickle
except:
   import pickle

class Lazy:
    def __init__(self, func):
        self.func = func # get_html_content(url)
        if os.path.isfile('yr_buffer.dat'): # If buffer exist, load it
            try:
                self.buffer = pickle.load(open('yr_buffer.dat', 'rb'))
            except:
                self.buffer = {} # If something wrong with buffer, get new data
        else:
            self.buffer = {}

    def __call__(self, arg):
        if arg in self.buffer: # If in buffer, return this
            print "found", arg, "in buffer!"
            return self.buffer[arg]
        retval = self.func(arg) #
        self.buffer[arg] = retval
        pickle.dump(self.buffer, open('yr_buffer.dat', 'wb'))
        return retval
