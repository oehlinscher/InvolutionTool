"""
    
	Involution Tool
	File: exp_delay_channel.py
	
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
import numpy as np

sys.path.append('vhdl/python_channel')
from python_channel_base import calc_tp, std_logic_t, round_results

def exp_delay_channel_idm(input_level, d_up, d_do, t_p, t_p_percent, t_p_mode, v_dd, v_th, now, last_output_time, first_transition, channel_parameters_dict):    
    delta_plus = 0
    delta_minus = 0
    d_min_up = calc_tp(t_p, t_p_percent, t_p_mode, d_up)
    d_min_do = calc_tp(t_p, t_p_percent, t_p_mode, d_do)

    # Currently only the same dmin for up and down are supported.
    # If this feature is required in the future, I would suggest to 
    # take the average as d_min and put the difference in delta_plus and delta_minus
    assert(d_min_up == d_min_do) 

    return exp_delay_channel_gidm(input_level, d_up, d_do, v_dd, v_th, d_min_up, delta_plus, delta_minus, now, last_output_time, first_transition, channel_parameters_dict)

def exp_delay_channel_gidm(input_level, d_inf_up, d_inf_do, v_dd, v_th, d_min, delta_plus, delta_minus, now, last_output_time, first_transition, channel_parameters_dict):
    delay = 0

    tau_up = calc_tau_up(d_inf_up, d_min, delta_plus, v_dd, v_th)
    tau_do = calc_tau_do(d_inf_do, d_min, delta_minus, v_dd, v_th)

    if round_results:
        tau_up = round(tau_up)
        tau_do = round(tau_do)
        

    T = now - last_output_time

    if input_level == std_logic_t.STD_LOGIC_1:
        if first_transition:
            delay = d_inf_up - delta_plus
        else:
            delay = delta_exp_up(T, d_inf_up, d_inf_do, tau_up, tau_do, delta_plus, delta_minus)
    elif input_level == std_logic_t.STD_LOGIC_0:
        if first_transition:
            delay = d_inf_do - delta_minus
        else:
            delay = delta_exp_do(T, d_inf_up, d_inf_do, tau_up, tau_do, delta_plus, delta_minus)      
    else:
        assert(False)

    last_output_time = now + int(round(delay))

    return (int(round(delay)), last_output_time, 0)  

def delta_exp_up(T, d_inf_up, d_inf_do, tau_up, tau_do, delta_plus, delta_minus):
    return d_inf_up - delta_plus + tau_up * np.log(1 - np.exp(-((T + d_inf_do - delta_minus) / tau_do)))

def delta_exp_do(T, d_inf_up, d_inf_do, tau_up, tau_do, delta_plus, delta_minus):
    return d_inf_do - delta_minus + tau_do * np.log(1 - np.exp(-((T + d_inf_up - delta_plus) / tau_up)))

def calc_tau_up(d_inf_up, d_min, delta_plus, v_dd, v_th):
    return (d_inf_up - d_min - delta_plus) / (-np.log(1.0 - v_th / v_dd))

def calc_tau_do(d_inf_do, d_min, delta_minus, v_dd, v_th):
    return (d_inf_do - d_min - delta_minus) / (-np.log(v_th / v_dd))
