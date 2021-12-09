"""
	@file prepareConfig.py

	@brief Generate configuration for characterization

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
import json
import os
import itertools
from difflib import get_close_matches
from typing import Tuple, List, Dict, Set
from anytree import Node, PreOrderIter
from anytree.exporter import JsonExporter, DictExporter
sys.path.append('../../experiment_setup/python')
from extractCircuitStructure import read_circuit_structure, CircuitStructure, Interconnect
from helper import my_print, EscCodes
sys.path.append('../fitting')
from fitting import FittingType


# python prepareConfig.py "../../circuits/hlth_chain_L_15nm/characterization/" "circuit/hlth_inv_chain_L_15nm.structure.json" "conf/hlth_inv_chain_L_15nm.idmplusbwd.json" "conf/spice_var_names.json" idm_plus_bwd
# python prepareConfig.py "../../circuits/hlth_chain_L_15nm/characterization/" "circuit/hlth_inv_chain_L_15nm.structure.json" "conf/hlth_inv_chain_L_15nm.cidm.json" "conf/spice_var_names.json" cidm
# python prepareConfig.py "../../circuits/hlth_chain_L_15nm/characterization/" "circuit/hlth_inv_chain_L_15nm.structure.json" "conf/hlth_inv_chain_L_15nm.idmstarbwd.json" "conf/spice_var_names.json" idm_star_bwd

# python prepareConfig.py "../../circuits/hlth_chain_L_skip_15nm/characterization/" "circuit/hlth_inv_chain_L_15nm.structure.json" "conf/hlth_inv_chain_L_15nm.idmplusbwd.json" "conf/spice_var_names.json" idm_plus_bwd
# python prepareConfig.py "../../circuits/hlth_chain_L_skip_15nm/characterization/" "circuit/hlth_inv_chain_L_15nm.structure.json" "conf/hlth_inv_chain_L_15nm.cidm.json" "conf/spice_var_names.json" cidm
# python prepareConfig.py "../../circuits/hlth_chain_L_skip_15nm/characterization/" "circuit/hlth_inv_chain_L_15nm.structure.json" "conf/hlth_inv_chain_L_15nm.idmstarbwd.json" "conf/spice_var_names.json" idm_star_bwd

# python prepareConfig.py "../../circuits/mips_clock_15nm/characterization/" "circuit/mips_clock_15nm.structure.json" "conf/mips_clock_15nm.idmplusbwd.json" "conf/spice_var_names.json" idm_plus_bwd
# python prepareConfig.py "../../circuits/mips_clock_15nm/characterization/" "circuit/mips_clock_15nm.structure.json" "conf/mips_clock_15nm.cidm.json" "conf/spice_var_names.json" cidm
# python prepareConfig.py "../../circuits/mips_clock_15nm/characterization/" "circuit/mips_clock_15nm.structure.json" "conf/mips_clock_15nm.idmstarfwd.json" "conf/spice_var_names.json" idm_star_fwd

# python prepareConfig.py "../../circuits/inv_x2_chain_15nm/characterization/" "circuit/inv_x2_chain_15nm.structure.json" "conf/inv_x2_chain_15nm.idmplusbwd.json" "conf/spice_var_names.json" idm_plus_bwd
# python prepareConfig.py "../../circuits/inv_x2_chain_15nm/characterization/" "circuit/inv_x2_chain_15nm.structure.json" "conf/inv_x2_chain_15nm.cidm.json" "conf/spice_var_names.json" cidm
# python prepareConfig.py "../../circuits/inv_x2_chain_15nm/characterization/" "circuit/inv_x2_chain_15nm.structure.json" "conf/inv_x2_chain_15nm.idmstarbwd.json" "conf/spice_var_names.json" idm_star_bwd
# python prepareConfig.py "../../circuits/inv_x2_chain_15nm/characterization/" "circuit/inv_x2_chain_15nm.structure.json" "conf/inv_x2_chain_15nm.idmstarfwd.json" "conf/spice_var_names.json" idm_star_fwd

# python prepareConfig.py "../../circuits/inv_x2_chain_skip_15nm/characterization/" "circuit/inv_x2_chain_15nm.structure.json" "conf/inv_x2_chain_15nm.idmplusbwd.json" "conf/spice_var_names.json" idm_plus_bwd
# python prepareConfig.py "../../circuits/inv_x2_chain_skip_15nm/characterization/" "circuit/inv_x2_chain_15nm.structure.json" "conf/inv_x2_chain_15nm.cidm.json" "conf/spice_var_names.json" cidm
# python prepareConfig.py "../../circuits/inv_x2_chain_skip_15nm/characterization/" "circuit/inv_x2_chain_15nm.structure.json" "conf/inv_x2_chain_15nm.idmstarbwd.json" "conf/spice_var_names.json" idm_star_bwd

# python prepareConfig.py "../../circuits/buf_x4_chain_15nm/characterization/" "circuit/buf_x4_chain_15nm.structure.json" "conf/buf_x4_chain_15nm.idmplusbwd.json" "conf/spice_var_names.json" idm_plus_bwd
# python prepareConfig.py "../../circuits/buf_x4_chain_15nm/characterization/" "circuit/buf_x4_chain_15nm.structure.json" "conf/buf_x4_chain_15nm.cidm.json" "conf/spice_var_names.json" cidm
# python prepareConfig.py "../../circuits/buf_x4_chain_15nm/characterization/" "circuit/buf_x4_chain_15nm.structure.json" "conf/buf_x4_chain_15nm.idmstarbwd.json" "conf/spice_var_names.json" idm_star_bwd
def main():
	if len(sys.argv) != 6: 
		my_print("usage: python prepareConfig.py root_folder circuit_structure_file_path config_output_file_path spice_var_names_path fitting_type", EscCodes.FAIL)
	else:
		prepare_config(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])	

def prepare_config(root_folder: str, circuit_structure_file_path: str, config_output_file_path: str, spice_var_names_path: str, fitting_type : str) -> None:
	circuit_structure_file_path = os.path.join(root_folder, circuit_structure_file_path)
	config_output_file_path = os.path.join(root_folder, config_output_file_path)
	spice_var_names_path = os.path.join(root_folder, spice_var_names_path)
	fitting_type = FittingType(fitting_type)
	v_th = 0.4 # TODO send via command line if required
	
	spice_config = dict()
	with open(spice_var_names_path, 'r') as f:
		spice_config = json.load(f)

	circuit_structure = read_circuit_structure(circuit_structure_file_path)

	# Build pairs which should be characterized (basically all interconnects from -> from)
	ignore_interconnects = list()
	if 'ignore_interconnects' in spice_config:
		for interconnect in spice_config['ignore_interconnects']:
			ignore_interconnects.append(Interconnect(**interconnect))

	ignore_pairs = list()
	if 'ignore_pairs' in spice_config:
		for pair in spice_config['ignore_pairs']:
			ignore_pairs.append((pair[0], pair[1]))

	pairs, pair_to_cellname = build_pairs(circuit_structure, ignore_pairs)

	# print("Pairs: ")
	# for pair in pairs:
	# 	print(pair)

	# We need to match the instances of the pairs with the actual names in SPICE (best effort, some manual adaption might be necessary...)
	spice_matching = match_with_spice(set(itertools.chain(*pairs)), spice_config['var_names'])

	# print("Spice matching: ", spice_matching)

	# Build probe string and create dictionary between probe and number
	(probe_string, order_string, description_string, probe_to_nr) = build_probe_string(pairs, spice_matching)

	# print("Probe Nr: ")
	# idx = 1
	# for probe_nr in probe_to_nr:
	# 	print(idx, probe_nr)
	# 	idx = idx + 1

	replacements = dict()	
	replacements['io'] = "io x y"
	replacements['cellName'] = "cellName x"
	replacements['vth_in'] = "vth_in x"
	replacements['vth_out'] = "vth_out x"

	# Now we need to generate a list of simulations (one element for each pair)
	simulations = list()

	input_probe_to_pair_id = dict()
	output_probe_to_pair_id = dict()
	pair_id_to_output_probe = dict()

	for pair_id, pair in enumerate(pairs):
		# Each simulation itself is a list 
		start = pair[0]
		stop = pair[1]
		simulation = dict()
		simulation['params'] = dict()

		input_probe = probe_to_nr[start] + 1
		output_probe = probe_to_nr[stop] + 1
		if input_probe not in input_probe_to_pair_id:
			input_probe_to_pair_id[input_probe] = list()
		input_probe_to_pair_id[input_probe].append(pair_id) # Must be a list since we can have forks
		output_probe_to_pair_id[output_probe] = pair_id # Assume only one output per cell
		pair_id_to_output_probe[pair_id] = output_probe # Each pair has exactly on output

		simulation['params']['io'] = "io {x} {y}".format(x = input_probe, y = output_probe)
		simulation['params']['cellName'] = "cellName {name}".format(name = pair_to_cellname[pair])

		v_th_in = None
		v_th_out = None
		if fitting_type == FittingType.CIDM:
			v_th_in = v_th
			v_th_out = v_th
		elif fitting_type == FittingType.IDM_PLUS_FWD:
			v_th_in = v_th
			v_th_out = -1
		elif fitting_type == FittingType.IDM_PLUS_BWD:
			v_th_in = -1
			v_th_out = 0.4
		elif fitting_type == FittingType.IDM_STAR_FWD or fitting_type == FittingType.IDM_STAR_BWD:
			# Only set all inputs or outputs to v_th once we know the dependency graph
			v_th_in = -1
			v_th_out = -1
		else:
			assert(False)

		simulation['params']['vth_in'] = "vth_in {val}".format(val = v_th_in)
		simulation['params']['vth_out'] = "vth_out {val}".format(val = v_th_out)

		simulations.append(simulation)
	
	# Now we need to find the input probe key which is not in the output dict
	# This must be the input, and we assume that there is only one input, 
	# since we are using single input gates, and therefore multiple inputs 
	# would lead to completely separated circuits)
	start_probe = None
	for probe in input_probe_to_pair_id:
		if probe not in output_probe_to_pair_id:
			# This should be the start
			assert(not start_probe)
			start_probe = probe

	dependency_tree = build_dependency_tree(Node("Top"), start_probe, input_probe_to_pair_id, pair_id_to_output_probe)

	if fitting_type == FittingType.IDM_STAR_FWD:
		for child in dependency_tree.children:
			simulations[child.name]['params']['vth_in'] = "vth_in {val}".format(val = v_th)

	if fitting_type == FittingType.IDM_STAR_BWD:
		for leaf in PreOrderIter(dependency_tree, filter_=lambda node: node.is_leaf):
			simulations[leaf.name]['params']['vth_out'] =  "vth_out {val}".format(val = v_th)


	exporter = DictExporter()
	dependency_tree_dict = exporter.export(dependency_tree)

	config = dict()
	config['replacements'] = replacements
	config['simulations'] = simulations
	config['dependency_tree'] = dependency_tree_dict
	config['signal_mapping'] = {v + 1: k for k, v in probe_to_nr.items()}


	with open(config_output_file_path, 'w') as f:
		json.dump(config, f, indent=4)

	# String needs to be replaced in Spice file
	print(probe_string)
	print(order_string)
	print(description_string)
	print("c {length}".format(length = len(probe_to_nr) + 1))	

class ConfigJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Node):
			exporter = JsonExporter(indent=2, sort_keys=True)
			return exporter.export(obj)
		# Let the base class default method raise the TypeError
		return json.JSONEncoder.default(self, obj)
	
def build_dependency_tree(parent: Node, current_probe, input_probe_to_pair_id, pair_id_to_output_probe) -> Node:
	if current_probe not in input_probe_to_pair_id:
		return parent # End of recursion
	
	# Need to add all pair_ids to the tree
	for pair_id in input_probe_to_pair_id[current_probe]:
		child = Node(pair_id, parent = parent)
		child = build_dependency_tree(child, pair_id_to_output_probe[pair_id], input_probe_to_pair_id, pair_id_to_output_probe)

	return parent


def match_with_spice(probes: set, spice_var_names: list) -> Dict:
	matching = dict()

	spice_var_names =  [x.lower() for x in spice_var_names]

	

	for probe in probes:
		probe_mod = ("v(" + probe + ")").lower()
		matches = get_close_matches(probe_mod, spice_var_names, n=3, cutoff=0.75)

		# print(probe, matches)

		if len(matches) >  0:
			matching[probe] = matches[0]
		else:
			# These matchings need manual postprocessing
			matching[probe] = probe + "TODO"


		# for match in matches:
		# 	print("score for: " + match + " vs. " + probe + " = " + str(SequenceMatcher(None, match, probe).ratio()))		

	# print(matching)

	return matching

def build_pairs(circuit_structure: CircuitStructure, ignore_pairs: List) -> Tuple[Set[str], Dict[str, str]]:
	pairs = set()
	pair_to_cellname = dict()

	for interconnect1 in circuit_structure.interconnects:
		# Last element, do not add a pair, since it is already included in the predecessor
		if interconnect1.to_port == "None":
			continue

		# if ignore_interconnects and interconnect1 in ignore_interconnects:
		# 	print("Ignore: ", interconnect1)
		# 	continue

		start = build_probe(interconnect1.from_instance, interconnect1.from_port)
		# we need to find for the to_insance the interconnect where it is used as from_instance
		successor = None
		for interconnect2 in circuit_structure.interconnects:
			if interconnect1.to_instance == interconnect2.from_instance:
				successor = interconnect2
				# We do not break here, since there might be multiple successors

				stop = None
				if successor.to_port != "":
					# not last element 								
					stop = build_probe(successor.from_instance, successor.from_port)   
				else:
					# last element
					stop = build_probe(successor.to_instance, successor.to_port)     
				pair = (start, stop) 
				# Remove all pairs that should be ignored
				if pair in ignore_pairs:
					continue

				pairs.add(pair)			

				pair_to_cellname[pair] = interconnect1.to_instance 


	return (pairs, pair_to_cellname)


def build_probe_string(pairs: set, spice_matching: Dict[str, str]) -> Tuple[str, str, str, Dict[str, str]]:
	probes = set()
	for pair in pairs:
		for elem in [pair[0], pair[1]]:
			if not elem in probes:
				probes.add(elem)

	probe_string = ".PROBE TRAN "
	order_string = "o "
	description_string = "d time "
	matching = dict()
	# Sorting the probes is important since we always want to have the same order
	for probe in sorted(probes):

		spice_var_name = spice_matching[probe]

		matching[probe] = len(matching)
		probe_string = probe_string + "{probe} ".format(probe = spice_var_name)
		order_string = order_string + "{desc} ".format(desc = spice_var_name)
		description_string = description_string + "{desc} ".format(desc = remove_special_chars(spice_var_name))
		

	return (probe_string, order_string, description_string, matching)

def build_probe(instance: str, port: str) -> str:
    probe = instance
    if port:
        probe = probe + ":" + port
    return probe

def remove_special_chars(value):
	special_chars = ['(', ')', ':', '[', ']', '.']
	for c in special_chars:
		value = str(value).replace(c, "")	
		
	return value


if __name__ == "__main__":
    main()
