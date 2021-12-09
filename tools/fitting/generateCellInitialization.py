"""
    @file generateCellInitialization.py

	@brief Script for updating the init section of a structure file

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
from anytree.importer import DictImporter
from anytree import PreOrderIter

from fittingHelper import find_cell_in_structure, get_cellname

sys.path.append('../../experiment_setup/python')
from helper import my_print, EscCodes, to_bool
from readGateCfg import read_gate_config
from generateGates import find_pred_interconnect
from extractCircuitStructure import read_circuit_structure, save_circuit_structure

# python generateCellInitialization.py ../../circuits/mips_clock_15nm/ characterization/conf/mips_clock_15nm.cidm.json structure.json ../gate_config.json gate_config.json 0

def main():    
    if len(sys.argv) != 7:
        my_print("usage: python generateCellInitialization.py circuit_folder characterization_conf_file_path structure_file_path default_gate_config_file_path circuit_gate_config_file_path start_value", EscCodes.FAIL)
    else:
        generate_cell_initialization(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

def generate_cell_initialization(circuit_folder, characterization_conf_file_path, structure_file_path, default_gate_config_file_path, circuit_gate_config_file_path, start_value):
    characterization_conf_file_path =  os.path.join(circuit_folder, characterization_conf_file_path)
    structure_file_path =  os.path.join(circuit_folder, structure_file_path)
    default_gate_config_file_path =  os.path.join(circuit_folder, default_gate_config_file_path)
    circuit_gate_config_file_path =  os.path.join(circuit_folder, circuit_gate_config_file_path)
    start_value = str(start_value)

    init_mapping = dict()

    # Need to read the characterization file
    char_conf = None
    with open(characterization_conf_file_path) as json_file:
        char_conf = json.load(json_file)

    # Need to read structure file
    structure = read_circuit_structure(structure_file_path)

    # Need to read the gate config file, to check which gate type we have
    gate_config = read_gate_config(default_gate_config_file_path, circuit_gate_config_file_path)

    # Traverse over the dependeny tree and fill out init mapping
    importer = DictImporter()
    dependency_tree = importer.import_(char_conf['dependency_tree'])
    for node in PreOrderIter(dependency_tree):	        
        if node.name == 'Top':
            continue

        cellname = get_cellname(char_conf, node.name)

        # Now use the cellname to find the cell_type in the structure.json file

        found_cell = find_cell_in_structure(structure, cellname)
        assert(found_cell)

        # Now we use the cell_type and find the function in the gate config
        gate = gate_config[found_cell.cell_type]
        # print(node.name, cellname, found_cell, gate, gate.function)

        assert(gate.function == "not" or gate.function == "")
        input_found_cell = gate.inputs
        assert(len(input_found_cell) == 1)
        input_found_cell = input_found_cell[0]

        # We need to find the predecessor and get the output value of the predecessor
        pred = find_pred_interconnect(structure, found_cell, input_found_cell)
        print(pred, cell)

        # Get the value of the predecessor from the dict
        in_value = None
        if pred.from_instance in init_mapping:
            in_value = init_mapping[pred.from_instance]
        else:
            in_value = start_value

        in_value = to_bool(in_value)
        logic_function = None
        if gate.function == "not":
            logic_function = my_not
        elif gate.funtion == "":
            logic_function = my_id
        else:
            assert(False)

        init_mapping[cell.instance] = bool_to_logic(logic_function(in_value))       
    

    # Write the init mapping to the structure file and save it
    structure.init = init_mapping
    save_circuit_structure(structure_file_path, structure)

def bool_to_logic(val):
    return "1" if val else "0"


def my_not(a):
    return not a

def my_id(a):
    return a

if __name__ == "__main__":
    main()