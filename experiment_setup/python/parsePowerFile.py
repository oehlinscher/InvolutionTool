"""
    
	Involution Tool
	File: parsePowerFile.py
	
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
from parserHelper import *
from helper import *

# mode:
# 0 ... DC
# 1 ... PT AVG
# 2 ... PT TIM

def main():
	if len(sys.argv) != 6:
		my_print("usage: python parseDCFile.py mode config_file input_file output_file prefix", EscCodes.FAIL)
		sys.exit(1)
	parse_power_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
	
def parse_power_file(mode, config_file, input_file, output_file, prefix):	
	results = dict()
	config = read_config_file(config_file)
	
	results.update(parse_power_report(input_file, prefix))
	# Not working for PT? -> Adding the results of the parse methods is working, but the methods for parsing should be improved, especially the parse_design method
	results.update(parse_design(input_file, prefix))
	results.update(parse_unit_information(input_file, prefix))
	
	my_print(str(results))
	
	d_source = 1
	pre = results[prefix + "Dynamic Power Units"].strip(" \t\n\r)()")
	if len(pre.strip()) >= 1 and pre[0] != "W":
		d_source = prefix_to_power(pre[0])
	d_target = float(config["DYNAMIC_POWER_UNIT"])
		
	l_source = 1
	pre = results[prefix + "Leakage Power Units"].strip(" \t\n\r)()")
	if len(pre.strip()) >= 1 and pre[0] != "W":
		l_source = prefix_to_power(pre[0])
	l_target = float(config["LEAKAGE_POWER_UNIT"])
	
	
	t_source = 1e-9 # default ns
	pre = results[prefix + "Time Units"].strip(" \t\n\r)()")
	if len(pre.strip()) >= 1 and pre[0] != "W":
		t_source = prefix_to_power(pre[0])
	t_target = float(config["TIME_UNIT"])
	
	# print t_source
	# print t_target
	
	
	# print "---------------"
	# print str(d_source) + " / " + str(d_target)
	# print str(l_source) + " / " + str(l_target)
	# print "---------------"
	
	results.update(parse_power_group(input_file, prefix, d_source, d_target, l_source, l_target))
	
	if int(mode) == 1 or int(mode) == 2:
		results.update(parse_power_total(input_file, prefix, d_source, d_target, l_source, l_target))
		
		
	if int(mode) == 2:
		results.update(parse_peak_power(input_file, prefix, d_source, d_target, l_source, l_target, t_source, t_target))
		
	extend_results(output_file, results)
	
if __name__ == "__main__":
    main()