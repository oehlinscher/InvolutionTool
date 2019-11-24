"""
    
	Involution Tool
	File: convertVCD.py
	
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
from helper import *

#********************************************************************************

def main():
	if len(sys.argv) != 4:
		my_print("usage: python convertVCD.py input_file output_file matching_file", EscCodes.FAIL)
		sys.exit(1)
	convertVCD(sys.argv[1], sys.argv[2], sys.argv[3])	
	
def convertVCD(input_file, output_file, matching_file):
	replacements = matching_file_to_dict(matching_file)
	
		
	replacing = False;
	module_list = list()
	with open(input_file) as infile:
	  with open(output_file, 'w') as outfile:
		for line in infile:
			modified_line = line;
			if line.startswith('$scope module toplevel $end'):
				my_print("Start replacing")
				# # TODO: make this general? circuit_tb + c1
				# modified_line = ('$scope module circuit_tb $end\n\n$scope module c1 $end\n')
				replacing = True
			elif line.startswith('$enddefinitions $end'):
				my_print("Stop replacing")
				#modified_line = ('\n$upscope $end\n') + modified_line # add another upscope, for additional c1 at the beginning
				replacing = False
			elif (replacing):
				my_print("Replacing")
				replaced = False
				for src, target in replacements.iteritems():
					# Check all possible replacements
					#print("Line: {0}, find: {1}".format(modified_line.lower(), " {0} $end".format(src).lower()))
					if modified_line.lower().find(" {0} $end".format(src).lower()) >= 0:			
						if replaced:
							my_print("This line has already been replaced, this should never happen!", EscCodes.WARNING)
						replaced = True
						# We have found a replacement (the one and only)
						#print("src: {0}\ntarget: {1}".format(src, target))
												
						# we replaced something, now check the module definitions
						current_module_list = target.split(r'/')						
						#print("Module list: {0}".format(current_module_list[:-1]))	
						
						open_modules = ""
						close_modules = ""
						
						for module in current_module_list[:-1]:
							open_modules = open_modules + "$scope module {0} $end\n".format(module)		
							close_modules = close_modules + "$upscope $end\n"
																							
						modified_line = open_modules + replace_ci(modified_line, " {0} $end".format(src), " {0} $end".format(current_module_list[-1])) + close_modules + "\n"
									
						
						#my_print(src + " in " + line + " new string " + modified_line)
						
						module_list = current_module_list
					
			outfile.write(modified_line)

if __name__ == "__main__":
    main()