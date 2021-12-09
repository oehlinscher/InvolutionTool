"""
	@file noiseTest.py

	@brief Script to add noise to an actual delay function pair

	@author Daniel OEHLINGER <d.oehlinger@outlook.com>
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
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import operator

sys.path.append('../../experiment_setup/python')
from helper import my_print, EscCodes

def main():
	# if len(sys.argv) != 5: 
	# 	my_print("usage: python prepareConfig.py root_folder circuit_structure_file_path config_output_file_path spice_var_names_path", EscCodes.FAIL)
	# else:
	# 	noise_test()

    noise_test()		

def noise_test():

	# Algorithm Idea:
	# Iterate over Delayfunction pairs (like in fitting.py)
	# Choose some \eta^+
	# Determine \eta^-
	# Plot

	# data_folder = '../../circuits/hlth_chain_L_15nm/characterization/results'
	data_folder = 'D:\Temp\data\hlth_inv_chain_L_15nm_idm_plus_bwd'

	# TODO: What to do with CIDM? Translate into IDM Channel? Or use without \Delta^+ / Delta^-
	delay_files = set()
	for result_file in os.listdir(data_folder):
		if "result" in result_file and result_file.endswith(".dat"):
			delay_file_up = result_file.replace('result', 'delayFctUp')
			delay_file_down = result_file.replace('result', 'delayFctDo')

			assert(os.path.exists(os.path.join(data_folder, delay_file_up)))
			assert(os.path.exists(os.path.join(data_folder, delay_file_down)))

			delay_files.add((delay_file_up, delay_file_down, result_file))

	for (up_file_path, down_file_path, result_file_path) in delay_files:
		print(up_file_path, down_file_path, result_file_path)
		
		up_file_path = open(os.path.join(data_folder, up_file_path), 'r')
		down_file_path = open(os.path.join(data_folder, down_file_path), 'r')
		result_file_path = open(os.path.join(data_folder, result_file_path), 'r')

		# Read result file:
		char_vth_in, char_vth_out, char_d_min, char_delta_up, char_delta_down, char_dinf_up, char_dinf_down = json.load(result_file_path)

		# Read delay functions:		
		delay = pd.read_csv(down_file_path, sep=';', header=None)
		x_values_down = delay.iloc[:, 0]
		y_values_down_delay = delay.iloc[:, 1]

		delay = pd.read_csv(up_file_path, sep=';', header=None)
		x_values_up = delay.iloc[:, 0]
		y_values_up_delay =  delay.iloc[:, 1]


		eta_plus = 2e-13
		eta_minus = delta_numeric(-eta_plus, x_values_down, y_values_down_delay, x_values_up, y_values_up_delay) - char_d_min - eta_plus
		print(char_vth_in, char_vth_out, char_d_min, char_delta_up, char_delta_down, char_dinf_up, char_dinf_down, eta_plus, eta_minus)


		
		plt.figure()
		plt.plot(np.array(x_values_down), np.array(y_values_down_delay), label='delta down', color='blue')
		plt.plot(np.array(x_values_down), np.array(y_values_down_delay + eta_plus), color='blue', linestyle='dotted')
		plt.plot(np.array(x_values_down), np.array(y_values_down_delay - eta_minus), color='blue', linestyle='dotted')

		plt.plot(np.array(x_values_up), np.array(y_values_up_delay), label='delta up', color='red')
		plt.plot(np.array(x_values_up), np.array(y_values_up_delay + eta_plus), color='red', linestyle='dotted')
		plt.plot(np.array(x_values_up), np.array(y_values_up_delay - eta_minus), color='red', linestyle='dotted')

		plt.xlim(-0.2e-11, 1e-10)

		plt.legend()
		plt.show()
    


		exit()

def interpolate(x_l, x_h, y_l, y_h, x_t):
	return ((y_h - y_l) / (x_h - x_l)) * (x_t - x_l) + y_l

def delta_numeric(T, xs_right, ys_right, xs_left, ys_left):

	# need to decide if we have to go to the left or the right
	xs = None
	ys = None
	comp_func = None
	if T >= xs_right[0]:
		# go right
		xs = xs_right
		ys = ys_right
		comp_func = operator.gt
	else:
		# go left
		xs = -xs_left
		ys = ys_left
		comp_func = operator.lt

	
	# Find the two x values in between T is
	# and iterpolate
	x_low_idx = None
	x_high_idx = None
	for idx, x in enumerate(xs):
		if comp_func(x, T):
			x_high_idx = idx
			x_low_idx = idx-1
			break

	
	print(T, xs, ys)
	assert(x_low_idx and x_high_idx)
	delta = interpolate(xs[x_low_idx], xs[x_high_idx], ys[x_low_idx], ys[x_high_idx], T)

	return delta

def plot(delta_up, delta_do, eta_plus, eta_minus):
	pass

    
if __name__ == "__main__":
    main()
