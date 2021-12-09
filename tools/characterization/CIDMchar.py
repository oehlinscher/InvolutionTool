"""
	@file CIDMChar.py

	@brief Main script for IDM and CIDM characterization of a single gate

	@author Daniel OEHLINGER <d.oehlinger@outlook.com>
	@author Juergen MAIER <juergen.maier@tuwien.ac.at>
	@date 2021

	@copyright
	@parblock
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <https://www.gnu.org/licenses/>.
	@endparblock	
""" 

import sys
import os
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import pickle
import random
import random
from typing import NoReturn, Tuple

sys.path.append('../../experiment_setup/python')
from rawread import rawread
from digitizeHelper import interpolate_crossing
from helper import to_bool

TOOL="hspice"

VAR_COUNT=5
EXPORT_IDX=[]
EXPORT_SKIP=1
DATA_NAMES=['','']
VAR_NAMES=['','IN','O3','O4','O5']
VAR_COLOR=['','y','g','r','b']
VTH_OUT=0.6
VTH_IN=0.6

IN_IDX=VAR_COUNT-2
OUT_IDX=VAR_COUNT-1

FIG_FOLDER=None
SPICE_FOLDER=None
SPECTRE_FOLDER=None
DATA_FOLDER=None

MIN_VALUE_BINARY_SEARCH = int(0)
MAX_VALUE_BINARY_SEARCH = int(1.5e9)
MAX_ACCURACY_OUT = 0.001
MAX_ACCURACY_IN = 0.001
STOP_VALUE = 400e6
CALCULATE_INVOLUTION = True

CELL_NAME=None

DEBUG_LVL=3

DERIV_STEP_SIZE=10
DELTA_TIME=1e-13
SCALE_SIGNAL=1e4

VTH=0.565593
VSUPP=0.8 # TODO: When using other technology, move to config file

CONF_FILE_NAME = ''

colorUp = "#0F1DB7"
colorDown = "#067702"
colorComp = "#AB6304"

def print_info(msg):
	print('[INFO]: ' + msg)

def print_error(msg):
	print('[ERROR]: ' + msg)

def print_debug(msg, lvl):
	if (lvl >= DEBUG_LVL):
		print('[DEBUG] [LVL ' + str(lvl) + ']: ' + msg)

def interpolate_crossing(x_curr, x_prev, y_curr, y_prev, v_th):
		return ((x_curr - x_prev) / (y_prev - y_curr)) * (y_prev - v_th) + x_prev



def split_str(seq, length):
	return [float(seq[i:i+length]) for i in range(0, len(seq), length)]

def read_file (filename, var_cnt):

	if TOOL=="spectre":
		return read_spectre(filename, var_cnt)
	else:
		return read_hspice(filename, var_cnt)

def clear_var_names(var_names: list()) -> list():
	var_names_cleared = list()
	for var_name in var_names:
		var_names_cleared.append(''.join(e for e in var_name if e.isalnum()).lower())
		
	return var_names_cleared

def read_spectre(filename, var_cnt):

	# print("Filename: ", filename)

	sim, structure = rawread(filename)

	data = []
	var_names = structure[0]['varnames']

	# We need to adapt the var_names and the DATA_NAMES, such that they are all lower-case and without special chars...


	var_names_cleared = clear_var_names(var_names)
	data_names_cleared = clear_var_names(DATA_NAMES)
	
	for i in range(var_cnt):
		data.append([])

	for line in sim[0]:
		data[0].append(line[0])
		for idx in range(1, var_cnt):
			data[idx].append(line[var_names_cleared.index(data_names_cleared[idx])])

	
	# print("Data names")
	# idx = 0
	# for var_name in data_names_cleared:
	# 	print(idx, var_name)
	# 	idx = idx + 1

	# print("Var names")
	# idx = 0
	# for var_name in var_names_cleared:
	# 	print(idx, var_name)
	# 	idx = idx + 1
	# exit()
			
	min_len = len(data[0])

	# determine length of shortest array
	for i in range(len(data)):
		if (len(data[i]) < min_len):
			min_len = len(data[i])

	# set each array to same length
	for i in range(len(data)):
		data[i] = data[i][:min_len]
	   
	return data
	
def read_hspice(filename, var_cnt):
	
	data=[]

	for i in range(var_cnt):
		data.append([])

	with open(filename, 'r') as f:
		lines = f.readlines()
	
	# cut first lines, unfortunately not fixed amount, so try splitting on first,
	# if exception thrown remove line
	while(1):
		try:
			field_count = lines[0][:-1].count(".")
			field_length = len(lines[0][:-1])/field_count
			elements = split_str(lines[0][:-1],field_length)
			break
		except:
			lines=lines[1:]

	index=0

	# seperate values in file and move them to their corresponding arrays
	for i in lines:
		field_count = i.count(".")
		field_length=len(i[:-1])/field_count
		elements = split_str(i[:-1],field_length)
	
		for k in elements:
			data[index].append(k)
			index = ((index+1)%var_cnt)

	min_len = len(data[0])

	# determine length of shortest array
	for i in range(var_cnt):
		if (len(data[i]) < min_len):
			min_len = len(data[i])

	# set each array to same length
	for i in range(var_cnt):
		data[i] = data[i][:min_len]

	return data

