'''
The script provides the solution to AM16 SPR20 Financial Reporting Analytics Group Assignment 3
'''

# Import libraries
import numpy as np
import pandas as pd
import math
import gurobipy as gp
import matplotlib.pyplot as plt
import seaborn as sns

# Define global parameters
capacity_one = 250000
fixed_cost = 2000000000

# Define search ranges
factory_number = [1, 2, 3]
price_a = list(range(10000, 100000, 10000))
price_b = list(range(10000, 100000, 10000))

class Optimisation:
	'''
	Module to solve the embedded optimisation problem
	'''
	def __init__(self, capacity_one, fixed_cost, price_a, price_b, factory_number):
		'''Initiate variables of the model'''
		self.capacity_one, self.fixed_cost = capacity_one, fixed_cost
		self.price_a, self.price_b, self.factory_number = price_a, price_b, factory_number
		self.best_params = [0, 0, 0, 0, 0]
		self.profit = []
		self.current_profit = 0
		self.best_profit = 0
		self.quantity_a = []
		self.current_quantity_a = 0
		self.quantity_b = []
		self.current_quantity_b = 0
		self.price_a_history = []
		self.price_b_history = []
		self.capacity_history = []
		self.df = pd.DataFrame()
		self.df_1 = pd.DataFrame()
		self.df_2 = pd.DataFrame()
		self.df_3 = pd.DataFrame()

	def grid_search(self):
		'''Calculate all viable solutions given ranges of input'''
		for i_1 in range(len(factory_number)):
			for i_2 in range(len(price_a)):
				for i_3 in range(len(price_b)):
					self.current_quantity_a = (1000000 - 1000000/(1 + math.exp(-(1/15000)*(price_a[i_2]-50000))))
					self.current_quantity_b = (1000000 - 1000000/(1 + math.exp(-(1/15000)*(price_b[i_3]-40000))))
					if self.current_quantity_a + self.current_quantity_b <= factory_number[i_1] * self.capacity_one:
						self.current_profit = self.current_quantity_a*price_a[i_2] + self.current_quantity_b*price_b[i_3] - (56000 - 5600/(1 + math.exp(1-(1/10000)*(self.current_quantity_a - 50000))))*self.current_quantity_a - (35000 - 3500/(1 + math.exp(-(1/20000)*(self.current_quantity_b - 100000))))*self.current_quantity_b - 2000000000*factory_number[i_1]
						self.quantity_a.append(self.current_quantity_a)
						self.quantity_b.append(self.current_quantity_b)
						self.profit.append(self.current_profit)
						if self.current_profit == max(self.profit):
							self.best_params = [factory_number[i_1], price_a[i_2], price_b[i_3], self.current_quantity_a, self.current_quantity_b]
							self.best_profit = self.current_profit
					else:
						self.quantity_a.append(0)
						self.quantity_b.append(0)
						self.profit.append(0)
					self.capacity_history.append(factory_number[i_1])
					self.price_a_history.append(self.price_a[i_2])
					self.price_b_history.append(self.price_b[i_3])
		self.df = pd.DataFrame({'Price_Model_A':self.price_a_history, 'Price_Model_B':self.price_b_history, 'Profit':self.profit, 'Capacity':self.capacity_history}, dtype = float)

	def result_display(self):
		'''Display optimal opearting parameters and the consequent profit'''
		print('*'*10 + 'The highest level of profit is:' + '*'*10)
		print(self.best_profit)
		print('The optimal number of factory is:')
		print(self.best_params[0])
		print('The optimal price level for model A is:')
		print(self.best_params[1])
		print('The optimal price level for model B is:')
		print(self.best_params[2])
		print('The corresponding demand level for model A is:')
		print(self.best_params[3])
		print('The corresponding demand level for model B is;')
		print(self.best_params[4])
		print('*'*10 + '*'*len('The highest level of profit is:') + '*'*10)

	def data_visualisation(self):
		'''Visualise the relationship between operating profit and prices of both models'''
		self.df_1 = self.df.loc[(self.df['Profit'] != 0) & (self.df['Capacity'] == 1),:]
		self.df_1.drop('Capacity', axis = 1, inplace = True)
		self.df_1 = pd.pivot_table(self.df_1, values = 'Profit', index = ['Price_Model_A'], columns = 'Price_Model_B')
		self.df_1 = self.df_1.loc[:,::-1]
		plt.figure(figsize = (16,9))
		sns.set(style = 'darkgrid')
		sns.heatmap(self.df_1, cmap = 'OrRd', vmin = 0, vmax = 7000000000)
		plt.xlabel('Price of Model B')
		plt.ylabel('Price of Model A')
		plt.title('Profit Levels of Varying Prices for Model A and B with One Factory')
		plt.savefig('Profitibility_Price_One_Factory.png', dpi = 300)
		plt.close()

		self.df_2 = self.df.loc[(self.df['Profit'] != 0) & (self.df['Capacity'] == 2),:].drop('Capacity', axis = 1)
		self.df_2 = pd.pivot_table(self.df_2, values = 'Profit', index = ['Price_Model_A'], columns = 'Price_Model_B')
		self.df_2 = self.df_2.loc[:,::-1]
		plt.figure(figsize = (16,9))
		sns.heatmap(self.df_2, cmap = 'OrRd', vmin = 0, vmax = 7000000000)
		plt.xlabel('Price of Model B')
		plt.ylabel('Price of Model A')
		plt.title('Profit Levels of Varying Prices for Model A and B with Two Factory')
		plt.savefig('Profitibility_Price_Two_Factory.png', dpi = 300)
		plt.close()

		self.df_3 = self.df.loc[(self.df['Profit'] != 0) & (self.df['Capacity'] == 3),:].drop('Capacity', axis = 1)
		self.df_3 = pd.pivot_table(self.df_3, values = 'Profit', index = ['Price_Model_A'], columns = 'Price_Model_B')
		self.df_3 = self.df_3.loc[:,::-1]
		plt.figure(figsize = (16,9))
		sns.heatmap(self.df_3, cmap = 'RdBu_r', center = 0)
		plt.xlabel('Price of Model B')
		plt.ylabel('Price of Model A')
		plt.title('Profit Levels of Varying Prices for Model A and B with Three Factory')
		plt.savefig('Profitibility_Price_Three_Factory.png', dpi = 300)
		plt.close()

	def exec(self):
		self.grid_search()
		self.result_display()
		self.data_visualisation()

if __name__ == '__main__':
	obj = Optimisation(capacity_one, fixed_cost, price_a, price_b, factory_number)
	obj.exec()
