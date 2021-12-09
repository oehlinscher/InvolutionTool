"""
    @file causalityChecker.py

	@brief Script for checking the causality of a CIDM fitted circuit

	@author Daniel OEHLINGER <d.oehlinger@outlook.com>
	@date 2021

	@copyright
	@parblock
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
	@endparblock	
""" 

import sys
import os
import json
import re
from anytree.importer import DictImporter
from anytree import PreOrderIter
import numpy as np
import matplotlib.pyplot as plt

from fittingHelper import find_cell_in_structure, get_cellname

sys.path.append('../../experiment_setup/python')
from helper import my_print, EscCodes
from extractCircuitStructure import read_circuit_structure
from readGateCfg import read_gate_config, ChannelType


sys.path.append('../../experiment_setup/vhdl/python_channel')
from exp_delay_channel import calc_tau_up, calc_tau_do, delta_exp_up, delta_exp_do
from sumexp_delay_channel import calc_c_up, calc_c_do, delta_sumexp_up, delta_sumexp_do

# TODO: Configure
v_th = 0.4
v_dd = 0.8

def main():    
    if len(sys.argv) != 8:
        my_print("usage: python causalityChecker.py circuit_folder default_gate_config_file_path circuit_gate_config_file_path structure_file_path characterization_conf_file_path sdf_file_path instance_mapping_file_path", EscCodes.FAIL)
    else:
        causality_checker(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])

# python causalityChecker.py "../../circuits/inv_x2_chain_skip_15nm/" "../gate_config.json" "gate_config.exp_channel.json" "structure.cidm.exp_channel.json" "characterization/conf/inv_x2_chain_15nm.cidm.json" "inv_x2_chain.cidm.sdf" "instance_mapping.json"
# python causalityChecker.py "../../circuits/inv_x2_chain_skip_15nm/" "../gate_config.json" "gate_config.sumexp_channel.json" "structure.cidm.sumexp_channel.paramscustom.json" "characterization/conf/inv_x2_chain_15nm.cidm.json" "inv_x2_chain.cidm.sdf" "instance_mapping.json"
# python causalityChecker.py "../../circuits/inv_x2_chain_skip_15nm/" "../gate_config.json" "gate_config.sumexp_channel.json" "structure.cidm.sumexp_channel.params1.json" "characterization/conf/inv_x2_chain_15nm.cidm.json" "inv_x2_chain.cidm.sdf" "instance_mapping.json"

# python causalityChecker.py "../../circuits/hlth_chain_L_skip_15nm/" "../gate_config.json" "gate_config.exp_channel.json" "structure.cidm.exp_channel.json" "characterization/conf/hlth_inv_chain_L_15nm.cidm.json" "hlth_L_custom.cidm.sdf" "instance_mapping.json"
# python causalityChecker.py "../../circuits/hlth_chain_L_skip_15nm/" "../gate_config.json" "gate_config.sumexp_channel.json" "structure.cidm.sumexp_channel.paramscustom.json" "characterization/conf/hlth_inv_chain_L_15nm.cidm.json" "hlth_L_custom.cidm.sdf" "instance_mapping.json"
# python causalityChecker.py "../../circuits/hlth_chain_L_skip_15nm/" "../gate_config.json" "gate_config.sumexp_channel.json" "structure.cidm.sumexp_channel.params1.json" "characterization/conf/hlth_inv_chain_L_15nm.cidm.json" "hlth_L_custom.cidm.sdf" "instance_mapping.json"

# python causalityChecker.py "../../circuits/mips_clock_15nm/" "../gate_config.json" "gate_config.exp_channel.json" "structure.cidm.exp_channel.json" "characterization/conf/mips_clock_15nm.idmplusbwd.json" "clk_own.cidm.sdf" "instance_mapping.json"
# python causalityChecker.py "../../circuits/mips_clock_15nm/" "../gate_config.json" "gate_config.sumexp_channel.json" "structure.cidm.sumexp_channel.params1.json" "characterization/conf/mips_clock_15nm.cidm.json" "clk_own.cidm.sdf" "instance_mapping.json"

