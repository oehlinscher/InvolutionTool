"""
    
	Involution Tool
	File: python_channel_implementation.py
	
    Copyright (C) 2018-2021  Daniel OEHLINGER <d.oehlinger@outlook.com>

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
# Our "base"-path is experiment_setup, 
# so we need to add the python subfolder to access all the scripts
sys.path.append('python') # Default
# sys.path.append('../../python') # Use this when testing via main
from readGateCfg import ChannelType
from helper import EscCodes, my_print
sys.path.append('vhdl/python_channel')
from python_channel_base import std_logic_t, tp_mode
from sumexp_delay_channel import sumexp_delay_channel_idm, sumexp_delay_channel_gidm
from hybrid_nor2_delay_channel import calculate_delay_hybrid_nor2
from pure_delay_channel import pure_delay_channel_idm
from exp_delay_channel import exp_delay_channel_idm, exp_delay_channel_gidm

import os


def extract_parameter(param):
    return param[0]

def extract_dict(in_dict):
    ret_dict = dict()
    for key, value in in_dict.items():
        ret_dict[key[0]] = value[0]
    return ret_dict

def calculate_delay_idm(channel_type, input_level, d_up, d_do, t_p, t_p_percent, t_p_mode, v_dd, v_th, now, last_output_time, first_transition, channel_parameters_dict): 
    sys.stdout.flush()

    channel_type = extract_parameter(channel_type)
    input_level = std_logic_t(extract_parameter(input_level))
    d_up = extract_parameter(d_up)
    d_do = extract_parameter(d_do)
    t_p = extract_parameter(t_p)
    t_p_percent = extract_parameter(t_p_percent)
    t_p_mode = tp_mode(extract_parameter(t_p_mode))
    v_dd = extract_parameter(v_dd)
    v_th = extract_parameter(v_th)
    now = extract_parameter(now)
    last_output_time = extract_parameter(last_output_time)
    first_transition = extract_parameter(first_transition)

    channel_parameters_dict = extract_dict(channel_parameters_dict)

    if channel_type.lower() == str(ChannelType.PUREDELAY_CHANNEL).lower():
        return pure_delay_channel_idm(input_level, d_up, d_do, t_p, t_p_percent, t_p_mode, v_dd, v_th, now, last_output_time, first_transition, channel_parameters_dict)
    elif channel_type.lower() == str(ChannelType.EXP_CHANNEL).lower():
        return exp_delay_channel_idm(input_level, d_up, d_do, t_p, t_p_percent, t_p_mode, v_dd, v_th, now, last_output_time, first_transition, channel_parameters_dict)
    elif channel_type.lower() == str(ChannelType.HILL_CHANNEL).lower():
        my_print('Not implemented yet!', EscCodes.FAIL, print_esc=False)
    elif channel_type.lower() == str(ChannelType.SUMEXP_CHANNEL).lower():
        return sumexp_delay_channel_idm(input_level, d_up, d_do, t_p, t_p_percent, t_p_mode, v_dd, v_th, now, last_output_time, first_transition, channel_parameters_dict)
    else:
        my_print('Not implemented yet!', EscCodes.FAIL, print_esc=False)

    sys.stdout.flush()


def calculate_delay_gidm(channel_type, input_level, d_inf_up, d_inf_do, v_dd, v_th, d_min, delta_plus, delta_minus, now, last_output_time, first_transition, channel_parameters_dict):   
    channel_type = extract_parameter(channel_type)
    input_level = std_logic_t(extract_parameter(input_level))
    d_inf_up = extract_parameter(d_inf_up)
    d_inf_do = extract_parameter(d_inf_do)
    v_dd = extract_parameter(v_dd)
    v_th = extract_parameter(v_th)
    d_min = extract_parameter(d_min)
    delta_plus = extract_parameter(delta_plus)
    delta_minus = extract_parameter(delta_minus)
    now = extract_parameter(now)
    last_output_time = extract_parameter(last_output_time)
    first_transition = extract_parameter(first_transition)

    channel_parameters_dict = extract_dict(channel_parameters_dict)

    if channel_type.lower() == "gidm_" + str(ChannelType.PUREDELAY_CHANNEL).lower():
        my_print('Not implemented yet!', EscCodes.FAIL, print_esc=False)
    elif channel_type.lower() == "gidm_" + str(ChannelType.EXP_CHANNEL).lower():
        return exp_delay_channel_gidm(input_level, d_inf_up, d_inf_do, v_dd, v_th, d_min, delta_plus, delta_minus, now, last_output_time, first_transition, channel_parameters_dict)
    elif channel_type.lower() == "gidm_" + str(ChannelType.HILL_CHANNEL).lower():
        my_print('Not implemented yet!', EscCodes.FAIL, print_esc=False)
    elif channel_type.lower() == "gidm_" + str(ChannelType.SUMEXP_CHANNEL).lower():
        return sumexp_delay_channel_gidm(input_level, d_inf_up, d_inf_do, v_dd, v_th, d_min, delta_plus, delta_minus, now, last_output_time, first_transition, channel_parameters_dict)
    else:
        my_print('Not implemented yet!', EscCodes.FAIL, print_esc=False)

    sys.stdout.flush()

def calculate_delay_hybrid_2in(gate_function, input_1_old, input_2_old, input_1, input_2, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay, v_dd, v_th, now, first_transition, last_input_switch_time, v_int, v_out):
    gate_function = extract_parameter(gate_function)
    input_1_old = std_logic_t(extract_parameter(input_1_old))
    input_2_old = std_logic_t(extract_parameter(input_2_old))
    input_1 = std_logic_t(extract_parameter(input_1))
    input_2 = std_logic_t(extract_parameter(input_2))
    r_1 = extract_parameter(r_1)
    r_2 = extract_parameter(r_2)
    r_3 = extract_parameter(r_3)
    r_4 = extract_parameter(r_4)
    c_int = extract_parameter(c_int)
    c_out = extract_parameter(c_out)
    scale_1 = extract_parameter(scale_1)
    pure_delay = extract_parameter(pure_delay)
    v_dd = extract_parameter(v_dd)
    v_th = extract_parameter(v_th)
    now = extract_parameter(now)
    first_transition = extract_parameter(first_transition)
    last_input_switch_time = extract_parameter(last_input_switch_time)
    v_int_in = extract_parameter(v_int)
    v_out_in = extract_parameter(v_out)

    if (gate_function.lower() == "nor".lower()):
        return calculate_delay_hybrid_nor2(input_1_old, input_2_old, input_1, input_2, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay, v_dd, v_th, now, first_transition, last_input_switch_time, v_int_in, v_out_in)
    else:
        my_print("Not implemented yet!", EscCodes.FAIL, print_esc=False)
    
    sys.stdout.flush()


# This is just to test if there are any errors, 
# since finding them is difficult when the script 
# is called from the VHDL / C
# def main():    
#     calculate_delay_idm(["exp_channel"], [2], [100], [100], [10], [0], [0], [0.80], [0.40], [0], [0], [0], {})

# if __name__ == "__main__":
#     main()
    