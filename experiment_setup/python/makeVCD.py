"""
    
	Involution Tool
	File: makeVCD.py
	
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

from __future__ import division
import numpy as np
from rawread import *
from pprint import pprint
from helper import *
import json
import sys

def main():
	if len(sys.argv) != 4:
		my_print("usage: python makeVCD.py VTH raw_name vcd_name", EscCodes.FAIL)
		sys.exit(1)
	make_vcd(sys.argv[1], sys.argv[2], sys.argv[3])

def make_vcd(vth, raw_name, vcd_name):
	vth = float(vth)
	symbol_pool = ['#','$','%','&','<','>','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q', \
	       '1#','1$','1%','1&','1<','1>','1A','1B','1C','1D','1E','1F','1G','1H','1I','1J','1K','1L','1M','1N','1O','1P','1Q', \
	       '2#','2$','2%','2&','2<','2>','2A','2B','2C','2D','2E','2F','2G','2H','2I','2J','2K','2L','2M','2N','2O','2P','2Q', \
	       '3#','3$','3%','3&','3<','3>','3A','3B','3C','3D','3E','3F','3G','3H','3I','3J','3K','3L','3M','3N','3O','3P','3Q', \
	       '4#','4$','4%','4&','4<','4>','4A','4B','4C','4D','4E','4F','4G','4H','4I','4J','4K','4L','4M','4N','4O','4P','4Q', \
	       '5#','5$','5%','5&','5<','5>','5A','5B','5C','5D','5E','5F','5G','5H','5I','5J','5K','5L','5M','5N','5O','5P','5Q', \
	       '6#','6$','6%','6&','6<','6>','6A','6B','6C','6D','6E','6F','6G','6H','6I','6J','6K','6L','6M','6N','6O','6P','6Q', \
	       '7#','7$','7%','7&','7<','7>','7A','7B','7C','7D','7E','7F','7G','7H','7I','7J','7K','7L','7M','7N','7O','7P','7Q', \
	       '8#','8$','8%','8&','8<','8>','8A','8B','8C','8D','8E','8F','8G','8H','8I','8J','8K','8L','8M','8N','8O','8P','8Q', \
	       '9#','9$','9%','9&','9<','9>','9A','9B','9C','9D','9E','9F','9G','9H','9I','9J','9K','9L','9M','9N','9O','9P','9Q', \
	       'A#','A$','A%','A&','A<','A>','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ', \
	       'B#','B$','B%','B&','B<','B>','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN','BO','BP','BQ', \
	       'C#','C$','C%','C&','C<','C>','CA','CB','CC','CD','CE','CF','CG','CH','CI','CJ','CK','CL','CM','CN','CO','CP','CQ', \
	       'D#','D$','D%','D&','D<','D>','DA','DB','DC','DD','DE','DF','DG','DH','DI','DJ','DK','DL','DM','DN','DO','DP','DQ', \
	       'E#','E$','E%','E&','E<','E>','EA','EB','EC','ED','EE','EF','EG','EH','EI','EJ','EK','EL','EM','EN','EO','EP','EQ', \
	       'F#','F$','F%','F&','F<','F>','FA','FB','FC','FD','FE','FF','FG','FH','FI','FJ','FK','FL','FM','FN','FO','FP','FQ', \
	       'G#','G$','G%','G&','G<','G>','GA','GB','GC','GD','GE','GF','GG','GH','GI','GJ','GK','GL','GM','GN','GO','GP','GQ', \
	       'H#','H$','H%','H&','H<','H>','HA','HB','HC','HD','HE','HF','HG','HH','HI','HJ','HK','HL','HM','HN','HO','HP','HQ', \
	       'I#','I$','I%','I&','I<','I>','IA','IB','IC','ID','IE','IF','IG','IH','II','IJ','IK','IL','IM','IN','IO','IP','IQ', \
	       'J#','J$','J%','J&','J<','J>','JA','JB','JC','JD','JE','JF','JG','JH','JI','JJ','JK','JL','JM','JN','JO','JP','JQ']

	darr, mdata = rawread(raw_name)
	f = open(vcd_name,'w')

	values = {}
	symbols = {}

	names = {}
	for mytuple in darr[0].dtype.descr:
		if mytuple[0].endswith('_prime'):
			continue
		if mytuple[0] == 'time':
			continue
		names[ mytuple[0] ] = mytuple[0][2:-1]

	initial_values = {}
	crossing_times = {}

	for name in names.keys():
		crossing_times[names[name]] = []
		if darr[0][name][0] < vth:
			values[name] = 0
			initial_values[names[name]] = 0
		else:
			values[name] = 1
			initial_values[names[name]] = 1
			
	f.write("$date\n\t%s\n$end\n\n"%"March 2019")
	f.write("$version\n\tHSPICERF L-2016.06-SP2-1\n$end\n\n")
	f.write("$timescale\n\t1fs\n$end\n\n")

	f.write("$scope module toplevel $end\n")

	symbolCounter = 0
	for name in names.keys():
		#print("{0} - {1}".format(symbolCounter, len(names.keys())))
		symbols[name] = symbol_pool[symbolCounter]
		symbolCounter += 1
		f.write("$var reg 1 %s %s $end\n"%(symbols[name],names[name]))

	f.write("$upscope $end\n$enddefinitions $end\n\n")

	f.write("$dumpvars\n#0\n")

	for name in values.keys():
		f.write("b%d %s\n"%(values[name], symbols[name]))

	f.write("$end\n")

	for idx in range(1,len(darr[0]['time'])):
		activity = {}
		times = {}
		for name in names.keys():
			if darr[0][name][idx] < vth and (values[name] == 1):
				values[name] = 0
				activity[name] = 0
				# crossing_times[names[name]].append((darr[0]['time'][idx-1] + darr[0]['time'][idx])/2.0)
				# Use better interpolation			
				ct = (darr[0]['time'][idx] - darr[0]['time'][idx-1]) / (darr[0][name][idx-1] - darr[0][name][idx]) * (darr[0][name][idx-1] - vth) + darr[0]['time'][idx-1]
				crossing_times[names[name]].append(ct)
				if ct in times:
					times[ct].append(name)
				else:
					times[ct] = [name]			
				
			elif darr[0][name][idx] > vth and (values[name] == 0):
				values[name] = 1
				activity[name] = 1
				# Use better interpolation
				# crossing_times[names[name]].append((darr[0]['time'][idx-1] + darr[0]['time'][idx])/2.0)
				ct = (darr[0]['time'][idx] - darr[0]['time'][idx-1]) / (darr[0][name][idx-1] - darr[0][name][idx]) * (darr[0][name][idx-1] - vth) + darr[0]['time'][idx-1]
				crossing_times[names[name]].append(ct)
				if ct in times:
					times[ct].append(name)
				else:
					times[ct] = [name]	
				
		if len(activity) == 0:
			continue
			
		if len(times) > 1:
			my_print("We have got different discrete timestamps for the same raw-timestep: {0}".format(times))

		#f.write("#%d\n"%(int(darr[0]['time'][idx]*1e12)))
		## TODO: Use better interpolation
		##f.write("#%d\n"%(time*1e12))
		#
		#for name in activity.keys():
		#    f.write("b%d %s\n"%(activity[name], symbols[name]))
		
		# Better interpolation
		# Sort the time ascending (possible that we have different timestamps for the signals), and we want to keep them in order
		for key in sorted(times.keys()):
			# write the timestamp
			f.write("#%d\n"%(key*1e15))
			for name in times[key]:
				# and now write all transitions for this timestamp
				f.write("b%d %s\n"%(activity[name], symbols[name]))
			
		
				
	f.close()

	data = {'crossing_times': crossing_times, 'initial_values': initial_values}
	output_file = vcd_name.split('.')[0] + ".json"
	with open(output_file, 'w') as outfile:
		json.dump(data, outfile)
		
if __name__ == "__main__":
    main()