## Reads the configuration file and initializes the global variables and the settings for up and down waveform
# 
# @param conf_file: Name of the configuration file
#
# @return 
def read_config (conf_file):

	global IN_IDX
	global OUT_IDX
	global VAR_COUNT
	global DATA_NAMES
	global VAR_NAMES
	global VAR_COLOR
	global EXPORT_IDX
	global EXPORT_SKIP
	global VTH_OUT
	global VTH_IN
	global TOOL

	global SPICE_FOLDER
	global SPECTRE_FOLDER

	global CELL_NAME

	global MIN_VALUE_BINARY_SEARCH
	global MAX_VALUE_BINARY_SEARCH
	global MAX_ACCURACY_OUT
	global MAX_ACCURACY_IN

	global STOP_VALUE

	global CALCULATE_INVOLUTION

	params_array = []

	try:
		f = open(conf_file,'r')
	except:
		print_error("config file '" + conf_file + "' could not be opened\n")
		return []

	lines = f.readlines()

	for i in lines:
		if i[0] == '#':
			continue

		ele = i[:-1].split(' ')

		# 'io' defines idx of input and output signal
		if ele[0] == 'io':
			IN_IDX = int(ele[1])
			OUT_IDX = int(ele[2])
			print_debug("IN_IDX: %d   OUT_IDX: %d"%(IN_IDX,OUT_IDX), 2)
			continue

		# 'c' defines the amount of signals
		if ele[0] == 'c':
			VAR_COUNT = int(ele[1])
			print_debug("VAR_COUNT: " + str(VAR_COUNT), 2)
			continue

		# 'o' defines the desired order of the signals in the internal data structure
		# only reasonable with tool spectre
		if ele[0] == 'o':
			DATA_NAMES = [''] + ele[1:]
			print_debug("DATA_NAMES: " + str(DATA_NAMES), 2)
			continue
		
		# 'd' defines the description of the signals in pictures
		if ele[0] == 'd':
			if len(ele) == VAR_COUNT:
				VAR_NAMES = [''] + ele[1:]
			else:
				# new possibility to also specify the name of index 0
				VAR_NAMES = ele[1:]

			print_debug("VAR_NAMES: " + str(VAR_NAMES), 2)
			continue

		# 'color' defines the colors of the signals in pictures
		if ele[0] == 'color':
			VAR_COLOR = [''] + ele[1:]
			print_debug("VAR_COLOR: " + str(VAR_COLOR), 2)
			continue

		# 'e' defines which signals shall be exported
		# note that index zero is exported automatically
		if ele[0] == 'e':
			print_array = [ int(j) for j in ele[1:] ]
			EXPORT_IDX = [0] + print_array
			print_debug("EXPORT_IDX: " + str(EXPORT_IDX), 2)
			continue

		# 'skip' defines that every skip th line is exported
		# default value is one
		if ele[0] == 'skip':
			print_array = [ int(j) for j in ele[1:] ]
			EXPORT_SKIP = int(ele[1])
			print_debug("EXPORT_SKIP: " + str(EXPORT_SKIP), 2)
			continue
		
		# 'vth_out' defines the desired output threshold voltage
		if ele[0] == 'vth_out':
			VTH_OUT = float(ele[1])
			print_debug("VTH_OUT " + str(VTH_OUT), 2)
			continue

		# 'vth_out' defines the desired output threshold voltage
		if ele[0] == 'vth_in':
			VTH_IN = float(ele[1])
			print_debug("VTH_IN " + str(VTH_IN), 2)
			continue		
		
		# 'tool' defines which tool shall be used for simulation
		if ele[0] == 'tool':
			if ele[1] == "spectre":
				TOOL = "spectre"
				SPICE_FOLDER = SPECTRE_FOLDER
			else:
				TOOL = "hspice"
				SPECTRE_FOLDER = SPICE_FOLDER

			print_debug("TOOL " + str(TOOL), 2)
			continue
			
		if ele[0] == 'cellName':
			CELL_NAME = ele[1]
			continue

		if ele[0] == 'min':
			MIN_VALUE_BINARY_SEARCH = int(ele[1])
			continue

		if ele[0] == 'max':
			MAX_VALUE_BINARY_SEARCH = int(ele[1])
			continue

		if ele[0] == 'stop':
			STOP_VALUE = int(ele[1])
			continue
		
		if ele[0] == 'maxaccuracyout':
			MAX_ACCURACY_OUT = float(ele[1])
			continue
		
		if ele[0] == 'maxaccuracyin':
			MAX_ACCURACY_IN = float(ele[1])

			continue

		if ele[0] == 'calcinvolution':
			CALCULATE_INVOLUTION = to_bool(ele[1])
			continue
	
		sim_params = dict()
		sim_params['circuitFolder'] = i.split(' ')[0]
		sim_params['tempFile'] = os.path.join(sim_params['circuitFolder'], i.split(' ')[1])
		sim_params['startName'] = i.split(' ')[2]
		sim_params['startVal'] = int(i.split(' ')[3])
		sim_params['stopVal'] = int(i.split(' ')[4])
		sim_params['stepVal'] = int(i.split(' ')[5])

		# defines pulse width T1 for three transition input
		if len(i.split(' ')) > 6 and i.split(' ')[7]!='':
			sim_params['t1'] = [int(i.split(' ')[6]), int(i.split(' ')[7]),
							   int(i.split(' ')[8])]
			print_debug("t1: " + str(sim_params['t1']), 2)

		params_array.append(sim_params)

	if params_array == []:
		print_error('file ' + conf_file + ' did not contain data')

	return params_array


def export_to_dat(print_data, file_name, skip=1, force_all=False):

	text = ''
	max_len = max([len(i) for i in print_data])


	for i in range(max_len):
		if i%skip > 0:
			continue
		if (EXPORT_IDX == []) or force_all:
			for j in range(len(print_data)):
				if j < (len(print_data) -1):
					if i >= len(print_data[j]):
						text += '%s;'%print_data[j][-1]
					else:
						text += '%s;'%print_data[j][i]
				else:
					if i >= len(print_data[j]):
						text += '%s\n '%print_data[j][-1]
					else:
						text += '%s\n'%print_data[j][i]    
		else:
			for j in range(len(EXPORT_IDX)):
				if j < (len(EXPORT_IDX) -1):
					if i >= len(print_data[EXPORT_IDX[j]]):
						text += '%s;'%print_data[EXPORT_IDX[j]][-1]
					else:
						text += '%s;'%print_data[EXPORT_IDX[j]][i]
				else:
					if i >= len(print_data[j]):
						text += '%s\n '%print_data[EXPORT_IDX[j]][-1]
					else:
						text += '%s\n'%print_data[EXPORT_IDX[j]][i]                    

	f_out = open (build_path(DATA_FOLDER, file_name), 'w')
	f_out.write(text[:-1])
	f_out.close()


## Get a list of indices where a trace is crossing a threshold
#
# @param data A list containing the trace for which we want to get the crossing indices
# @param vth The threshold voltage that we want to check
#
# @return A list containing the indices where the threshold is crossed
def get_crossing_idx (data: list, vth: float) -> list:

	UP=0
	DOWN=1

	cross_idx=[]

	# Determine mode with which to start
	if data[0] < vth:
		mode = UP
	else:
		mode = DOWN

	# Go over the trace
	for i in range(2,len(data)):
		# We check the last three values, to make sure that it is a proper crossing and not just an outlier
		if mode == UP and (data[i-2] > vth) and (data[i-1] > vth) and (data[i] > vth):
			cross_idx.append(i-2)
			mode=DOWN
		elif mode == DOWN and (data[i-2] < vth) and (data[i-1] < vth) and (data[i] < vth):
			cross_idx.append(i-2)
			mode=UP

	return cross_idx


## Gets the crossing of an up and down trace at the input, based on the corresponding output traces
#
# @param trace1 	A list containing the y-values of trace 1
# @param time1 		A list containing the x-values of trace 1
# @param idx1 		The idx where the corresponding output trace reaches maximum / minimum
# @param trace2 	A list containing the y-values of trace 2
# @param time2 		A list containing the x-values of trace 2
# @param idx2 		The index where the corresponding output trace reaches maximum / minimum
#
# @details	The basic idea for finding the crossing is to go back in time on the two input signals 
# 			as long as the distance between the two signals decreases.
#
# @return 	A tuple containing the indices where trace 1 and trace 2 cross, 
# 			the value at the crossing (\f$V_{th}^{in}\f$) and the 
# 			pure delay (\f$\delta_{min}\f$) between input crossing and the time the output traces are touching
def get_crossing_from_start_backwards_vthdmin(trace1: list, time1: list, idx1: int, trace2: list, time2: list, idx2: int) -> Tuple[int, int, float, float]:
	# Time where the output traces touch
	time_ex = time1[idx1]
	# The current distance between the input signals
	distance = abs(trace1[idx1] - trace2[idx2])

	# Go back at the signal with the higher time
	if (time1[idx1-1] > time2[idx2-1]):
		idx1 -= 1
	else:
		idx2 -= 1
	
	# Go back as long as the distance between the two signals gets smaller
	while abs(trace1[idx1] - trace2[idx2]) < distance:
		distance = abs(trace1[idx1] - trace2[idx2])
		
		# Go back on the signal with the higher time
		if (time1[idx1-1] >time2[idx2-1]):
			idx1 -= 1
		else:
			idx2 -= 1

	# Line for trace 1: y1 = slope1 * x1 + d1
	# Calculate slope for trace 1: (y2 - y1) / (x2 - x1)
	slope1 = (trace1[idx1+1]-trace1[idx1])/(time1[idx1+1]-time1[idx1])	
	d1 = trace1[idx1] - slope1*time1[idx1]

	slope2 = (trace2[idx2+1]-trace2[idx2])/(time2[idx2+1]-time2[idx2])
	d2 = trace2[idx2] - slope2*time2[idx2]

	time_cross = (d2-d1)/(slope1-slope2)
	dmin = time_ex - time_cross
	# Now calculate the y value
	vth_in = slope1*time_cross + d1
	
	return (idx1, idx2, vth_in, dmin, time_cross)


