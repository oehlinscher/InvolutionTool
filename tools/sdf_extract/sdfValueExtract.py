"""
    
	Involution Tool
	File: extractSdf.py
	
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

import sys
import json
sys.path.append('../../experiment_setup/python')
from vcdParser import *

def main():	
	# Parameters: matching_dict sdf_file

	# Adapt for each circuit
	line_finder = "IOPATH I ZN"	
	
	matching_dict = dict()
	with open(sys.argv[1]) as json_file:
		matching_dict = json.load(json_file)

	sdf_file = open(sys.argv[2])
	lines = sdf_file.readlines()
	delta_sum = 0
	delta_count = 0
	delta_min = sys.float_info.max
	delta_max = 0
	for key in matching_dict.keys():
		found_key = False
		for line_idx, line in enumerate(lines):
			instance = key
			if len(matching_dict[key]) >= 7:
				instance = matching_dict[key][6]
			if line.find("(INSTANCE  {0})".format(instance)) >= 0:		
				# find the next line withing the next few lines which contains IOPATH, and replace...
				start_idx = line_idx
				act_line_finder = line_finder
				if len(matching_dict[key]) >= 8:
					act_line_finder = matching_dict[key][7]
				while line_idx < start_idx + 5:		
					if lines[line_idx].find(act_line_finder) >= 0:				
						found_key = True	

						parts = lines[line_idx].split(' ')
						up_val = float(parts[4].split("::")[0].strip('('))
						do_val = float(parts[5].split("::")[0].strip('('))
						if up_val < delta_min:
							delta_min = up_val
						if up_val > delta_max:
							delta_max = up_val
						if do_val < delta_min:
							delta_min = do_val
						if do_val > delta_max:
							delta_max = do_val							
						delta_sum += up_val
						delta_sum += do_val
						delta_count += 2
						
						break;
					line_idx += 1
				break				
			
		if not found_key:
			print("There was a problem for key: {0}".format(key))
				
	print("Min delta: {0:.6f}, Avg delta: {1:.6f}, Max delta: {2:.6f}".format(delta_min, delta_sum / delta_count, delta_max))

if __name__ == "__main__":
	main()