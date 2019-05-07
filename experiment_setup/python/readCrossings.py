"""
    
	Involution Tool
	File: readCrossings.py
	
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
from helper import *

outFileNameStart = 'vectors_'

def main():
	if len(sys.argv) < 4:
		my_print("usage: python readCrossings.py input_dir out_put_dir {input_names}", EscCodes.FAIL)
		sys.exit(1)
	read_crossings(sys.argv[1], sys.argv[2], sys.argv[3:])	

def read_crossings(input_dir, output_dir, names ):
	in_filename = os.path.join(input_dir, 'crossings.json') 

	with open(in_filename, 'r') as f:
		data=json.load(f)
			
	# check if output folder exists
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	for name in names:
		outFileName = os.path.join(output_dir, outFileNameStart+name)

		value=data['initial_values'][name]

		f = open(outFileName, 'w')

		f.write('# Input values for involution tool\n')
		f.write('# time [fs] \t value\n')

		f.write(str(int(0)) + '\t' + str(value) + '\n')

		for i in data['crossing_times'][name]:

			if value == 0 :
				value=1
			else:
				value=0
	
			# int() truncates, maybe we should use rounding instead of truncating?
			#f.write(str(int(i*1e15)) + '\t' + str(value) + '\n')
			f.write(str(int(round(i*1e15))) + '\t' + str(value) + '\n')

		f.close()

		my_print("File '" + outFileName + "' sucessfully generated")
	
if __name__ == "__main__":
    main()
