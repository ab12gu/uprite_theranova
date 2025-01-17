####
# filename: compare_gait.py
# by: Abhay Gupta
# date: 09/21/18
#
# description: compare properties of zeno & uprite TO_HS
####

# Library imports
import pickle
import os
import sys
import csv
import statistics as stats
import time as clocktime
from pathlib import Path
 

# global variables
top = ['Patient', 'Pace', 'Stride time', 'Right step time',
		   'Left step time', 'Double stance time', 'Right single stance', 'Left single stance', 'Cadence']
	
def extract(directory, output):
	"""Compare gait of zeno and uprite system"""

	pace = ['S', 'C', 'F']
	system = ['zeno', 'uprite']
	orientation = ['r', 'l']
	foot = ['HS', 'TO']
	gait_names = ['stride', 'right_step', 'left_step', 'double_stnace', 'right_single_stance', 'left_single_stance', 'cadence']

	# iterate through each patient file
	patient_number = directory[-6:]
	print("Extrating data from patient: ", patient_number)
	gait = {}

	"""Extract Pickle Data"""
	zeno_file = os.path.join(directory, 'zeno_gait.pkl')
	uprite_file = os.path.join(directory, 'uprite_gait.pkl')
	with open(zeno_file, 'rb') as afile:
		zeno = pickle.load(afile)
	file_check =  Path(uprite_file)
	if not file_check.is_file():
		uprite = {}
		for p in pace:
			uprite[p] = None
	else:
		with open(uprite_file, 'rb') as afile:
			uprite = pickle.load(afile)

	"""Find Gait Parameters from HS & TO"""

	for p in pace:
		gait[p] = []

		for i in range(0, len(gait_names)):
			if uprite[p] is None:
				error = None
			else:
				UR = uprite[p][gait_names[i]]
				ZN = zeno[p][gait_names[i]]
				if UR is None:
					error = None
				else:
					error = (UR - ZN)/ZN

			
			gait[p].append(error)

	"""Add data to csv_file"""
	for p in pace:
		output.writerow([patient_number, p] + gait[p])

	return


			# find the % difference




	gait['dif'] = {}

	for p in pace:
		gait['dif'][p] = [] 
		for i in range(0, len(gait['uprite'][p])):
			if i > 0: # only do first one rn... due to missing analyzes
				continue
			elif gait['uprite'][p][0] is None:
				gait['dif'][p].append(None)
				continue
			gait['dif'][p].append((gait['uprite'][p][i] - gait['zeno'][p][i]) / gait['zeno'][p][i])
		gait['dif'][p].extend(['', '', '', ''])
		

	"""Add data to csv_file"""
	for p in pace:
		output.writerow([patient_number, 'uprite', p] + gait['uprite'][p])
		output.writerow(['', 'zeno', p] + gait['zeno'][p])
		output.writerow(['', '', '% Error'] + gait['dif'][p])

def input_check(directory, folder_type):
	"""Check input folder type"""

	if (folder_type == 'n'): # run single patient file
		with open('../docs/compare_gait.csv', 'a') as csvfile:
			output = csv.writer(csvfile)

			extract(directory, output)
	else: # iterate through every patient file
		start_time = clocktime.time()

		with open('../docs/compare_gait.csv', 'w') as csvfile:
			output = csv.writer(csvfile)
			output.writerow(top)
		
			for c, filename in enumerate(os.listdir(directory)):
				if c < 0:
					continue
				if filename == ".DS_Store":
					continue

				print("Current patient iteration: ", c)
				afile = os.path.join(directory, filename)
				extract(afile, output)

		print('Successful run!') 
		print('-----------RUNTIME: %s second ----' % (clocktime.time() - start_time))

		

if __name__ == '__main__':
	print('Running test files... skipping GUI')

	directory = '../../data_files/analyzed_data'
	folder_type = 'y'
	#directory = '../../data_files/analyzed_data/no_003'
	#folder_type = 'n'

	input_check(directory, folder_type)






