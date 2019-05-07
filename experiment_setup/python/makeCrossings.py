"""
    
	Involution Tool
	File: makeCrossings.py
	
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

import numpy as np
from readCSDF import *
import matplotlib.pyplot as plt
import json
import sys
import os
from helper import *

############################################################

def main():
	if len(sys.argv) != 4:
		my_print("usage: python makeCrossings.py input_dir out_put_dir vth", EscCodes.FAIL)
		sys.exit(1)
	make_crossings(sys.argv[1], sys.argv[2], sys.argv[3])	
	
def make_crossings(input_dir, output_dir, vth):
	raw_name = os.path.join(input_dir, 'main_new_exp.tr0') 
	output_file = os.path.join(output_dir, 'crossings.json')
	VTH = float(vth)
	
	# extract data
	#darr, mdata = rawread(raw_name)
	
	my_print('Raw_name {0}'.format(raw_name))
	
	darr = read_file(raw_name)
	y = {}
	for key in darr:
		if key == 'time':
			x= np.real(darr['time'])
		else:
			y[key] = np.real(darr[key])
		
		my_print('Name: ' + key + ' Values: ' + str(np.real(darr[key])) + ' Length: ' + str(len(np.real(darr[key]))))

	# show which signals we have
	#pprint(mdata[0]['varnames'])
		
	# process data
	crossing_times = {}
	initial_values = {}
	for name in y:
		
		y_tmp = y[name]
		old_disc_value = None
		crossing_times[name] = []
		for idx, value in enumerate(y_tmp):
			
			if old_disc_value is None:
				# initially
				old_disc_value = 0 if value < VTH else 1
				initial_values[name] = old_disc_value
				
			else:
				# check for crossing
				new_disc_value = 0 if value < VTH else 1 
				if not (new_disc_value == old_disc_value):
					# there was a crossing
					# Better interpolation:
					#crossing_times[name].append( (x[idx-1] + x[idx])/2.0 )					
					ct = (x[idx] - x[idx-1]) / (y_tmp[idx-1] - y_tmp[idx]) * (y_tmp[idx-1] - VTH) + x[idx-1]
					crossing_times[name].append(ct)
					old_disc_value = new_disc_value


	#pprint(crossing_times)
	#pprint(initial_values)
	
	# check if output folder exists
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	# write json
	data = {'crossing_times': crossing_times, 'initial_values': initial_values}
	with open(output_file, 'w') as outfile:
		json.dump(data, outfile)
		
if __name__ == "__main__":
    main()

	