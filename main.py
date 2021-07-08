from csv import writer
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def remove_row(dataframe):
	dataframe = dataframe.drop(dataframe.index[-1])
	return dataframe


while True:
	df = pd.read_csv("data.csv")
	df.columns = ["FT made", "FT attempted", "Session FT Percentage"]
	print("\nPlease enter a command\n(1)Add Free Throw data\n(2)Delete data\n" + 
		"(3)Get Data\n(4)Get Free Throw Percentage\n" +
		"(5)Get Lowest Session Free Throw Percentage\n(6)Get Highest Session Free Throw Percentage\n" + 
		"(7)Get Shooting Graph\n(8)Predicting Shooting\n(q)Quit")
	command = input().lower()
	if command == "q":
		break
	if command == "1":
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

	if command == "2":
		df = remove_row(df)
		df.to_csv("data.csv", index=False)

	if command == "3":
		print(df.tail())
	
	if command == "4":
		made = df["FT made"].sum()
		total = df["FT attempted"].sum()
		proportion = float(made)/float(total)
		percent = round(proportion, 3)*100
		print("\nYour Free Throw Percentage: " + str(percent) + "%\n" + 
			"Total Free Throws Made: " + str(made) + 
			"\nTotal Free Throws Attempted: " + str(total))
	if command == "5":
		new_df = df[df['FT attempted'] > 0]
		highest = new_df['Session FT Percentage'].max()
		highest_index = new_df[new_df['Session FT Percentage'] == highest].index.values[0]
		highest_made = new_df.iloc[highest_index]['FT made']
		highest_attempted = new_df.iloc[highest_index]['FT attempted']
		print("Highest Session Free Throw Percentage: " + str(highest) + "%")
		print("Free Throws Made: " + str(int(highest_made)))
		print("Free Throws Attempted: " + str(int(highest_attempted)))

	if command == "6":
		new_df = df[df['FT attempted'] > 0]
		lowest = new_df['Session FT Percentage'].min()
		lowest_index = new_df[new_df['Session FT Percentage'] == lowest].index.values[0]
		lowest_made = new_df.iloc[lowest_index]['FT made']
		lowest_attempted = new_df.iloc[lowest_index]['FT attempted']
		print("Lowest Session Free Throw Percentage: " + str(lowest) + "%")
		print("Free Throws Made: " + str(int(lowest_made)))
		print("Free Throws Attempted: " + str(int(lowest_attempted)))
	if command == "7":
		plt.scatter(df['FT attempted'], df['FT made'])
		plt.title("Free Throws Made vs Free Throws Attempted", fontdict={'fontname': 'Comic Sans MS', 'fontsize':20})
		plt.xlabel("FT attempted", fontdict={'fontname': 'Comic Sans MS'})
		plt.ylabel("FT made", fontdict={'fontname': 'Comic Sans MS'})
		plt.show()
	if command == "8":
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
		if choice == "1":
			from matplotlib import pyplot as plt
			print("Total shots put up?")
			guess = input()
			g_made = ((float(guess))*m) + b
			g_made = int(g_made)
			print("If you shot " + str(guess) + " free throws you would approximately make " + 
				str(g_made) + " free throws")

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


		if choice == "2":
			print("Total shots made?")
			guess = input()
			g_attempted = ((float(guess)) - b)/m 
			g_attempted = int(g_attempted)
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
