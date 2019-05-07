"""
    
	Involution Tool
	File: generateDependencies.py
	
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
sys.path.append('../../experiment_setup/python')

def main():	
	# read from the sdf File all lines containing INTERCONNECT and generate the "dependency"-tree
	f = open(sys.argv[1])
	lines = f.readlines()
	counter = 0
	dep_dict = dict()
	for line in lines:
		if line.find("(INTERCONNECT") >= 0:
			# found interconnect, now split into start and stop
			start = line.split()[1]
			stop = line.split()[2]
			
			#if (start.lower().find("cts") >= 0 and stop.lower().find("cts") >= 0):
			if ((start.lower().endswith("/zn") or start.lower() == "clk") and stop.lower().endswith("/i")):
				counter += 1			
				print("Start: {0}, Stop: {1}".format(start, stop))
				instance_name = stop[:-2]		
				mod_start = "Xmycir." + start[:-3] + ":ZN"
				if start.lower() == "clk":
					mod_start = "clk"
				mod_stop = "Xmycir." + stop[:-2] + ":ZN"
				dep_dict[instance_name] = [mod_start, mod_stop, -1, -1, 0, 0]
				
				
	
	for key, value in dep_dict.iteritems():
		print("matching_dict['{0}'] = (['{1}', '{2}', -1, -1, 0, 0])".format(key, value[0], value[1]))
	
	
	print("Found {0} dependencies".format(counter))
	

if __name__ == "__main__":
    main()