def data_to_file(data, file_name):

	text = ''
	
	for i in range(len(data[0])):
		for j in range(len(data)):
			if j < (len(data) -1):
				text += '%s '%data[j][i]
			else:
				text += '%s\n'%data[j][i]
		
	f = open (DATA_FOLDER + file_name, 'w')
	f.write(text[:-1])
	f.close()

## Runs a SPICE simulation with the globally specified TOOL for the simulation parameters
#
# @parameter sim_params A dictionary containing the simulation parameters
def run_spice (sim_params: dict) -> None:   
	tmp_temp_file = sim_params['startName'] + '_tmp' + str(int(random.random()*1e6)) + '.sp'
	tmp_temp_file_2 = sim_params['startName'] + '_tmp2' + str(int(random.random()*1e6)) + '.sp'
	tmp_temp_file_3 = sim_params['startName'] + '_tmp3' + str(int(random.random()*1e6)) + '.sp'

	stop_value = str(int(sim_params['startVal'] + STOP_VALUE)) + "as"

	if sim_params['startName'][-1] == 'u':
		command = "sed 's/<sed>base<sed>/0V/g' " + sim_params['tempFile'] + \
			" | sed 's/<sed>stop<sed>/{stop}/g' " \
			" | sed 's/<sed>peak<sed>/vsrc/g' > " + tmp_temp_file
	else:
		command = "sed 's/<sed>base<sed>/vsrc/g' " + sim_params['tempFile'] + \
			" | sed 's/<sed>stop<sed>/{stop}/g' " \
			" | sed 's/<sed>peak<sed>/0V/g' > " + tmp_temp_file

	command = command.format(stop = stop_value)

	code = subprocess.call(command, shell=True)
	if (code != 0):
		print_error("sed failed")
		return

	for i in range(sim_params['startVal'],sim_params['stopVal'],sim_params['stepVal']):

		command = "sed 's/<sed>random<sed>/" + str(random.randint(0,360)) + "/g' " + tmp_temp_file + " > " + \
			tmp_temp_file_2

		code = subprocess.call(command, shell=True)
		if (code != 0):
			print_error("sed failed")
			continue

		print("\n")
		print_info("starting simulation for pulse width " + str(i))

		if 't1' in sim_params:
			# If 't1' is specified, we can also iterate over the slope of the transitions
			command = "sed 's/<sed>pw<sed>/" + str(i) + "/g' " + tmp_temp_file_2 + " > " + \
					  tmp_temp_file_3

			code = subprocess.call(command, shell=True)
			if (code != 0):
				print_error("sed failed")
				continue

			for slope in range (sim_params['t1'][0], sim_params['t1'][1], sim_params['t1'][2]):
				name = sim_params['startName'] + "%020d" % i + "_%020d"%slope
				if TOOL== "spectre":
					spicename = SPECTRE_FOLDER + name
				else:
					spicename = SPICE_FOLDER + name
				print_info("doing slope " + str(slope))
				command = "sed 's/<sed>slope<sed>/" + str(slope) + "/g' " + \
						  tmp_temp_file_3 + " > " + spicename + ".sp"

				code = subprocess.call(command, shell=True)
				if (code != 0):
					print_error("sed failed")
					return

				if TOOL == "spectre":
					command = "spectre +spp -format nutbin -outdir " + SPECTRE_FOLDER[:-1] + " =log " + spicename + ".log " + spicename + ".sp" + " -I" + sim_params['circuitFolder']
				else:
					command = "hspice64 -i " + spicename + " -o " + spicename 

				print(command)
		
				code = subprocess.call(command, shell=True)
				if (code != 0):
					
					if TOOL == "spectre":
						print_error("spectre failed")
					else:
						print_error("hspice64 failed")
				
			os.remove(tmp_temp_file_3)

		else:
			name = sim_params['startName'] + "%020d" % i
			if TOOL== "spectre":
				spicename = SPECTRE_FOLDER + name
			else:
				spicename = SPICE_FOLDER + name
			command = "sed 's/<sed>pw<sed>/" + str(i) + "/g' " + tmp_temp_file_2 + " > " + \
					  spicename + ".sp"

			code = subprocess.call(command, shell=True)
			if (code != 0):
				print_error("sed failed")
				continue

			if TOOL == "spectre":
				command = "spectre +spp -format nutbin -outdir " + SPECTRE_FOLDER[:-1] + " =log " + spicename + ".log " + spicename + ".sp"  + " -I" + sim_params['circuitFolder']
			else:
				command = "hspice64 -i " + spicename + " -o " + spicename 
		
			code = subprocess.call(command, shell=True)
			if (code != 0):                
				if TOOL == "spectre":
					print_error("spectre failed")
				else:
					print_error("hspice64 failed")

	os.remove(tmp_temp_file)
	os.remove(tmp_temp_file_2)

	
def generate_involution_analysis(start_name, data_delta, data_delay):

	print_info("starting involution analysis for " + start_name)

	styles = ['bo-','go-','r--','m--','c--','k--']
	labels = ['u','d']
	
	# with open(DATA_FOLDER+ start_name + 'dataDelta.dat','rb') as f:
	# 	data_delta = pickle.load(f)

	# with open(DATA_FOLDER+ start_name + 'dataDelay.dat','rb') as f:
	# 	data_delay = pickle.load(f)
		
	max_x = max(max(data_delta[0]),max(data_delta[1]))
	max_y = max(max(data_delay[0]),max(data_delay[1]))
	min_y = min(data_delay[0]+data_delay[1])
	d_min = max(data_delay[0][0], data_delay[1][0])
	low_boundary = d_min*1.5
	
	
	plt.figure()
	
	plt.plot([-low_boundary,0],[low_boundary,0],'r')
	plt.plot([-low_boundary, max_x*1.1],[0,0],'k')
	plt.plot([0,0],[0,max_y*1.1],'k')

	for idx in range(2):
		plt.plot(data_delta[idx],data_delay[idx],styles[idx], label=labels[idx], markersize=2.2)
		
	for idx in range(2):
		plt.plot([-data_delay[idx][0],-data_delay[idx][0]+max_y], [data_delay[idx][0],data_delay[idx][0]+max_y], 'r-')
		
	plt.xlim([-low_boundary, max_x*1.1])
	plt.ylim([min_y*1.4, max_y*1.1])
	plt.legend(prop={'size':8}, loc=4)
	plt.xlabel('$T$ [s]')
	plt.ylabel('delay [s]')
	plt.grid()
	plt.savefig(build_path(FIG_FOLDER, start_name + "%s_%s_involution.png"%(VAR_NAMES[IN_IDX], VAR_NAMES[OUT_IDX])))

	plt.xlim([-2*low_boundary, 5*low_boundary])
	plt.ylim([0,7*low_boundary])
	plt.savefig(build_path(FIG_FOLDER, start_name + "%s_%s_involution_zoom.png"%(VAR_NAMES[IN_IDX], VAR_NAMES[OUT_IDX])))

	plt.xlim([-2*low_boundary, max_x/10])
	plt.ylim([0, 2*low_boundary + max_y/10])
	plt.savefig(build_path(FIG_FOLDER, start_name + "%s_%s_involution_zoom2.png"%(VAR_NAMES[IN_IDX], VAR_NAMES[OUT_IDX])))
	
	# Find the last x value for up and down waveform where the value is off for at most x% (this should also allow as to depict overshooting)
	right_x = float('-inf')
	for i in range(2):
		end_value = data_delay[i][-1]
		for idx, e in reversed(list(enumerate(data_delay[i]))):
			# print(idx, e, end_value, data_delay[i][idx], abs((e - end_value) / end_value))
			if abs((e - end_value) / end_value) > 0.02:
				if data_delta[i][idx] > right_x:
					right_x = data_delta[i][idx]
				break

	right_x = right_x * 1.5
	top_y = max_y * 1.2	

	# We want to have a plot where we x from min(-dmin) to 4*where the y value is within 95% of the maximum value
	left_x = min(min(data_delta[0]), min(data_delta[1]))
	left_x = left_x - right_x * 0.1
	bottom_y = min(min(data_delay[0]), min(data_delay[1]))
	bottom_y = bottom_y - top_y * 0.1


	plt.xlim([left_x, right_x])
	plt.ylim([bottom_y, top_y])
	plt.savefig(build_path(FIG_FOLDER, start_name + "%s_%s_involution_zoom3.png"%(VAR_NAMES[IN_IDX], VAR_NAMES[OUT_IDX])))

	plt.close()
	
	plt.figure()

	deriv = [[],[]]
	
	for dir_idx in range(2):

		for idx in range(1,len(data_delta[dir_idx])):
			deriv[dir_idx].append( (data_delay[dir_idx][idx]-data_delay[dir_idx][idx-1]) /
						  (data_delta[dir_idx][idx]-data_delta[dir_idx][idx-1]))
		plt.plot(data_delta[dir_idx][1:],deriv[dir_idx],styles[dir_idx], label=labels[dir_idx], markersize=2.2)

	plt.legend(prop={'size':8}, loc=4)
	plt.xlabel('$T$ [s]')
	plt.ylabel('deriv [s/s]')
	plt.grid()
	plt.savefig(build_path(FIG_FOLDER, start_name + "%s_%s_involution_deriv.png"%(VAR_NAMES[IN_IDX], VAR_NAMES[OUT_IDX])))
	plt.close()

	
	plt.figure()

	for dir_idx in range(2):
		plt.plot(data_delta[dir_idx][1:],deriv[dir_idx],styles[dir_idx], label=labels[dir_idx], markersize=2.2)
		tmp = [1/value for value in deriv[dir_idx] if value > 0.01]

		plt.plot(data_delta[dir_idx][:len(tmp)],tmp,styles[dir_idx], label=labels[dir_idx], markersize=2.2)
	
	plt.legend(prop={'size':8}, loc=4)
	plt.xlabel('$T$ [s]')
	plt.ylabel('deriv and 1/deriv')
	plt.ylim([0,1.2])
	plt.grid()
	plt.savefig(build_path(FIG_FOLDER, start_name + "%s_%s_involution_deriv2.png"%(VAR_NAMES[IN_IDX], VAR_NAMES[OUT_IDX])))
	plt.close()