def causality_checker(circuit_folder, default_gate_config_file_path, circuit_gate_config_file_path, structure_file_path, characterization_conf_file_path, sdf_file_path, instance_mapping_file_path):

    # structure file
    structure_file_path =  os.path.join(circuit_folder, structure_file_path)
    structure = read_circuit_structure(structure_file_path)

    # sdf file
    sdf_file_path = os.path.join(circuit_folder, sdf_file_path)
    dinf_dict = read_sdf_file(sdf_file_path)

    # instance_mapping
    instance_mapping_file_path =  os.path.join(circuit_folder, instance_mapping_file_path)
    
    instance_mapping = dict()
    if os.path.exists(instance_mapping_file_path):
        with open(instance_mapping_file_path) as f:
            instance_mapping = json.load(f)

    # gate config files (general and circuit specific files)    
    default_gate_config_file_path =  os.path.join(circuit_folder, default_gate_config_file_path)
    circuit_gate_config_file_path =  os.path.join(circuit_folder, circuit_gate_config_file_path)    
    gate_config = read_gate_config(default_gate_config_file_path, circuit_gate_config_file_path)

    # Characterization config file (the tree)
    characterization_conf_file_path =  os.path.join(circuit_folder, characterization_conf_file_path)
    char_conf = None
    with open(characterization_conf_file_path) as json_file:
        char_conf = json.load(json_file)

    # Algorithm: Go over the tree in preorder
    importer = DictImporter()
    dependency_tree = importer.import_(char_conf['dependency_tree'])

    node_cnt = 0

    for node in PreOrderIter(dependency_tree):	        
        if node.name == 'Top':
            continue

        print("-----------", node_cnt)
        node_cnt = node_cnt + 1

        
        cellname = get_cellname(char_conf, node.name)

        # Find the cell with cellname        
        curr_cell = find_cell_in_structure(structure, cellname)

        if not curr_cell:
            print("Did not find a cell for {}".format(cellname))
            continue

        assert(curr_cell.instance in instance_mapping)
        sdf_instance_name = instance_mapping[curr_cell.instance]
        (d_inf_up, d_inf_do) = dinf_dict[sdf_instance_name]

        curr_gate = gate_config[curr_cell.cell_type]

        # now we need to check causality from this cell to all successor cells
        for succ in node.children:
            succ_cellname = get_cellname(char_conf, succ.name)
            succ_cell = find_cell_in_structure(structure, succ_cellname)

            print(curr_cell, succ_cell)

            if succ_cell:

                succ_gate = gate_config[succ_cell.cell_type]
                assert(succ_gate.function.lower() == "not" or succ_gate.function == "")
                succ_cell_inverting = succ_gate.function.lower() == "not"

                if succ_cell_inverting:
                    succ_pure_delay_up = extract_delay_from_structure(succ_cell.pure_delay_down)
                    succ_pure_delay_do = extract_delay_from_structure(succ_cell.pure_delay_up)
                else:
                    succ_pure_delay_up = extract_delay_from_structure(succ_cell.pure_delay_up)
                    succ_pure_delay_do = extract_delay_from_structure(succ_cell.pure_delay_down)


                succ_pure_delay = extract_delay_from_structure(succ_cell.pure_delay)
                succ_delta_plus = succ_pure_delay_up - succ_pure_delay
                succ_delta_minus = succ_pure_delay_do - succ_pure_delay

                curr_pure_delay = extract_delay_from_structure(curr_cell.pure_delay)                
                curr_pure_delay_up = extract_delay_from_structure(curr_cell.pure_delay_up)
                curr_pure_delay_do = extract_delay_from_structure(curr_cell.pure_delay_down)
                curr_delta_plus = curr_pure_delay_up - curr_pure_delay
                curr_delta_minus = curr_pure_delay_do - curr_pure_delay
                
                # If none of them is > 0, we are definitely acausal
                assert(succ_delta_plus >=  0 or succ_delta_minus >= 0) 
                # One must be <= 0, the other one >= 0
                assert((succ_delta_plus >=  0 and succ_delta_minus <= 0) or (succ_delta_plus <=  0 and succ_delta_minus >= 0))
                assert(d_inf_up > 0)
                assert(d_inf_do > 0)

                assert(curr_pure_delay < d_inf_up)
                assert(curr_pure_delay < d_inf_do)

                # No algorithm yet implemented to automatically fix acausality, this is currently done manually
                # But of course, the simplest solution would be a binary search on the negative delta value and stop once we have two subsequent iteration 
                # where the previous one was causal and the current acausal, and the difference between the two delta values is less than 1 fs (this is the highest possible precision of Questa)
                # TODO: Not sure anymore if this simple approach would be sufficient
                (causal_up, causal_do) = check_causality(curr_gate, curr_cell, d_inf_up, d_inf_do, curr_pure_delay, succ_delta_plus, succ_delta_minus, curr_delta_plus, curr_delta_minus)
                # plot_involution(curr_gate, curr_cell, d_inf_up, d_inf_do, curr_pure_delay, succ_delta_plus, succ_delta_minus, curr_delta_plus, curr_delta_minus)
                print(succ_cell_inverting, cellname, succ_cellname, "d_inf_up: ", d_inf_up, "d_inf_do: ", d_inf_do, "curr_pure_delay: ", curr_pure_delay, "curr_delta_plus: ", curr_delta_plus, "curr_delta_minus:", curr_delta_minus, "succ_delta_plus: ", succ_delta_plus, "succ_delta_minus: ", succ_delta_minus, "causal_up: ", causal_up, "causal_do: ", causal_do)
                # We need at least 1 fs, otherwise we are potentially due to rounding at 0, which is not strictly causal any more
                assert(causal_up >= 0 and causal_do >= 0)

            else:
                # Only the current dmin needs to be > 0
                curr_pure_delay = extract_delay_from_structure(curr_cell.pure_delay)
                assert(curr_pure_delay > 0)

