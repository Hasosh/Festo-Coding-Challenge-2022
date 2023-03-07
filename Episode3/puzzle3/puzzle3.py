import numpy as np
import sys
import pickle
import itertools

def main(file1, file2, file3):	
	protocol_per_person = process_security_log(file1)
	protocol_per_person_sorted = sort_protocol_per_person(protocol_per_person)
	travel_times = process_travel_times(file2)
	possible_persons = no_alibi_persons(protocol_per_person_sorted, travel_times)
	# sum up all the IDs of all the possible persons
	with open(file3, "r") as filestreamthree:
		with open("solution.txt", "w") as filestreamfour:
			sum_of_outlier_IDs = 0
			lines = filestreamthree.readlines()
			for i in range(int(len(lines) / 14)):
				cur_name = lines[i * 14].split(":")[1].strip()
				cur_ID = lines[i * 14 + 1].split(":")[1].strip()
				#print(cur_ID)
				#check if planet is an outlier planet
				if cur_name in possible_persons:
					sum_of_outlier_IDs += int(cur_ID)
			print(sum_of_outlier_IDs)
			filestreamfour.write(str(sum_of_outlier_IDs))
			save_list(possible_persons)

def process_security_log(file):
	with open(file, "r") as filestream:
		protocol_per_person = {} # NOT SORTED YET !
		time_in_minutes = -1
		cur_place = "ERROR"
		for c, line in enumerate(filestream):
			print("Current Line: ", c)
			if not line.isspace(): #check if line is empty
				splitted_line = line.split(":")
				part1 = splitted_line[0].strip()
				part2 = splitted_line[1].strip()
				if part1.isnumeric(): # if its a time
					time_in_minutes = int(part1) * 60 + int(part2)
				else:
					if part1 == "in" or part1 == "out":
						names = part2.split(",")
						for name in names:
							n = name.strip()
							if part1 == "in": # in 
								if n in protocol_per_person:	
									protocol_per_person[n].append((cur_place, time_in_minutes, 1)) # (place, time translated into minutes, 1 for in and 0 for out)
								else:
									protocol_per_person[n] = [(cur_place, time_in_minutes, 1)]
							else: # out
								if n in protocol_per_person:	
									protocol_per_person[n].append((cur_place, time_in_minutes, 0))
								else:
									protocol_per_person[n] = [(cur_place, time_in_minutes, 0)]
					else: # must be place in this case
						cur_place = part2
		return protocol_per_person

def sort_protocol_per_person(protocol_per_person):
	#sorting of the created dictionary (ordering with respect to time; early to late)
	protocol_per_person_sorted = {}
	for person in protocol_per_person:
		sorted_list = protocol_per_person[person]
		sorted_list.sort(key=lambda y: y[1])
		protocol_per_person_sorted[person] = sorted_list
	return protocol_per_person_sorted

def process_travel_times(file):
	with open(file, "r") as f:
		travel_times = {}
		for l in f:
			splitted_line = l.split(":")
			site = splitted_line[0].strip()
			time = int(splitted_line[1].strip())
			travel_times[site] = time
		#print(travel_times)
		#sys.exit()
		return travel_times

def no_alibi_persons(protocol_per_person_sorted, travel_times):
	possible_persons = []
	for person in protocol_per_person_sorted:
		logs = protocol_per_person_sorted[person]
		print(logs)
		for i in range(int(len(logs) / 2)):
			print(logs[2*i + 1])
			cur_site = logs[2*i + 1][0]
			cur_end_time = logs[2*i + 1][1]
			window = cur_end_time + travel_times[cur_site]
			if window <= 760:
				if i == int(len(logs) / 2) - 1:
					print("THIS PERSON" + person)
					possible_persons.append(person)
					sys.exit()
					break
				next_site = logs[2*i + 2][0]
				next_start_time = logs[2*i + 2][1]	
				if next_start_time - travel_times[next_site] >= 680:	
					if next_start_time - travel_times[next_site] >= 780:
						possible_persons.append(person)
						break
					else: 
						if (next_start_time - travel_times[next_site]) - window >= 20:
							#print(person)
							#print(nicely(logs))
							#sys.exit()
							possible_persons.append(person)
							break
		#sys.exit()
	print("Length of possible persons: ", len(possible_persons))
	return possible_persons

def nicely(logs):
	nice_logs = []
	for l in logs:
		a = l[0]
		b = l[1]
		c = l[2]
		nice_logs.append((a, str(int(b / 60)) + ":" + str(b % 60), c))
	return nice_logs

def save_list(mylist):
	with open('possible_users.pkl', 'wb') as f:
		pickle.dump(mylist, f)
	
def test():
	t = "11:07"
	print(int("07"))
	sys.exit()
	splitted_line = line.split(":")
	part1 = splitted_line[0].strip()
	part2 = splitted_line[1].strip()
	if part1.isnumeric(): # if its a time
		time_in_minutes = int(part1) * 60 + int(part2)

if __name__ == '__main__':
	#test()
	security_log_file = "security_log.txt"
	travel_times_file = "travel_times.txt"
	population_file = "population.txt"
	main(security_log_file, travel_times_file, population_file)