def run_additional_simulations(sim_params: dict, min_value : int, max_value: int, simulations : int):
	current_value = max_value
	for sim_nr in range(simulations):
		print("SimNr: ", sim_nr, "current_value: ", current_value, min_value, max_value)

		sim_params['startVal'] = current_value
		sim_params['stopVal'] = current_value+1
		sim_params['stepVal'] = 1
			
		if TOOL=="spectre":
			file_name = SPECTRE_FOLDER + sim_params['startName'] + "%020d.raw" % current_value
		else:
			file_name = SPICE_FOLDER + sim_params['startName'] + "%020d.tr0" % current_value
		
		if not os.path.isfile(file_name):
			run_spice(sim_params)
		else:
			print_info("file %s already exists"%file_name)

		current_value = int((min_value + current_value) / 2)

		if current_value == min_value:
			break

def run_complete_simulations_binary_search(sim_params: dict, bounds: list, accuracy: float, vth_out: float) -> int:	
	best_fit = None
	best_distance = None

	first_bound = True

	while len(bounds) > 0:
		bound = bounds.pop()
		min_value = bound[0]
		max_value = bound[1]

		if first_bound:			
			# we start with the max_value, and check if we need to increase the pulse width.
			# If this is the case, we need to increase the max value in the configuration
			current_value = int(max_value)
		else:
			current_value = int((min_value + max_value) / 2)

		distance = VSUPP

		negative_distance = None
		negative_distance_value = None
		positive_distance = None
		positive_distance_value = None

		is_falling = False
		is_rising = False

		while abs(distance) > accuracy and (max_value - min_value) > 1:

			sim_params['startVal'] = current_value
			sim_params['stopVal'] = current_value+1
			sim_params['stepVal'] = 1
				
			if TOOL=="spectre":
				file_name = SPECTRE_FOLDER + sim_params['startName'] + "%020d.raw" % current_value
			else:
				file_name = SPICE_FOLDER + sim_params['startName'] + "%020d.tr0" % current_value
			
			if not os.path.isfile(file_name):
				run_spice(sim_params)
			else:
				print_info("file %s already exists"%file_name)

			
			data = read_file(file_name, VAR_COUNT)

			new_min_value = min_value
			new_max_value = max_value

			if data[OUT_IDX][0] > vth_out:
				is_falling = True
				ex_value = min(data[OUT_IDX])

				if ex_value < vth_out:
					# Pulse too wide
					new_max_value = current_value
					next_value = (min_value + current_value) / 2
				else:
					# Pulse too short
					assert(not first_bound)
					new_min_value = current_value
					next_value = (max_value + current_value) / 2

			else:
				is_rising = True
				ex_value = max(data[OUT_IDX])

				if ex_value < vth_out:
					# Pulse too short
					assert(not first_bound) 
					new_min_value = current_value
					next_value = (max_value + current_value) / 2
				else:
					# Pulse too wide
					new_max_value = current_value
					next_value = (min_value + current_value) / 2

			assert(not (is_falling and is_rising))
			first_bound = False

			new_distance = ex_value - vth_out 

			if new_distance < 0:
				# print("Neg: ", negative_distance, new_distance, is_falling, is_rising)
				if not (negative_distance is None or new_distance >= negative_distance - 1e-2):
					bounds.append((next_value, new_max_value))
					print(bounds)
				# What shall we do if this assertion fails? Is it some kind of non-linearity
				negative_distance = new_distance
				negative_distance_value = current_value


			if new_distance > 0:
				# print("Pos: ", positive_distance, new_distance, is_falling, is_rising)
				if not (positive_distance is None or new_distance <= positive_distance + 1e-2):
					bounds.append((new_min_value, next_value))
					print(bounds)
				# What shall we do if this assertion fails?
				positive_distance = new_distance
				positive_distance_value = current_value

			min_value = new_min_value
			max_value = new_max_value

			if best_distance is None or abs(new_distance) < abs(best_distance):
				best_distance = new_distance 
				best_fit = current_value

			current_value = next_value
	
			# print("Signal name in: ", DATA_NAMES[IN_IDX])
			# print("Signal name out: ", DATA_NAMES[OUT_IDX])
			print(min_value, current_value, max_value, "Old distance: ", distance, "New distance: ", new_distance, "distances:", negative_distance, negative_distance_value, positive_distance, positive_distance_value, "bounds: ", bounds)

			current_value = int(current_value)
			distance = new_distance

		if abs(distance) <= accuracy:			
			return best_fit

	return best_fit



def extract_vthout_dmin(paramsArray, timeExData):

	print_info("Determining V_TH^OUT for V_TH^IN = %s"%VTH_IN)

	fileList = os.listdir(SPICE_FOLDER)
	fileList.sort()

	bestDiff = 1e9
	
	for idx0 in range(len(timeExData[0][0])):
		bestVal = 1e9
		bestParams = []

		# not optimal!!
		if (timeExData[0][1][idx0] < 0.24) or (timeExData[0][1][idx0] > 0.27):
			continue

