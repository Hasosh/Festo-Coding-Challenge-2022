import numpy as np
import sys
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
from random import randrange
import pickle

def main(file1, file2):	
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
		a, b, c, d, figure = plot_random_plane(all_coordinates, figure)
		# identify all potential outliers
		outliers = []
		outliers_coordinates = []
		for planet, coords in planet_coord_mapping.items():
			x, y, z = coords
			if shortest_distance(x, y, z, a, b, c, d) >= 10:
				outliers.append(planet)
				outliers_coordinates.append(coords)
		plot_outliers(outliers_coordinates, figure)
		print(outliers)
		with open(file2, "r") as filestreamtwo:
			with open("solution.txt", "w") as filestreamthree:
				possible_persons = []
				sum_of_outlier_IDs = 0
				lines = filestreamtwo.readlines()
				for i in range(int(len(lines) / 14)):
					cur_name = lines[i * 14].split(":")[1].strip()
					cur_ID = lines[i * 14 + 1].split(":")[1].strip()
					cur_planet = lines[i * 14 + 2].split(":")[1].strip()
					#check if planet is an outlier planet
					if cur_planet in outliers:
						possible_persons.append(cur_name)
						sum_of_outlier_IDs += int(cur_ID)
				print(sum_of_outlier_IDs)
				filestreamthree.write(str(sum_of_outlier_IDs))
				save_list(possible_persons)

def save_list(mylist):
	with open('possible_users.pkl', 'wb') as f:
		pickle.dump(mylist, f)

def plot_outliers(outliers_coordinates, figure):
	x, y, z = zip(*outliers_coordinates)
	figure.scatter3D(x, y, z, c='red')
	plt.show()

def plot_galaxy(x, y, z, all):
	fig = plt.figure()
	#plt.rcParams['figure.figsize'] = (8,6)
	#ax = plt.axes(projection='3d')
	ax = Axes3D(fig)
	ax.set_title('Galaxy')

	ax.scatter3D(x, y, z, c='green')
	ax.view_init(90,90)
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	return ax

def shortest_distance(x1,y1,z1,a,b,c,d):
	nominator = abs((a*x1 + b*y1 + c * z1 + d))
	denominator = math.sqrt(a*a + b*b + c*c)
	distance = nominator / denominator
	return distance

def plot_random_plane(all_coordinates, figure):
	random_coordinates = []
	for i in range(3):
		random_coordinates.append(all_coordinates[randrange(len(all_coordinates))])
	print(random_coordinates)

	p0, p1, p2 = random_coordinates
	x0, y0, z0 = p0
	x1, y1, z1 = p1
	x2, y2, z2 = p2

	ux, uy, uz = u = [x1-x0, y1-y0, z1-z0]
	vx, vy, vz = v = [x2-x0, y2-y0, z2-z0]

	u_cross_v = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx]

	point  = np.array(p0)
	normal = np.array(u_cross_v)

	d = -point.dot(normal)

	xx, yy = np.meshgrid(range(300), range(300))

	z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]

	# plot the surface
	#plt3d = plt.figure(1).gca(projection='3d')
	#plt3d.plot_surface(xx, yy, z)
	#plt.show()
	
	figure.plot_surface(xx, yy, z)
	plt.show()

	return u_cross_v[0], u_cross_v[1], u_cross_v[2], d, figure

			
if __name__ == '__main__':
	galaxy_file = "galaxy_map.txt"
	population_file = "population.txt"
	main(galaxy_file, population_file)