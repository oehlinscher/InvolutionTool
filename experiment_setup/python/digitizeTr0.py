"""
    
	Involution Tool
	File: digitizeTr0.py
	
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
from digitizeHelper import *

############################################################

def main():
	if len(sys.argv) != 6:
		my_print("usage: python digitizeTr0.py tr0_file vcd_file crossings_file vth matching_file", EscCodes.FAIL)
		sys.exit(1)
	digitize_tr0(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])	
	
def digitize_tr0(tr0_file, vcd_file, crossings_file, vth, matching_file):
	VTH = float(vth)
	
	# extract data
	#darr, mdata = rawread(raw_name)
	
	my_print('Tr0 file {0}'.format(tr0_file))
	
	darr = read_file(tr0_file)
	y = {}
	for key in darr:
		if key == 'time':
			x= np.real(darr['time'])
		else:
			y[key] = np.real(darr[key])
		
		my_print('Name: ' + key + ' Values: ' + str(np.real(darr[key])) + ' Length: ' + str(len(np.real(darr[key]))))

	# show which signals we have
	#pprint(mdata[0]['varnames'])
	
	matching_dict = matching_file_to_dict(matching_file)
		
	# process data
	crossing_times = {}
	initial_values = {}
	for name in y:
		if name not in matching_dict:
			continue
		
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
					ct = interpolate_crossing(x[idx], x[idx-1], y_tmp[idx], y_tmp[idx-1], VTH)
					crossing_times[name].append(ct)
					old_disc_value = new_disc_value
	
	trace_to_vcd(vcd_file, crossing_times, initial_values)	
	trace_to_json(crossings_file, crossing_times, initial_values)
		
if __name__ == "__main__":
    main()

	