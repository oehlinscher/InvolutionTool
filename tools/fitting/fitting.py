"""
    @file fitting.py

	@brief Script for fitting the parameters for various 
    switching waveforms, based on the results of the 
    characterization script

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
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import json
import re
from json import JSONEncoder
from enum import Enum
from pathlib import Path
import matplotlib.pyplot as plt
from lmfit import minimize, Parameters, fit_report

sys.path.append('../../experiment_setup/python')
from extractCircuitStructure import read_circuit_structure, CircuitStructureEncoder
from readGateCfg import ChannelType
from helper import my_print, EscCodes, to_bool

sys.path.append('../../experiment_setup/vhdl/python_channel')
from sumexp_delay_channel import calc_c_up, calc_c_do, delta_sumexp_up, delta_sumexp_do
from exp_delay_channel import calc_tau_up, calc_tau_do, delta_exp_up, delta_exp_do


class FittingType(Enum):
    CIDM = "cidm"
    IDM_PLUS_FWD = "idm_plus_fwd"
    IDM_PLUS_BWD = "idm_plus_bwd"
    IDM_STAR_FWD = "idm_star_fwd"
    IDM_STAR_BWD = "idm_star_bwd"

    def __str__(self):
        return str(self.value)


#  TODO: Configure
v_dd = 0.8
v_th = 0.4

def main():    
    if len(sys.argv) != 9 and len(sys.argv) != 10:
        my_print("usage: python fitting.py circuit_folder data_folder result_folder fitting_type channel_type structure_file_path sdf_file_path instance_mapping_file_path", EscCodes.FAIL)
    else:
        disable_fitting = False
        if (len(sys.argv) == 10):
            disable_fitting = to_bool(sys.argv[9])

        run_fitting(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], disable_fitting)

# python fitting.py ../../circuits/inv_x2_chain_15nm/ characterization/data/inv_x2_chain_15nm_idm_plus_bwd characterization/result/inv_x2_chain_15nm_idm_plus_bwd idm_plus_bwd EXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/inv_x2_chain_15nm/ characterization/data/inv_x2_chain_15nm_idm_star_bwd characterization/result/inv_x2_chain_15nm_idm_star_bwd idm_star_bwd EXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/inv_x2_chain_15nm/ characterization/data/inv_x2_chain_15nm_cidm characterization/result/inv_x2_chain_15nm_cidm cidm EXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json 

# python fitting.py ../../circuits/hlth_chain_L_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_plus_bwd characterization/result/hlth_inv_chain_L_15nm_idm_plus_bwd idm_plus_bwd EXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 
# python fitting.py ../../circuits/hlth_chain_L_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_star_bwd characterization/result/hlth_inv_chain_L_15nm_idm_star_bwd idm_star_bwd EXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 
# python fitting.py ../../circuits/hlth_chain_L_15nm/ characterization/data/hlth_inv_chain_L_15nm_cidm characterization/result/hlth_inv_chain_L_15nm_cidm cidm EXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 

# python fitting.py ../../circuits/hlth_chain_L_fast_shape_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_plus_bwd characterization/result/hlth_inv_chain_L_15nm_idm_plus_bwd idm_plus_bwd EXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 
# python fitting.py ../../circuits/hlth_chain_L_fast_shape_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_star_bwd characterization/result/hlth_inv_chain_L_15nm_idm_star_bwd idm_star_bwd EXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 
# python fitting.py ../../circuits/hlth_chain_L_fast_shape_15nm/ characterization/data/hlth_inv_chain_L_15nm_cidm characterization/result/hlth_inv_chain_L_15nm_cidm cidm EXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 


# python fitting.py ../../circuits/buf_x4_chain_15nm/ characterization/data/buf_x4_chain_15nm_idm_plus_bwd characterization/result/buf_x4_chain_15nm_idm_plus_bwd idm_plus_bwd EXP_CHANNEL structure.json buf_x4_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/buf_x4_chain_15nm/ characterization/data/buf_x4_chain_15nm_idm_star_bwd characterization/result/buf_x4_chain_15nm_idm_star_bwd idm_star_bwd EXP_CHANNEL structure.json buf_x4_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/buf_x4_chain_15nm/ characterization/data/buf_x4_chain_15nm_cidm characterization/result/buf_x4_chain_15nm_cidm cidm EXP_CHANNEL structure.json buf_x4_chain.sdf instance_mapping.json 

####
# python fitting.py ../../circuits/inv_x2_chain_skip_15nm/ characterization/data/inv_x2_chain_15nm_idm_plus_bwd characterization/result/inv_x2_chain_15nm_idm_plus_bwd_exp idm_plus_bwd EXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/inv_x2_chain_skip_15nm/ characterization/data/inv_x2_chain_15nm_idm_plus_bwd characterization/result/inv_x2_chain_15nm_idm_plus_bwd_sumexp_fitting idm_plus_bwd SUMEXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/inv_x2_chain_skip_15nm/ characterization/data/inv_x2_chain_15nm_idm_plus_bwd characterization/result/inv_x2_chain_15nm_idm_plus_bwd_sumexp_nofitting idm_plus_bwd SUMEXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json  True

# python fitting.py ../../circuits/inv_x2_chain_skip_15nm/ characterization/data/inv_x2_chain_15nm_idm_star_bwd characterization/result/inv_x2_chain_15nm_idm_star_bwd_exp idm_star_bwd EXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/inv_x2_chain_skip_15nm/ characterization/data/inv_x2_chain_15nm_idm_star_bwd characterization/result/inv_x2_chain_15nm_idm_star_bwd_sumexp_fitting idm_star_bwd SUMEXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/inv_x2_chain_skip_15nm/ characterization/data/inv_x2_chain_15nm_idm_star_bwd characterization/result/inv_x2_chain_15nm_idm_star_bwd_sumexp_nofitting idm_star_bwd SUMEXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json True

# python fitting.py ../../circuits/inv_x2_chain_skip_15nm/ characterization/data/inv_x2_chain_15nm_cidm characterization/result/inv_x2_chain_15nm_cidm_exp cidm EXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/inv_x2_chain_skip_15nm/ characterization/data/inv_x2_chain_15nm_cidm characterization/result/inv_x2_chain_15nm_cidm_sumexp_fitting cidm SUMEXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json 
# python fitting.py ../../circuits/inv_x2_chain_skip_15nm/ characterization/data/inv_x2_chain_15nm_cidm characterization/result/inv_x2_chain_15nm_cidm_sumexp_nofitting cidm SUMEXP_CHANNEL structure.json inv_x2_chain.sdf instance_mapping.json True

####
# python fitting.py ../../circuits/hlth_chain_L_skip_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_plus_bwd characterization/result/hlth_inv_chain_L_15nm_idm_plus_bwd_exp idm_plus_bwd EXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 
# python fitting.py ../../circuits/hlth_chain_L_skip_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_plus_bwd characterization/result/hlth_inv_chain_L_15nm_idm_plus_bwd_sumexp idm_plus_bwd SUMEXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 
# python fitting.py ../../circuits/hlth_chain_L_skip_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_plus_bwd characterization/result/hlth_inv_chain_L_15nm_idm_plus_bwd_sumexp_nofitting idm_plus_bwd SUMEXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json True

# python fitting.py ../../circuits/hlth_chain_L_skip_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_star_bwd characterization/result/hlth_inv_chain_L_15nm_idm_star_bwd_exp idm_star_bwd EXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 
# python fitting.py ../../circuits/hlth_chain_L_skip_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_star_bwd characterization/result/hlth_inv_chain_L_15nm_idm_star_bwd_sumexp idm_star_bwd SUMEXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json
# python fitting.py ../../circuits/hlth_chain_L_skip_15nm/ characterization/data/hlth_inv_chain_L_15nm_idm_star_bwd characterization/result/hlth_inv_chain_L_15nm_idm_star_bwd_sumexp_nofitting idm_star_bwd SUMEXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json True

# python fitting.py ../../circuits/hlth_chain_L_skip_15nm/ characterization/data/hlth_inv_chain_L_15nm_cidm characterization/result/hlth_inv_chain_L_15nm_cidm_exp cidm EXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json 
# python fitting.py ../../circuits/hlth_chain_L_skip_15nm/ characterization/data/hlth_inv_chain_L_15nm_cidm characterization/result/hlth_inv_chain_L_15nm_cidm_sumexp cidm SUMEXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json
# python fitting.py ../../circuits/hlth_chain_L_skip_15nm/ characterization/data/hlth_inv_chain_L_15nm_cidm characterization/result/hlth_inv_chain_L_15nm_cidm_sumexp_no_fitting cidm SUMEXP_CHANNEL structure.json hlth_L_custom.sdf instance_mapping.json True

####
# python fitting.py ../../circuits/mips_clock_15nm/ characterization/data/mips_clock_15nm_cidm characterization/result/mips_clock_15nm_cidm_exp cidm EXP_CHANNEL structure.json clk_own.sdf instance_mapping.json 
# python fitting.py ../../circuits/mips_clock_15nm/ characterization/data/mips_clock_15nm_cidm characterization/result/mips_clock_15nm_cidm_sumexp_no_fitting cidm SUMEXP_CHANNEL structure.json clk_own.sdf instance_mapping.json True

# python fitting.py ../../circuits/mips_clock_15nm/ characterization/data/mips_clock_15nm_idm_plus_bwd characterization/result/mips_clock_15nm_idm_plus_bwd_exp idm_plus_bwd EXP_CHANNEL structure.json clk_own.sdf instance_mapping.json 
# python fitting.py ../../circuits/mips_clock_15nm/ characterization/data/mips_clock_15nm_idm_plus_bwd characterization/result/mips_clock_15nm_idm_plus_bwd_no_fitting idm_plus_bwd SUMEXP_CHANNEL structure.json clk_own.sdf instance_mapping.json True

def run_fitting(circuit_folder, data_folder, result_folder, fitting_type, channel_type, structure_file_path, sdf_file_path, instance_mapping_file_path, disable_fitting):
    data_folder = os.path.join(circuit_folder, data_folder)
    result_folder = os.path.join(circuit_folder, result_folder)
    fitting_type = FittingType(fitting_type)
    evenly_space = False
    channel_type = ChannelType(channel_type)
    structure_filename_in = os.path.join(circuit_folder, structure_file_path)
    structure_filename_out = os.path.join(result_folder, "structure.{fitting_type}.{channel_type}.json".format(fitting_type = fitting_type, channel_type = str(channel_type).lower()))
    sdf_filename_in = os.path.join(circuit_folder, sdf_file_path)
    sdf_filename_out = os.path.join(result_folder, '{file}.{fitting_type}.sdf'.format(file = Path(sdf_file_path).stem, fitting_type = fitting_type))
    instance_mapping_file_path = os.path.join(circuit_folder, instance_mapping_file_path)

    instance_mapping = dict()
    if os.path.exists(instance_mapping_file_path):
        with open(instance_mapping_file_path) as f:
            instance_mapping = json.load(f)

    if not os.path.exists(result_folder):
        os.makedirs(result_folder) 

    # Create a set of pairs of matching fitting files
    delay_files = set()
    for result_file in os.listdir(data_folder):
        if "result" in result_file and result_file.endswith(".dat"):
            delay_file_up = result_file.replace('result', 'delayFctUp')
            delay_file_down = result_file.replace('result', 'delayFctDo')

            assert(channel_type == ChannelType.EXP_CHANNEL or os.path.exists(os.path.join(data_folder, delay_file_up)) or disable_fitting)
            assert(channel_type == ChannelType.EXP_CHANNEL or os.path.exists(os.path.join(data_folder, delay_file_down)) or disable_fitting)
            assert(os.path.exists(os.path.join(data_folder, result_file)))


            delay_files.add((delay_file_up, delay_file_down, result_file))
    
    structure = read_circuit_structure(structure_filename_in)
    sdf_dict = dict()
    result_dict = dict()

    for (up_file, down_file, result_file) in sorted(delay_files):
        print(up_file, down_file)
        fitting(data_folder, result_folder, up_file, down_file, fitting_type, channel_type, evenly_space, structure, sdf_dict, instance_mapping, result_file, result_dict, disable_fitting)     

    total_up_error = 0
    total_down_error = 0

    for cell, val in result_dict.items():
        (up_error, down_error) = val
        if not up_error:
            up_error = 0
        if not down_error:
            down_error = 0
        total_up_error = total_up_error + up_error
        total_down_error = total_down_error + down_error

    print("Total up error: {}, total down error: {}, total error: {}".format(total_up_error, total_down_error, total_up_error + total_down_error))


    # dump structure back to file
    with open(structure_filename_out, 'w') as outfile:
        json.dump(structure.__dict__, outfile, sort_keys=True, indent=4, cls=CircuitStructureEncoder)

    # Write SDF files
    write_sdf_file(sdf_filename_in, sdf_filename_out, sdf_dict)

def parse_filename(up_file):
    regex = r"(.*)_(.*)_(.*)_(.*)_(-?\d+)_(-?\d+)_delayFct(Up|Do).dat"

    matches = re.finditer(regex, up_file, re.MULTILINE)

    for _, match in enumerate(matches, start=1):
        circuit = match.group(1)
        from_sig = match.group(2)
        to_sig = match.group(3)
        cell_name = match.group(4)
        v_th_in = match.group(5)
        v_th_out = match.group(6)
        updo = match.group(7)

    return circuit, updo, from_sig, to_sig, cell_name, v_th_in, v_th_out 

def find_sdf_instance(instance_mapping, structure_instance_name):
    if structure_instance_name in instance_mapping:
        return instance_mapping[structure_instance_name]
    else:
        # Fallback, if the name in SPICE and SDF is the same
        print("Not found: ", structure_instance_name, instance_mapping)
        return structure_instance_name

    

def fitting(data_folder, result_folder, up_file, down_file, fitting_type, channel_type, evenly_space, structure, sdf_dict, instance_mapping, characterization_result_file_path, result_dict, disable_fitting):
    # print(up_file, down_file)
    circuit, updo, from_sig, to_sig, cell_name, v_th_in, v_th_out = parse_filename(up_file)
    result_file_prefix = "{circuit}_{fitting_type}_{from_sig}_{to_sig}".format(circuit = circuit, fitting_type = fitting_type, from_sig = from_sig, to_sig = to_sig)

    up_filepath = os.path.join(data_folder, up_file)
    down_filepath = os.path.join(data_folder, down_file)
    characterization_result_file_path = os.path.join(data_folder, characterization_result_file_path)

    assert(up_filepath != down_filepath)

    cell = find_instance_in_cells(structure, cell_name)

    if cell is None:
        print("Ignore cell: ", cell_name)
        return

    sdf_instance = find_sdf_instance(instance_mapping, cell_name)
    

    characterization_result_file = open(characterization_result_file_path, 'r')
    char_vth_in, char_vth_out, char_d_min, char_delta_up, char_delta_down, char_dinf_up, char_dinf_down = json.load(characterization_result_file)
    char_d_min = char_d_min * 1e12
    char_delta_up = char_delta_up * 1e12
    char_delta_down = char_delta_down * 1e12

    x_values_up, x_values_down, y_values_up_delay, y_values_down_delay = None, None, None, None
    
    real_delay_func_exists = os.path.exists(up_filepath) and os.path.exists(down_filepath)
    if real_delay_func_exists:
        delay = pd.read_csv(down_filepath, sep=';', header=None)
        x_values_down = delay.iloc[:, 0]
        y_values_down_delay = delay.iloc[:, 1]
        d_inf_down = y_values_down_delay.iloc[-1]

        delay = pd.read_csv(up_filepath, sep=';', header=None)
        x_values_up = delay.iloc[:, 0]
        y_values_up_delay =  delay.iloc[:, 1]
        d_inf_up =  y_values_up_delay.iloc[-1]

        # Transform to evenly spaced x-values, since we want to make sure that the all values are equally important
        if evenly_space:
            nr_of_values = 20 # TODO: Configure
            x_values_up_evenly_spaced = np.linspace(
                x_values_up[0], x_values_up.iloc[-1], nr_of_values)
            x_values_down_evenly_spaced = np.linspace(
                x_values_down[0], x_values_down.iloc[-1], nr_of_values)
            y_values_up_delay = create_evenly_spaced_y_values(
                x_values_up_evenly_spaced, x_values_up, y_values_up_delay)
            y_values_down_delay = create_evenly_spaced_y_values(
                x_values_down_evenly_spaced, x_values_down, y_values_down_delay)
            x_values_up = x_values_up_evenly_spaced
            x_values_down = x_values_down_evenly_spaced

            result_file_prefix += "_evenly"

    
    if real_delay_func_exists:
        plt.figure()

    (up_error, down_error) = (None, None)


    # Read from the dat file
    if channel_type == ChannelType.SUMEXP_CHANNEL:
        dmindo = char_d_min + char_delta_down
        dminup = char_d_min + char_delta_up
        d_inf_down = char_dinf_down
        d_inf_up = char_dinf_up
        (up_error, down_error, channel_parameters)  = fit_sumexp(x_values_up, x_values_down, y_values_up_delay, y_values_down_delay, d_inf_up, d_inf_down, char_d_min * 1e3, char_delta_up * 1e3, char_delta_down * 1e3, disable_fitting)
        
        # Need to set the channel parameters 
        cell.channel_params = channel_parameters
    elif channel_type == ChannelType.EXP_CHANNEL:
        # no fitting possible           
        dmindo = char_d_min + char_delta_down
        d_inf_down = char_dinf_down
        dminup = char_d_min + char_delta_up
        d_inf_up = char_dinf_up
        
        if real_delay_func_exists:
            (up_error, down_error) = fit_exp(d_inf_up, d_inf_down, char_d_min * 1e-12, char_delta_up * 1e-12, char_delta_down * 1e-12, x_values_up, x_values_down, y_values_up_delay, y_values_down_delay)

    else:
        print("Channel " + channel_type + " not implemented for CIDM")
        assert(False)

    result_dict[cell] = (up_error, down_error)

    # Plot real delta functions
    if real_delay_func_exists:
        plt.plot(np.array(x_values_down), np.array(y_values_down_delay), label='delta down', color='blue', linestyle='dotted')
        plt.plot(np.array(x_values_up), np.array(y_values_up_delay), label='delta up', color='red', linestyle='dotted')

        plt.legend()
        plt.savefig(os.path.join(result_folder, result_file_prefix + "_delay.pdf"), dpi=150)
        plt.close()

    
    if fitting_type == FittingType.CIDM:                
        cell.pure_delay_down = "{dmindo:.3f} ps".format(dmindo = dmindo)
        cell.pure_delay_up = "{dminup:.3f} ps".format(dminup = dminup)    
        cell.pure_delay = "{dmin:.3f} ps".format(dmin = char_d_min)           
    else:
        if char_d_min < 0:
            char_d_min = 0.001    

        cell.pure_delay = "{dmin:.3f} ps".format(dmin = char_d_min)
        if hasattr(cell, 'pure_delay_down'):
            delattr(cell, 'pure_delay_down')
        if hasattr(cell, 'pure_delay_up'):
            delattr(cell, 'pure_delay_up')

    sdf_dict[sdf_instance] = (d_inf_up, d_inf_down)


def create_evenly_spaced_y_values(x_values_evenely_spaced, x_values, y_values):
    y_values_evenly_spaced = np.empty(x_values_evenely_spaced.shape)
    old_idx = 0
    for new_idx in range(0, len(x_values_evenely_spaced)):
        if x_values_evenely_spaced[new_idx] == x_values[old_idx]:
            y_values_evenly_spaced[new_idx] = y_values[old_idx]
        else:
            # we need to find the old_idx where x_values[old_idx] < x_values_evenely_spaced[new_idx] <= x_values[old_idx+1]
            while x_values[old_idx+1] < x_values_evenely_spaced[new_idx]:
                old_idx += 1

            # Now make linear interpolation
            x1 = x_values[old_idx]
            x2 = x_values[old_idx+1]
            y1 = y_values[old_idx]
            y2 = y_values[old_idx+1]
            x = x_values_evenely_spaced[new_idx]

            y = ((y2 - y1) / (x2 - x1)) * (x - x1) + y1
            y_values_evenly_spaced[new_idx] = y

    return y_values_evenly_spaced


def find_instance_in_cells(structure, instance):
    for cell in structure.cells:
        if cell.instance == instance:
            return cell
    return None


def plot_median(d_min_up, d_min_down):
    # Plot 2nd median
    left = d_min_up
    right = d_min_down
    if d_min_up > d_min_down:
        left = d_min_down
        right = d_min_up

    x_values_median = np.linspace(left * 5, right * 5, 10)
    y_values_median = np.array([-xi for xi in x_values_median])
    plt.plot(x_values_median, y_values_median, label='2nd median')

def fit_exp(d_inf_up, d_inf_down, d_min, delta_plus, delta_minus, x_values_up, x_values_down, y_values_up_delay, y_values_down_delay):
    exp_tau_up = calc_tau_up(d_inf_up, d_min, delta_plus, v_dd, v_th)
    exp_tau_down = calc_tau_do(d_inf_down, d_min, delta_minus, v_dd, v_th)
    exp_up_delay = np.array([delta_exp_up(xi + delta_plus, d_inf_up, d_inf_down, exp_tau_up, exp_tau_down, delta_plus, delta_minus) + delta_plus for xi in x_values_up])
    exp_down_delay = np.array([delta_exp_do(xi + delta_minus, d_inf_up, d_inf_down, exp_tau_up, exp_tau_down, delta_plus, delta_minus) + delta_minus for xi in x_values_down])
    plt.plot(np.array(x_values_down), np.array(exp_down_delay),
             label='cidm exp down', color='blue')
    plt.plot(np.array(x_values_up), np.array(exp_up_delay), label='cidm exp up', color='red')
    plt.plot(np.array(x_values_down), np.array(exp_down_delay - y_values_down_delay),
             label='cidm exp down diff', color='blue', linestyle='dashed', alpha=0.5)
    plt.plot(np.array(x_values_up), np.array(exp_up_delay - y_values_up_delay),
             label='cidm exp up diff', color='red', linestyle='dashed', alpha=0.5)
    up_error = calc_error(y_values_up_delay, exp_up_delay)
    down_error = calc_error(y_values_down_delay, exp_down_delay)
    plt.title('total error: {:.4f}, up error: {:.4f}, down error: {:.4f}'.format(
        (up_error + down_error)*1e23, up_error*1e23, down_error*1e23), pad=20)
        
    plt.xlim(left = -0.2e-10, right=0.050e-8)
    
    return (up_error, down_error)

def fit_sumexp(x_values_up, x_values_down, y_values_up_delay, y_values_down_delay, d_inf_up, d_inf_down, d_min, delta_plus, delta_minus, disable_fitting):   
    up_error, down_error = None, None
    if disable_fitting:
        # TODO: This parameters should come from some configuration file (gate_config), but since they do not influence anything except the plots and the deviation calculation we currently use some fixed parameters
        
        x_1_up = 0.25
        x_1_do = 0.25
    
        tau_1_up = 30 # fs
        tau_2_up = 3000
    
        tau_1_do = 30 # fs
        tau_2_do = 3000
    else:        
        # Convert all parameters to fs
        x_values_up  = x_values_up * 1e15
        x_values_down = x_values_down * 1e15
        y_values_up_delay = y_values_up_delay * 1e15
        y_values_down_delay = y_values_down_delay * 1e15
        d_inf_up = d_inf_up * 1e15
        d_inf_down = d_inf_down * 1e15

        params = Parameters()
        # TODO: Find a good range for min and max
        # params.add('tau_r_up', value = 100, min = 1, max = 1000)   
        # params.add('x_1_up', value = 0.25, min = 0, max = 1)
        # params.add('tau_r_do', value = 100, min = 1, max = 1000)   
        # params.add('x_1_do', value = 0.25, min = 0, max = 1)
        
        params.add('tau_r', value = 100, min = 1, max = 1000)
        params.add('x_1', value = 0.25, min = 0, max = 1)

        out = minimize(cidm_sumexp_delta_fit_function, params, kws={"x_up_values": x_values_up, "x_down_values": x_values_down, "y_up_values": y_values_up_delay, "y_down_values": y_values_down_delay, "d_min": d_min, "delta_plus": delta_plus, "delta_minus": delta_minus, 'd_inf_up': d_inf_up, 'd_inf_down': d_inf_down})
        # print(fit_report(out))
        
        tau_r_up = out.params['tau_r'].value
        x_1_up = out.params['x_1'].value
        tau_r_do = out.params['tau_r'].value
        x_1_do = out.params['x_1'].value
    
        tau_1_up = 30 # fs
        tau_2_up = tau_1_up * tau_r_up
        
        tau_1_do = 30 # fs
        tau_2_do = tau_1_do * tau_r_do
    
        c_up = calc_c_up(v_dd, v_th, x_1_up, tau_1_up, tau_2_up, d_inf_up, d_min, delta_plus)
        c_do = calc_c_do(v_dd, v_th, x_1_do, tau_1_do, tau_2_do, d_inf_down, d_min, delta_minus)

        sumexp_up_delay = np.array([delta_sumexp_up(xi + delta_plus, d_inf_up, d_inf_down, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, delta_plus, delta_minus) + delta_plus for xi in x_values_up]) * 1e-15
        sumexp_down_delay = np.array([delta_sumexp_do(xi + delta_minus, d_inf_up, d_inf_down, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, delta_plus, delta_minus) + delta_minus for xi in x_values_down]) * 1e-15
        
        x_values_up  = x_values_up * 1e-15
        x_values_down = x_values_down * 1e-15
        
        y_values_up_delay = y_values_up_delay * 1e-15
        y_values_down_delay = y_values_down_delay * 1e-15

        plt.plot(np.array(x_values_down), np.array(sumexp_down_delay),
                label='cidm sumexp down', color='blue')
        plt.plot(np.array(x_values_up), np.array(sumexp_up_delay), label='cidm sumexp up', color='red')
        plt.plot(np.array(x_values_down), np.array(sumexp_down_delay - y_values_down_delay),
                label='cidm sumexp down diff', color='blue', linestyle='dashed', alpha=0.5)
        plt.plot(np.array(x_values_up), np.array(sumexp_up_delay - y_values_up_delay),
                label='cidm sumexp up diff', color='red', linestyle='dashed', alpha=0.5)
        up_error = calc_error(y_values_up_delay, sumexp_up_delay)
        down_error = calc_error(y_values_down_delay, sumexp_down_delay)

        # plt.xlim(-20000, 40000)
        plt.xlim(left = -0.2e-10, right=0.050e-8)

        plt.title('total error: {:4f}, up error: {:4f}, down error: {:4f}'.format(
            (up_error + down_error)*1e23, up_error*1e23, down_error*1e23), pad=20)

    channel_parameters = dict()
    channel_parameters['X_1_UP'] = x_1_up
    channel_parameters['X_1_DO'] = x_1_do
    channel_parameters['TAU_1_UP'] = "{} fs".format(int(tau_1_up))
    channel_parameters['TAU_1_DO'] = "{} fs".format(int(tau_1_do))
    channel_parameters['TAU_2_UP'] = "{} fs".format(int(tau_2_up))
    channel_parameters['TAU_2_DO'] = "{} fs".format(int(tau_2_do))

    return (up_error, down_error, channel_parameters)

def calc_error(target, actual):
    return np.sum((target-actual)**2)

def cidm_sumexp_delta_fit_function(params, x_up_values, x_down_values, y_up_values, y_down_values, d_min, delta_plus, delta_minus, d_inf_up, d_inf_down):
    # Extract the parameters. 
    # TODO: Think about different up / down parameters
    x_1_up = params['x_1'].value
    tau_r_up = params['tau_r']. value
    x_1_do = params['x_1'].value
    tau_r_do = params['tau_r']. value

    tau_1_up = 30 # fs
    tau_2_up = tau_1_up * tau_r_up
    
    tau_1_do = 30 # fs
    tau_2_do = tau_1_do * tau_r_do

    # print("Params: ", d_min, delta_plus, delta_minus, d_inf_up, d_inf_down)



    # Now calculate c_up and c_down
    c_up = calc_c_up(v_dd, v_th, x_1_up, tau_1_up, tau_2_up, d_inf_up, d_min, delta_plus)
    c_do = calc_c_do(v_dd, v_th, x_1_do, tau_1_do, tau_2_do, d_inf_down, d_min, delta_minus)

    # And now let us calculate y_up and y_down
    y_up = np.array([delta_sumexp_up(xi + delta_plus, d_inf_up, d_inf_down, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, delta_plus, delta_minus) + delta_plus for xi in x_up_values])
    y_down = np.array([delta_sumexp_do(xi + delta_minus, d_inf_up, d_inf_down, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, delta_plus, delta_minus) + delta_minus for xi in x_down_values])

    # print("Res: ", y_up[0], y_up[-1], y_down[0], y_down[-1])

    resid_up = (y_up - y_up_values)
    resid_down = (y_down - y_down_values)

    return np.concatenate((resid_up, resid_down))

def write_sdf_file(sdf_file_in_path, sdf_file_out_path, sdf_dict):
    # now go and set each interconnect to 0 (the following code is taken from Juergens customSDF.py script)
    f = open(sdf_file_in_path, "r")
    fout = open(sdf_file_out_path, "w")
    line_finder = "IOPATH I Z"	# TODO: This needs to be configured...

    lines = f.readlines()
    modified_lines = list()
    for line in lines:
        if line.count('INTERCONNECT') > 0:       
            parts = line.split(' ')
            parts[4] = '(0.000::0.000)'
            parts[5] = '(0.000::0.000))\n'
            modified_lines.append(' '.join(parts))
        else:
            modified_lines.append(line)

    # print(sdf_dict)
			
    # now find for each key in the matching dict the corresponding entry and modify the rise and fall time
    for key, value in sdf_dict.items():
        found_key = False
        for line_idx, line in enumerate(modified_lines):
            instance = key
            if line.lower().find("(INSTANCE  {0})".format(instance).lower()) >= 0:		
                # find the next line within the next few lines which contains IOPATH, and replace...
                start_idx = line_idx
                act_line_finder = line_finder
                while line_idx < start_idx + 5:			
                    if modified_lines[line_idx].find(act_line_finder) >= 0:				
                        found_key = True	

                        parts = modified_lines[line_idx].split(' ')
                        parts[4] = "({0:.6f}::{0:.6f})".format(value[0]*1e12)
                        parts[5] = "({0:.6f}::{0:.6f}))\n".format(value[1]*1e12)
                            
                        modified_lines[line_idx] = ' '.join(parts)
                        
                        break
                    line_idx += 1
                break
                
        if not found_key:
            print("There was a problem for key: {0}".format(key))
			
    for line in modified_lines:
        fout.write(line)

if __name__ == "__main__":
    main()
