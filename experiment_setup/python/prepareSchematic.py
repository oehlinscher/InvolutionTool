"""
    
	Involution Tool
	File: prepareSchematic.py
	
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
from shutil import copyfile

def main():
	if len(sys.argv) != 4:
		my_print("usage: python prepareSchematic.py file schematic_template_file config_file", EscCodes.FAIL)
		sys.exit(1)
	prepare_schematic(sys.argv[1], sys.argv[2], sys.argv[3])
	
def prepare_schematic(file, schematic_template_file, config_file):		
	
	config = read_config_file(config_file)
	if "SCHEMATIC_PATH" not in config:
		my_print("No schematic for printing configured in report.cfg")
		# just print empty tex file..
		
		with open(file, 'w') as outfile:
			outfile.write("% No figures defined in report.cfg")
		return
		
	schematic_path = config["SCHEMATIC_PATH"];	
	path = os.path.relpath(os.path.join(os.path.split(config_file)[0], schematic_path), os.path.split(file)[0])
	
	schematic_template = ""
	with open(schematic_template_file, 'r') as tempfile:
		schematic_template = tempfile.read()
		
	# we need to copy the schematic file, because this file can change for different reports
	dest_path = os.path.join(os.path.split(file)[0], os.path.split(schematic_path)[1])
	copyfile(os.path.join(os.path.split(config_file)[0], schematic_path), dest_path)
		
	with open(file, 'w') as outfile:
		content = schematic_template.replace("%##SCHEMATIC_PATH##%", os.path.split(schematic_path)[1])
		outfile.write(content)
			
if __name__ == "__main__":
    main()