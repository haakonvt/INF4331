import sys

fah = float(sys.argv[1])    # Given on commando line
cel = (fah-32)*(5.0/9)

print "%.1f Fahrenheit is equal to %.1f Celsius" %(fah,cel)
