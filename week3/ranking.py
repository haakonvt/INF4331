
filename 	 = "data.log"
log_file 	 = open(filename, 'r')
list_of_file = log_file.readlines()

for line in list_of_file:
	if "CPU" in line:
		





"""
for filename in sys.argv[1:]:
	word_counter  = 0
	crnt_file     = open(filename,'r')    # Opens file for reading
	list_of_file  = crnt_file.readlines() # List of all lines
	for line in list_of_file:			  # Loop over all lines
		line_list = line.split()		  # Split all words
		word_counter += len(line_list)	  # Count all words
	print "%s: %i" %(filename, word_counter)
"""