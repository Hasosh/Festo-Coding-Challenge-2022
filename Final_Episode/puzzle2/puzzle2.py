import sys
import copy
from itertools import combinations
import time
import pickle

def test():	
	a = [i+1 for i in range(5)]
	print(a)
	for l in combinations(a[1:-1], 2):
		print(l)
	sys.exit()

def main(file):
	with open(file, "r") as filestream:
		lines = filestream.readlines()
		planet_booty_mapping = {}
		counter = 0
		for i in range(len(lines)):
			counter += 1
			print("Current Counter: ", counter)
			if 4*i+3 < len(lines):
				chunk = lines[4*i:4*i+3]
				planet, bunker = process_chunk(chunk)
				if planet != "Scorvus":
					continue
				#bunker, gold_bunker_tuples = process_bunker(bunker_raw)
				#print(bunker)
				booty = get_maximum_booty(bunker)
				print("Booty: ", booty)
				sys.exit()
				planet_booty_mapping[planet] = booty
			else: break
		maximum_planet, maximum_booty = identify_planet_with_maximum_booty(planet_booty_mapping)
		print(maximum_planet, maximum_booty)
		save_list([maximum_planet])

def identify_planet_with_maximum_booty(planet_booty_mapping):
	maximum_planet = ""
	maximum_booty = 0
	for planet in planet_booty_mapping:
		booty = planet_booty_mapping[planet]
		if booty > maximum_booty:
			maximum_planet = planet
			maximum_booty = booty
	return maximum_planet, maximum_booty

def process_chunk(chunk):
	planet = chunk.pop(0).strip()
	bunker_line1 = [int(l.strip()) for l in chunk[0].split(",")]
	bunker_line2 = [int(l.strip()) for l in chunk[1].split(",")]
	return planet, [bunker_line1, bunker_line2]

def get_maximum_booty(bunker):
	upper_limit = len(bunker[0])
	lower_limit = int(((upper_limit + 1) / 2) + 0.5)
	#print("LIMITS: ", upper_limit, lower_limit)
	maximum_booty = 0
	for i in range(upper_limit, lower_limit-1, -1):
		print("Current Permutation index: ", i)
		#combs = combinations(gold_bunker_tuples, i)
		booty = max_booty(bunker, i, upper_limit)
		#print(combs)
		if booty > maximum_booty: #TODO CHECK IF EQUAL
			maximum_booty = booty
		#reset_alerts(gold_bunker_tuples)
	return maximum_booty

def max_booty(bunker, combinations_size, upper_limit):
	bootys = []
	helper_list = [i for i in range(1, upper_limit-1)]
	rel_combs = relevant_combinations(helper_list, combinations_size-2, upper_limit)
	print("Number of combinations: ", len(rel_combs))
	for c in rel_combs:
		comb1 = 0
		comb1_mirrored = 0
		for num, pl in enumerate(list(c)):
			if num % 2 == 0:
				comb1 += bunker[0][pl]
				comb1_mirrored += bunker[1][pl]
			else:
				comb1 += bunker[1][pl]
				comb1_mirrored += bunker[0][pl]
		bootys.append(comb1)
		bootys.append(comb1_mirrored)
	return max(bootys)

def relevant_combinations(helper_list, size, upper_limit):
	valid_combinations = []
	for comb_raw in combinations(helper_list, size):
		take_it = True
		comb = (0,) + comb_raw + (upper_limit-1,)
		for i in range(len(comb)-1):
			if comb[i+1] - comb[i] > 2:
				take_it = False
				break
		if take_it:
			valid_combinations.append(comb)
	return valid_combinations

def save_list(mylist):
	with open('solution_planet.pkl', 'wb') as f:
		pickle.dump(mylist, f)

# def process_bunker(bunker_raw):
# 	bunker = []
# 	gold_bunker_tuples = []
# 	for i in range(len(bunker_raw)):
# 		buffer = []
# 		for j in range(len(bunker_raw[i])):
# 			gold_val = bunker_raw[i][j]
# 			bunker_obj = Bunker(gold=gold_val)
# 			buffer.append(bunker_obj)
# 			gold_bunker_tuples.append((bunker_obj, gold_val))			
# 		bunker.append(buffer)
# 	for i in range(len(bunker)):
# 		for j in range(len(bunker[i])):
# 			if i == 0: #upper bunker
# 				if j == 0: # left corner
# 					bunker[i][j].set_neighbours([bunker[i][j+1], bunker[i+1][j]])
# 				elif j == len(bunker[i]) - 1: # right corner
# 					bunker[i][j].set_neighbours([bunker[i][j-1], bunker[i+1][j]])
# 				else:
# 					bunker[i][j].set_neighbours([bunker[i][j-1], bunker[i][j+1], bunker[i+1][j]])
# 			else: #lower bunker
# 				if j == 0: # left corner
# 					bunker[i][j].set_neighbours([bunker[i][j+1], bunker[i-1][j]])
# 				elif j == len(bunker[i]) - 1: # right corner
# 					bunker[i][j].set_neighbours([bunker[i][j-1], bunker[i-1][j]])
# 				else:
# 					bunker[i][j].set_neighbours([bunker[i][j-1], bunker[i][j+1], bunker[i-1][j]])
# 	gold_bunker_tuples.sort(key=lambda tup: tup[1], reverse=True)
# 	return bunker, gold_bunker_tuples

# def collision(bunkers):
# 	collison_happenend = False
# 	for b in bunkers:
# 		if not b.alerted:
# 			b.alert_neighbours()
# 		else: 
# 			collison_happenend = True
# 			break
# 	if collison_happenend:
# 		return True
# 	else:
# 		return False

# def reset_alerts(gold_bunker_tuples):
# 	for t in gold_bunker_tuples:
# 		t[0].alerted = False

# def get_maximum_booty(bunker, gold_values, gold_bunker_mapping):
# 	booty = 0
# 	return get_maximum_booty_recursively(bunker, gold_values, gold_bunker_mapping, booty, 0)

# def get_maximum_booty_recursively(bunker, gold_values, gold_bunker_mapping, booty, recursive_depth):
# 	current_gold_value = gold_values[0]
# 	next_bunkers = gold_bunker_mapping[current_gold_value]
# 	for b in next_bunkers:
# 		if not b.alert and not b.neighbours_alerted():
# 			b.alert()
# 			b.alert_neighbours()
# 			get_maximum_booty_recursively(bunker, gold_values, gold_bunker_mapping, booty + current_gold_value, recursive_depth+1)

# class Bunker:
# 	def __init__(self, gold, neighbours=None, alerted=False):
# 		self.gold = gold
# 		self.neighbours = None
# 		self.alerted = alerted

# 	def alert(self):
# 		self.alerted = True

# 	def alert_neighbours(self):
# 		for n in self.neighbours:
# 			n.alert()

# 	def neighbours_alerted(self):
# 		for n in self.neighbours:
# 			if n.alerted:
# 				return True
# 		return False

# 	def print_neighbours(self):
# 		for n in self.neighbours:
# 			print((n.gold,n.alerted), end=", ")

# 	def set_neighbours(self, neighbours):
# 		self.neighbours = neighbours

if __name__ == '__main__':
	bunker_gold_file = "bunker_gold.txt"
	#test()
	main(bunker_gold_file)