import numpy as np
import sys
import pickle
import copy

def test():	
	t = []
	print(len(t))
	sys.exit()

def main(file):
	all_passages = process_passages(file)
	cleared_passages = ""
	for number, passage in enumerate(all_passages):
		if number == 0: # for debug purposes
			continue
		if clear(passage):
			cleared_passages += str(number) + "-"
	cleared_passages = cleared_passages[:-1] #omit - at the last spot
	print(cleared_passages)
	save_list(cleared_passages)

def clear(passage):
	cleared_objects = []
	first_iteration(passage, cleared_objects)
	return check_if_clearable(passage, cleared_objects)

def first_iteration(passage, cleared_objects):
	delete_obj = []
	for obj in passage:
		blocked_by = passage[obj]
		if len(blocked_by) == 1:
			if blocked_by[0] == "-":
				cleared_objects.append(obj)
				delete_obj.append(obj)
	delete_procedure(passage, delete_obj)

def delete_procedure(passage, delete_obj):
	for obj in delete_obj:
		del passage[obj]

def check_if_clearable(passage, cleared_objects):
	removed_something = True
	while removed_something:
		removed_something = False
		delete_obj_for_passages = []
		#print("Passage is: ", passage)
		for obj in passage:
			delete_obj_for_blocked_by = []
			blocked_by = passage[obj]
			#print("Blocked by is: ", blocked_by)
			for o in blocked_by:
				if o in cleared_objects:
					delete_obj_for_blocked_by.append(o)
					removed_something = True
			if removed_something:
				delete_procedure_list(blocked_by, delete_obj_for_blocked_by)
			if len(blocked_by) == 0:
				cleared_objects.append(obj)
				delete_obj_for_passages.append(obj)
		delete_procedure(passage, delete_obj_for_passages)
	print(passage)
	if passage:
		print(False)
		return False
	else:
		print(True)
		return True

def delete_procedure_list(blocked_by, delete_obj):
	for obj in delete_obj:
		blocked_by.remove(obj)

def process_passages(file):
	with open(file, "r") as filestream:
		lines = filestream.readlines()
		all_passages = []
		for i in range(len(lines)):
			l = lines[i]
			if l[:7] == "Passage":
				passage = {}
				while True:
					i += 1
					l = lines[i]
					if l.isspace():
						break
					splitted_line = l.split(":")
					obj = splitted_line[0].strip()
					blocked_by_str = splitted_line[1].strip().split(",")
					blocked_by = [a.strip() for a in blocked_by_str]
					passage[obj] = blocked_by
				all_passages.append(passage)
				#print(passage)
			i += 1
		#print(all_passages)
		print("Processing passages DONE")
		return all_passages

def save_list(mylist):
	with open('solution_sequence.pkl', 'wb') as f:
		pickle.dump(mylist, f)

if __name__ == '__main__':
	scrap_scan_file = "scrap_scan.txt"
	#test()
	main(scrap_scan_file)