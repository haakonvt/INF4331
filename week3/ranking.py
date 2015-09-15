filename 	 = "data.log"
log_file 	 = open(filename, 'r')
list_of_file = log_file.readlines()

cpu_dict = {} # Dictionary to store test name and cpu-times

for line in list_of_file:
	if "CPU" in line:
		word_list = line.split()
		current_test_name  = word_list[1]
		current_time_taken = float(word_list[3])
		if current_test_name not in cpu_dict:
			cpu_dict[current_test_name] = []
		cpu_dict[current_test_name].append(current_time_taken)

for key in cpu_dict:
	cpu_times = map(float, cpu_dict[key])
	avg = sum(cpu_times)/len(cpu_times)
	print "Test name: %s" %key
	print "CPU time: %.1f s (min)"   % min(cpu_times)
	print "          %.1f s (avg)"   % avg
	print "          %.1f s (max)\n" % max(cpu_times)