#        print_info("starting file %s"%timeExData[0][2][idx0])
		
		#find optimal extreme value fit first
		for idx1 in range(len(timeExData[1][0])):

			# difference of extreme values
			curVal = abs(timeExData[0][1][idx0] - timeExData[1][1][idx1])
#            print_info("file %s: deviation %s"%(timeExData[1][2][idx1], curVal))
			
			if curVal < bestVal:
				bestVal = curVal
				dMin = abs(timeExData[0][0][idx0] + timeExData[1][0][idx1]) / 2
				vthOut = abs(timeExData[0][1][idx0] + timeExData[1][1][idx1]) / 2
				bestParams = [idx0, idx1, dMin, vthOut]

		diff = abs(timeExData[1][0][bestParams[1]] - timeExData[0][0][bestParams[0]])
		print_info("Best diff dmin for file %s was file %s with diff=%s and vth_out=%s"%(
			timeExData[0][2][bestParams[0]], timeExData[1][2][bestParams[1]],\
			diff,bestParams[-1]) )
		
		if diff < bestDiff:
			bestDiff = diff
			optParams = bestParams

	bestParams = optParams
	idx0 = optParams[0]
	idx1 = optParams[1]
	print_info("Best overall fit between files %s and %s with diff dMin = %s and Vth_out=%s"%(
		timeExData[0][2][idx0], timeExData[1][2][idx1],\
		 bestParams[-2],bestParams[-1]) )
		
	dMin = bestParams[-2]
	vthOut = bestParams[-1]
	optIdx = bestParams[:2]
	
	plt.figure()

	diff = abs(timeExData[1][4][optIdx[1]] - timeExData[0][4][optIdx[0]])
	if (timeExData[1][4][optIdx[1]] > timeExData[0][4][optIdx[0]]):
		data = read_file(SPICE_FOLDER+timeExData[1][2][optIdx[1]], VAR_COUNT)
		tmpTime = [i-data[0][diff] for i in data[0][diff:]]
		data2 = read_file(SPICE_FOLDER+timeExData[0][2][optIdx[0]], VAR_COUNT)
	else:
		data = read_file(SPICE_FOLDER+timeExData[0][2][optIdx[0]], VAR_COUNT)
		tmpTime = [i-data[0][diff] for i in data[0][diff:]]
		data2 = read_file(SPICE_FOLDER+timeExData[1][2][optIdx[1]], VAR_COUNT)
		
	plt.plot(tmpTime, data[IN_IDX][diff:], 'b-', label='in up')
	plt.plot(tmpTime, data[OUT_IDX][diff:], 'g-', label='out up')
	plt.plot(data2[0], data2[IN_IDX], 'm-', label='in down')
	plt.plot(data2[0], data2[OUT_IDX], 'c-', label='out down')
		
	data_to_file([data2[0], data2[IN_IDX], data2[OUT_IDX], data[IN_IDX][diff:], data[OUT_IDX][diff:]],
				 paramsArray[0]['startName'][:-1] + 'VTH_OUT.dat')
		
		
	plt.plot([0,tmpTime[-1]],[VTH_IN, VTH_IN], 'k-', label='Vth_in')
	plt.plot([0,tmpTime[-1]],[vthOut, vthOut], 'k--', label='Vth_out')
	plt.grid()
	plt.title("VTH_OUT = %.5f, VTH_IN = %.5f, d_min = %s"%(vthOut, VTH_IN, dMin))
	plt.xlabel("time [s]")
	plt.ylabel("voltage [V]")
	plt.legend(prop={'size':8}, loc='lower right')
	plt.savefig(build_path(FIG_FOLDER, paramsArray[0]['startName'][:-1]+"involution_VTH_OUT.png"))
	plt.close()

	return [vthOut, dMin]


## Extracts \f$V_{th}^{in}\f$ and \f$\delta_{min}\f$ for \f$V_{th}^{out}\f$
#
# @param data 		A two-element list, containing the up waveforms and the input waveforms. 
# 					Each element contains another list with the different signals.
#					The first element is the time, and IN_IDX and OUT_IDX contain the waveforms
#					of the input and the output
# @param start_name Prefix for figures
#
# @return a tuple containing \f$V_{th}^{in}\f$ and \f$\delta_{min}\f$
def extract_vthin_dmin(data: list, start_name: str, vth_out: float) -> Tuple[float, float, Tuple[float, float], float]:

	# determine VTH_IN
	# is the point where the input curves cross when both output traces hit
	# vth_out at the same time
	
	dir_idx_up = 0
	dir_idx_down = 1

	# We need to check the first element.
	# If the waveform starts from > vth_out, we need to find the index with the minimum value
	# Else we need to find the index with the maximum value
	if data[dir_idx_up][OUT_IDX][0] > vth_out:
		ex_idx_up = data[dir_idx_up][OUT_IDX].index(min(data[dir_idx_up][OUT_IDX]))
	else:
		ex_idx_up = data[dir_idx_up][OUT_IDX].index(max(data[dir_idx_up][OUT_IDX]))

	if data[dir_idx_down][OUT_IDX][0] > vth_out:
		ex_idx_down = data[dir_idx_down][OUT_IDX].index(min(data[dir_idx_down][OUT_IDX]))
	else:
		ex_idx_down = data[dir_idx_down][OUT_IDX].index(max(data[dir_idx_down][OUT_IDX]))

	# Time difference between the minimum and maximum value of the up and down traces
	time_diff = data[dir_idx_up][0][ex_idx_up] - data[dir_idx_down][0][ex_idx_down]
	# We shift the time axis of the up trace, such that minimum / maximum are reached at the same time
	time_up = [i-time_diff for i in data[dir_idx_up][0]]
	
	(idx_up, idx_down, vth_in, d_min, crossing_time) = get_crossing_from_start_backwards_vthdmin(data[dir_idx_up][IN_IDX], time_up, ex_idx_up,
														 data[dir_idx_down][IN_IDX], data[dir_idx_down][0], ex_idx_down)

	# Plot up and down traces at input and output of the gate
	# Useful for manually checking if the calculation is reasonably accurate
	for length in [20, 100, None]:
		if length:
			time_diff = data[dir_idx_up][0][ex_idx_up] - data[dir_idx_down][0][ex_idx_down]
			time_up = [i-time_diff for i in data[dir_idx_up][0][idx_up-length:ex_idx_up+length]]
			trace_in_up = data[dir_idx_up][IN_IDX][idx_up-length:ex_idx_up+length]
			trace_out_up = data[dir_idx_up][OUT_IDX][idx_up-length:ex_idx_up+length]
			time_do = data[dir_idx_down][0][idx_down-length:ex_idx_down+length]
			trace_in_do = data[dir_idx_down][IN_IDX][idx_down-length:ex_idx_down+length]
			trace_out_do = data[dir_idx_down][OUT_IDX][idx_down-length:ex_idx_down+length]
		else:
			length = "complete"
			time_up = [i-time_diff for i in data[dir_idx_up][0]]
			trace_in_up = data[dir_idx_up][IN_IDX]
			trace_out_up = data[dir_idx_up][OUT_IDX]
			time_do = data[dir_idx_down][0]
			trace_in_do = data[dir_idx_down][IN_IDX]
			trace_out_do = data[dir_idx_down][OUT_IDX]

		plt.figure()
		plt.plot(time_up, trace_in_up, 'b-*', label='in up')
		plt.plot(time_up, trace_out_up, 'g-*', label='out up')
		plt.plot(time_do, trace_in_do, 'm-*', label='in down')
		plt.plot(time_do, trace_out_do, 'c-*', label='out down')
			
		plt.plot([time_up[0],time_up[-1]],[vth_in, vth_in], 'k-', label='Vth_in')
		plt.plot([time_up[0],time_up[-1]],[vth_out, vth_out], 'k--', label='Vth_out')
		plt.grid()
		plt.title("VTH_IN = %.5f, VTH_OUT = %.5f, d_min = %s"%(vth_in, vth_out, d_min))
		plt.xlabel("time [s]")
		plt.ylabel("voltage [V]")
		plt.legend(prop={'size':8}, loc='lower right')
		plt.savefig(build_path(FIG_FOLDER, start_name+"%s_%s_involution_%s_VTH_IN.png"%(VAR_NAMES[IN_IDX], VAR_NAMES[OUT_IDX], str(length))))
		plt.close()

	export_to_dat([['time_up']+time_up, ['in_up']+trace_in_up, ['out_up']+trace_out_up,
				   ['time_do']+time_do, ['in_do']+trace_in_do, ['out_do']+trace_out_do],
				   start_name+"vthInFitTraces_%d_%d.dat"%(IN_IDX, OUT_IDX), 10)

	return (vth_in, d_min, (idx_up, idx_down), crossing_time, time_diff)


