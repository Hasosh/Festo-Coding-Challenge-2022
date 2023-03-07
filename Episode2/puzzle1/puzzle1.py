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
				cell_list = create_cell_structure(blood_sample)
				pico_contained = scan_for_gen2(cell_list)
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
					cell_list = create_cell_structure(blood_sample)
					pico_contained = scan_for_gen2(cell_list)
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

# probably save for every cell the neighbour cells and then solve recursively
def create_cell_structure(blood_sample):
	# save for every cell the neighbours
	cell_list = []
	length_blood_sample = len(blood_sample)
	for i in range(length_blood_sample):
		length_blood_row = len(blood_sample[i])
		cell_row = []
		for j in range(length_blood_row):
			val, up, down, left, right = (None, None, None, None, None)
			val = blood_sample[i][j]
			tup = (val, up, down, left, right)
			cell_row.append(Cell(tup))
		cell_list.append(cell_row)
	print("Initialized Cells")
	# up, down, right, left should point to Cell classes
	length_cell_list = len(cell_list)
	for i in range(length_cell_list):
		length_cell_row = len(cell_list[i])
		for j in range(length_cell_row):
			cur_cell = cell_list[i][j]
			if i != 0:
				cur_cell.set_up(cell_list[i-1][j])
			# down case
			if i != length_blood_sample - 1:
				cur_cell.set_down(cell_list[i+1][j])
			# left case
			if j != 0:
				cur_cell.set_left(cell_list[i][j-1])
			# right case
			if j != length_blood_row - 1:
				cur_cell.set_right(cell_list[i][j+1])
	print("Finished tree structure!") # tree structure works
	# TODO make it more efficient by not saving the space cells
	# TODO ich sollte auf Zellobjekte verweisen, nicht nur auf Werte

	#test_cell = cell_list[4][5]
	#test_cell.print_value()
	#test_cell.print_neighbours()
	return cell_list

def scan_for_gen2(cell_list):
	length_cell_list = len(cell_list)
	for i in range(length_cell_list):
		length_cell_row = len(cell_list[i])
		for j in range(length_cell_row):
			cur_cell = cell_list[i][j]
			if cur_cell.val == "p":
				#print("P-Cell at: ", i + 1, " ", j + 1)
				if check_gen2_recursively(cur_cell, cell_list, "p"):
					return True
	return False

def check_gen2_recursively(cur_cell, cell_list, cur_substr):
	relevant_neighbours = cur_cell.get_relevant_neighbours(cur_substr)
	#print("Current Substring: " + cur_substr + ", Relevant Neighbours: ", cur_cell.cells_obj_to_values(relevant_neighbours))
	if len(relevant_neighbours) == 0:
		return False
	for n in relevant_neighbours:
		if cur_substr == "p" and n.val == "i":
			if check_gen2_recursively(n, cell_list, "pi"):
				return True
		elif cur_substr == "pi" and n.val == "c":
			if check_gen2_recursively(n, cell_list, "pic"):
				return True
		elif cur_substr == "pic" and n.val == "o":
			if check_gen2_recursively(n, cell_list, "pico"):
				return True
		elif cur_substr == "pico" and n.val == "i":
			if check_gen2_recursively(n, cell_list, "picoi"):
				return True
		elif cur_substr == "picoi" and n.val == "c":
			if check_gen2_recursively(n, cell_list, "picoic"):
				return True
		elif cur_substr == "picoic" and n.val == "o":
			return True
	return False


"""
each Cell can have 2 - 4 neighbours:
1.
X - o  
|
o

2.
o - X - o  
    |
    o

3.
    o
    |
o - X - o  
    |
    o

"""
class Cell:
	def __init__(self, tup=None):
		val, up, down, left, right = tup
		self.val = val
		self.up = up
		self.down = down
		self.left = left
		self.right = right

	def set_up(self, new_up):
		self.up = new_up

	def set_down(self, new_down):
		self.down = new_down

	def set_left(self, new_left):
		self.left = new_left

	def set_right(self, new_right):
		self.right = new_right

	def print_value(self):
		print("value: " + self.val)

	def get_neighbours(self):
		neighbours = []
		obj = self.up
		if obj:
			if obj.val != " ":
				neighbours.append(obj)
		obj = self.down
		if obj:
			if obj.val != " ":
				neighbours.append(obj)
		obj = self.right
		if obj:
			if obj.val != " ":
				neighbours.append(obj)
		obj = self.left
		if obj:
			if obj.val != " ":
				neighbours.append(obj)
		return neighbours

	def get_relevant_neighbours(self, cur_substr):
		neighbours = self.get_neighbours()
		relevant_neighbours = []
		for n in neighbours:
			if cur_substr == "p" and n.val == "i":
				relevant_neighbours.append(n)
			elif cur_substr == "pi" and n.val == "c":
				relevant_neighbours.append(n)
			elif cur_substr == "pic" and n.val == "o":
				relevant_neighbours.append(n)
			elif cur_substr == "pico" and n.val == "i":
				relevant_neighbours.append(n)
			elif cur_substr == "picoi" and n.val == "c":
				relevant_neighbours.append(n)
			elif cur_substr == "picoic" and n.val == "o":
				relevant_neighbours.append(n)
		return relevant_neighbours

	def print_neighbours(self):
		print("up: ", self.up.val, "\n" +
				"down: ", self.down.val, "\n" +
				"left: ", self.left.val, "\n" +
				"right: ", self.right.val)

	def cells_obj_to_values(self, cells):
		values = []
		for c in cells:
			values.append(c.val)
		return values

	def scan_gen2(cells):
		pass

if __name__ == '__main__':
	main_file = "population.txt"
	clean_file = "lab_blood_clean.txt"
	gen1_file = "lab_blood_gen2.txt"

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