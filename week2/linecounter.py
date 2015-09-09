import sys

# Open any number of files dictated from the command line
# ..and print out number of lines in these files

for filename in sys.argv[1:]:
	crnt_file     = open(filename,'r')    # Opens file for reading
	list_of_file  = crnt_file.readlines() # List of all lines
	nmbr_of_lines = len(list_of_file) 
	print "%s: %i" %(filename, nmbr_of_lines)
