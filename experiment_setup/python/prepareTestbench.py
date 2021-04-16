"""
    
	Involution Tool
	File: prepareTestbench.py
	
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
from helper import *
from readGateCfg import *

def main():
	if len(sys.argv) == 8:
		prepare_testbench(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], "")
	elif len(sys.argv) == 9:
		prepare_testbench(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
	else:
		my_print("usage: python prepareTestbench.py circuit_file_in circuit_file_out process_template_file input_names vector_names default_gate_config_file circuit_gate_config_file [circuit_configuration_file]", EscCodes.FAIL)
		sys.exit(1)
	

def prepare_testbench(circuit_file_in, circuit_file_out, process_template_file, input_names, vector_names, default_gate_config_file, circuit_gate_config_file, circuit_configuration_file):
	my_print("prepare_testbench")
		
	gates = read_gate_config(default_gate_config_file, circuit_gate_config_file)
	
	circuit_content = ""
	with open(circuit_file_in, 'r') as tempfile:
		circuit_content = tempfile.read()
	
	process_template = ""
	with open(process_template_file, 'r') as tempfile:
		process_template = tempfile.read()
	
	
	circuit_configuration = ""
	if circuit_configuration_file and os.path.isfile(circuit_configuration_file):		
		with open(circuit_configuration_file, 'r') as tempfile:
			circuit_configuration = tempfile.read()
	
	input_list = input_names.split(" ")
	vector_list = vector_names.split(" ")
	
	input_list = [x.strip(" \r\t\n") for x in input_list if x.strip(" \r\n\t")]
	vector_list = [x.strip(" \r\t\n") for x in vector_list if x.strip(" \r\n\t")]
	
	if len(input_list) != len(vector_list):
		my_print("input_names and vector_names have a different length, this should not happen!", EscCode.FAIL)
		return
	
	#print input_list
	#print vector_list
	#print process_template
	
	
	input_process_content = ""
	for x in range(0, len(input_list)):
		my_print("Signal: " + input_list[x])
		input_process_content += process_template.replace("##SIGNALNAME##", input_list[x]).replace("##VECTORNAME##", vector_list[x])
		input_process_content += "\n\n\n"
	
	for name, gate in gates.items():	
		additional_generics = ""
		for key, value in gate.channel_parameters.items():
			additional_generics = ",\n\t\t\t" + str(key) + " => " + str(value)
		circuit_configuration = circuit_configuration.replace("##GATE_ARCHITECTURE_" + name + "##", gate.channel_type + "_" + gate.channel_location).replace("##T_P_" + name + "##", str(gate.T_P) + " ps").replace("##CHANNEL_SPECIFIC_GENERICS_" + name + "##", additional_generics)
	
	content_to_write = circuit_content.replace("##INPUT_PROCESS##", input_process_content).replace("##CIRCUIT_CONFIGURATION##", circuit_configuration)
	
	with open(circuit_file_out, 'w') as outfile:
		outfile.write(content_to_write)
	

if __name__ == "__main__":
    main()