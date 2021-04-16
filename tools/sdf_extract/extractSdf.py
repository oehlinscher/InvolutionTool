"""
    
	Involution Tool
	File: extractSdf.py
	
    Copyright (C) 2018-2019  Daniel OEHLINGER <d.oehlinger@outlook.com>

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
"""

import sys
import json
sys.path.append('../../experiment_setup/python')
from vcdParser import *

def main():		
	# Parameters: vcd_file sdf_file new_sdf_file matching_dict
	
	# Define timescale and matching dict for each circuit 
	vcd_timescale = 1 # in femto seconds
	subsequent_transition_range = 0.5e6 / 2 # in femto seconds, use for example mu/2 from generate.json
	sdf_output_scale = 1e3 # in femto seconds
	
	# line_finder = "IOPATH A Z"
	# line_finder = "IOPATH I ZN"	
	line_finder = "IOPATH I ZN"	
	
	warning_delay_change = 10
	
	matching_dict = dict()
	with open(sys.argv[4]) as json_file:
		matching_dict = json.load(json_file)			
	
	# iterate over all data we have (normally at least two, one for rising transition at the input, the other one for falling transition):
	file_list = list()
	file_list.append(sys.argv[1]) # "./main_new_exp.vcd0"
	
	for file in file_list:		
		data = read_modelsim(file, 1.0, 0.50, 0) # vdd / vth / vss not relevant here * (returns the time values / 1e6)
		
		#print(data)
				
		# order the data by transition time, list (time, value, port)	
		transition_times = list()
		
		for key in sorted(data.keys()):
			prev_value = -1
			for i in range(len(data[key][0])):				
				time = data[key][0][i] * 1e6 / vcd_timescale # to get time in femto seconds
				value = data[key][1][i]
				if time == 0:
					# ignore initial values
					continue
				
				if time == prev_value:
					# only take the first value (we have for each transition two values)
					continue
				
				prev_value = time
				transition_times.append((time, value, key))
		
		transition_times = sorted(transition_times)
		
		#print(transition_times)
		
		# Definitely not the most performant implementation, but working ...
		for idx, (time, value, port) in enumerate(transition_times):
			for key, entry in matching_dict.items():
				if entry[0].lower() == port.lower():
					# print("Port: {0}".format(port))
					# we found the "starting port"
					# look into the future for x ns
					future = subsequent_transition_range
					# print("Future: ", time, time+future)
					temp_idx = idx
					found_transition = False
					while len(transition_times) > temp_idx and transition_times[temp_idx][0] < time + future:						
						if transition_times[temp_idx][2].lower() == entry[1].lower():
							#print("{0} < {1} + {2}".format(transition_times[temp_idx][0], time, future))
							# we found a transition in the specified time range, on the "end" port
							# now add the information to the matching_dict
							delay = transition_times[temp_idx][0] - time
							type = value # 0 = rising; 1 = falling
		
							if type== 1 and delay > 0: # rising transition
								#if entry[2] != -1.0 and abs(entry[3] - delay) > warning_delay_change:
								#	print("Change rising delay from {0} to {1}".format(entry[2], delay))
									
								entry[2] += delay
								entry[4] += 1
							elif type == 0 and delay > 0:
								#if entry[3] != -1.0 and abs(entry[3] - delay) > warning_delay_change:
								#	print("Change falling delay from {0} to {1}".format(entry[3], delay))		
								entry[3] += delay
								entry[5] += 1
							elif delay > 0:
								print('This should not happen')
							
							found_transition = True
							
							# No break, because we can also find other transitions that have been caused by this transition
							#break							
						
						temp_idx = temp_idx + 1		
					
					if not found_transition:
						print('Did not find a matching transition for {0} at {1}'.format(entry[0], time))
	
	
	for key in sorted(matching_dict.keys()):
		# time values are in femto seconds, multiply with the multiplicator for sdf files
		rising_time = -1
		falling_time = -1
		if matching_dict[key][4] > 0:
			rising_time = matching_dict[key][2] / matching_dict[key][4]
			matching_dict[key][2] = rising_time
		if matching_dict[key][5] > 0:
			falling_time = matching_dict[key][3] / matching_dict[key][5]
			matching_dict[key][3] = falling_time
		#if rising_time < 0:
		#	print('Rising time < 0, Rising time: {0}, Nr of Transitions: {1}'.format(matching_dict[key][2], matching_dict[key][4]))
		#if falling_time < 0:
		#	print('Falling time < 0, Falling time: {0}, Nr of Transitions: {1}'.format(matching_dict[key][3], matching_dict[key][5]))
		print('Instance: {0}, rise: {1:.6f}, fall: {2:.6f}'.format(key, rising_time / sdf_output_scale, falling_time / sdf_output_scale))
		
	# now go and set each interconnect to 0 (the following code is taken from Juergens customSDF.py script)
	f = open(sys.argv[2])
	fout = open(sys.argv[3],'w')

	lines = f.readlines()
	modified_lines = list()
	for line in lines:
		if line.count('INTERCONNECT') > 0:       
			parts = line.split(' ')
			parts[4] = '(0.000::0.000)'
			parts[5] = '(0.000::0.000))\n'
			modified_lines.append(' '.join(parts))
		else:
			modified_lines.append(line)
			
	# now find for each key in the matching dict the corresponding entry and modify the rise and fall time
	for key in matching_dict.keys():
		found_key = False
		for line_idx, line in enumerate(modified_lines):
			instance = key
			if len(matching_dict[key]) >= 7:
				instance = matching_dict[key][6]
			if line.lower().find("(INSTANCE  {0})".format(instance).lower()) >= 0:		
				# find the next line withing the next few lines which contains IOPATH, and replace...
				start_idx = line_idx
				act_line_finder = line_finder
				if len(matching_dict[key]) >= 8:
					act_line_finder = matching_dict[key][7]
				while line_idx < start_idx + 5:
					# TODO: Generalize this...					
					if modified_lines[line_idx].find(act_line_finder) >= 0:				
						found_key = True	

						parts = modified_lines[line_idx].split(' ')
						parts[4] = "({0:.6f}::{0:.6f})".format(matching_dict[key][2] / sdf_output_scale)
						parts[5] = "({0:.6f}::{0:.6f}))\n".format(matching_dict[key][3] / sdf_output_scale)
							
						modified_lines[line_idx] = ' '.join(parts)
						
						break;
					line_idx += 1
				break
				
		if not found_key:
			print("There was a problem for key: {0}".format(key))
			
	for line in modified_lines:
		fout.write(line)
				
		
if __name__ == "__main__":
	main()