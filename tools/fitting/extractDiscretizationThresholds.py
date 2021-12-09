"""
    @file extractDiscretizationThresholds.py

	@brief Script for extracting the discretization threshold voltages
    of a structure file and storing them into a dictionary

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

sys.path.append('../../experiment_setup/python')
from helper import my_print, EscCodes


def main():    
    if len(sys.argv) != 4:
        my_print("usage: python extractDiscretizationThresholds.py char_conf_file_path target_file_path", EscCodes.FAIL)
    else:
        extract_discretization_thresholds(sys.argv[1], sys.argv[2], sys.argv[3])

# python extractDiscretizationThresholds.py "../../circuits/hlth_chain_L_15nm/characterization/" "conf/hlth_inv_chain_L_15nm.cidm.json" "result/hlth_inv_chain_L_15nm_cidm/discretization_thresholds.cidm.json"
# python extractDiscretizationThresholds.py "../../circuits/hlth_chain_L_15nm/characterization/" "conf/hlth_inv_chain_L_15nm.idmstarbwd.json" "result/hlth_inv_chain_L_15nm_idm_star_bwd/discretization_thresholds.idmstarbwd.json"

# python extractDiscretizationThresholds.py "../../circuits/hlth_chain_L_fast_shape_15nm/characterization/" "conf/hlth_inv_chain_L_15nm.cidm.json" "result/hlth_inv_chain_L_15nm_cidm/discretization_thresholds.cidm.json"
# python extractDiscretizationThresholds.py "../../circuits/hlth_chain_L_fast_shape_15nm/characterization/" "conf/hlth_inv_chain_L_15nm.idmstarbwd.json" "result/hlth_inv_chain_L_15nm_idm_star_bwd/discretization_thresholds.idmstarbwd.json"

# python extractDiscretizationThresholds.py "../../circuits/hlth_chain_L_skip_15nm/characterization/" "conf/hlth_inv_chain_L_15nm.cidm.json" "result/hlth_inv_chain_L_15nm_cidm/discretization_thresholds.cidm.json"
# python extractDiscretizationThresholds.py "../../circuits/hlth_chain_L_skip_15nm/characterization/" "conf/hlth_inv_chain_L_15nm.idmstarbwd.json" "result/hlth_inv_chain_L_15nm_idm_star_bwd/discretization_thresholds.idmstarbwd.json"

# python extractDiscretizationThresholds.py "../../circuits/buf_x4_chain_15nm/characterization/" "conf/buf_x4_chain_15nm.idmstarbwd.json" "result/buf_x4_chain_15nm_idm_star_bwd/discretization_thresholds.idmstarbwd.json"

# python extractDiscretizationThresholds.py "../../circuits/inv_x2_chain_15nm/characterization/" "conf/inv_x2_chain_15nm.idmstarbwd.json" "result/inv_x2_chain_15nm_idm_star_bwd/discretization_thresholds.idmstarbwd.json"

# python extractDiscretizationThresholds.py "../../circuits/inv_x2_chain_skip_15nm/characterization/" "conf/inv_x2_chain_15nm.idmstarbwd.json" "result/inv_x2_chain_15nm_idm_star_bwd/discretization_thresholds.idmstarbwd.json"

def extract_discretization_thresholds(root_folder: str, char_conf_file_path: str, target_file_path: str):
    char_conf_file_path = os.path.join(root_folder, char_conf_file_path)
    target_file_path = os.path.join(root_folder, target_file_path)

    char_conf = None
    signal_to_threshold_mapping = dict()
    with open(char_conf_file_path, 'r') as f:
        char_conf = json.load(f)

    for simulation in char_conf['simulations']:

        if 'params' not in simulation:
            # Ignore this simulation (probably cell at the end or beginning)
            continue

        matches = re.match(r"io\s(\d+)\s(\d+)", simulation['params']['io'], re.MULTILINE)
        in_nr = matches[1]
        in_signal = char_conf["signal_mapping"][in_nr]
        out_nr = matches[2]
        out_signal = char_conf["signal_mapping"][out_nr]

        vth_in = None
        if 'results' in simulation and 'vth_in' in simulation['results']:
            vth_in = simulation['results']['vth_in']
        else:
            matches = re.match(r"vth_in\s(.*)", simulation['params']['vth_in'], re.MULTILINE)
            vth_in = float(matches[1])
        
        vth_out = None
        if 'results' in simulation and 'vth_out' in simulation['results']:
            vth_out = simulation['results']['vth_out']
        else:
            matches = re.match(r"vth_out\s(.*)", simulation['params']['vth_out'], re.MULTILINE)
            vth_out = float(matches[1])

        signal_to_threshold_mapping = add_signal(signal_to_threshold_mapping, in_signal, vth_in)
        signal_to_threshold_mapping = add_signal(signal_to_threshold_mapping, out_signal, vth_out)



    with open(target_file_path, 'w') as f:
        json.dump(signal_to_threshold_mapping, f, indent=4)

def add_signal(signal_to_threshold_mapping, signal, vth):
    if signal in signal_to_threshold_mapping:
        assert(signal_to_threshold_mapping[signal] == vth)
    else:
        signal_to_threshold_mapping[signal] = vth

    return signal_to_threshold_mapping


if __name__ == "__main__":
    main()