## Calculates \f$\delta(T):\downarrow\f$ and \f$\delta(T):\uparrow\f$ and stores the result in dat files and plots figures
#
# @param params_array 	A list containg the parameters for up and down waveform simulation
# @param vth_in 		Threshold voltage at the input to use
# @param vth_out 		Threshold voltage at the output to use
# @param d_min			The delay between input threshold crossing and output threshold crossing
# @param deltas			A list containing the values for \f$\Delta^+\f$ and \f$\Delta^-\f$
def calculate_involution(params_array: list, vth_in: float, vth_out: float, d_min: float, deltas: list) -> Tuple[float, float]:

	data_delay = [[],[]]
	data_delta = [[],[]]

	file_list = os.listdir(SPICE_FOLDER)
	file_list.sort()

	# Calculate involution for up and down waveform
	for idx in range(2):
		sim_params = params_array[idx]

		start_name = sim_params['startName']

		# leftmost value
		data_delta[idx].append(-d_min - deltas[idx])
		data_delay[idx].append(d_min + deltas[idx])

		found = False

		# Go over all relevant trace files
		for file_name in file_list:

			if not file_name.startswith(start_name):
				continue

			if TOOL=='spectre':
				if not file_name.endswith('.raw'):
					continue
			else:
				if not file_name.endswith('.tr0'):
					continue
				
			print_info("processing file " + file_name)

			if TOOL=='spectre':
				data = read_file(SPECTRE_FOLDER+file_name, VAR_COUNT)
			else:
				data = read_file(SPICE_FOLDER+file_name, VAR_COUNT)

			# Check if the output waveform is up (idx == 0) or down (idx == 1)
			if idx == 0:
				# Up waveform at output
				assert(data[OUT_IDX][0] > VTH_OUT and data[OUT_IDX][-1] > VTH_OUT)
			elif idx == 1:
				# Down waveform at output
				assert(data[OUT_IDX][0] < VTH_OUT and data[OUT_IDX][-1] < VTH_OUT)				
			else:
				assert(False)

			# List of indices of threshold crossing on the input and output
			idx_in = get_crossing_idx(data[IN_IDX], vth_in)
			idx_out = get_crossing_idx(data[OUT_IDX], vth_out)

			# print("Indices: ", idx_in, idx_out)

			# We must at least cross the threshold once and then go back (for the output)
			if len(idx_out) < 2:
				assert(not found) # Once we find a pulse which is ok, larger pulses should be ok as well. If not, there might be a problem with the simulation duration
				continue
			
			# We must at least cross the threshold once (for the input)
			if len(idx_in) < 1:
				assert(not found) # Once we find a pulse which is ok, larger pulses should be ok as well. If not, there might be a problem with the simulation duration
				continue

			found = True
			
			time_out_last = interpolate_crossing(data[0][idx_out[-1]], data[0][idx_out[-1]-1],
										 data[OUT_IDX][idx_out[-1]], data[OUT_IDX][idx_out[-1]-1], vth_out)
			time_out_first = interpolate_crossing(data[0][idx_out[0]], data[0][idx_out[0]-1],
										 data[OUT_IDX][idx_out[0]], data[OUT_IDX][idx_out[0]-1], vth_out)
			time_in_last = interpolate_crossing(data[0][idx_in[-1]], data[0][idx_in[-1]-1],
											  data[IN_IDX][idx_in[-1]], data[IN_IDX][idx_in[-1]-1], vth_in)
			
			# TODO: Discuss this with Juergen why we use different times for the output crossing
			# Calculate T
			# print("T, \delta(T): ", time_in_last - time_out_first, time_out_last - time_in_last, file_name)
			data_delta[idx].append(time_in_last - time_out_first)
			# Calculate delta(T)
			data_delay[idx].append(time_out_last - time_in_last)

	file_name = params_array[0]['startName'][:-1]

	export_to_dat([data_delta[0],data_delay[0]], file_name +
				  '%s_%s_%s_%s_%s_delayFctUp.dat'%(VAR_NAMES[IN_IDX],
												VAR_NAMES[OUT_IDX],
												CELL_NAME,
												str(vth_in).replace('.',''),
												str(vth_out).replace('.','')))
	export_to_dat([data_delta[1],data_delay[1]], file_name +
				  '%s_%s_%s_%s_%s_delayFctDo.dat'%(VAR_NAMES[IN_IDX],
												VAR_NAMES[OUT_IDX],
												CELL_NAME,
												str(vth_in).replace('.',''),
												str(vth_out).replace('.','')))


	generate_involution_analysis(file_name, data_delta, data_delay)

	return data_delay[0][-1], data_delay[1][-1]


def calc_dinf(params_array: list, vth_in: float, vth_out: float) -> Tuple[float, float]: 
	dinfs = list()

	
	file_list = os.listdir(SPICE_FOLDER)
	file_list.sort(reverse=True)

	# Calculate involution for up and down waveform
	for idx in range(2):
		sim_params = params_array[idx]

		start_name = sim_params['startName']
		print("Start name: ", start_name)

		last_file = NoReturn
		# Go over all relevant trace files
		for file_name in file_list:

			if not file_name.startswith(start_name):
				continue			

			if TOOL=='spectre':
				if not file_name.endswith('.raw'):
					continue
			else:
				if not file_name.endswith('.tr0'):
					continue

			last_file = file_name
			break

		assert(last_file)		
		
		print_info("processing file " + last_file)

		if TOOL=='spectre':
			data = read_file(SPECTRE_FOLDER+last_file, VAR_COUNT)
		else:
			data = read_file(SPICE_FOLDER+last_file, VAR_COUNT)

		# Check if the output waveform is up (idx == 0) or down (idx == 1)
		if idx == 0:
			# Up waveform at output
			assert(data[OUT_IDX][0] > vth_out and data[OUT_IDX][-1] > vth_out)
		elif idx == 1:
			# Down waveform at output
			assert(data[OUT_IDX][0] < vth_out and data[OUT_IDX][-1] < vth_out)				
		else:
			assert(False)

		# List of indices of threshold crossing on the input and output
		idx_in = get_crossing_idx(data[IN_IDX], vth_in)
		idx_out = get_crossing_idx(data[OUT_IDX], vth_out)

		# print("Indices: ", idx_in, idx_out)

		# We must at least cross the threshold once and then go back (for the output)
		if len(idx_out) < 2:
			assert(not found) # Once we find a pulse which is ok, larger pulses should be ok as well. If not, there might be a problem with the simulation duration
			continue
		
		# We must at least cross the threshold once (for the input)
		if len(idx_in) < 1:
			assert(not found) # Once we find a pulse which is ok, larger pulses should be ok as well. If not, there might be a problem with the simulation duration
			continue

		found = True
		
		time_out_last = interpolate_crossing(data[0][idx_out[-1]], data[0][idx_out[-1]-1],
										data[OUT_IDX][idx_out[-1]], data[OUT_IDX][idx_out[-1]-1], vth_out)
		time_in_last = interpolate_crossing(data[0][idx_in[-1]], data[0][idx_in[-1]-1],
											data[IN_IDX][idx_in[-1]], data[IN_IDX][idx_in[-1]-1], vth_in)

		dinfs.append(time_out_last - time_in_last)

	assert(len(dinfs) == 2)
	return dinfs[0], dinfs[1]

