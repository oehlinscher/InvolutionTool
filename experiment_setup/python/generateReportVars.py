"""
    
	Involution Tool
	File: generateReportVars.py
	
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
import json
import sys
from parserHelper import *
from helper import *

def main():
	if len(sys.argv) != 3:
		my_print("usage: python parseDCFile.py input_file output_file", EscCodes.FAIL)
		sys.exit(1)
	generate_report_vars(sys.argv[1], sys.argv[2])

def generate_report_vars(input_file, output_file):
	output_dir = os.path.split(output_file)[0]   

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)	

	with open(input_file, 'r') as infile:
		current_dict = json.load(infile)
		
	# create a dictionary with the "modified" keys
	modified_dict = dict()
	for key, value in current_dict.items(): 	
		# replace special chars in the key
		k = key.replace(" ", "").replace("_", "").replace("[", "").replace("]", "").lower().lower()
									
		# replace digits in the key
		if any(c.isdigit() for c in k):
			new_key = ""
			for c in k:
				new_key += convert_char(c)
			k = new_key	
		
		# escape special chars in the value
		value = replace_special_chars(value)
		# and remove the delete character, LaTex cannot handle this char
		value = value.replace(u'\u007f', '')
		
		if k in modified_dict.keys():
			if modified_dict[k] == value:
				# already in the dict, and same value --> throw away and show information
				my_print("Found key '" + k + "' already in the dictionary (same value)", EscCodes.OKGREEN)
			else:
				my_print("Found key '" + k + "' already in the dictionary (different value)", EscCodes.WARNING)
		else:
			# not in the dict, just add
			modified_dict[k] = value
	
		
	with open(output_file, 'w') as outfile:			
		# now iterate over the dictionary, and write line for line
		for key, value in modified_dict.items(): 			
			outfile.write("\\newcommand{\%s}{%s}\n" % (key, value))
			
def convert_char(c):
	if c.isdigit():
		if c == "0":
			return "zero"
		elif c == "1":
			return "one"
		elif c == "2":
			return "two"
		elif c == "3":
			return "three"
		elif c == "4":
			return "four"
		elif c == "5":
			return "five"
		elif c == "6":
			return "six"
		elif c == "7":
			return "seven"
		elif c == "8":
			return "eight"
		elif c == "9":
			return "nine"
			
	return c
		
if __name__ == "__main__":
    main()