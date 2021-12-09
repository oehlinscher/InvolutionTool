"""
    
	Involution Tool
	File: gateGenerationToResults.py
	
    Copyright (C) 2018-2020  Daniel OEHLINGER <d.oehlinger@outlook.com>

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
from helper import my_print, EscCodes
from readGateCfg import read_gate_config
from parserHelper import extend_results

def main():
	if len(sys.argv) != 5: 
		my_print("usage: python gateGenerationToResults.py gate_config_file required_gates results_file prefix", EscCodes.FAIL)
	else:
		print_to_results(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])	
	
def print_to_results(gate_config_file, required_gates, results_file, prefix):	
	gates = read_gate_config(gate_config_file, None)
	
	generate_all = required_gates is None or required_gates == "" or "ALL" in required_gates
	
	t_p_list = []
	t_p_percent_list = []
	t_p_mode_list = []
	name_list = []
	channel_type_list = []
	channel_location_list = []
	n_up_list = []
	n_do_list = []
	x_1_up_list = []
	x_1_do_list = []
	tau1_up_list = []
	tau1_do_list = []
	tau2_up_list = []
	tau2_do_list = []
	
	for name in sorted(gates.keys()):
		gate = gates[name]
		if not generate_all and name not in required_gates:
			my_print("Ignoring: " + name) 
			continue # we do not want to generate all gates, if not necessary for the circuit
		
		t_p_list.append(gate.T_P)
		t_p_percent_list.append(gate.T_P_percent)
		t_p_mode_list.append(gate.T_P_mode)
		name_list.append(gate.entity_name)
		channel_type_list.append(gate.channel_type)
		channel_location_list.append(gate.channel_location)
		append_channel_parameter(n_up_list, gate, "N_UP")
		append_channel_parameter(n_do_list, gate, "N_DO")
		append_channel_parameter(x_1_up_list, gate, "X_1_UP")
		append_channel_parameter(x_1_do_list, gate, "X_1_DO")
		append_channel_parameter(tau1_up_list, gate, "TAU_1_UP")
		append_channel_parameter(tau1_do_list, gate, "TAU_1_DO")
		append_channel_parameter(tau2_up_list, gate, "TAU_2_UP")
		append_channel_parameter(tau2_do_list, gate, "TAU_2_DO")
		
	# Now extend the results dictionary
	results = dict()
	append_to_result_dict(results, prefix + 'T_P', t_p_list)
	append_to_result_dict(results, prefix + 'T_P_Percent', t_p_percent_list)
	append_to_result_dict(results, prefix + 'T_P_Mode', t_p_mode_list)
	append_to_result_dict(results, prefix + 'name', name_list)
	append_to_result_dict(results, prefix + 'channel_type', channel_type_list)
	append_to_result_dict(results, prefix + 'channel_location', channel_location_list)
	append_to_result_dict(results, prefix + 'n_up', n_up_list)
	append_to_result_dict(results, prefix + 'n_do', n_do_list)
	append_to_result_dict(results, prefix + 'x_1_up', x_1_up_list)
	append_to_result_dict(results, prefix + 'x_1_do', x_1_do_list)
	append_to_result_dict(results, prefix + 'tau_1_up', tau1_up_list)
	append_to_result_dict(results, prefix + 'tau_1_do', tau1_do_list)
	append_to_result_dict(results, prefix + 'tau_2_up', tau2_up_list)
	append_to_result_dict(results, prefix + 'tau_2_do', tau2_do_list)
	
	extend_results(results_file, results)
	
def append_to_result_dict(result_dict, key_name, list):	
	result_dict[key_name] = ','.join([str(x) for x in list])
	
	
def append_channel_parameter(list, gate, parameter_name):
	if parameter_name in gate.channel_parameters:
		list.append(gate.channel_parameters[parameter_name])
	else:
		list.append('')
	
if __name__ == "__main__":
    main()