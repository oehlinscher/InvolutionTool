"""
    
	Involution Tool
	File: vcdParser.py
	
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

def read_modelsim(fileName, vdd, vth, vss):

	data = {}
	mapping = {}
	time = 0 # fs
	
	module_prefix_list = list()

	module_prefix = ""
	with open(fileName) as inFile:
		for line in inFile:
			if line.startswith("$scope module"):
				module_prefix_list.append(line.split(' ')[2]) # add element, we are going in one level down
			if line.startswith("$upscope $end"):
				module_prefix_list = module_prefix_list[:-1] # remove last element, we are going one level up
				
			
			if len(line) > 3 and line[:4] == '$var':
				splitStr = line.split(' ')
				
				# now we also add the module prefix (but ignore the first two modules, since these are normally the testbench and the circuit under test)
				module_prefix = ""
				if len(module_prefix_list) > 2:
					for elem in module_prefix_list[2:]:
						module_prefix = module_prefix + elem + "/" 
				
				
				mapping[splitStr[3]] = module_prefix + splitStr[4]				
				data[module_prefix + splitStr[4]] = [[],[]]
				continue
				
				
			# HSPICE vcd is slightly different
			line = line.rstrip("\n\r")
			if line.startswith('b') and len(line) >= 4:
				line = line[1:] # remove b at the beginning
				line = line.replace(' ', '') # now remove the spaces
				
			if len(line) > 0 and line[0] == '#':
				time = int(line[1:])/1.0/1e6
				continue

			if len(line) > 0 and line[0] == 'x':
				do_append(data[mapping[line[1:]]], vth, time)
				continue

			if len(line) > 0 and line[0] == '0':
				do_append(data[mapping[line[1:]]], vss, time)
				continue

			if len(line) > 0 and line[0] == '1':
				do_append(data[mapping[line[1:]]], vdd, time)
				continue


	return data

#--------------------------------------------------------------------------------
	
def do_append(data, value, time):

    if len(data[0]) == 0:
        data[0].append(time)
        data[1].append(value)
        return

    # same value as before
    if data[1][-1] == value:
        return

    data[0].append(time)
    data[1].append(data[1][-1])

    data[0].append(time)
    data[1].append(value)
