import numpy as np
import sys
import pickle

def test(file):	
	with open(file, "r") as filestream:
		lines = filestream.readlines()
		blood_sample_counter = 1
		i = 0
		while i < len(lines):
			line = lines[i]
			stripped_line = line.strip()
			if not stripped_line:
				i += 1
				continue
			elif stripped_line[0] != '+':
				i += 1
				continue
			else:
				# save the index where i should continue after this case 
				continuation_index = i + 8

				# get next line because at next line blood sample begins
				i += 1
				line = lines[i]
				stripped_line = line.strip()

				blood_sample = []
				blood_row = stripped_line[1:-1]
				blood_sample.append(blood_row)
				for j in range(5):
					i += 1
					line = lines[i]
					stripped_line = line.strip()
					blood_row = stripped_line[1:-1]
					blood_sample.append(blood_row)
				pico_contained = scan_for_gen1(blood_sample)
				print("{}. blood sample: {} ".format(blood_sample_counter, pico_contained))
				blood_sample_counter += 1
				i = continuation_index

def main(file):	
	with open(file, "r") as filestream:
		with open("solution.txt", "w") as filestreamtwo:
			lines = filestream.readlines()
			current_name = "unknown"
			current_ID = "9999999"
			possible_users = {}
			i = 0
			while i < len(lines):
				line = lines[i]
				stripped_line = line.strip()
				if not stripped_line:
					i += 1
					continue
				elif stripped_line[:4] == "Name":
					current_name = stripped_line[6:]
					i += 1
					continue
				elif stripped_line[:2] == "ID":
					current_ID = stripped_line[4:]
					i += 1
					continue
				elif stripped_line[0] != '+':
					i += 1
					continue
				else:
					# save the index where i should continue after this case 
					continuation_index = i + 8

					# get next line because at next line blood sample begins
					i += 1
					line = lines[i]
					stripped_line = line.strip()

					blood_sample = []
					blood_row = stripped_line[1:-1]
					blood_sample.append(blood_row)
					for j in range(5):
						i += 1
						line = lines[i]
						stripped_line = line.strip()
						blood_row = stripped_line[1:-1]
						blood_sample.append(blood_row)
					pico_contained = scan_for_gen1(blood_sample)
					#print("{}. blood sample: {} ".format(current_name, pico_contained))
					if pico_contained:
						print(current_name)
						possible_users[current_ID] = current_name
					i = continuation_index
			solution = calculate_solution(possible_users)
			print(solution)
			filestreamtwo.write(str(solution))
			possible_persons = []
			for ID in possible_users:
				possible_persons.append(possible_users[ID])
			save_list(possible_persons)

def save_list(mylist):
	with open('possible_users.pkl', 'wb') as f:
		pickle.dump(mylist, f)

def calculate_solution(possible_users):
	sum_of_ids = 0
	for ID in possible_users:
		sum_of_ids += int(ID)
	return sum_of_ids

def scan_for_gen1(blood_sample):
	vertical_blood_sample = ["","","","","","","",""]
	# first horizontally 
	for blood_row in blood_sample:
		if 'pico' in blood_row:
			return True
		elif 'ocip' in blood_row:
			return True
		else:
			# prepare vertical array
			for i in range(len(blood_row)):
				vertical_blood_sample[i] += blood_row[i]
	# second vertically 
	for blood_row in vertical_blood_sample:
		if 'pico' in blood_row:
			return True
		elif 'ocip' in blood_row:
			return True
	return False

if __name__ == '__main__':
	main_file = "population.txt"
	clean_file = "lab_blood_clean.txt"
	gen1_file = "lab_blood_gen1.txt"

	print("1.	{}".format(main_file))
	print("2.	{}".format(clean_file))
	print("3.	{}".format(gen1_file))

	option = input("What option do you want?")

	if option == '1':
		main(main_file)		
	elif option == '2':
		test(clean_file)	
	else:
		test(gen1_file)	