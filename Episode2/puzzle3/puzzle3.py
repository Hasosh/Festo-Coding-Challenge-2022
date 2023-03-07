import numpy as np
import sys
import pickle
import itertools

def main(file1, file3):	
	with open(file1, "r") as filestream:
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
		print(protocol_per_person['Yen Banda'])

	#sorting of the created dictionary (ordering with respect to time; early to late)
	protocol_per_person_sorted = {}
	for person in protocol_per_person:
		sorted_list = protocol_per_person[person]
		sorted_list.sort(key=lambda y: y[1])
		protocol_per_person_sorted[person] = sorted_list
	print(protocol_per_person_sorted['Yen Banda'])

	#list of places per person (AB HIER: COULD BE WRONG)
	list_of_times_per_person = {}
	cur_place = ""
	first_time = 0
	second_time = 0
	for person in protocol_per_person_sorted:
		protocol = protocol_per_person_sorted[person]
		for flag, t in enumerate(protocol):
			if flag % 2 == 1: # only look at "in" tuples
				if t[0] != cur_place or t[2] != 0:
					print("Error 10 happenend. Program stopped")
					sys.exit()
				else:
					second_time = t[1]
					diff = second_time - first_time
					if person in list_of_times_per_person:
						if diff <= 79:
							list_of_times_per_person[person].append(diff) 
					else:
						if diff <= 79:
							list_of_times_per_person[person] = [diff]
			else:
				if t[2] != 1:
					print("Error 20 happenend. Program stopped")
					sys.exit()
				else:
					cur_place = t[0]
					first_time = t[1]

	# check if list of places of a person is same of that from Jelly Jones
	print(list_of_times_per_person)
	possible_persons = []
	for person in list_of_times_per_person:
		times = list_of_times_per_person[person]
		print(times)
		n = len(times)
		for i in range(0, n+1):
			combs = list(itertools.combinations(times, i))
			print(combs)
			for c in combs:
				cur_sum = 0
				for t in c:
					cur_sum += int(t)
				if cur_sum == 79:
					possible_persons.append(person)
					print(person)
					break
		#sys.exit()

	print(list_of_times_per_person['Miriam Nawaz'])
	print(list_of_times_per_person['Krishna Song'])
	print(list_of_times_per_person['Anil Trinh'])

	# sum up all the IDs of all the possible persons
	with open(file3, "r") as filestreamthree:
		with open("solution.txt", "w") as filestreamfour:
			sum_of_outlier_IDs = 0
			lines = filestreamthree.readlines()
			for i in range(int(len(lines) / 14)):
				cur_name = lines[i * 14].split(":")[1].strip()
				cur_ID = lines[i * 14 + 1].split(":")[1].strip()
				print(cur_ID)
				#check if planet is an outlier planet
				if cur_name in possible_persons:
					sum_of_outlier_IDs += int(cur_ID)
			print(sum_of_outlier_IDs)
			filestreamfour.write(str(sum_of_outlier_IDs))
			save_list(possible_persons)

def save_list(mylist):
	with open('possible_users.pkl', 'wb') as f:
		pickle.dump(mylist, f)
			
if __name__ == '__main__':
	security_log_file = "security_log.txt"
	population_file = "population.txt"
	main(security_log_file, population_file)