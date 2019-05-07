"""
    
	Involution Tool
	File: parseMeasureFile.py
	
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
import re
from helper import *
from parserHelper import *

def main():
	if len(sys.argv) != 5:
		my_print("usage: python parseMeasureFile.py config_file spice_folder output_file prefix", EscCodes.FAIL)
		sys.exit(1)
	parse_measure_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

def parse_measure_file(config_file, spice_folder, output_file, prefix):	
	names = list();
	values = list();
	config = read_config_file(config_file)
	results = dict()
	for file in os.listdir(spice_folder):
		if re.match(".*mt\d+$", file):
			my_print("Parsing measure file: " + file);
			# iterate over each line ...
			parse_names = True
			with open(os.path.join(spice_folder, file), 'r') as f:
				for line in f:
					if line.startswith('$'): 
						# we also parse the "header"
						words = line.split(" ")
						for w in words:
							if "=" in w:
								elem = w.split("=", 1)
								results[prefix + elem[0].strip(" \n\r\t'")] = elem[1].strip(" \n\r\t'")
						
						continue

					if line.startswith('.'):
						# we also want the title
						words = line.split(" ", 1)
						if len(words) == 2 and "title" in words[0].lower():
							results[prefix + "TITLE"] = words[1].strip(" \n\r\t'")
							my_print(words[0] + " / " + words[1])
						
						continue 
					
					if parse_names:
						if '#' in line:
							parse_names = False
						line = line.split('#', 1)[0]
						names.extend(line.split())
					else:
						values.extend(line.split())
						
	results.update(dict(zip([prefix + x for x in names], [float(x) for x in values])))	
	
	# now we need to find the power measures and set the correct unit
	if prefix + "pwr_avg" in results:
		results[prefix + "pwr_avg"] = convert_units(float(1), float(config["DYNAMIC_POWER_UNIT"]), float(results[prefix + "pwr_avg"]))
		
	if prefix + "pwr_max" in results:
		results[prefix + "pwr_max"] = convert_units(float(1), float(config["DYNAMIC_POWER_UNIT"]), float(results[prefix + "pwr_max"]))
	
	extend_results(output_file, results)

	
	
		
if __name__ == "__main__":
    main()