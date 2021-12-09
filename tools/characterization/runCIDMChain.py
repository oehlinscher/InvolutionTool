"""
    @file runCIDMChain.py

	@brief Script for configuration of the characterization script

	@author Daniel OEHLINGER <d.oehlinger@outlook.com>
	@author Juergen MAIER <juergen.maier@tuwien.ac.at>
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
from anytree.importer import DictImporter
from anytree import Node, PreOrderIter, PostOrderIter
from CIDMchar import generate_involution_fully_automatic
sys.path.append('../../experiment_setup/python')
from helper import my_print, EscCodes

sys.path.append('../fitting')
from fitting import FittingType

# python runCIDMChain.py ../../circuits/buf_x4_chain_15nm/characterization/ conf/buf_x4_chain_15nm.temp conf/buf_x4_chain_15nm.conf conf/buf_x4_chain_15nm.idmplusbwd.json buf_x4_chain_15nm_idm_plus_bwd/ idm_plus_bwd
# python runCIDMChain.py ../../circuits/buf_x4_chain_15nm/characterization/ conf/buf_x4_chain_15nm.temp conf/buf_x4_chain_15nm.conf conf/buf_x4_chain_15nm.cidm.json buf_x4_chain_15nm_cidm/ cidm
# python runCIDMChain.py ../../circuits/buf_x4_chain_15nm/characterization/ conf/buf_x4_chain_15nm.temp conf/buf_x4_chain_15nm.conf conf/buf_x4_chain_15nm.idmstarbwd.json buf_x4_chain_15nm_idm_star_bwd/ idm_star_bwd

# python runCIDMChain.py ../../circuits/hlth_chain_L_15nm/characterization/ conf/hlth_inv_chain_L_15nm.temp conf/hlth_inv_chain_L_15nm.conf conf/hlth_inv_chain_L_15nm.idmplusbwd.json hlth_inv_chain_L_15nm_idm_plus_bwd/ idm_plus_bwd
# python runCIDMChain.py ../../circuits/hlth_chain_L_15nm/characterization/ conf/hlth_inv_chain_L_15nm.temp conf/hlth_inv_chain_L_15nm.conf conf/hlth_inv_chain_L_15nm.cidm.json hlth_inv_chain_L_15nm_cidm/ cidm
# python runCIDMChain.py ../../circuits/hlth_chain_L_15nm/characterization/ conf/hlth_inv_chain_L_15nm.temp conf/hlth_inv_chain_L_15nm.conf conf/hlth_inv_chain_L_15nm.idmstarbwd.json hlth_inv_chain_L_15nm_idm_star_bwd/ idm_star_bwd

# python runCIDMChain.py ../../circuits/hlth_chain_L_fast_shape_15nm/characterization/ conf/hlth_inv_chain_L_15nm.temp conf/hlth_inv_chain_L_15nm.conf conf/hlth_inv_chain_L_15nm.idmplusbwd.json hlth_inv_chain_L_15nm_idm_plus_bwd/ idm_plus_bwd
# python runCIDMChain.py ../../circuits/hlth_chain_L_fast_shape_15nm/characterization/ conf/hlth_inv_chain_L_15nm.temp conf/hlth_inv_chain_L_15nm.conf conf/hlth_inv_chain_L_15nm.cidm.json hlth_inv_chain_L_15nm_cidm/ cidm
# python runCIDMChain.py ../../circuits/hlth_chain_L_fast_shape_15nm/characterization/ conf/hlth_inv_chain_L_15nm.temp conf/hlth_inv_chain_L_15nm.conf conf/hlth_inv_chain_L_15nm.idmstarbwd.json hlth_inv_chain_L_15nm_idm_star_bwd/ idm_star_bwd

# python runCIDMChain.py ../../circuits/inv_x2_chain_15nm/characterization/ conf/inv_x2_chain_15nm.temp conf/inv_x2_chain_15nm.conf conf/inv_x2_chain_15nm.idmplusbwd.json inv_x2_chain_15nm_idm_plus_bwd/ idm_plus_bwd
# python runCIDMChain.py ../../circuits/inv_x2_chain_15nm/characterization/ conf/inv_x2_chain_15nm.temp conf/inv_x2_chain_15nm.conf conf/inv_x2_chain_15nm.cidm.json inv_x2_chain_15nm_cidm/ cidm
# python runCIDMChain.py ../../circuits/inv_x2_chain_15nm/characterization/ conf/inv_x2_chain_15nm.temp conf/inv_x2_chain_15nm.conf conf/inv_x2_chain_15nm.idmstarbwd.json inv_x2_chain_15nm_idm_star_bwd/ idm_star_bwd
# python runCIDMChain.py ../../circuits/inv_x2_chain_15nm/characterization/ conf/inv_x2_chain_15nm.temp conf/inv_x2_chain_15nm.conf conf/inv_x2_chain_15nm.idmstarfwd.json inv_x2_chain_15nm_idm_star_fwd/ idm_star_fwd

####
# python runCIDMChain.py ../../circuits/inv_x2_chain_skip_15nm/characterization/ conf/inv_x2_chain_15nm.temp conf/inv_x2_chain_15nm.conf conf/inv_x2_chain_15nm.idmplusbwd.json inv_x2_chain_15nm_idm_plus_bwd/ idm_plus_bwd
# python runCIDMChain.py ../../circuits/inv_x2_chain_skip_15nm/characterization/ conf/inv_x2_chain_15nm.temp conf/inv_x2_chain_15nm.conf conf/inv_x2_chain_15nm.cidm.json inv_x2_chain_15nm_cidm/ cidm
# python runCIDMChain.py ../../circuits/inv_x2_chain_skip_15nm/characterization/ conf/inv_x2_chain_15nm.temp conf/inv_x2_chain_15nm.conf conf/inv_x2_chain_15nm.idmstarbwd.json inv_x2_chain_15nm_idm_star_bwd/ idm_star_bwd

####
# python runCIDMChain.py ../../circuits/hlth_chain_L_skip_15nm/characterization/ conf/hlth_inv_chain_L_15nm.temp conf/hlth_inv_chain_L_15nm.conf conf/hlth_inv_chain_L_15nm.idmplusbwd.json hlth_inv_chain_L_15nm_idm_plus_bwd/ idm_plus_bwd
# python runCIDMChain.py ../../circuits/hlth_chain_L_skip_15nm/characterization/ conf/hlth_inv_chain_L_15nm.temp conf/hlth_inv_chain_L_15nm.conf conf/hlth_inv_chain_L_15nm.cidm.json hlth_inv_chain_L_15nm_cidm/ cidm
# python runCIDMChain.py ../../circuits/hlth_chain_L_skip_15nm/characterization/ conf/hlth_inv_chain_L_15nm.temp conf/hlth_inv_chain_L_15nm.conf conf/hlth_inv_chain_L_15nm.idmstarbwd.json hlth_inv_chain_L_15nm_idm_star_bwd/ idm_star_bwd

####
# python runCIDMChain.py ../../circuits/mips_clock_15nm/characterization/ conf/mips_clock_15nm.temp conf/mips_clock_15nm.conf conf/mips_clock_15nm.idmplusbwd.json mips_clock_15nm_idm_plus_bwd/ idm_plus_bwd
# python runCIDMChain.py ../../circuits/mips_clock_15nm/characterization/ conf/mips_clock_15nm.temp conf/mips_clock_15nm.conf conf/mips_clock_15nm.cidm.json mips_clock_15nm_cidm/ cidm
# python runCIDMChain.py ../../circuits/mips_clock_15nm/characterization/ conf/mips_clock_15nm.temp conf/mips_clock_15nm.conf conf/mips_clock_15nm.idmstarfwd.json mips_clock_15nm_idm_star_fwd/ idm_star_fwd



def main():
	if len(sys.argv) != 7: 
		my_print("usage: python runCIDMChain.py circuit_folder conf_template_file conf_output_file conf_cell_file sub_folder fitting_type", EscCodes.FAIL)
	else:
		run_cidm_chain(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])	


def run_cidm_chain(circuit_folder, conf_template_file, conf_output_file, conf_cell_file, sub_folder, fitting_type):
	conf_template_file = os.path.join(circuit_folder, conf_template_file)
	conf_output_file = os.path.join(circuit_folder, conf_output_file)
	conf_cell_file = os.path.join(circuit_folder, conf_cell_file)
	fitting_type = FittingType(fitting_type)

	with open(conf_cell_file) as json_file:
		data = json.load(json_file)

	# instead of generating a deepcopy for the results dictionary
	with open(conf_cell_file) as json_file:
		data_results = json.load(json_file)

	simulations = data['simulations']
	simulation_results = data_results['simulations']
	replacements = data['replacements']
	dependency_tree_dict = data['dependency_tree']
	importer = DictImporter()
	dependency_tree = importer.import_(dependency_tree_dict)

	# IDM_STAR_FWD and IDM_STAR_BWD must have a dependency tree
	assert(not(fitting_type == FittingType.IDM_STAR_FWD or fitting_type == FittingType.IDM_STAR_BWD) or dependency_tree)

	if not dependency_tree:
		dependency_tree = Node("Top")
		for idx, simulation in enumerate(simulations):
			Node(idx, parent = dependency_tree)

	traverse_order = PreOrderIter
	if fitting_type == FittingType.IDM_STAR_BWD:
		traverse_order = PostOrderIter

	counter = 0

	simulate_all = True

	if simulate_all:
		for node in traverse_order(dependency_tree):		
			if node.name == 'Top':
				continue
			
			counter = counter + 1

			print("===========================")
			print("Progress: {counter}/{total}".format(counter = counter, total = len(simulations)))
			print("===========================")

			# counter = counter + 1
			# if counter == 4:
			# 	break

			simulation = simulations[node.name]

			print(node.name, simulation)

			perform_simulation(simulation, conf_template_file, conf_output_file, replacements, circuit_folder, sub_folder, fitting_type, simulations, simulation_results, node, conf_cell_file, data)
	else:
		node_ids = [76, 126]
		for node_id in node_ids:
			simulation = simulations[node_id]
			node = None		
			for n in traverse_order(dependency_tree):		
				if n.name == node_id:
					node = n
					break
			print(node.name, simulation)
			perform_simulation(simulation, conf_template_file, conf_output_file, replacements, circuit_folder, sub_folder, fitting_type, simulations, simulation_results, node, conf_cell_file, data)

def perform_simulation(simulation, conf_template_file, conf_output_file, replacements, circuit_folder, sub_folder, fitting_type, simulations, simulation_results, node, conf_cell_file, data):
	with open(conf_template_file, 'r') as fin:
		with open(conf_output_file, 'w') as fout:    
			for line in fin.readlines():
				for repl_key, repl_value in replacements.items():
					line = line.replace(repl_value, simulation['params'][repl_key])

				fout.write(line)

	(vth_in, vth_out, dmin, deltas) = generate_involution_fully_automatic(circuit_folder, conf_output_file, sub_folder)

	if fitting_type == FittingType.IDM_STAR_BWD:
		parent = node.parent.name
		simulations[node.name]['params']['vth_in'] = "vth_in {val}".format(val = vth_in)	
		simulation_results[node.name] = add_results_dict(simulation_results[node.name])
		simulation_results[node.name]['results']['vth_in'] = vth_in	
		# We need to adapt the parents appropriately
		if parent != "Top":
			simulations[parent]['params']['vth_out'] = "vth_out {val}".format(val = vth_in)	
			simulation_results[parent] = add_results_dict(simulation_results[parent])
			simulation_results[parent]['results']['vth_out'] = vth_in
		
		update_simulations(conf_cell_file, data, simulation_results)


	if fitting_type == FittingType.IDM_STAR_FWD:
		simulations[node.name]['params']['vth_out'] = "vth_out {val}".format(val = vth_out)	
		simulation_results[node.name] = add_results_dict(simulation_results[node.name])
		simulation_results[node.name]['results']['vth_out'] = vth_out
		# We need to adapt the childs appropriately
		for child in node.children:
			child = child.name
			simulations[child]['params']['vth_in'] = "vth_in {val}".format(val = vth_out)	
			simulation_results[child] = add_results_dict(simulation_results[child])
			simulation_results[child]['results']['vth_in'] = vth_out
		update_simulations(conf_cell_file, data, simulation_results)
		
def add_results_dict(simulation_dict: dict):	
	if not 'results' in simulation_dict:
		simulation_dict['results'] = dict()

	return simulation_dict

def update_simulations(conf_cell_file, config, simulations):	
	config['simulations'] = simulations
	with open(conf_cell_file, 'w') as f:
		json.dump(config, f, indent=4)		


if __name__ == "__main__":
	main()
