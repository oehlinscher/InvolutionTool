"""
    
	Involution Tool
	File: generate_matching.py
	
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

import os
import re

def main():
	# print('SPICE')
	# extract_CTS("clk.spf", r"[^ ]*CTS_\d+\:ZN")
	# print('Verilog')
	# extract_CTS("clk.vh", r"[^ ]*CTS_\d+")
	generate_matching()
	
def extract_CTS(filename, regex):
	f = open(filename, 'r')
	lines = f.readlines()
	
	all_matches = set()
	for line in lines:		
		matches = re.finditer(regex, line, re.MULTILINE)

		for matchNum, match in enumerate(matches, start=1):
			
			all_matches.add(match.group())
			#print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
			
			for groupNum in range(0, len(match.groups())):
				groupNum = groupNum + 1
				
				#print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
				
	all_matches = list(all_matches)
	all_matches.sort()
	
	print(all_matches)
	print("Number of matches: {0}".format(len(all_matches)))
	
def generate_matching():
	# find all instances in the SPICE file...	
	f = open("clk.spf", 'r')
	lines = f.readlines()
	
	instance_section = False
	instance_names = list()
	complete_instance_names_dict = dict()
	for line in lines:
		if re.search("instance section", line, re.IGNORECASE):
			instance_section = True
			
		if instance_section:
			if line.startswith("X"):
				instance_name = line.split()[0]
				
				if instance_name.startswith('X'):
					instance_name = instance_name[1:]
				
				complete_instance_name = instance_name
				if instance_name.find("/"):
					instance_name = instance_name.split('/')[-1]				
				
				if re.search("CTS", instance_name, re.IGNORECASE) or re.search("INV", instance_name, re.IGNORECASE):
				#if instance_name.find("CTS") >= 0 or instance_name.find("INV") >= 0:
					instance_names.append(instance_name)
					complete_instance_names_dict[instance_name] = "xmycir.{0}".format(complete_instance_name)
					
				#instance_names.append(instance_name)
	
	
	
	print(instance_names)
	print(len(instance_names))
	
	# Now try to find matching entries in the Verilog file:
	f = open('clk.vh', 'r')
	lines = f.readlines()
	
	# Inefficent^2, but ...
	found_all = True
	matching_dict = dict()
	for instance_name in instance_names:
		found_idx = -1
		current_module = None
		for idx, line in enumerate(lines):
			if line.lower().startswith("module"):
				current_module = line.split(' ')[1]
			if line.find(" " + instance_name + " ") >= 0: # important: we need an exact match, therefore add spaces before and after the instance_name		
				found_idx = idx
				break
				
		if found_idx == -1:
			print('This should not happen, instance_name: {0}'.format(instance_name))
			found_all = False
		else:
			#print('Found line {0} at index {1}'.format(lines[found_idx], found_idx))
			#print('Current model {0}'.format(current_module))
			
			# now try to find the correct name for the output.
			zn_line = line
			if re.search("ZN", line, re.IGNORECASE):
				# we are in the correct line
				zn_line = line
			elif len(lines) > idx+1 and re.search('ZN', lines[idx+1], re.IGNORECASE):
				zn_line = lines[idx+1]
			else:
				found_all = False
				print('Did not find the output name for instance: {0}'.format(instance_name))
				continue
				
			regex = r"\.ZN\((.*)\)\)\;"
			output_name = None
			matches = re.finditer(regex, zn_line, re.MULTILINE)
			
			# if len(matches) == 1: #and len(matches[0].groups() == 1):
				# output_name = matches[0].groups()[0]
			# else:
				# print("Should not happen")
				# found_all = False
				# continue
			
			for matchnum, match in enumerate(matches, start=1):    
				#print ("match {matchnum} was found at {start}-{end}: {match}".format(matchnum = matchnum, start = match.start(), end = match.end(), match = match.group()))
				
				for groupnum in range(0, len(match.groups())):
					groupnum = groupnum + 1
					
					#print ("group {groupnum} found at {start}-{end}: {group}".format(groupnum = groupnum, start = match.start(groupnum), end = match.end(groupnum), group = match.group(groupnum)))
					
					output_name = match.group(groupnum)
			

			# now try to find the complete name of ModelSim signal	
			# we have got the current_module --> look where it is used
			module_prefix = ""
			module = ""
			while current_module != "mips":
				# go up in the hierachy:				
				for idx, line in enumerate(lines):
					if line.startswith("module"):
						module = line.split(' ')[1]
				
					if line.find(current_module) >= 0 and not line.startswith("module"):
						split = [x for x in line.split(' ') if x] # remove empty strings
						name = split[1]
						#print("YEAH : {0}".format(name))
						module_prefix = name + '/' + module_prefix
						current_module = module
						# we fount the name of the module
						
			#print("Complete: {0}".format(module_prefix + output_name))
			
			matching_dict[instance_name] = module_prefix + output_name	
		
	print('======= MATCHING =======')
	
	for key, value in matching_dict.iteritems():
		print('{0}:ZN {1}'.format(complete_instance_names_dict[key], value))
		
		
	print('======= PROBING =======')
	probing = ""
	for key in matching_dict.keys():
		probing += ('v({0}:ZN) '.format(complete_instance_names_dict[key]))
		# print('v({0}:ZN) '.format(complete_instance_names_dict[key]))
	print probing
		
	print('======= VCD =======')
	vcd = ""
	for value in matching_dict.values():
		vcd += ('{0} '.format(value))
	print vcd
		
	if found_all:
		print('Yeah, we found matchings for all {0} instance names'.format(len(matching_dict)))
	else:
		print('There was at least one instance were we could not find a matching')
					
	
if __name__ == "__main__":
    main()