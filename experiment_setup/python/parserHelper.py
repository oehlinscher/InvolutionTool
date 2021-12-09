"""
    
	Involution Tool
	File: parserHelper.py
	
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

import re
import os
import json
from helper import EscCodes, my_print

def parse_power_report(input_file, prefix):
	report_state = 0
	results = dict()
	with open(input_file, 'r') as f:
		for line in f:
			# Check if we are in the "Report" section
			if report_state == 0 and line.startswith("***"):
				report_state = 1
				continue
				
			if report_state == 1:
				if line.startswith('Report') and 'power' in line.lower():
					report_state = 2 # we have found the power report
				else:
					report_state = 0 # false alarm
					continue				
			
			if report_state == 2 and line.startswith('***'):
				report_state = 3
				break # we are done here				
		
			if report_state == 2:
				if ":" in line: # we use the first : as seperator between key and value
					elems = line.split(':', 1)
					results[prefix + elems[0].strip(' \t\n\r')] = elems[1].strip(' \t\n\r')
				else:
					key = prefix + "Report_Parameters"					
					if key in results:
						results[key] += results[key]  +  line.strip(' \t\n\r')
					else:
						results[key] = line.strip(' \t\n\r')
											
	return results


def parse_design(input_file, prefix):
	design_state = 0
	results = dict()
	line_header_values = list()
	line_header_indices = list()
	lines_info = list()
	header_indices_mapping = dict()
	with open(input_file, 'r') as f:
		for line in f:
			# Check if we are in the "Design" section for the DC report
			if design_state == 0 and "design" in line.lower() and "library" in line.lower() and "wire load model" in line.lower():
				design_state = 1
				continue
			
			if design_state == 1:
				if line.startswith("---"): 
					continue
					
				words = line.split()
				if len(words) >= 3:
					results[prefix + "Design"] = words[0].strip(' \t\n\r')
					results[prefix + "Wire Load Model"] = words[1].strip(' \t\n\r')
					results[prefix + "Library"] = words[2].strip(' \t\n\r')
					break # We are completely done with this section
			
			# Check if we are in the "Design" section for the PT report
			if design_state == 0 and "design" in line.lower() and "library" in line.lower() and "wire" in line.lower() and "model" in line.lower():
				design_state = 11
				# less than two subsequent whitespaces in the name of the property											
				line_header_values = [(prefix + x).strip(" \r\n\t") for x in line.split("  ") if x.strip()]
				line_header_indices = [m.start() for m in re.finditer(r'([\S]+[\s]?)+', line)] 
				results.update(dict((key, "") for key in line_header_values))
				
				for idx, val in enumerate(line_header_values):
					header_indices_mapping[line_header_indices[idx]] = val
					
				continue
			
			if design_state == 11:
				if line.startswith("---"): 
					continue
								
				if line.strip():	
					# print("Header indices mapping: ", header_indices_mapping)		
					split_indices = []
					for index in header_indices_mapping.keys():
						# print("Idx:", index, len(line))
						if (index > 0 and index-1 < len(line)-1 and line[index-1] == " "):
							# print("YEAH")
							split_indices.append(index)
					
					split_indices = sorted(split_indices)

					indices = split_indices
					indices.extend([m.start() for m in re.finditer(r'([\S]+[\s]?)+', line)] )
					indices = sorted(list(set(indices)))

					if len(indices) > 0:
						values = [line[i:j].strip() for i,j in zip(indices, indices[1:]+[None])]
					else:
						values = [line]

					for idx, key in enumerate(indices):
						if (not values[idx].strip()):
							continue
						if key in header_indices_mapping:
							results[header_indices_mapping[key]] = values[idx]
						else:
							my_print("Problem during parsing the design information of the file: " + input_file, EscCodes.WARNING)
				else:
					# we are done			
					break
							
	return results		
					
def parse_unit_information(input_file, prefix):
	unit_information_state = 0
	results = dict()
	with open(input_file, 'r') as f:
		for line in f:
			if unit_information_state == 0 and line.startswith("Power-specific unit information"):
				unit_information_state = 1
				continue
			
			if unit_information_state == 1:
				if not line.strip():
					unit_information_state = 2
					break
				
				
				elems = line.split('=', 1)
				key = elems[0].strip(' \t\n\r')
				# now get the first match of chars after digits... (we assume this is the unit)
				regex = "\d+\s*(\w+)"
				
				matches = re.finditer(regex, elems[1], re.MULTILINE)
				for matchNum, match in enumerate(matches):
					matchNum = matchNum + 1					
					for groupNum in range(0, len(match.groups())):
						groupNum = groupNum + 1
						results[prefix + key] = match.group(groupNum)
						continue
					continue
	
	return results

def parse_power_group(input_file, prefix, d_source, d_target, l_source, l_target):	
	power_group_state = 0
	results = dict()
	with open(input_file, 'r') as f:
		for line in f:
			if power_group_state == 0 and line.startswith("Power Group"):
				power_group_state = 1
				continue
				
			if power_group_state == 1:
				if line.startswith("---"):
					continue
					
				if not line.strip():
					power_group_state = 2
					break # done, maybe we have no Total line, like in PT
					
				elems = line.split()
				key = prefix + elems[0]
				
				column = 1
				for e in elems[1:]:
					if re.match("\d+.\d+(e?[+|-]\d+)?", e):
						subkey = ""
						source = d_source
						target = d_target
						if column == 1:
							subkey = "Internal Power"
						if column == 2:
							subkey = "Switching Power"
						if column == 3:
							subkey = "Leakage Power"
							source = l_source
							target = l_target
						if column == 4:
							subkey = "Total"
						if column == 5:
							subkey = "Percent"
							
						if subkey == "Percent":
							results[key + "_" + subkey] = e.strip(' \t\n\r)(')
						else:
							results[key + "_" + subkey] = convert_units(source, target, float(e.strip(' \t\n\r)(')))
							
						column = column + 1		
					elif e.strip(" ()\r\n\t") and column > 5:
						# attribute column?
						results[key + "_" + "Attrs"] = e.strip(' ()\t\n\r)(')
												
				if line.startswith("Total"):
					power_group_state = 2
					break # done
			
	return results

def parse_power_total(input_file, prefix, d_source, d_target, l_source, l_target):
	results = dict()
	with open(input_file, 'r') as f:
		for line in f:
			parse_line = False
			key_final = ""
			source = d_source
			target = d_target
			
			key = "net switching power"
			if key in line.lower() and "=" in line:
				parse_line = True
				key_final = key
						
			key = "cell internal power"
			if "cell internal power" in line.lower() and "=" in line:
				parse_line = True
				key_final = key
			
			key = "cell leakage power"
			if "cell leakage power" in line.lower() and "=" in line:
				parse_line = True
				key_final = key
				source = l_source
				target = l_target
			
			key = "total power"
			if "total power" in line.lower() and "=" in line:
				parse_line = True
				key_final = key
				
			if parse_line:
				elems = line.split("=", 1)
				values = elems[1].split()
				value = values[0]
				percent = values[1]
				results[prefix + "_" + key_final] = convert_units(source, target, float(value.strip(' \t\n\r)(')))
				results[prefix + "_" + key_final + "_percent"] = percent.strip(' \t\n\r)(')
			
	return results

def parse_peak_power(input_file, prefix, d_source, d_target, l_source, l_target, t_source, t_target):
	results = dict()	
	with open(input_file, 'r') as f:
		for line in f:
			parse_line = False
			key_final = ""
			source = d_source
			target = d_target
			
			key = "x transition power"
			if key in line.lower() and "=" in line:
				parse_line = True
				key_final = key
								
			key = "glitching power"
			if key in line.lower() and "=" in line:
				parse_line = True
				key_final = key
				# Which power unit?
				
			key = "peak power"
			if key in line.lower() and "=" in line:
				parse_line = True
				key_final = key
				
			key = "peak time"
			if key in line.lower() and "=" in line:
				source = t_source
				target = t_target
				parse_line = True
				key_final = key
			
			if parse_line:
				elems = line.split("=", 1)
				results[prefix + "_" + key_final] = convert_units(source, target, float(elems[1].strip(' \t\n\r)(')))
				
				
	return results
	
def convert_units(source, dest, value):
	return value * source / dest
	
def read_config_file(config_file):
	config = dict()
	with open(config_file, 'r') as f:
		for line in f:
			words = line.split("=")
			config[words[0].strip(' \t\n\r)(')] = words[1].strip(' \t\n\r)(')
	return config

	

def prefix_to_power(prefix):
	if prefix == "m":
		return float(1e-3)
	elif prefix == "u":
		return float(1e-6)
	elif prefix == "n":
		return float(1e-9)
	elif prefix == "p":
		return float(1e-12)
	elif prefix == "k":
		return float(1e3)
	elif prefix == "M":
		return float(1e6)
	elif prefix == "G":
		return float(1e9)
	elif prefix == "T":
		return float(1e12)
	
	my_print("Prefix " + prefix + " not recognized!", EscCodes.WARNING)
	return float(1)

		
def power_to_si_prefix(power):
	if power == 1e-12:
		return "\pico"
	elif power == 1e-9:
		return "\nano"
	elif power == 1e-6:
		return "\micro"
	elif power == 1e-3:
		return "\milli"
	elif power == 1e3:
		return "\kilo"
	elif power == 1e6:
		return "\mega"
	elif power == 1e9:
		return "\giga"
	elif power == 1e12:
		return "\tera"
		
	my_print("No prefix found for power: " + str(power), EscCodes.WARNING)
	return ""
	
def extend_results(output_file, results):
	output_dir = os.path.split(output_file)[0]   

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)	

	current_dict = read_results(output_file)

	# now merge our new dictionary with the one we've read
	current_dict.update(results)
			
	with open(output_file, 'w') as outfile:			
		json.dump(current_dict, outfile)
		
def read_results(output_file):
	current_dict = dict()	
	if os.path.isfile(output_file):
		with open(output_file, 'r') as infile:
			current_dict = json.load(infile)
	return current_dict
	
special_chars = ["&", "%", "$", "#", "_", "{", "}", "~"]	
def replace_special_chars(value):		
	for c in special_chars:
		value = str(value).replace(c, "\\" + c)	
		
	return value
	
def remove_special_chars(value):
	for c in special_chars:
		value = str(value).replace(c, "")	
		
	return value
	