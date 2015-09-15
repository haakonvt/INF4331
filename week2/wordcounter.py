import sys

# Open any number of files dictated from the command line
# ..and print out number of lines in these files

for filename in sys.argv[1:]:
	word_counter  = 0
	crnt_file     = open(filename,'r')    # Opens file for reading
	list_of_file  = crnt_file.readlines() # List of all lines
	for line in list_of_file:			  # Loop over all lines
		line_list = line.split()		  # Split all words
		word_counter += len(line_list)	  # Count all words
	print "%s: %i" %(filename, word_counter)
