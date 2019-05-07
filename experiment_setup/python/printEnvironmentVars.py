"""
    
	Involution Tool
	File: printEnvironmentVars.py
	
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
from parserHelper import *

def main():
	if len(sys.argv) != 4:
		my_print("usage: python printEnvironmentVars.py config_file output_file prefix", EscCodes.FAIL)
		sys.exit(1)
	print_env_vars(sys.argv[1], sys.argv[2], sys.argv[3])

def print_env_vars(config_file, output_file, prefix):	
	result = dict()
		
	for k, v in os.environ.items(): 
		result[prefix + k] = v.strip(' \t\n\r"')	
		
	# now also add the variables from the report.cfg
	config = read_config_file(config_file)
	for k, v in config.items():
		if "power_unit" in k.lower():
			result[prefix + k] = v.strip(' \t\n\r"')
			result[prefix + k + "siprefix"] = str(power_to_si_prefix(float(v)))
	
	
	extend_results(output_file, result)
	
if __name__ == "__main__":
    main()