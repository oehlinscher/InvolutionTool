"""
    
	Involution Tool
	File: digitizeRaw.py
	
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

from rawread import rawread
from helper import my_print, dict_key_to_lower_case, EscCodes, matching_file_to_dict
from digitizeHelper import interpolate_crossing, trace_to_vcd, trace_to_json
import json
import sys
import os

def main():
	if len(sys.argv) == 6:
		digitize_raw(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], None)
	elif len(sys.argv) == 7:
		digitize_raw(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
	else:
		my_print("usage: python digitizeRaw.py raw_file vcd_file crossings_file vth maching_file discretization_thresholds_file", EscCodes.FAIL)
		sys.exit(1)

def digitize_raw(raw_file, vcd_file, crossings_file, vth, matching_file, discretization_thresholds_file):
	default_vth = float(vth)

	darr, _ = rawread(raw_file)
	
	matching_dict = matching_file_to_dict(matching_file)

	discretization_thresholds = dict()
	if discretization_thresholds_file and os.path.isfile(discretization_thresholds_file):
		with open(discretization_thresholds_file, 'r') as f:
			discretization_thresholds = json.load(f)

	discretization_thresholds = dict_key_to_lower_case(discretization_thresholds)
	
	names = {}
	for mytuple in darr[0].dtype.descr:
		if mytuple[0].endswith('_prime'):
			continue
		if mytuple[0] == 'time':
			continue
			
		if mytuple[0][2:-1].lower() not in matching_dict:
			continue
			
		names[mytuple[0]] = mytuple[0][2:-1]

	values = {}
	initial_values = {}
	crossing_times = {}
	
	for name in names.keys():
		crossing_times[names[name]] = []
		if darr[0][name][0] < get_vth(discretization_thresholds, names[name], default_vth):
			values[name] = 0
			initial_values[names[name]] = 0
		else:
			values[name] = 1
			initial_values[names[name]] = 1
			
	for idx in range(1,len(darr[0]['time'])):
		for name in names.keys():
			# print(name)

			vth = get_vth(discretization_thresholds, names[name], default_vth)

			if darr[0][name][idx] < vth and (values[name] == 1):
				values[name] = 0
				ct = interpolate_crossing(darr[0]['time'][idx], darr[0]['time'][idx-1], darr[0][name][idx], darr[0][name][idx-1], vth)
				crossing_times[names[name]].append(ct)		
				
			elif darr[0][name][idx] > vth and (values[name] == 0):
				values[name] = 1
				ct = interpolate_crossing(darr[0]['time'][idx], darr[0]['time'][idx-1], darr[0][name][idx], darr[0][name][idx-1], vth)
				crossing_times[names[name]].append(ct)					
					
	trace_to_vcd(vcd_file, crossing_times, initial_values)	
	trace_to_json(crossings_file, crossing_times, initial_values)	

def get_vth(discretization_thresholds, name, default_vth):
	if name.lower() in discretization_thresholds:
		return discretization_thresholds[name.lower()]
	else:
		return default_vth

		
if __name__ == "__main__":
    main()

