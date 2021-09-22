from csv import writer
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math

# function that creates spaces throughout the program to make the program look more clean
def spaces():
	print('\n')
	for i in range(4):
		print('///////////////////////////////////////////////////////')
	print('\n')

# function that displays the user with a welcome message
def welcome_message():
	print('***         Welcome user to the Free Throw Calculator          ***')
	print('***          My name is Arnav Karnik and I have been           ***')
	print('***           playing basketball since I can remember.         ***')
	print('***           My basektball coach would make us record         ***')
	print('***         the out free throw statistics in high school.      ***')
	print('***   So i decided to make a free throw tracker using python   ***')
	print('***       ENJOY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     ***')
	
# function gets called when you want to get rid of the last inputed free throw session
def remove_row(dataframe):
	dataframe = dataframe.drop(dataframe.index[-1])
	return dataframe

welcome_message()
while True:
	spaces()
	df = pd.read_csv("data.csv")
	df.columns = ["FT made", "FT attempted", "Session FT Percentage"]
	print("\nPlease enter a command\n(1)Add Free Throw data\n(2)Delete data\n" + 
		"(3)Get Data\n(4)Get Free Throw Percentage\n" + 
		"(5)Get Lowest Session Free Throw Percentage\n(6)Get Highest Session Free Throw Percentage\n" + 
		"(7)Get Shooting Graph\n(8)Predicting Shooting\n(9)Last 5 Free Throw Sessions Percentage\n" + 
		"(10)Get standard deviation\n(q)Quit")
	command = input().lower()
	
	# exits the program
	if command == "q":
		break

	# Adds a free throw session with how many FT made by the user and the total number of FT the shot
	if command == "1":
		spaces()
		print("How many Free Throws did you make?")
		made = float(input())
		print("How many total Free Throws did you shoot?")
		attempted = float(input())
		if(made>attempted):
			print("Invalid Values! Please enter values again!")
			continue
		proportion = round(made/attempted, 2)*100
		list_FT_data = [made, attempted, proportion]
		# Open file in append mode
		with open('data.csv', 'a+', newline='') as write_obj:
			# Create a writer object from csv module
			csv_writer = writer(write_obj)
			# Add conents of list as last row in the csv file
			csv_writer.writerow(list_FT_data)

	# Removes the last row in the data.csv file or removes the last FT session from the csv file
	if command == "2":
		df = remove_row(df)
		df.to_csv("data.csv", index=False)

	# Displays the tail of the dataframe for the user to see
	if command == "3":
		spaces()
		print(df.tail())
	
	# Displays the user with their free throw percentage
	if command == "4":
		spaces()
		made = df["FT made"].sum()
		total = df["FT attempted"].sum()
		proportion = float(made)/float(total)
		percent = round(proportion, 3)*100
		print("\nYour Free Throw Percentage: " + str(percent) + "%\n" + 
			"Total Free Throws Made: " + str(made) + 
			"\nTotal Free Throws Attempted: " + str(total))

	# Displays the user with their highest free throw session percentage
	if command == "6":
		spaces()
		new_df = df[df['FT attempted'] > 0]
		highest = new_df['Session FT Percentage'].max()
		highest_index = new_df[new_df['Session FT Percentage'] == highest].index.values[0]
		highest_made = new_df.iloc[highest_index]['FT made']
		highest_attempted = new_df.iloc[highest_index]['FT attempted']
		print("Highest Session Free Throw Percentage: " + str(highest) + "%")
		print("Free Throws Made: " + str(int(highest_made)))
		print("Free Throws Attempted: " + str(int(highest_attempted)))

	# Displays the user with their lowest free throw session percentage
	if command == "5":
		spaces()
		new_df = df[df['FT attempted'] > 0]
		lowest = new_df['Session FT Percentage'].min()
		lowest_index = new_df[new_df['Session FT Percentage'] == lowest].index.values[0]
		lowest_made = new_df.iloc[lowest_index]['FT made']
		lowest_attempted = new_df.iloc[lowest_index]['FT attempted']
		print("Lowest Session Free Throw Percentage: " + str(lowest) + "%")
		print("Free Throws Made: " + str(int(lowest_made)))
		print("Free Throws Attempted: " + str(int(lowest_attempted)))

	# Displays the user with a graph representing the relationship between FT made and FT attempted
	if command == "7":
		plt.scatter(df['FT attempted'], df['FT made'])
		plt.title("Free Throws Made vs Free Throws Attempted", fontdict={'fontname': 'Comic Sans MS', 'fontsize':20})
		plt.xlabel("FT attempted", fontdict={'fontname': 'Comic Sans MS'})
		plt.ylabel("FT made", fontdict={'fontname': 'Comic Sans MS'})
		plt.show()

	# Allows the user to predict information based on their past data
	if command == "8":
		spaces()
		made = df['FT made'].to_list()
		attempted = df['FT attempted'].to_list()
		x = np.array(attempted)
		y = np.array(made)
		m, b = np.polyfit(x, y, 1)
		print("In this setting we will predict free throw attempts and makes based on previous data.")
		print("Choose option?")
		print("(1)Predict FT made given total shots put up")
		print("(2)Predict FT attempted given shots made")
		choice = input().lower()

		# Predicts the FT made by the user when the user inputs the total shots they supposably put up
		if choice == "1":
			from matplotlib import pyplot as plt
			print("Total shots put up?")
			guess = input()
			g_made = ((float(guess))*m) + b
			g_made = int(g_made)
			print(f"If you shot {guess} free throws you would approximately make {g_made} free throws")

			predict_made = [0] * (len(x)-1)
			predict_made.append(g_made)
			predict_attempted = [0] * (len(y)-1)
			predict_attempted.append(guess)
			predict_proportion = []
			for i in range(len(predict_attempted)):
				if predict_attempted[i] == 0:
					proportion = 0
				else:
					proportion = round((predict_made[i])/(float(predict_attempted[i])), 2)*100
				predict_proportion.append(proportion)

			temp = pd.DataFrame(list(zip(predict_made, predict_attempted, predict_proportion)),
				columns = ['FT Made', 'FT attempted', 'Session FT Percentage'])
			plt.plot(x, y,'o')
			line = m*x + b
			
			plt.plot(x, line, label='line of best fit')
			plt.scatter(temp['FT attempted'].to_list(), temp['FT Made'].to_list(), c='r')
			plt.title("Free Throws Made vs Free Throws Attempted", fontdict={'fontname': 'Comic Sans MS', 'fontsize':20})
			plt.xlabel("FT attempted", fontdict={'fontname': 'Comic Sans MS'})
			plt.ylabel("FT made", fontdict={'fontname': 'Comic Sans MS'})
			plt.show()

		# Predicts the FT attempted by the user when the user inputs the free throws the supposably made
		if choice == "2":
			print("Total shots made?")
			guess = input()
			g_attempted = ((float(guess)) - b)//m 
			#g_attempted = int(g_attempted)  // rounds down through division
			print("if you made " + str(guess) + " free throws you would approximately have" + 
			" shot a total of " + str(g_attempted) + " free throws")

			predict_made = [0] * (len(x)-1)
			predict_made.append(guess)
			predict_attempted = [0] * (len(y) - 1)
			predict_attempted.append(g_attempted)
			predict_proportion = []
			for i in range(len(predict_attempted)):
				if predict_attempted[i] == 0:
					proportion = 0
				else:
					proportion = round((float(predict_made[i]))/(float(predict_attempted[i])), 2)*100
				predict_proportion.append(proportion)

			temp = pd.DataFrame(list(zip(predict_made, predict_attempted, predict_proportion)),
				columns = ['FT Made', 'FT attempted', 'Session FT Percentage'])
			plt.plot(x, y, 'o')
			line = m*x + b
			plt.plot(x, line, label='line of best fit')
			plt.scatter(temp['FT attempted'].to_list(), temp['FT Made'].to_list(), c='r')
			plt.title("Free Throws Made vs Free Throws Attempted", fontdict={'fontname': 'Comic Sans MS', 'fontsize':20})
			plt.xlabel("FT attempted", fontdict={'fontname': 'Comic Sans MS'})
			plt.ylabel("FT made", fontdict={'fontname': 'Comic Sans MS'})
			plt.show()

	# Displays the user with their FT percentage from the last 5 free throw sessions
	if command == '9':
		spaces()
		last_5 = df.tail()
		last_5_made = last_5['FT made'].sum()
		last_5_attempted = last_5['FT attempted'].sum()
		proportion_last_5 = last_5_made/last_5_attempted
		percentage_last_5 = round(proportion_last_5,3)*100
		#print(percentage_last_5)
		total_made = df['FT made'].sum()
		total_attempted = df['FT attempted'].sum()
		total_proportion = total_made/total_attempted
		total_percentage = round(total_proportion, 3)*100
		#print(total_percentage)
		print(f"\nIn the past 5 free throw sessions you have shot {percentage_last_5}% on {last_5_made} of {last_5_attempted} shooting.")
		dif = abs(percentage_last_5 - total_percentage)
		difference = round(dif,3)
		if percentage_last_5 > total_percentage:
			print(f"You shot {difference}% above your total free throw percentage")
		elif percentage_last_5 < total_percentage:
			print(f"You shot {difference}% below your total free throw percentage")
		else:
			print("In your last 5 free throw sessions you are shooting the same as your total free throw percentage")

	# Calculating the standard deviation of all the FT sessions from the mean
	if command == "10":
		spaces()
		#print("Using function: " + str(round(df['Session FT Percentage'].std(), 2)))

		total_made = df['FT made'].sum()
		total_attempted = df['FT attempted'].sum()
		proportion = total_made/total_attempted
		mean = round(proportion, 2)*100

		sessions = df['Session FT Percentage'].to_list()
		total = 0 
		counter = 0
		for val in sessions:
			new_val = abs(mean-val)
			squared = new_val**2
			counter+=1
			total += squared
		variance = total / counter
		standard_deviation = math.sqrt(variance)
		answer = round(standard_deviation,2)
		print("Standard deviation: " + str(answer) + "%")
