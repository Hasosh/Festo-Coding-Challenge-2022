import sys

def print_all_lists(usernames, IDs, access_keys, first_login_times):
	print(usernames)
	print(IDs)
	print(access_keys)
	print(first_login_times)

def main():	
	with open("office_database.txt") as filestream:
		with open("solution.txt", "w") as filestreamtwo:
			IDs, access_keys, first_login_times = {}, {}, {}
			for line in filestream:
				currentline = line[:-1].split(",")
				IDs[currentline[0]] = currentline[1]
				access_keys[currentline[0]] = currentline[2]
				first_login_times[currentline[0]] = currentline[3]
			solution1, possible_users1 = puzzle1(IDs)
			print(solution1); filestreamtwo.write(str(solution1) + "\n")
			solution2, possible_users2 = puzzle2(IDs, access_keys)
			print(solution2); filestreamtwo.write(str(solution2) + "\n")
			solution3, possible_users3 = puzzle3(IDs, first_login_times)
			print(solution3); filestreamtwo.write(str(solution3))
			final_solution = final_puzzle(possible_users1, possible_users2, possible_users3)
			print(final_solution); filestreamtwo.write(str(final_solution))

def puzzle1(IDs):
	solution = 0
	possible_users = []
	for key in IDs:
		value = IDs[key]
		if '814' in value:
			solution += int(value)
			possible_users.append(key)
	return solution, possible_users

def puzzle2(IDs, access_keys):
	solution = 0
	possible_users = []
	for key in access_keys:
		value = access_keys[key]
		binary_value = bin(int(value))[2:]
		if len(binary_value) >= 4:
			if binary_value[-4] == '1':
				possible_users.append(key)
	for user in possible_users:
		solution += int(IDs[user])
	return solution, possible_users

def puzzle3(IDs, first_login_times):
	solution = 0
	possible_users = []
	counter = 0
	for key in first_login_times:
		value = first_login_times[key].strip()
		if value[1] == '5' or value[1] == '6':
			possible_users.append(key)
		if value[1] == '7':
			if value[3] == '0':
				possible_users.append(key)
			elif value[3] == '1':
				if value[4] == '0' or value[4] == '1' or value[4] == '2' or value[4] == '3':
					possible_users.append(key)
	for user in possible_users:
		solution += int(IDs[user])
	return solution, possible_users

def final_puzzle(possible_users1, possible_users2, possible_users3):
	return list(set(possible_users1) & set(possible_users2) & set(possible_users3))

def print_all_lists(usernames, IDs, access_keys, first_login_times):
	print(usernames)
	print(IDs)
	print(access_keys)
	print(first_login_times)

if __name__ == '__main__':
	main()