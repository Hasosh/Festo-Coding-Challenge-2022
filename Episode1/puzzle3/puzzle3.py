import numpy as np
import sys
import pickle

def main(file1, file2, file3):	
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

	#sorting of the created dictionary
	protocol_per_person_sorted = {}
	for person in protocol_per_person:
		sorted_list = protocol_per_person[person]
		sorted_list.sort(key=lambda y: y[1])
		protocol_per_person_sorted[person] = sorted_list
	print(protocol_per_person_sorted['Yen Banda'])

	#list of places per person
	list_of_places_per_person = {}
	cur_place = ""
	for person in protocol_per_person_sorted:
		protocol = protocol_per_person_sorted[person]
		for flag, t in enumerate(protocol):
			if flag % 2 == 0: # only look at "in" tuples
				cur_place = t[0]
				if t[2] != 1:
					print("Error happenend. Program stopped")
					sys.exit()
				if person in list_of_places_per_person:
					list_of_places_per_person[person].append(cur_place) 
				else:
					list_of_places_per_person[person] = [cur_place]
			else:
				if t[0] != cur_place or t[2] != 0:
					print("Error happenend. Program stopped")
					sys.exit()
	print(list_of_places_per_person['Yen Banda'])

	# check if list of places of a person is same of that from Jelly Jones
	with open(file2, "r") as filestreamtwo:
		place_sequence = filestreamtwo.readlines()
		possible_persons = []
		for i in range(len(place_sequence)):
			place_sequence[i] = place_sequence[i].strip()
		for person in list_of_places_per_person:
			protocol = list_of_places_per_person[person]
			if protocol[0] == place_sequence[0] and \
			   protocol[1] == place_sequence[1] and \
			   protocol[2] == place_sequence[2] and \
			   protocol[3] == place_sequence[3] and \
			   protocol[4] == place_sequence[4] and \
			   len(protocol) == len(place_sequence):
			   possible_persons.append(person)

	# sum up all the IDs of all the possible persons
	with open(file3, "r") as filestreamthree:
		with open("solution.txt", "w") as filestreamfour:
			sum_of_outlier_IDs = 0
			lines = filestreamthree.readlines()
			for i in range(int(len(lines) / 14)):
				cur_name = lines[i * 14].split(":")[1].strip()
				cur_ID = lines[i * 14 + 1].split(":")[1].strip()
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
	place_sequence_file = "place_sequence.txt"
	population_file = "population.txt"
	main(security_log_file, place_sequence_file, population_file)