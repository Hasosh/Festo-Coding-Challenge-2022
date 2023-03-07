import numpy as np
import sys
import pickle

def main(path1, path2, path3):	
	possible_users1 = load_list(path1)
	possible_users2 = load_list(path2)
	possible_users3 = load_list(path3)
	final_solution = calculate_final_solution(possible_users1, possible_users2, possible_users3)
	print(final_solution)
	with open('final_solution.txt', 'w') as filestream:
		filestream.write(final_solution[0])

def load_list(path):
	with open(path, 'rb') as f:
		mylist = pickle.load(f)
		return mylist

def calculate_final_solution(p1, p2, p3):
	return list(set(p1) & set(p2) & set(p3))

if __name__ == '__main__':
	path1 = "puzzle1\\possible_users.pkl"
	path2 = "puzzle2\\possible_users.pkl"
	path3 = "puzzle3\\possible_users.pkl"
	main(path1, path2, path3)