def plot_involution(curr_gate, curr_cell, d_inf_up, d_inf_do, curr_pure_delay, succ_delta_plus, succ_delta_minus, curr_delta_plus, curr_delta_minus):
    channel_type = curr_gate.channel_type

    if channel_type == ChannelType.EXP_CHANNEL:
        tau_up = calc_tau_up(d_inf_up, curr_pure_delay, curr_delta_plus, v_dd, v_th)
        tau_do = calc_tau_do(d_inf_do, curr_pure_delay, curr_delta_minus, v_dd, v_th)

        # Time values are required in fs
        # causal_up = succ_delta_plus + delta_exp_up(succ_delta_minus, d_inf_up, d_inf_do, tau_up, tau_do, curr_delta_plus, curr_delta_minus)
        # causal_do = succ_delta_minus + delta_exp_do(succ_delta_plus, d_inf_up, d_inf_do, tau_up, tau_do, curr_delta_plus, curr_delta_minus)

        assert(False)

    elif channel_type == ChannelType.SUMEXP_CHANNEL:
        # Get parameters from gate
        channel_parameter = curr_gate.channel_parameters

        channel_parameter.update(curr_cell.channel_params)
        x_1_up = channel_parameter['X_1_UP']
        x_1_do = channel_parameter['X_1_DO']
        tau_1_up = convert_time(channel_parameter['TAU_1_UP'])
        tau_1_do = convert_time(channel_parameter['TAU_1_DO'])
        tau_2_up = convert_time(channel_parameter['TAU_2_UP'])
        tau_2_do = convert_time(channel_parameter['TAU_2_DO'])

        print(x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do)

        c_up = calc_c_up(v_dd, v_th, x_1_up, tau_1_up, tau_2_up, d_inf_up, curr_pure_delay, curr_delta_plus)
        c_do = calc_c_do(v_dd, v_th, x_1_do, tau_1_do, tau_2_do, d_inf_do, curr_pure_delay, curr_delta_minus)

        # causal_up = succ_delta_plus + delta_sumexp_up(succ_delta_minus, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, curr_delta_plus, curr_delta_minus)
        # causal_do = succ_delta_minus + delta_sumexp_do(succ_delta_plus, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, curr_delta_plus, curr_delta_minus)

        xmin = -1000
        xmax = 100000

        x_values_up = np.linspace(xmin, xmax, 100)
        x_values_do = np.linspace(xmin, xmax, 100)
        

        y_values_up = np.array([succ_delta_plus + delta_sumexp_up(xi + succ_delta_minus, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, curr_delta_plus, curr_delta_minus) for xi in x_values_up])
        y_values_do =  np.array([succ_delta_minus + delta_sumexp_do(xi + succ_delta_plus, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, curr_delta_plus, curr_delta_minus) for xi in x_values_do])

        fig = plt.figure()
        
        plt.plot(x_values_up, y_values_up, label='delta up', color='blue')
        plt.plot(x_values_do, y_values_do, label='delta do', color='red')
        plt.xlabel('T')
        plt.ylabel('$\delta(T)$')

        ax_list = fig.axes
        ax_list[0].axhline(y=0, color='k')
        ax_list[0].axvline(x=0, color='k')

        plt.axis([xmin, xmax, min(min(y_values_up), min(y_values_do)), max(max(y_values_up), max(y_values_do))])
        plt.savefig(os.path.join("plot.pdf"), dpi=150)

        plt.close()
        exit()

    else:
        print("{} not implemented!".format(channel_type))
        assert(False)

