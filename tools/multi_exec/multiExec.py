"""
    
	Involution Tool
	File: multiExec.py
	
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
import os
import json
import sys
import shutil
import subprocess
import time
import copy
import re
sys.path.append('../../experiment_setup/python')
from readGateCfg import *
from parserHelper import *
from readGenerateCfg import *
from helper import *

override_print_env_flag = True

def main():
	if len(sys.argv) != 2:
		my_print("usage: python multiExec.py config_file", EscCodes.FAIL, override_print_env_flag)
		sys.exit(1)
		
	multi_exec_sim(sys.argv[1])

def multi_exec_sim(config_file):						
	# 1. "Copy" the config files which will be adapted to the temp folder
	temp_folder_name = 'temp'
	gate_config_name = 'gate_config.json'
	gate_default_config_file = os.path.join(os.environ["GENERAL_GATE_CONFIG_DIR"], gate_config_name)
	gate_circuit_config_file = os.path.join(os.environ["CIRCUIT_GATE_CONFIG_DIR"], gate_config_name)
	gates = read_gate_config(gate_default_config_file, gate_circuit_config_file)
	
	
	if not os.path.exists(temp_folder_name):
		os.makedirs(temp_folder_name)
	
	with open(os.path.join(temp_folder_name, gate_config_name), "w") as gate_cfg_file:
		gate_cfg_file.write(json.dumps(gates, cls=ObjectEncoder, indent=2, sort_keys=True))
	
	waveform_file_name = 'generate.json'
	waveform_generation = read_generate_cfg(os.path.join(os.environ["WAVEFORM_GENERATION_CONFIG_DIR"], waveform_file_name))
	with open(os.path.join(temp_folder_name, waveform_file_name), "w") as waveform_cfg_file:
		waveform_cfg_file.write(json.dumps(waveform_generation, cls=ObjectEncoder, indent=2, sort_keys=True))
	
	# 2. Read the multi_exec config file
	multi_exec = MultiExec()
	with open(config_file, "r") as cfg_file:
		jsonobject = json.load(cfg_file)	
		for key, value in jsonobject.items():
			if key.lower() == "waveform_generation":
				for elem in value:				
					cfg = copy.deepcopy(waveform_generation) # Required, because we want the default values from the default config file
					cfg.__dict__.update(elem);
					multi_exec.waveform_generation.append(cfg);
			elif key.lower() == "gate_generation":
				multi_exec.gate_generation.__dict__.update(value)
			else:
				multi_exec.__dict__[key] = value;	
					
	# 3. update the environemt variables to the new generated config files (valid for this process and all child process)	
	os.environ["GENERAL_GATE_CONFIG_DIR"] = os.path.join(os.getcwd(), temp_folder_name)
	os.environ["CIRCUIT_GATE_CONFIG_DIR"] = os.path.join(os.getcwd(), temp_folder_name)
	os.environ["WAVEFORM_GENERATION_CONFIG_DIR"] = os.path.join(os.getcwd(), temp_folder_name) 
	
	if get_print_level() > PrintLevel.INFORMATION:
		os.environ["MAKEFILE_PRINT_INFO"] = "False"
		
	# 3.a. set report folder (relative from $RESULT_OUTPUT_DIR), so that all generated reports for this run are in the same folder
	# done in a config file which is called by the Makefile
	#os.environ["ME_REPORT_FOLDER"] = "multi_exec_" + time.strftime("%Y%m%d_%H%M%S")
			
	# innermost loops (keep waveform!) must have lower numbers than than properties where a new waveform has to be created
	KEY_WAVEFORM = 7
	KEY_SPICE_PROPERTIES = 6 # we can keep the waveform, but need to re-execute the Spice Simulation for these properties
	KEY_DIGSIM_PROPERTIES = 5 # no need to re-execute SPICE, but we need to re-run our digital (ModelSim) simulation. ==> For example if only the sdf / spef File is changed
	KEY_INVOLUTION_PROPERTIES = 4 # we need to reexectue make sim_involution, since for example the SDF has changed (only allowed if we use a different SDF file for (G)IDM and Standard Delay Model, or if USE_GIDM flag is changed) 
	KEY_CHANNEL_LOCATION = 3
	KEY_CHANNEL_TYPE = 2
	KEY_T_P = 1
	
	# Prepare a dictionary with the properties to change and a index to the current element
	property_dict = dict()
	total_sim_num = 1
	if len(multi_exec.waveform_generation) > 0:
		property_dict[KEY_WAVEFORM] = 0
		total_sim_num = total_sim_num * len(multi_exec.waveform_generation)
	if len(multi_exec.gate_generation.t_p_list) > 0:	
		property_dict[KEY_T_P] = 0
		total_sim_num = total_sim_num * len(multi_exec.gate_generation.t_p_list)
	if len(multi_exec.gate_generation.channel_location_list) > 0:	
		property_dict[KEY_CHANNEL_LOCATION] = 0
		total_sim_num = total_sim_num * len(multi_exec.gate_generation.channel_location_list)
	if len(multi_exec.gate_generation.channel_type_list) > 0:	
		property_dict[KEY_CHANNEL_TYPE] = 0
		total_sim_num = total_sim_num * len(multi_exec.gate_generation.channel_type_list)
	if len(multi_exec.spice_properties) > 0:
		property_dict[KEY_SPICE_PROPERTIES] = 0
		total_sim_num = total_sim_num * len(multi_exec.spice_properties)
	if len(multi_exec.digsim_properties) > 0:
		property_dict[KEY_DIGSIM_PROPERTIES] = 0
		total_sim_num = total_sim_num * len(multi_exec.digsim_properties)
	if len(multi_exec.involution_properties) > 0:
		property_dict[KEY_INVOLUTION_PROPERTIES] = 0
		total_sim_num = total_sim_num * len(multi_exec.involution_properties)
		
	
	last_key_to_keep_waveform = KEY_SPICE_PROPERTIES
	last_key_to_keep_spice = KEY_DIGSIM_PROPERTIES
	last_key_to_keep_stddigsim = KEY_INVOLUTION_PROPERTIES
	
	last_key_to_keep_group_count = KEY_T_P
	last_key_to_keep_reference_count = KEY_SPICE_PROPERTIES
	
	length_dict = dict()
	length_dict[KEY_WAVEFORM] = len(multi_exec.waveform_generation)
	length_dict[KEY_SPICE_PROPERTIES] = len(multi_exec.spice_properties)
	length_dict[KEY_DIGSIM_PROPERTIES] = len(multi_exec.digsim_properties)
	length_dict[KEY_INVOLUTION_PROPERTIES] = len(multi_exec.involution_properties)
	length_dict[KEY_CHANNEL_LOCATION] = len(multi_exec.gate_generation.channel_location_list)	
	length_dict[KEY_CHANNEL_TYPE] = len(multi_exec.gate_generation.channel_type_list)		
	length_dict[KEY_T_P] = len(multi_exec.gate_generation.t_p_list)		
		
	# 4. simulate
	my_print("Keep waveform: " + str(multi_exec.keep_waveform), EscCodes.OKBLUE, override_print_env_flag)
	# If keep_waveform is false, we just re-execute the complete toolchain fpr each configuration (do not keep SPICE, STD DIGISIM if possible)
	for iteraterion in range(multi_exec.N):
		my_print("Iteration: " + str(iteraterion + 1), EscCodes.OKBLUE, override_print_env_flag)
		keep_waveform_local = False # we ALWAYS want a new waveform in a new iteration
		keep_std_digsim = False
		keep_spice = False
				
		curr_sim_num = 1
		config_num = 0	

		# Reset ME_reference_group and ME_group, these are "counters" which are later used for reporting
		os.environ["ME_reference_group"] = "0" 	# The ME_reference_group is incremented when the waveform config changes
		os.environ["ME_group"] = "0"				# The ME_group is incremented when a channel property changes
		prev_param_mode = None
		me_group_param_mode_dict = dict()
		
		
		# reset property_dict indices (value is a pointer to the current setting for each key)
		for key in property_dict.keys():
			property_dict[key] = 0
		
		while True:			
			if not keep_waveform_local:
				my_print("New waveform should be generated!", EscCodes.OKBLUE, override_print_env_flag)
				waveform_file = "multi_exec_" + time.strftime("%Y%m%d_%H%M%S") +  ".json"
				os.environ["INPUT_WAVEFORM"] = waveform_file
		
			my_print("Iteration: " + str(iteraterion + 1) + " / " + str(multi_exec.N)+ ", Simulation: " + str(curr_sim_num) + " / " + str(total_sim_num), EscCodes.OKBLUE, override_print_env_flag)			
						
			# Deepcopy required if we set one property in the previous simulation, but not in th current one
			# --> we want to have the value of the default config file
			new_gates = copy.deepcopy(gates)
			new_waveform_generation = copy.deepcopy(waveform_generation)
			config_num = config_num + 1
			# iterate over all properties to set
			for key, value in property_dict.items():
				if key == KEY_WAVEFORM:		
					new_waveform_generation = multi_exec.waveform_generation[value]
				elif key == KEY_T_P:
					for gate in new_gates.values():
						# Make distinction between ABSOLUTE and PERCENT
						if isinstance(multi_exec.gate_generation.t_p_list[value], list):
							mode = multi_exec.gate_generation.t_p_list[value][1]
							gate.T_P_mode = mode
							if mode == ParameterMode.ABSOLUTE:
								gate.T_P = multi_exec.gate_generation.t_p_list[value][0]
							elif mode == ParameterMode.PERCENT:
								gate.T_P_percent = multi_exec.gate_generation.t_p_list[value][0]
							else:
								my_print("Error: Unknown T_P_mode:  " + mode, EscCodes.FAIL, override_print_env_flag)
						else:
							# Default behaviour (ABSOLUTE)
							gate.T_P = multi_exec.gate_generation.t_p_list[value]
							gate.T_P_mode = ParameterMode.ABSOLUTE
							
						# Handle ME_group counter (must be different between ABSOLUTE and percent
						if prev_param_mode is None:
							prev_param_mode = gate.T_P_mode
							me_group_param_mode_dict[prev_param_mode] = int(os.environ["ME_group"])
						elif prev_param_mode != gate.T_P_mode:
							# check the dict if we already have a group id for this T_P
							if gate.T_P_mode in me_group_param_mode_dict:
								# go back to the already used group id
								os.environ["ME_group"] = str(me_group_param_mode_dict[gate.T_P_mode])
							else:
								# Create new group id								
								me_group_param_mode_dict[gate.T_P_mode] = max(me_group_param_mode_dict.values()) + 1
								# and use this id
								os.environ["ME_group"] = str(me_group_param_mode_dict[gate.T_P_mode])
							prev_param_mode = gate.T_P_mode
						
				elif key == KEY_CHANNEL_LOCATION:	
					for gate in new_gates.values():
						gate.channel_location = multi_exec.gate_generation.channel_location_list[value]
				elif key == KEY_CHANNEL_TYPE:
					gate_config_dict = multi_exec.gate_generation.channel_type_list[value]
					for gate_key, gate_value in new_gates.items():
						gate_key_for_copy = "ALL" # use the default configuration for this gate
						if gate_key in gate_config_dict:
							gate_key_for_copy = gate_key # we found a more specific configuration for this gate => use it	
						if "channel_type" in gate_config_dict[gate_key_for_copy].keys():
							gate_value.channel_type = gate_config_dict[gate_key_for_copy]["channel_type"]							
						if "channel_parameters" in gate_config_dict[gate_key_for_copy].keys():
							gate_value.channel_parameters = gate_config_dict[gate_key_for_copy]["channel_parameters"]
				elif key == KEY_SPICE_PROPERTIES:
					# nothing to do?
					pass
				elif key == KEY_DIGSIM_PROPERTIES:
					# nothing to do?
					pass
				elif key == KEY_INVOLUTION_PROPERTIES:
					# nothing to do?
					pass
				else:
					my_print("Error: Undefined key", EscCodes.FAIL, override_print_env_flag)
						
			# write the files after setting all the properties
			with open(os.path.join(temp_folder_name, gate_config_name), "w") as gate_cfg_file:
				gate_cfg_file.write(json.dumps(new_gates, cls=ObjectEncoder, indent=2, sort_keys=True))
								
			with open(os.path.join(temp_folder_name, waveform_file_name), "w") as waveform_cfg_file:
				waveform_cfg_file.write(json.dumps(new_waveform_generation, cls=ObjectEncoder, indent=2, sort_keys=True))
				
			# TODO: Remove, just for debugging reasons:						
			with open(os.path.join(temp_folder_name, gate_config_name + str(config_num)), "w") as gate_cfg_file:
				gate_cfg_file.write(json.dumps(new_gates, cls=ObjectEncoder, indent=2, sort_keys=True))
			with open(os.path.join(temp_folder_name, waveform_file_name + str(config_num)), "w") as waveform_cfg_file:
				waveform_cfg_file.write(json.dumps(new_waveform_generation, cls=ObjectEncoder, indent=2, sort_keys=True))
					
			# set the path for the (single-)report
			os.environ["TARGET_FOLDER"] = os.path.join(os.environ["RESULT_OUTPUT_DIR"], os.environ["ME_REPORT_FOLDER"], time.strftime("%Y%m%d_%H%M%S"))
			my_print("target folder: " + str(os.environ["TARGET_FOLDER"]))
			
			# set the current spice_properties (if we have some). Note that these properties need to be checked with ifndef PROP_NAME before they are exported in the default *.cfg files
			set_config_property_list(multi_exec.spice_properties, property_dict, KEY_SPICE_PROPERTIES)
			set_config_property_list(multi_exec.digsim_properties, property_dict, KEY_DIGSIM_PROPERTIES)
			set_config_property_list(multi_exec.involution_properties, property_dict, KEY_INVOLUTION_PROPERTIES)
			
			# always check for the keep_waveform setting from the json file ==> If disabled, we always rerun the complete simulation
			if multi_exec.keep_waveform and keep_std_digsim:			
				my_print("Keep DIGSIM!", EscCodes.OKBLUE, override_print_env_flag)
				execute_make_cmd("make me_involution")		
			elif multi_exec.keep_waveform and keep_spice:
				my_print("Keep SPICE!", EscCodes.OKBLUE, override_print_env_flag)
				execute_make_cmd("make me_digsim")		
			elif multi_exec.keep_waveform and keep_waveform_local:
				my_print("Keep Waveform!", EscCodes.OKBLUE, override_print_env_flag)
				execute_make_cmd("make clean")
				execute_make_cmd("make all") # Careful, altough we clean up, we still want to keep the waveform		
			else:		
				my_print("Complete run!", EscCodes.OKBLUE, override_print_env_flag)	
				# Clean up after previous simulation
				execute_make_cmd("make clean")
						
				# Now execute the simulation
				execute_make_cmd("make all")
						
			# Add a file with the "configuration id" - required for reporting
			if not (os.getenv('SKIP_SIMULATION', None)):		
				with open(os.path.join(os.environ["TARGET_FOLDER"], "config_id"), "w") as cfg_id_file:
					cfg_id_file.write(str(config_num))
			
			#increment all the counters in the dict (needs to be done in a sorted way)
			# sorted is also required, because properties where the waveform can be kept have to be in the innermost loop
			overflow = False			
			
			for key in sorted(property_dict):					
				overflow = False
					
				property_dict[key] += 1		
				if property_dict[key] == length_dict[key]:
					overflow = True
					#print "Overflow at: " + key + ""
					property_dict[key] = 0
					# We had an overflow. Now check if we can keep the waveform (true as long this is not the last parameter that keeps the waveform)
					

					keep_std_digsim = calc_keep_property(key, last_key_to_keep_stddigsim, True)
					keep_spice = calc_keep_property(key, last_key_to_keep_spice, True)
					keep_waveform_local = calc_keep_property(key, last_key_to_keep_waveform, True)
					keep_group_count = calc_keep_property(key, last_key_to_keep_group_count, True)
					keep_reference_group_count = calc_keep_property(key, last_key_to_keep_reference_count, True)
				else:
					keep_std_digsim = calc_keep_property(key, last_key_to_keep_stddigsim, False)
					keep_spice = calc_keep_property(key, last_key_to_keep_spice, False)
					keep_waveform_local = calc_keep_property(key, last_key_to_keep_waveform, False)
					keep_group_count = calc_keep_property(key, last_key_to_keep_group_count, False)
					keep_reference_group_count = calc_keep_property(key, last_key_to_keep_reference_count, False)
					
					break # no need to increment the other properties
			
			if len(property_dict) == 0:
				# if we just want to execute the standard configuration multiple times, we have an overflow after each simulation run:
				overflow = True
				
			if not keep_group_count:			
				# we need to get the maximum value from the dict (because we could configure ABSOLUTE, PERCENT, ABSOLUTE)
				new_group_id = int(os.environ["ME_group"]) + 1
				if not me_group_param_mode_dict:
					if len(me_group_param_mode_dict.values()) == 0:
						new_group_id = 0
					else:
						new_group_id = max(me_group_param_mode_dict.values()) + 1
				os.environ["ME_group"] = str(new_group_id)
				# Reset our datastructures
				me_group_param_mode_dict = dict()
				prev_param_mode = None
				
			if not keep_reference_group_count:
				os.environ["ME_reference_group"] = str(int(os.environ["ME_reference_group"]) + 1)
					
			# "first" property has "overflowed", we are done			
			if overflow:	
				#print "Iterated over all configurations"
				break
				
			curr_sim_num = curr_sim_num + 1
	
def execute_make_cmd(cmd):		
	if (os.getenv('SKIP_SIMULATION', None)):		
		return

	#make_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.environ["EXPERIMENT_SETUP_DIR"])
	postfix = ""
	print_level = get_print_level()
	if print_level > PrintLevel.INFORMATION:
		postfix = "--silent"
	
	make_process = subprocess.Popen(cmd + " " + postfix, shell=True, cwd=os.environ["EXPERIMENT_SETUP_DIR"])
	if make_process.wait() != 0:
		my_print (cmd + " failed!", EscCodes.FAIL, override_print_env_flag)
	else:
		my_print(cmd + " succeeded!", EscCodes.OKGREEN, override_print_env_flag)
		
def set_config_property_list(lst, property_dict, key):
	if len(lst) > 0:				
		props = lst[property_dict[key]]
		for key_prop, value_prop in props.items():
			os.environ[key_prop] = value_prop
			
def calc_keep_property(key, last_key, overflow):
	if overflow:
		if key < last_key:
			return True
	else:
		if key <= last_key:
			return True
	return False
	

	
	
class MultiExec:
	def __init__(self):
		self.N = 1
		self.waveform_generation = list()
		self.spice_properties = list()
		self.digsim_properties = list()
		self.involution_properties = list()
		self.gate_generation = GateGeneration()
		self.keep_waveform = True
		
class GateGeneration:
	def __init__(self):
		self.t_p_list = list() # If this is just a list of values, we assume that these are ABSOLUTE values in ps, if it is a list of 2-element arrays, the first value is either the value in ps or percent, and the second value is the type (ABSOLUTE or RELATIVE)
		self.channel_location_list = list()	
		# a list which contains the configurations to sweep over.
		# each element of the list contains a dictionary, where the key is the mame of the gate, and the value is again a dict.
		# Currently, channel_type and channel_parameters can be specified
		# Note that there must be a special entry with the key "ALL", which specifies the configuration of all gates which have not been specified more specifically
		self.channel_type_list = list() 
		
class ChannelType:
	def __init__(self):
		channel_type = CHANNEL_TYPE.EXP_CHANNEL
		channel_parameters = dict()
		
if __name__ == "__main__":
    main()