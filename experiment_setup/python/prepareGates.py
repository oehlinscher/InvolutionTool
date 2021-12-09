"""
    
	Involution Tool
	File: prepareGates.py
	
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
from readGateCfg import read_gate_config
from helper import my_print, EscCodes
from parserHelper import replace_special_chars

def main():
	if len(sys.argv) != 6:
		my_print("usage: python prepareGates.py default_config_file circuit_config_file template_gate_config_file output_file required_gates", EscCodes.FAIL)
		sys.exit(1)
	prepate_gates(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

def prepate_gates(default_config_file, circuit_config_file, template_gate_config_file, output_file, required_gates):		
	gates = read_gate_config(default_config_file, circuit_config_file)
	
	gate_config_template = ""
	with open(template_gate_config_file, 'r') as tempfile:
		gate_config_template = tempfile.read()		
	
	generate_all = required_gates is None or "ALL" in required_gates
	file_content = ""			
	# now that we have all the gates we want to create --> create them
	for name, gate in gates.items():			
		if not generate_all and name not in required_gates:
			my_print("Ignoring: " + name) 
			continue # we do not want to generate all gates, if not necessary for the circuit
		
		channel_parameters = ""
		for param_key, param_value in gate.channel_parameters.items():
			channel_parameters += replace_special_chars(str(param_key)) + ": " + replace_special_chars(str(param_value)) + "\\\\"
			
		if channel_parameters != "":
			channel_parameters = "Additional channel parameters: \\\\\n" + channel_parameters
		

		
		file_content = gate_config_template.replace("%##ENTITY_NAME##%", replace_special_chars(gate.entity_name)).replace("%##CHANNEL_TYPE##%", replace_special_chars(str(gate.channel_type))).replace("%##EXP_CHANNEL_LOCATION##%", replace_special_chars(str(gate.channel_location))).replace("%##CHANNEL_LOCATION##%", str(gate.channel_location)).replace("%##T_P##%", str(gate.T_P)).replace("%##FUNCTION##%", gate.function).replace("%##INPUTS##%", ", ".join(gate.inputs)).replace("%##OUTPUTS##%", ", ".join(gate.outputs)).replace("%##CHANNEL_PARAMETERS##%", channel_parameters)
		
		
	
	with open(output_file, 'w') as outfile:
		outfile.write(file_content)
	
if __name__ == "__main__":
    main()