def check_causality(curr_gate, curr_cell, d_inf_up, d_inf_do, curr_pure_delay, succ_delta_plus, succ_delta_minus, curr_delta_plus, curr_delta_minus):   
    causal_up = None
    causal_do = None

    channel_type = curr_gate.channel_type

    if channel_type == ChannelType.EXP_CHANNEL:
        tau_up = calc_tau_up(d_inf_up, curr_pure_delay, curr_delta_plus, v_dd, v_th)
        tau_do = calc_tau_do(d_inf_do, curr_pure_delay, curr_delta_minus, v_dd, v_th)

        # Time values are required in fs
        causal_up = succ_delta_plus + delta_exp_up(succ_delta_minus, d_inf_up, d_inf_do, tau_up, tau_do, curr_delta_plus, curr_delta_minus)
        causal_do = succ_delta_minus + delta_exp_do(succ_delta_plus, d_inf_up, d_inf_do, tau_up, tau_do, curr_delta_plus, curr_delta_minus)
    elif channel_type == ChannelType.SUMEXP_CHANNEL:
        # Get parameters from gate
        channel_parameter = curr_gate.channel_parameters

        channel_parameter.update(curr_cell.channel_params)
        x_1_up = channel_parameter['X_1_UP']
        x_1_do = channel_parameter['X_1_DO']
        tau_1_up = convert_time(channel_parameter['TAU_1_UP'])
        tau_1_do = convert_time(channel_parameter['TAU_1_DO'])
        tau_2_up = convert_time(channel_parameter['TAU_2_UP'])
        tau_2_do = convert_time(channel_parameter['TAU_2_DO'])

        print(x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do)

        c_up = calc_c_up(v_dd, v_th, x_1_up, tau_1_up, tau_2_up, d_inf_up, curr_pure_delay, curr_delta_plus)
        c_do = calc_c_do(v_dd, v_th, x_1_do, tau_1_do, tau_2_do, d_inf_do, curr_pure_delay, curr_delta_minus)


        causal_up = succ_delta_plus + delta_sumexp_up(succ_delta_minus, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, curr_delta_plus, curr_delta_minus)
        causal_do = succ_delta_minus + delta_sumexp_do(succ_delta_plus, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, curr_delta_plus, curr_delta_minus)
    else:
        print("{} not implemented!".format(channel_type))
        assert(False)

    return (causal_up, causal_do)

def convert_time(param):
    assert(param.endswith(" fs"))
    time = param.rstrip(" fs")
    return float(time)

def read_sdf_file(sdf_file_path):
    dinf_dict = dict()

    sdf_file_content = open(sdf_file_path, 'r')
    sdf_file_lines = sdf_file_content.readlines()

    state = 0 
    # 0 ... We wait for INSTANCE ...
    # 1 ... We wait for IOPATH

    instance = None


    for line in sdf_file_lines:
        if state == 0:            
            matches = re.match(r".*\(INSTANCE\s+(.*)\).*", line)
            if matches:
                instance = matches[1]
                state = 1
        elif state == 1:       
            matches = re.match(r".*\(IOPATH\s+.*\s+\((.*)::.*\)\s+\((.*)::.*\)\).*", line)
            if matches:
                state = 0
                up = float(matches[1])
                do = float(matches[2])
                dinf_dict[instance] = (up * 1e3, do * 1e3)
        else:
            assert(False)

    return dinf_dict

def extract_delay_from_structure(delay):
    return float(delay.rstrip("ps")) * 1e3

if __name__ == "__main__":
    main()