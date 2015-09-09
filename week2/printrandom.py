from numpy.random import random

x = random()    # Returns rand uniform in [0,1)
x = (x-0.5)*2   # Changed interval to [-1,1]

print "%.4f" %x # Print with 4 decimals
