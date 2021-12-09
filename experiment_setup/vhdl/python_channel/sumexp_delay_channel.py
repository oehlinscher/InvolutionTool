"""
    
	Involution Tool
	File: sumexp_delay_channel.py
	
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
from numpy.lib.arraysetops import isin
from scipy import optimize
from itertools import chain

sys.path.append('vhdl/python_channel')
from python_channel_base import convert_fsolve_result, calc_tp, std_logic_t


full_output = True

def sumexp_up_t(t, v_dd, x_1_up, c_up, tau_1_up, tau_2_up, res=0.0):
    
    t = np.longdouble(t)
    v_dd = np.longdouble(v_dd)
    x_1_up = np.longdouble(x_1_up)
    if isinstance(c_up, np.ndarray):
        assert(len(c_up) == 1)
        c_up = np.longdouble(c_up[0])
    else:
        c_up = np.longdouble(c_up)
    tau_1_up = np.longdouble(tau_1_up)
    tau_2_up = np.longdouble(tau_2_up)
    res = np.longdouble(res)

    exp_1 = -c_up * t / tau_1_up
    exp_2 = -c_up * t / tau_2_up
    value = v_dd * (1 - x_1_up * np.exp(exp_1) - (1 - x_1_up) * np.exp(exp_2)) - res
    return value

    # with np.errstate(all='warn'):
    #     try:

    #         t = np.longdouble(t)
    #         v_dd = np.longdouble(v_dd)
    #         x_1_up = np.longdouble(x_1_up)
    #         if isinstance(c_up, np.ndarray):
    #             assert(len(c_up) == 1)
    #             c_up = np.longdouble(c_up[0])
    #         else:
    #             c_up = np.longdouble(c_up)
    #         tau_1_up = np.longdouble(tau_1_up)
    #         tau_2_up = np.longdouble(tau_2_up)
    #         res = np.longdouble(res)

    #         exp_1 = -c_up * t / tau_1_up
    #         exp_2 = -c_up * t / tau_2_up
    #         value = v_dd * (1 - x_1_up * np.exp(exp_1) - (1 - x_1_up) * np.exp(exp_2)) - res
    #         return value
    #     except FloatingPointError as e:
    #         print("FloatingPointError, sumexp_up_t exception",  exp_1, exp_2, x_1_up, v_dd, res, e, np.exp(exp_1), np.exp(exp_2))
    #         # sys.stdout.flush()
    #         return 0

def sumexp_up_t_prime(t, v_dd, x_1_up, c_up, tau_1_up, tau_2_up, res=0.0):
    return v_dd * (- x_1_up * (-c_up / tau_1_up) * np.exp(-c_up * t / tau_1_up) - (1 - x_1_up) * (-c_up / tau_2_up) * np.exp(-c_up * t / tau_2_up))

def sumexp_up_c(c_up, t, v_dd, x_1_up, tau_1_up, tau_2_up, res=0.0):
    return sumexp_up_t(t, v_dd, x_1_up, c_up, tau_1_up, tau_2_up, res)
    
def sumexp_up_c_prime(c_up, t, v_dd, x_1_up, tau_1_up, tau_2_up, res=0.0):
    return v_dd * (- x_1_up * (-t / tau_1_up) * np.exp(-c_up * t / tau_1_up) - (1 - x_1_up) * (-t / tau_2_up) * np.exp(-c_up * t / tau_2_up))


def sumexp_do_t(t, v_dd, x_1_do, c_do, tau_1_do, tau_2_do, res=0.0):     
    t = np.longdouble(t)
    v_dd = np.longdouble(v_dd)
    x_1_do = np.longdouble(x_1_do)
    if isinstance(c_do, np.ndarray):
        assert(len(c_do) == 1)
        c_do = np.longdouble(c_do[0])
    else:
        c_do = np.longdouble(c_do)
    tau_1_do = np.longdouble(tau_1_do)
    tau_2_do = np.longdouble(tau_2_do)
    res = np.longdouble(res)

    exp_1 = -c_do * t / tau_1_do
    exp_2 = -c_do * t / tau_2_do           

    value = v_dd * (x_1_do * np.exp(exp_1) + (1 - x_1_do) * np.exp(exp_2)) - res
    return value

    # with np.errstate(all='ignore'):
    #     try:            
    #         t = np.longdouble(t)
    #         v_dd = np.longdouble(v_dd)
    #         x_1_do = np.longdouble(x_1_do)
    #         if isinstance(c_do, np.ndarray):
    #             assert(len(c_do) == 1)
    #             c_do = np.longdouble(c_do[0])
    #         else:
    #             c_do = np.longdouble(c_do)
    #         tau_1_do = np.longdouble(tau_1_do)
    #         tau_2_do = np.longdouble(tau_2_do)
    #         res = np.longdouble(res)

    #         exp_1 = -c_do * t / tau_1_do
    #         exp_2 = -c_do * t / tau_2_do           

    #         value = v_dd * (x_1_do * np.exp(exp_1) + (1 - x_1_do) * np.exp(exp_2)) - res
    #         return value
    #     except FloatingPointError as e:
    #         print("sumexp_do_t exception",  exp_1, exp_2, x_1_do, v_dd, res, e)
    #         sys.stdout.flush()
    #         return 0

def sumexp_do_t_prime(t, v_dd, x_1_do, c_do, tau_1_do, tau_2_do, res=0.0):    
    return v_dd * (x_1_do * (-c_do / tau_1_do) * np.exp(-c_do * t / tau_1_do) + (1 - x_1_do) * (-c_do / tau_2_do) * np.exp(-c_do * t / tau_2_do))
    
def sumexp_do_c(c_do, t, v_dd, x_1_do,tau_1_do, tau_2_do, res=0.0):    
    return sumexp_do_t(t, v_dd, x_1_do, c_do, tau_1_do, tau_2_do, res)

def sumexp_do_c_prime(c_do, t, v_dd, x_1_do,tau_1_do, tau_2_do, res=0.0):    
    return v_dd * (x_1_do * (-t / tau_1_do) * np.exp(-c_do * t / tau_1_do) + (1 - x_1_do) * (-t / tau_2_do) * np.exp(-c_do * t / tau_2_do)) - res

def calc_brackets(init_a, init_b, step_size, func, func_args):
    a = init_a
    b = init_b
    count = 0
    while np.sign(func(a, *chain(func_args))) == np.sign(func(b, *chain(func_args))):
        a = a - step_size
        b = b + step_size

        count = count + 1
        # if count > 10:
        #     break

    return a, b

def sumexp_delay_channel_idm(input_level, d_up, d_do, t_p, t_p_percent, t_p_mode, v_dd, v_th, now, last_output_time, first_transition, channel_parameters_dict):    
    delta_plus = 0
    delta_minus = 0
    d_min_up = calc_tp(t_p, t_p_percent, t_p_mode, d_up)
    d_min_do = calc_tp(t_p, t_p_percent, t_p_mode, d_do)

    # Currently only the same dmin for up and down are supported.
    # If this feature is required in the future, I would suggest to 
    # take the average as d_min and put the difference in delta_plus and delta_minus
    assert(d_min_up == d_min_do) 

    return sumexp_delay_channel_gidm(input_level, d_up, d_do, v_dd, v_th, d_min_up, delta_plus, delta_minus, now, last_output_time, first_transition, channel_parameters_dict)

def calc_c_up(v_dd, v_th, x_1_up, tau_1_up, tau_2_up, d_inf_up, d_min, delta_plus):
    c_up = optimize.fsolve(sumexp_up_c, x0=0, fprime=sumexp_up_c_prime, args=(d_inf_up - d_min - delta_plus, v_dd, x_1_up, tau_1_up, tau_2_up, v_th))
    return convert_fsolve_result(c_up)

def calc_c_do(v_dd, v_th, x_1_do, tau_1_do, tau_2_do, d_inf_do, d_min, delta_minus):
    c_do = optimize.fsolve(sumexp_do_c, x0=0, fprime=sumexp_do_c_prime, args=(d_inf_do - d_min - delta_minus, v_dd, x_1_do, tau_1_do, tau_2_do, v_th))
    return convert_fsolve_result(c_do)

def sumexp_delay_channel_gidm(input_level, d_inf_up, d_inf_do, v_dd, v_th, d_min, delta_plus, delta_minus, now, last_output_time, first_transition, channel_parameters_dict):    
    # np.seterr(all='raise')
    # np.seterr(all='warn')
    sys.stderr = sys.stdout # Send errors to stdout as well, so that everything is in the logfile
    # 0. Extract parameters
    x_1_up = channel_parameters_dict["x_1_up"]
    x_1_do = channel_parameters_dict["x_1_do"]
    tau_1_up = channel_parameters_dict["tau_1_up"]
    tau_1_do = channel_parameters_dict["tau_1_do"]
    tau_2_up = channel_parameters_dict["tau_2_up"]
    tau_2_do = channel_parameters_dict["tau_2_do"]

    delay = 0

    c_up = calc_c_up(v_dd, v_th, x_1_up, tau_1_up, tau_2_up, d_inf_up, d_min, delta_plus)
    c_do = calc_c_do(v_dd, v_th, x_1_do, tau_1_do, tau_2_do, d_inf_do, d_min, delta_minus)

    # print("Type 1", type(c_up), type(c_do))
    
    T = now - last_output_time

    if input_level == std_logic_t.STD_LOGIC_1:
        if first_transition:
            delay = d_inf_up - delta_plus
        else:
            delay = delta_sumexp_up(T, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, delta_plus, delta_minus)
    elif input_level == std_logic_t.STD_LOGIC_0:
        if first_transition:
            delay = d_inf_do - delta_minus
        else:
            delay = delta_sumexp_do(T, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, delta_plus, delta_minus)
    else:
        assert(False)

    # print("now", now, "last_output_time", last_output_time, "transition time: ", int(round(delay)), "new transition time: ", now + int(round(delay)), "T", T, "input_level", input_level, first_transition, T, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, delta_plus, delta_minus)
    # sys.stdout.flush()
    
    last_output_time = now + int(round(delay))

    
    return (int(round(delay)), last_output_time, 0)

def delta_sumexp_up(T, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, delta_plus, delta_minus):    
    target_value = sumexp_do_t(T + d_inf_do - delta_minus, v_dd, x_1_do, c_do, tau_1_do, tau_2_do, 0)
    assert(target_value >= 0 and target_value <= 1)    

    # There seems to be a strange issue when the target value is too small with fsolve, therefore we cap it here to 0.
    if target_value < 1e-308:
        target_value = 0
    # fsolve seems to be behave bad for this specific problem (not quite sure why), therefore we use brentq
    a, b = calc_brackets(0, d_inf_do, d_inf_do, sumexp_up_t, func_args=(v_dd, x_1_up, c_up, tau_1_up, tau_2_up, target_value))
    turnaround_time = full_output_check(optimize.brentq(sumexp_up_t, args=(v_dd, x_1_up, c_up, tau_1_up, tau_2_up, target_value), a=a, b=b, full_output=full_output))
    # print("Target value up:", target_value, d_inf_up, delta_plus, turnaround_time, d_inf_up - delta_plus - turnaround_time)
    return d_inf_up - delta_plus - turnaround_time

def delta_sumexp_do(T, d_inf_up, d_inf_do, x_1_up, x_1_do, tau_1_up, tau_1_do, tau_2_up, tau_2_do, c_up, c_do, v_dd, delta_plus, delta_minus):
    target_value = sumexp_up_t(T + d_inf_up - delta_plus, v_dd, x_1_up, c_up, tau_1_up, tau_2_up, 0)
    assert(target_value >= 0 and target_value <= 1)
    a, b = calc_brackets(0, d_inf_up, d_inf_up, sumexp_do_t, func_args=(v_dd, x_1_do, c_do, tau_1_do, tau_2_do, target_value))
    turnaround_time = full_output_check(optimize.brentq(sumexp_do_t, args=(v_dd, x_1_do, c_do, tau_1_do, tau_2_do, target_value), a=a, b=b, full_output=full_output))
    # print("Target value do:", target_value, d_inf_do, delta_minus, turnaround_time, d_inf_do - delta_minus - turnaround_time)
    return d_inf_do - delta_minus - turnaround_time

def full_output_check(inp):
    if not full_output:
        return inp
    else:
        x0, r = inp
        # print(r)
        assert(r.converged)
        return x0