## Generates the involution for the configuration in conf_file
#
# @param circuit_path 	The path to the root characterization folder for a circuit
# @param conf_file 		The name of the configuration file
# @param sub_folder 	Optional parameter in case a subfolder should be used to store the results (data and figure)
#
# @return 				A tuple consisting of \f$V_{th}^{in}, V_{th}^{out}, \delta_{min}\f$
def generate_involution_fully_automatic(circuit_path: str, conf_file: str, sub_folder: str = None) -> Tuple[float, float, float]:
	global DATA_FOLDER
	global FIG_FOLDER
	global SPICE_FOLDER
	global SPECTRE_FOLDER

	DATA_FOLDER = os.path.join(circuit_path, 'data/')
	FIG_FOLDER = os.path.join(circuit_path, 'figures/')
	SPICE_FOLDER = os.path.join(circuit_path, 'hspice/')
	SPECTRE_FOLDER = os.path.join(circuit_path, 'spectre/')

	if sub_folder: 
		DATA_FOLDER = os.path.join(DATA_FOLDER, sub_folder)
		FIG_FOLDER = os.path.join(FIG_FOLDER, sub_folder)

	if not os.path.exists(DATA_FOLDER):
		os.makedirs(DATA_FOLDER)
	if not os.path.exists(FIG_FOLDER):
		os.makedirs(FIG_FOLDER)
	if not os.path.exists(SPICE_FOLDER):
		os.makedirs(SPICE_FOLDER)
	if not os.path.exists(SPECTRE_FOLDER):
		os.makedirs(SPECTRE_FOLDER)

	print_info('starting automatic characterization for config file ' + conf_file + '\n')

	params_array = read_config(conf_file)
	if params_array == []:
		assert(False)

	# We need exactly one configuration for up waveforms and one for down waveforms
	assert(len(params_array) == 2)

	# We might need to swap the two elements in params_array, 
	# to ensure that the up waveform at the output is always at
	# params_array[0] and the down waveform is at params_array[1]

	# We perform this check by sending a very long pulse through the circuit and analyse the waveform
	params_array = check_params_array(params_array, MAX_VALUE_BINARY_SEARCH)

	# return None, None, None, []

	bwd = VTH_OUT > 0 and VTH_IN < 0
	fwd = VTH_OUT < 0 and VTH_IN > 0
	cidm = VTH_OUT > 0 and VTH_IN > 0
	if bwd:
		return bwd_char(params_array)		
	elif fwd:
		return fwd_char(params_array)
	elif cidm:
		return cidm_char(params_array)
	else:
		assert(False)

def fwd_char(params_array):
	data = [[],[]]
	vth_in = VTH_IN
	vth_out = None
	d_min = None
	inverting = True # TODO: Detect if gate is inverting or not
	accuracy = MAX_ACCURACY_IN

	# General idea: Start with vth_out = 0.4
	# Check the resulting vth_in
	# Depending on the type of the gate and the desired vth_in, 
	# increase / decrease vth_out binary search like until we match the desired vth_in with a certain accuracy

	vth_out_min = 0
	vth_out_max = VSUPP
	vth_out_current = (vth_out_min + vth_out_max) / 2


	while True:
		print("Try vth_out: ", vth_out_current)
		for idx in range(2):

			sim_params = params_array[idx]
			best_fit = run_complete_simulations_binary_search(sim_params, [(MIN_VALUE_BINARY_SEARCH, MAX_VALUE_BINARY_SEARCH)], MAX_ACCURACY_OUT, vth_out_current)
			if TOOL=="spectre":
				file_name = SPECTRE_FOLDER + sim_params['startName'] + "%020d.raw" % best_fit
			else:
				file_name = SPICE_FOLDER + sim_params['startName'] + "%020d.tr0" % best_fit
				
			data[idx] = read_file(file_name, VAR_COUNT)

		(vth_in_current, d_min, _, _, _) = extract_vthin_dmin(data, sim_params['startName'][:-1], vth_out_current)

		deviation = (vth_in_current - vth_in)
		print("vthin current: ", vth_in_current, "Vthin target: ", vth_in, "deviation: ", deviation, "vth_out_current:", vth_out_current)			

		if abs(deviation) < accuracy:
			break	
		
		increase_vth_out = True
		if vth_in_current < vth_in:
			increase_vth_out = not inverting
		else:
			increase_vth_out = inverting

		if increase_vth_out:			
			vth_out_min = vth_out_current
		else:
			vth_out_max = vth_out_current
		vth_out_current = (vth_out_min + vth_out_max) / 2
			

	vth_in = vth_in_current
	vth_out = vth_out_current
	
	# Now determine the involution according to plain IDM
	dinf_up = None
	dinf_do = None
	if CALCULATE_INVOLUTION:
		dinf_up, dinf_do = calculate_involution(params_array, vth_in, vth_out, d_min, [0, 0])
	else:
		dinf_up, dinf_do = calc_dinf(params_array, vth_in, vth_out)
		

	write_results(params_array, vth_in, vth_out, d_min, [0, 0], dinf_up, dinf_do)

	
	return (vth_in, vth_out, d_min, None)


