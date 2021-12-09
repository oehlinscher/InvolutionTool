"""
    
	Involution Tool
	File: generateWaveform.py
	
    Copyright (C) 2018-2021  Daniel OEHLINGER <d.oehlinger@outlook.com>

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

import random
import os
import pprint
import sys
import time
import json
from helper import *
from readGenerateCfg import *

def main():
	if len(sys.argv) == 9:
		generate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], None)	
	elif len(sys.argv) == 10:
		generate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])	
	else:	
		my_print("usage: python generate.py input_dir output_dir config_dir vdd vth temp spice_lib spice_cir [input_waveform]", EscCodes.FAIL)
		sys.exit(1)
		
def generate(input_dir, output_dir, config_dir, vdd, vth, temp, spice_lib, spice_cir, input_waveform):
	in_filename = os.path.join(input_dir, 'main_new.sp') 
	out_filename = os.path.join(output_dir, 'main_new_exp.sp') 
	config_filename = os.path.join(config_dir, 'generate.json') 
			
			
	generate_cfg = read_generate_cfg(config_filename)

	# print(generate_cfg)
			
	signal_crossings_dict = dict()
	signal_spice_dict = dict()
	tran_time_ns = generate_cfg.rise_time
	subsequent_crossings_diff = 1e-9	
	signal_vdd = float(vdd)
	current_time = 1.0 # start each signal after 1ns
	
			
	for idx, item in enumerate(generate_cfg.signals):	
		signal_crossings_dict[item] =  [current_time, ]
		signal_spice_dict[item] = list()
	
	
	# Check if a file with the name "input_waveform" exists
	# if so, load the file, otherwise save the file with the name "input_waveform"
	load = True
	if (input_waveform is None) or not (os.path.isfile(os.path.join(output_dir, input_waveform))):
		load = False	
	
	my_print("Input waveform: " + str(input_waveform))
	my_print("Waveform loading?: " + str(load))
	
	if not load:		
		i = 0
		while i < generate_cfg.N:
			# randomly select the signal which should have the next transition
			next_sig = random.choice(generate_cfg.signals)
			
			difference = generate_sample(generate_cfg.mue, generate_cfg.sigma, generate_cfg.bound)
			
			next_transition_time = 0
			last_local_trans_time = signal_crossings_dict[next_sig][-1]
			if generate_cfg.calc_next_transition_mode == CalcNextTransitionMode.GLOBAL: # global			
				next_transition_time = current_time + difference
			elif generate_cfg.calc_next_transition_mode == CalcNextTransitionMode.LOCAL: # local
				next_transition_time = last_local_trans_time + difference
			else:
				my_print("Unspecified calc_next_transition_mode: " + str(generate_cfg.calc_next_transition_mode), EscCodes.WARNING)
				
			# Check if there is enough time between two successive transitions -> Working
			if next_transition_time - last_local_trans_time < tran_time_ns + subsequent_crossings_diff:
				next_transition_time = last_local_trans_time + tran_time_ns + subsequent_crossings_diff
				
			# current_time is only valid when calc_next_transition_mode = 0
			current_time = next_transition_time		

			# print("Next sig: ", next_sig, "Next trans time: ", next_transition_time, "Current time: ", current_time, "Difference:", difference)
					
			signal_crossings_dict[next_sig] += [next_transition_time]
		
			i = i + 1
			max_diff = 0
			for g in generate_cfg.groups:
				if next_sig not in g.signals:
					# nothing to do for this group
					continue
					
				for sig in g.signals:
					if sig == next_sig:
						# nothing to do for the causing signal
						continue
						
					# if we want "one-way", and we are the first signal -> ignore
					if g.oneway and sig == g.signals[0]:
						my_print("Ignore one way for signal " + sig + " in group " + str(g.signals))
						continue
					
					# use the correlation possibility of the group, to decide if we want a transition or not
					# and not the old "50-percent version"
					#if bool(random.getrandbits(1)): 
						# we add a transition to a "pair-signal"	
					rand_val = random.random()
					my_print("Correlation possibility: " + str(g.correlation_possibility) + ", rand_val: " + str(rand_val))
					if rand_val < g.correlation_possibility: 		
						difference = generate_sample(g.mue, g.sigma, g.bound) # abs(...)? -> not necessary, but if the difference is negative it can happen that the "causing" transition is after the "caused" 			
						last_local_trans_time = signal_crossings_dict[sig][-1]
										
						my_print("Adding transition to signal " + sig + ", which is in a pair with " + next_sig)
						my_print("Transition time for the 'main' signal: " + str(next_transition_time))
						my_print("Transition time for the secondary signal: " +str(next_transition_time + difference))
						my_print("Difference: " + str(difference))
						
						# if the transition to be added is before (plus minimal time between successive transitions) the last transition of the secondary signal, we throw it away...
						if next_transition_time + difference < last_local_trans_time + tran_time_ns + subsequent_crossings_diff:
							my_print("Had to throw away a transition.")
							my_print("Last transition time on the secondary signal: " + str(last_local_trans_time))
							continue
						
						signal_crossings_dict[sig] += [next_transition_time + difference]
						if difference > max_diff:
							max_diff = difference
						i = i + 1
						if i >= generate_cfg.N:
							# break inner loop if we have enough transitions
							break
					
				
				if i >= generate_cfg.N:
					# break outer loop if we have enough transitions
					break
			
			current_time = current_time + max_diff	
			
		# save waveform to file	
		filename = ""
		if input_waveform is None:		
			filename = os.path.join(output_dir, "input_" + time.strftime("%Y%m%d_%H%M%S") +  ".json") 
		else:
			filename = os.path.join(output_dir, input_waveform)
			
		my_print("Saving waveform file with the name: " + filename)
			
		with open(filename, "w") as wave_file:
			json.dump(signal_crossings_dict, wave_file)
	else: # load from file
		filename = os.path.join(output_dir, input_waveform) 
		my_print("Load waveform from file: " + filename)
		with open(filename) as wave_file:
			signal_crossings_dict = json.load(wave_file)
			
	# (over-)write "old" waveform.json file (required because we want to copy this file into the report folder (so that we can simulate again with the same waveform if necessary))
	with open(os.path.join(output_dir, "waveform.json"), "w") as wave_file:
		json.dump(signal_crossings_dict, wave_file)

	time_max = 0
	for sig in generate_cfg.signals:
		value = 0
		time1 = 0
		signal_spice_dict[sig] = "{time:.9f}ns {value}".format(time = time1, value = value * signal_vdd,) # set starting value to 0	
		for timesegment_ns in signal_crossings_dict[sig][1:]: 
			#[1:] because we want to ignore the first point at 1.0, otherwise this violates our waveform generation configuration
			#Nevertheless we need to set first to 1.0, because we do not want to genererate signal before.
			time1 = timesegment_ns
			signal_spice_dict[sig] += " {time:.9f}ns {value}".format(time = time1 - tran_time_ns/2.0, value = value * signal_vdd)
			value = 1 - value
			signal_spice_dict[sig] += " {time:.9f}ns {value}".format(time = time1 + tran_time_ns/2.0, value = value * signal_vdd)
		if time1 > time_max:
			time_max = time1

	#print("Signal SPICE dict")
	#print(signal_spice_dict) 

	replacements = {'<STOPTIME>': str(time_max + 0.3), '<VDD>': vdd, '<VTH>': vth, '<TEMP>' : temp, '<SPICE_LIB>' : spice_lib, '<SPICE_CIR>' : spice_cir}
	for spice_sig in signal_spice_dict:
		replacements["<" + spice_sig + ">"] = signal_spice_dict[spice_sig]

	# check if output folder exists
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	with open(in_filename) as infile:
		with open(out_filename, 'w') as outfile:
			for line in infile:
				for src, target in replacements.items():
					line = line.replace(src, target)
				outfile.write(line)

def generate_sample(mu, sigma, bound):
	while True:
		# generate until we find a difference in ou bound
		difference = random.gauss(mu, sigma)
		if bound is None or abs(mu - difference) < bound * sigma:
			#print('Sample: {0}'.format(difference))
			return difference
		else:
			#print('Resample. Value {0} is out of bounds'.format(difference))
			pass
			
if __name__ == "__main__":
    main()
