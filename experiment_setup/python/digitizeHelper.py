"""
    
	Involution Tool
	File: digitizeHelper.py.py
	
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

import json

def interpolate_crossing(x_curr, x_prev, y_curr, y_prev, V_TH):
	return ((x_curr - x_prev) / (y_prev - y_curr)) * (y_prev - V_TH) + x_prev

def trace_to_json(json_file, crossing_times, initial_values):
	data = {'crossing_times': crossing_times, 'initial_values': initial_values}
	with open(json_file, 'w') as outfile:
		json.dump(data, outfile)


def trace_to_vcd(vcd_file, crossing_times, initial_values):

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

	symbols = {}
	
	f = open(vcd_file,'w')

	f.write("$date\n\t%s\n$end\n\n"%"March 2019")
	f.write("$version\n\tHSPICERF L-2016.06-SP2-1\n$end\n\n")
	f.write("$timescale\n\t1fs\n$end\n\n")

	f.write("$scope module toplevel $end\n")

	symbolCounter = 0
	for name in sorted(initial_values.keys()):
		symbols[name] = symbol_pool[symbolCounter]
		symbolCounter += 1
		f.write("$var reg 1 %s %s $end\n"%(symbols[name],name))

	f.write("$upscope $end\n$enddefinitions $end\n\n")

	f.write("$dumpvars\n#0\n")

	for name in initial_values.keys():
		f.write("b%d %s\n"%(initial_values[name], symbols[name]))

	f.write("$end\n")
	
	# Now transform the crossing_times dictionary from Key: Signal, Value: List of Crossings into
	# Key: Crossing Time, Value: List of tuples Signals
	# Moreover, we need a dictionary (activity )which holds the current value for each signal
	activity = initial_values.copy()
	time_dict = dict()
	for signal_name, transitions in crossing_times.items():
		for transition in transitions:
			if transition not in time_dict:
				time_dict[transition] = list()
			time_dict[transition].append(signal_name)
	
	for time in sorted(time_dict.keys()):
		# write the timestamp
		f.write("#%d\n"%(time*1e15))
		for signal_name in time_dict[time]:
			# and now write all transitions for this timestamp
			activity[signal_name] = 1 - activity[signal_name]
			f.write("b%d %s\n"%(activity[signal_name], symbols[signal_name]))
			
		
				
	f.close()
