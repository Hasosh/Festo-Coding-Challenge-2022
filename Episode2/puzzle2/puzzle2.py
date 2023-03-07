import numpy as np
import sys
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
from random import randrange
import pickle
from numpy.linalg import norm

def main(file1, file2, file3):	
	with open(file1, "r") as filestream:
		xcoordinates = []
		ycoordinates = []
		zcoordinates = []
		all_coordinates = []
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
			planet_coord_mapping[planet] = (x, y, z)
		figure = plot_galaxy(xcoordinates, ycoordinates, zcoordinates, all_coordinates)
		#figure = plot_galaxy2(planet_coord_mapping)
		trade_routes = process_trade_routes(file3)
		trade_routes_coords = []
		for t in trade_routes:
			# FORMAT: trade_routes = (planet1, planet2, reachable)
			trade_routes_coords.append((planet_coord_mapping[t[0]], planet_coord_mapping[t[1]], t[2]))
		figure = plot_trade_routes(trade_routes_coords, figure)
		# identify possible pirat planets
		possible_pirate_planets = []
		possible_pirate_planets_coords = []
		print("The trade routes: ", trade_routes)
		for planet in planet_coord_mapping:
			planet_coords = planet_coord_mapping[planet]
			toggle = True
			for t_r in trade_routes:
				#print("Current Planet: " + planet)
				trade_coords1 = planet_coord_mapping[t_r[0]]
				trade_coords2 = planet_coord_mapping[t_r[1]]
				if t_r[2] != check_distance(planet_coords, trade_coords1, trade_coords2):
					toggle = False
					break
			if toggle:
				#print("TOOK THE PLANET!")
				possible_pirate_planets.append(planet)
				possible_pirate_planets_coords.append(planet_coords)

		print("possible_pirate_planets: ", possible_pirate_planets)

		#plotting
		plot_pirate_planets(possible_pirate_planets_coords, figure)
		#finding out possible inhabitants for pirats
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

def test():
	#p = (3,2,1)
	#t1 = (-3, 4, -1)
	#t2 = (-4, 6, 0)
	#check_distance(p, t1, t2)
	#p1 = (1, 2, 3)
	#p2 = (7, 5, 4)
	#basic_distance_debugging(p1, p2)

	print(int(9.9999))
	print(int(10.0))
	print(int(10.12))
	print(int(9.456))
			

def basic_distance_debugging(p1, p2):
	p1 = np.asarray(p1)
	p2 = np.asarray(p2)
	diff = p2 - p1
	dist = norm(diff) # works as intended
	return dist

def check_distance(p, a, b):
	p = np.asarray(p)
	a = np.asarray(a)
	b = np.asarray(b)

	# Source: Stackoverflow - https://stackoverflow.com/questions/56463412/distance-from-a-point-to-a-line-segment-in-3d-python
	# normalized tangent vector
	d = np.divide(b - a, np.linalg.norm(b - a))

	# signed parallel distance components
	s = np.dot(a - p, d)
	t = np.dot(p - b, d)

	# clamped parallel distance
	h = np.maximum.reduce([s, t, 0])

	# perpendicular distance component
	c = np.cross(p - a, d)

	# perpendicular distance
	dist = np.hypot(h, np.linalg.norm(c))

	dist = int(dist)
	limit = 9
	if dist <= limit:
		return True
	else: 
		return False

def process_trade_routes(file):
	trade_routes = []
	with open(file, "r") as filestream:
		for line in filestream:
			splitted_line = line.split(":")
			# 1. filter planets
			planets = splitted_line[0].strip()
			splitted_planets = planets.split("-")
			planet1 = splitted_planets[0].strip()
			planet2 = splitted_planets[1].strip()
			# 2. filter reachability
			reachable = splitted_line[1].strip()
			if reachable == "Ok":
				reachable = True
			elif reachable == "too far":
				reachable = False
			else:
				print("ERROR occurred 01")
			trade_routes.append((planet1, planet2, reachable))
	return trade_routes

def save_list(mylist):
	with open('possible_users.pkl', 'wb') as f:
		pickle.dump(mylist, f)

def plot_pirate_planets(pirate_planets_coordinates, figure):
	x, y, z = zip(*pirate_planets_coordinates)
	figure.scatter3D(x, y, z, c='red', s=50)
	plt.show()

def plot_trade_routes(trade_routes_coords, figure):
	for t in trade_routes_coords:
		t1, t2, reachable = t
		x, y, z = zip(*(t1,t2))
		if reachable:
			figure.plot(x, y, z, c='black')
		else: 
			figure.plot(x, y, z, c='red')
		figure.scatter3D(x, y, z, 'bo', linestyle="--", c='blue')
	return figure

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

def plot_galaxy2(mapping_planet_coords):
	fig = plt.figure()
	#plt.rcParams['figure.figsize'] = (8,6)
	#ax = plt.axes(projection='3d')
	ax = Axes3D(fig)
	ax.set_title('Galaxy')

	for p in mapping_planet_coords:
		c = mapping_planet_coords[p]
		x, y, z = c
		ax.scatter3D(x, y, z, c='green')
		ax.text(x, y, z,  '%s' % p, size=5, color='k')
	ax.view_init(-20,-105)
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	ax.dist = 1
	return ax
			
if __name__ == '__main__':
	galaxy_file = "galaxy_map.txt"
	population_file = "population.txt"
	trade_routes_file = "trade_routes.txt"
	main(galaxy_file, population_file, trade_routes_file)
	#test() # debugging
	#print(10 / math.sqrt(3))