def cidm_char(params_array):
	data = [[],[]]

	# We need to determine \dmin

	# carry out SPICE simulations
	# Index 0 = Up Waveform
	# Index 1 = Down Waveform
	for idx in range(2):

		sim_params = params_array[idx]
		
		# Returns the name / pulse width of the best fitting trace and 
		# time_ex_data which is required for extracting vth_out and dmin
		# best_fit_first, _ = run_complete_simulations(sim_params)
		# best_fit = run_complete_simulations_binary_search(sim_params, best_fit_first * 0.5, best_fit_first * 1.5)
		# For example if the stop time of the simulation is 2000ps == 2000e6as, and therefore the max value is set to 1.5e9
		best_fit = run_complete_simulations_binary_search(sim_params, [(MIN_VALUE_BINARY_SEARCH, MAX_VALUE_BINARY_SEARCH)], MAX_ACCURACY_OUT, VTH_OUT)

		# Now we want to run some additional simulations to ensure that we have enough data points for the involution function
		# run_additional_simulations(sim_params, best_fit, 8 * best_fit, 13)

		if TOOL=="spectre":
			file_name = SPECTRE_FOLDER + sim_params['startName'] + "%020d.raw" % best_fit
		else:
			file_name = SPICE_FOLDER + sim_params['startName'] + "%020d.tr0" % best_fit
			
		data[idx] = read_file(file_name, VAR_COUNT)

	# Calculate \dmin bar		
	(_, d_min, d_min_indices, crossing_time, time_diff) = extract_vthin_dmin(data, sim_params['startName'][:-1], VTH_OUT)

	# Based on \dmin we calculate \Delta^+ and Delta^-
	# We need to go back / forward in time until the the up and down input waveform cross V_th^in
	
	# Index 0 = Up Waveform
	# Index 1 = Down Waveform
	deltas = []
	delta_plus = None
	delta_minus = None

	for idx in range(2):

		current_idx = d_min_indices[idx]
		current_waveform = data[idx][IN_IDX]
		time = data[idx][0]

		if idx == 0: # Up Waveform
			# We need to shift the time axis of the up waveform
			time = [i-time_diff for i in time]

		idx_inc = 0

		# Determine if we have up or down waveform at the input
		if np.average(current_waveform[0:5]) > VTH_IN:
			# down waveform
			min_idx = current_waveform.index(min(current_waveform))
			if current_waveform[current_idx] > VTH_IN:
				# into the direction of min
				# print("Into")
				idx_inc = -1 if (current_idx > min_idx) else 1 
			else:
				# away from min
				# print("Away")
				idx_inc = 1 if (current_idx > min_idx) else -1 
		else:
			# up waveform			
			max_idx = current_waveform.index(max(current_waveform))
			if current_waveform[current_idx] < VTH_IN:
				# into the direction of max
				# print("Into")
				idx_inc = -1 if (current_idx > max_idx) else 1 
			else:
				# away from max
				# print("Away")
				idx_inc = 1 if (current_idx > max_idx) else -1 

		# print("Idx inc: ", idx_inc)

		# We need to take one step back
		current_idx = current_idx - idx_inc

		while True:
			# print(current_idx, current_waveform[current_idx], current_waveform[current_idx + idx_inc])
			if np.sign(current_waveform[current_idx] - VTH_IN) != np.sign(current_waveform[current_idx + idx_inc] - VTH_IN):
				break
			else:
				current_idx = current_idx + idx_inc

		# Need to interpolate crossing to find Delta^+/-
		crossing_time_vthin = interpolate_crossing(time[current_idx], time[current_idx + idx_inc], current_waveform[current_idx], current_waveform[current_idx + idx_inc], VTH_IN)
		# print(time[current_idx], current_waveform[current_idx], time[current_idx + idx_inc], current_waveform[current_idx + idx_inc], crossing_time_vthin, crossing_time, d_min)


		# We need to determine the shape of the output waveform, and depending on the wavefom set \Delta^+ or \Delta^-
		if np.average(data[idx][OUT_IDX][0:5]) > VTH_OUT:
			delta_plus = crossing_time - crossing_time_vthin
		else:
			delta_minus = crossing_time - crossing_time_vthin

	assert(delta_plus and delta_minus)
	deltas.append(delta_plus)
	deltas.append(delta_minus)


	assert(len(deltas) == 2)
	assert(np.sign(deltas[0]) + np.sign(deltas[1]) == 0) # Either both 0, or different sign
			
	dinf_up = None
	dinf_do = None
	if CALCULATE_INVOLUTION:
		dinf_up, dinf_do = calculate_involution(params_array, VTH_IN, VTH_OUT, d_min, deltas)
	else:
		dinf_up, dinf_do = calc_dinf(params_array, VTH_IN, VTH_OUT)

	
	write_results(params_array, VTH_IN, VTH_OUT, d_min, deltas, dinf_up, dinf_do)

	return (VTH_IN, VTH_OUT, d_min, deltas)

def bwd_char(params_array):	
	data = [[],[]]

	# We need to determine the missing threshold voltage and dmin first

	# carry out SPICE simulations to find the missing threshold voltage
	# Index 0 = Up Waveform
	# Index 1 = Down Waveform
	for idx in range(2):

		sim_params = params_array[idx]
		
		# Returns the name / pulse width of the best fitting trace and 
		# time_ex_data which is required for extracting vth_out and dmin
		# best_fit_first, _ = run_complete_simulations(sim_params)
		# best_fit = run_complete_simulations_binary_search(sim_params, best_fit_first * 0.5, best_fit_first * 1.5)
		# For example if the stop time of the simulation is 2000ps == 2000e6as, and therefore the max value is set to 1.5e9
		best_fit = run_complete_simulations_binary_search(sim_params, [(MIN_VALUE_BINARY_SEARCH, MAX_VALUE_BINARY_SEARCH)], MAX_ACCURACY_OUT, VTH_OUT)
		
		# Now we want to run some additional simulations to ensure that we have enough data points for the involution function
		# run_additional_simulations(sim_params, best_fit, 8 * best_fit, 13)

		if TOOL=="spectre":
			file_name = SPECTRE_FOLDER + sim_params['startName'] + "%020d.raw" % best_fit
		else:
			file_name = SPICE_FOLDER + sim_params['startName'] + "%020d.tr0" % best_fit
			
		data[idx] = read_file(file_name, VAR_COUNT)
		
	(vth_in, d_min, _, _, _) = extract_vthin_dmin(data, sim_params['startName'][:-1], VTH_OUT)
	vth_out = VTH_OUT

	# Now determine the involution according to plain IDM
	dinf_up = None
	dinf_do = None
	if CALCULATE_INVOLUTION:
		dinf_up, dinf_do = calculate_involution(params_array, vth_in, vth_out, d_min, [0, 0])
	else:
		dinf_up, dinf_do = calc_dinf(params_array, vth_in, vth_out)
		
	write_results(params_array, vth_in, vth_out, d_min, [0, 0], dinf_up, dinf_do)

	return (vth_in, vth_out, d_min, None)

def write_results(params_array, vth_in, vth_out, d_min, deltas, dinf_up, dinf_do):

	file_name = params_array[0]['startName'][:-1]

	result_filename = file_name + '%s_%s_%s_%s_%s_result.dat'%(VAR_NAMES[IN_IDX],
												VAR_NAMES[OUT_IDX],
												CELL_NAME,
												str(vth_in).replace('.',''),
												str(vth_out).replace('.',''))
												
	f_out = open (build_path(DATA_FOLDER, result_filename), 'w')
	f_out.write(str([vth_in, vth_out, d_min, deltas[0], deltas[1], dinf_up, dinf_do]))
	f_out.close()


def check_params_array(params_array, pulse_width):
	sim_params = params_array[0] # Just check if this results in an up waveform at the output
	
	sim_params['startVal'] = pulse_width
	sim_params['stopVal'] = pulse_width+1
	sim_params['stepVal'] = 1
		
	if TOOL=="spectre":
		file_name = SPECTRE_FOLDER + sim_params['startName'] + "%020d.raw" % pulse_width
	else:
		file_name = SPICE_FOLDER + sim_params['startName'] + "%020d.tr0" % pulse_width
	
	if not os.path.isfile(file_name):
		run_spice(sim_params)
	else:
		print_info("file %s already exists"%file_name)

	
	data = read_file(file_name, VAR_COUNT)

	vth_out = VTH_OUT
	if VTH_OUT < 0: # fwd char
		vth_out = VSUPP / 2

	# print(data[OUT_IDX][0], data[OUT_IDX][-1], max(data[OUT_IDX]), min(data[OUT_IDX]))

	if data[OUT_IDX][0] > vth_out and data[OUT_IDX][-1] > vth_out and min(data[OUT_IDX]) < vth_out:
		# up waveform at the output with threshold crossing
		pass
	elif data[OUT_IDX][0] < vth_out and data[OUT_IDX][-1] < vth_out and max(data[OUT_IDX]) > vth_out:
		# down waveform at the output with threshold crossing, we need to swap the elements
		params_array[0], params_array[1] = params_array[1], params_array[0]
		print("Swapped!")
	else:
		assert(False)

	# This is just for testing. TODO Remove
	# params_array[0], params_array[1] = params_array[1], params_array[0]

	return params_array


def build_path(path, filename):
	path = os.path.join(path + "/", remove_special_chars_from_filename(filename))
	return path

def remove_special_chars_from_filename(filename):
	return filename.replace('/', '')

