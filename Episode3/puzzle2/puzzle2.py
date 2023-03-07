import numpy as np
import sys
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
from random import randrange
import pickle
from numpy.linalg import norm

def main(file1, file2, file3, file4):	
	xcoordinates, ycoordinates, zcoordinates, planets, planet_coord_mapping = process_galaxy(file1)
	#figure = plot_galaxy(xcoordinates, ycoordinates, zcoordinates, all_coordinates)
	initialize_galaxy(planets) #identify neighbours of all planets
	possible_pirate_planets = find_potential_planets(planet_coord_mapping, file4)
	print("possible_pirate_planets: ", possible_pirate_planets)
	print("Length of possible_pirate_planets:", len(possible_pirate_planets))
	with open(file2, "r") as filestreamtwo:
		with open("solution.txt", "w") as filestreamthree:
			possible_persons = []
			sum_of_outlier_IDs = 0
			lines = filestreamtwo.readlines()
			for i in range(int(len(lines) / 14)):
				cur_name = lines[i * 14].split(":")[1].strip()
				cur_ID = lines[i * 14 + 1].split(":")[1].strip()
				cur_planet = lines[i * 14 + 2].split(":")[1].strip()
				#print(cur_name, cur_ID, cur_planet)
				#check if planet is an outlier planet
				if cur_planet in possible_pirate_planets:
					possible_persons.append(cur_name)
					sum_of_outlier_IDs += int(cur_ID)
			print(sum_of_outlier_IDs)
			filestreamthree.write(str(sum_of_outlier_IDs))
			save_list(possible_persons)

class Planet:
	def __init__(self, name, x, y, z):
		self.name = name
		self.x = x
		self.y = y
		self.z = z
		self.neighbours = set()

	def get_coordinates(self):
		return (self.x, self.y, self.z)

	def get_distance_to(self, planet):
		p1 = np.asarray(self.get_coordinates())
		p2 = np.asarray(planet.get_coordinates())
		diff = p2 - p1
		dist = norm(diff) # works as intended
		return dist

	def get_neighbours_names(self):
		neighbours_names = []
		for p in self.neighbours:
			neighbours_names.append(p.name)
		return neighbours_names

	def get_distance_dict(self):
		my_dict = {}
		for n in self.neighbours:
			my_dict[n.name] = 1
		return my_dict

def process_galaxy(file):
	with open(file, "r") as filestream:
		xcoordinates = []
		ycoordinates = []
		zcoordinates = []
		all_coordinates = []
		planets = []
		planet_coord_mapping = {}
		for line in filestream:
			splitted_line = line.split(":")
			planet = splitted_line[0].strip()
			coordinates = splitted_line[1] 
			coordinates = coordinates[2:-2] # leave out the parentheses
			coordinates = coordinates.split(",")
			x = int(coordinates[0].strip())
			y = int(coordinates[1].strip())
			z = int(coordinates[2].strip())
			xcoordinates.append(x)
			ycoordinates.append(y)
			zcoordinates.append(z)
			all_coordinates.append((x, y, z))
			planet_obj = Planet(planet, x, y, z)
			planets.append(planet_obj)
			planet_coord_mapping[planet] = planet_obj
		return xcoordinates, ycoordinates, zcoordinates, planets, planet_coord_mapping

def initialize_galaxy(planets):
	for p1 in planets:
		for p2 in planets:
			if p1.get_distance_to(p2) <= 50:
				p1.neighbours.add(p2)
	print("Galaxy intitialized!")

def find_potential_planets(planet_coord_mapping, file):
	with open(file, "r") as f:
		lines = f.readlines()
		potential_planets = []
		for i in range(len(lines)):
			splitted_line = lines[i].split(":")
			plnt = splitted_line[0].strip()
			dist = int(splitted_line[1].strip())
			print("distance is:", dist)
			visited = search_planets(planet_coord_mapping, plnt, dist)
			print("DONE SEARCHING")
			relevant_visited = [p for p in visited if visited[p] == dist] #only take those that are of distance 2
			print("relevant_visited: ", relevant_visited)
			potential_planets.append(relevant_visited)
		return list(set(potential_planets[0]) & set(potential_planets[1]) & set(potential_planets[2]))

def search_planets(planet_coord_mapping, cur_planet, desired_distance): #dijkstra algorithm
	unvisited = {planet: None for planet in planet_coord_mapping} #using None as +inf
	visited = {}
	current = planet_coord_mapping[cur_planet].name
	currentDistance = 0
	newDistance = 0
	unvisited[current] = currentDistance

	distances = {}
	while currentDistance - 1 < desired_distance:
		d = planet_coord_mapping[current].get_distance_dict()
		distances[current] = d
		for neighbour, distance in distances[current].items():
			if neighbour not in unvisited: 
				continue
			newDistance = currentDistance + distance
			#print("newDistance is:", newDistance)
			if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
				unvisited[neighbour] = newDistance
		visited[current] = currentDistance
		del unvisited[current]
		if not unvisited: break
		#print(unvisited)
		candidates = [planet for planet in unvisited.items() if planet[1]]
		#print(candidates)
		#print(sorted(candidates, key = lambda x: x[1]))
		current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]
		#print(visited)
	print(visited)
	#print(visited['Venis'])
	return visited

def test(planet_coord_mapping):
	t = planet_coord_mapping["Beta Urado"].get_neighbours_names()
	print(t)
	if "Alpha Lyralia" in t:
		print(True)
	else:
		print(False)

def save_list(mylist):
	with open('possible_users.pkl', 'wb') as f:
		pickle.dump(mylist, f)

def plot_pirate_planets(pirate_planets_coordinates, figure):
	x, y, z = zip(*pirate_planets_coordinates)
	figure.scatter3D(x, y, z, c='red', s=50)
	plt.show()

def plot_galaxy(x, y, z, all):
	fig = plt.figure()
	#plt.rcParams['figure.figsize'] = (8,6)
	#ax = plt.axes(projection='3d')
	ax = Axes3D(fig)
	ax.set_title('Galaxy')

	ax.scatter3D(x, y, z, c='green')
	ax.view_init(-20,-105)
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	ax.dist = 1.5
	return ax
			
if __name__ == '__main__':
	galaxy_file = "galaxy_map.txt"
	population_file = "population.txt"
	signal_examples_file = "signal_examples.txt"
	signal_ranging_file = "signal_ranging.txt"
	main(galaxy_file, population_file, signal_examples_file, signal_ranging_file)
	#test() # debugging
	#print(10 / math.sqrt(3))