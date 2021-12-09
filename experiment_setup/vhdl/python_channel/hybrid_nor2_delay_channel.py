"""
    
	Involution Tool
	File: hybrid_nor2_delay_channel.py
	
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
from enum import Enum
import scipy
from scipy import optimize
import timeit

sys.path.append('vhdl/python_channel')
from python_channel_base import std_logic_t, convert_fsolve_result


sys.path.append('python')
from helper import my_print, EscCodes

# TODO: These parameters should probably be specified somewhere for each circuit, if we are not able to automatically obtain them
x0 = 1e-11
xtol = 1e-15
full_output = False

print_level = EscCodes.FAIL
# print_level = None

def calculate_delay_hybrid_nor2(input_1_old, input_2_old, input_1, input_2, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay, v_dd, v_th, now, first_transition, last_input_switch_time, v_int_in, v_out_in):    
    v_int_out = v_int_in
    v_out_out = v_out_in
    
    # Convert to fs
    now = now * 1e-15
    last_input_switch_time = last_input_switch_time * 1e-15
    pure_delay = pure_delay * 1e-15

    # 1. state, timedelta, last_curve -> state
    # Calculate the state in which we are now
    t = now - last_input_switch_time
    
    my_print("Old_input: {input_1_old}/{input_2_old}, New input: {input_1}/{input_2}".format(input_1_old = input_1_old, input_2_old = input_2_old, input_1 = input_1, input_2 = input_2), print_level, print_esc=False)
    my_print("Now: {now}, last_input_switch_time: {last_input_switch_time}, t: {t}".format(now = now, last_input_switch_time = last_input_switch_time, t = t), print_level, print_esc=False)

    if input_1_old == std_logic_t.STD_LOGIC_0 and input_2_old == std_logic_t.STD_LOGIC_0:
        # System (0,0)
        my_print("System 0 0", print_level, print_esc=False)
        alpha, beta, gamma, lambda_1, lambda_2 = hybrid_nor2_0_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out)
        
        # Solve initial condition
        c_1, c_2 = hybrid_nor2_0_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, v_int_in, v_out_in)
        
        # Calculate new state
        v_int_out = hybrid_nor2_0_0_vint(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2)
        v_out_out = hybrid_nor2_0_0_vout(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2)

    elif input_1_old == std_logic_t.STD_LOGIC_0 and input_2_old == std_logic_t.STD_LOGIC_1:
        # System (0,1)
        my_print("System 0 1", print_level, print_esc=False)
        # Solve initial condition
        c_1, c_2 = hybrid_nor2_0_1_initial_condition(v_dd, v_int_in, v_out_in)
        # Calculate new state
        v_int_out = hybrid_nor2_0_1_vint(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, c_1, c_2)
        v_out_out = hybrid_nor2_0_1_vout(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, c_1, c_2)
    elif input_1_old == std_logic_t.STD_LOGIC_1 and input_2_old == std_logic_t.STD_LOGIC_0:
        # System (1,0)
        my_print("System 1 0", print_level, print_esc=False)
        alpha, beta, lambda_1, lambda_2 = hybrid_nor2_1_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out)
        # Solve initial condition
        c_1, c_2 = hybrid_nor2_1_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, v_int_in, v_out_in)
        # Calculate new state
        v_int_out = hybrid_nor2_1_0_vint(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, c_1, c_2)
        v_out_out = hybrid_nor2_1_0_vout(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, c_1, c_2)
    elif input_1_old == std_logic_t.STD_LOGIC_1 and input_2_old == std_logic_t.STD_LOGIC_1:
        # System (1,1)
        my_print("System 1 1", print_level, print_esc=False)
        # Solve initial condition        
        c_1, c_2 = hybrid_nor2_1_1_initial_condition(v_dd, v_int_in, v_out_in)
        # Calculate new state        
        v_int_out = hybrid_nor2_1_1_vint(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, c_1, c_2)
        v_out_out = hybrid_nor2_1_1_vout(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, c_1, c_2)
    else:
        my_print("Unexpected system state", print_level, print_esc=False)
        sys.stdout.flush()
        assert(False)
    
    my_print("OLD. c_1: {c_1}, c_2: {c_2}".format(c_1 = c_1, c_2 = c_2), print_level, print_esc=False)
    my_print("old state: {v_int_in}/{v_out_in}, new state: : {v_int_out}/{v_out_out}".format(v_int_in = v_int_in, v_out_in = v_out_in, v_int_out = v_int_out, v_out_out = v_out_out), print_level, print_esc=False)

    
    # 2. state, current_curve -> time
    # Calculate how long it takes from our current state (at the time of the input switch) until the threshold is crossed.
    # In some cases, the threshold will be not crossed, and we need to set delay_valid to False    
    delay = 0
    delay_valid = True

    if input_1 == std_logic_t.STD_LOGIC_0 and input_2 == std_logic_t.STD_LOGIC_0:
        # System (0,0)
        my_print("System 0 0", print_level, print_esc=False)
        if v_out_out > v_th:
            delay_valid = False
        else:
            alpha, beta, gamma, lambda_1, lambda_2 = hybrid_nor2_0_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out)        
            # Solve initial condition
            c_1, c_2 = hybrid_nor2_0_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, v_int_out, v_out_out)

            # Find the time until the threshold is crossed
            fsolve_res = optimize.fsolve(hybrid_nor2_0_0_vout, fprime=hybrid_nor2_0_0_vout_prime, x0=x0, args=(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2, v_th), xtol=xtol, full_output=full_output)
            fsolve_x = full_output_checks(fsolve_res, full_output)
            delay = convert_fsolve_result(fsolve_x)
    elif input_1 == std_logic_t.STD_LOGIC_0 and input_2 == std_logic_t.STD_LOGIC_1:
        # System (0,1)
        my_print("System 0 1", print_level, print_esc=False)
        if v_out_out < v_th:
            delay_valid = False
        else:
            # Solve initial condition   
            c_1, c_2 = hybrid_nor2_0_1_initial_condition(v_dd, v_int_out, v_out_out)

            # Find the time until the threshold is crossed
            fsolve_res = optimize.fsolve(hybrid_nor2_0_1_vout, fprime=hybrid_nor2_0_1_vout_prime, x0=x0, args=(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, c_1, c_2, v_th), xtol=xtol, full_output=full_output)
            fsolve_x = full_output_checks(fsolve_res, full_output)
            delay = convert_fsolve_result(fsolve_x)        
    elif input_1 == std_logic_t.STD_LOGIC_1 and input_2 == std_logic_t.STD_LOGIC_0:
        # System (1,0)
        my_print("System 1 0", print_level, print_esc=False)
        if v_out_out < v_th:
            delay_valid = False
        else:
            alpha, beta, lambda_1, lambda_2 = hybrid_nor2_1_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out)
            # Solve initial condition   
            c_1, c_2 = hybrid_nor2_1_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, v_int_out, v_out_out)
                    
            # Find the time until the threshold is crossed
            fsolve_res = optimize.fsolve(hybrid_nor2_1_0_vout, fprime=hybrid_nor2_1_0_vout_prime, x0=x0, args=(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, c_1, c_2, v_th), xtol=xtol, full_output=full_output)
            fsolve_x = full_output_checks(fsolve_res, full_output)
            delay = convert_fsolve_result(fsolve_x)        

    elif input_1 == std_logic_t.STD_LOGIC_1 and input_2 == std_logic_t.STD_LOGIC_1:
        # System (1,1)
        my_print("System 1 1", print_level, print_esc=False)
        # Check if we will get a threshold crossing
        if v_out_out < v_th:
            delay_valid = False
        else:
            # Solve initial condition        
            c_1, c_2 = hybrid_nor2_1_1_initial_condition(v_dd, v_int_out, v_out_out)

            # Find the time until the threshold is crossed
            fsolve_res = optimize.fsolve(hybrid_nor2_1_1_vout, fprime=hybrid_nor2_1_1_vout_prime, x0=x0, args=(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, c_1, c_2, v_th), xtol=xtol, full_output=full_output)
            fsolve_x = full_output_checks(fsolve_res, full_output)
            delay = convert_fsolve_result(fsolve_x)          

    else:
        my_print("Unexpected system state", print_level, print_esc=False)
        sys.stdout.flush()
        assert(False)
    
    # If the delay is valid, we also need to add the pure delay to it
    if delay_valid:
        delay = delay + pure_delay

    # Convert to fs
    delay = delay * 1e15 
    now = now * 1e15

        
    my_print("NEW. c_1: {c_1}, c_2: {c_2}".format(c_1 = c_1, c_2 = c_2), print_level, print_esc=False)
    my_print("Delay: {delay} fs, valid: {valid}".format(delay = delay, valid = delay_valid), print_level, print_esc=False)

    print("calculate_delay_hybrid_nor2 end")

    sys.stdout.flush()

    return (delay, delay_valid, False, now, v_int_out, v_out_out)


def hybrid_nor2_0_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out):
    denominator = (2 * c_out * c_int * r_1 * r_2)
    alpha = (c_out * (r_1 + r_2) - c_int * r_1) / denominator
    beta = np.sqrt(np.square(c_int * r_1 + c_out * (r_1 + r_2)) - 4 * c_out * c_int * r_1 * r_2) / denominator
    gamma = -(c_int * r_1 + c_out * (r_1 + r_2)) / denominator
    lambda_1 = gamma + beta
    lambda_2 = gamma - beta
    return (alpha, beta, gamma, lambda_1, lambda_2)

def hybrid_nor2_0_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, v_int_in, v_out_in):
    c_1 = (-alpha*beta*c_int*r_1*r_2*v_int_in - alpha*c_int*gamma*r_1*r_2*v_int_in - alpha*r_2*v_dd + beta**2*c_int*r_1*r_2*v_int_in + beta*c_int*gamma*r_1*r_2*v_int_in + beta*r_1*v_out_in + beta*r_2*v_dd + gamma*r_1*v_out_in)/(2*beta**2*r_1 + 2*beta*gamma*r_1)
    c_2 = (alpha*beta*c_int*r_1*r_2*v_int_in - alpha*c_int*gamma*r_1*r_2*v_int_in - alpha*r_2*v_dd + beta**2*c_int*r_1*r_2*v_int_in - beta*c_int*gamma*r_1*r_2*v_int_in - beta*r_1*v_out_in - beta*r_2*v_dd + gamma*r_1*v_out_in)/(2*beta**2*r_1 - 2*beta*gamma*r_1)
    return c_1, c_2

def hybrid_nor2_0_0_vint(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2):    
    part_1 = (c_1 / (c_int * r_2)) * np.exp(lambda_1 * t)
    part_2 = (c_2 / (c_int * r_2)) * np.exp(lambda_2 * t)
    inhomogeneous_part = (-v_dd * (alpha + gamma) / (c_int * r_1 * (gamma*gamma - beta*beta)))
    return  part_1 + part_2 + inhomogeneous_part

def hybrid_nor2_0_0_vout(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2, res = 0.0):
    part_1 = (c_1 * (alpha + beta)) * np.exp(lambda_1 * t)
    part_2 = (c_2 * (alpha - beta)) * np.exp(lambda_2 * t)
    inhomogeneous_part = (v_dd * (-(alpha*alpha)+beta*beta)*r_2) / (r_1 * (gamma * gamma - beta * beta))
    return  part_1 + part_2 + inhomogeneous_part - res


def hybrid_nor2_0_0_vout_prime(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2, res = 0.0):
    return c_1*lambda_1*(alpha + beta)*np.exp(lambda_1*t) + c_2*lambda_2*(alpha - beta)*np.exp(lambda_2*t)

def hybrid_nor2_0_1_initial_condition(v_dd, v_int_in, v_out_in):
    c_1 = -v_dd + v_int_in
    c_2 = v_out_in
    return c_1, c_2

def hybrid_nor2_0_1_vint(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, c_1, c_2):  
    return c_1 * np.exp(-t / (c_int * r_1)) + v_dd

def hybrid_nor2_0_1_vout(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, c_1, c_2, res = 0.0):
    return c_2 * np.exp(-t / (c_out * r_4)) - res

def hybrid_nor2_0_1_vout_prime(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, c_1, c_2, res = 0.0):
    return -c_2*np.exp(-t/(c_out*r_4))/(c_out*r_4)

def hybrid_nor2_1_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out):    
    alpha = (c_out * r_3 - c_int*(r_2 + r_3)) / (2*c_out*c_int*r_2*r_3)
    beta = np.sqrt(np.square(c_out*r_3 + c_int*(r_2 + r_3)) - 4 * c_out * c_int * r_2 * r_3) / (2*c_out*c_int*r_2*r_3)
    lambda_base = -(c_out * r_3 + c_int*(r_2 + r_3)) / (2 * c_out * c_int * r_2 * r_3)
    lambda_1 = lambda_base + beta
    lambda_2 = lambda_base - beta
    return alpha, beta, lambda_1, lambda_2

def hybrid_nor2_1_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, v_int_in, v_out_in):    
    c_1 = (-alpha*c_int*r_2*v_int_in + beta*c_int*r_2*v_int_in + v_out_in)/(2*beta)
    c_2 = (alpha*c_int*r_2*v_int_in + beta*c_int*r_2*v_int_in - v_out_in)/(2*beta)
    return c_1, c_2

def hybrid_nor2_1_0_vint(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, c_1, c_2):
    return (c_1 * (1 / (c_int * r_2))) * np.exp(lambda_1 * t) + (c_2 * (1 / (c_int * r_2))) * np.exp(lambda_2 * t)

def hybrid_nor2_1_0_vout(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, c_1, c_2, res = 0.0):
    return (c_1 * (alpha + beta)) * np.exp(lambda_1 * t) + c_2 * (alpha - beta) * np.exp(lambda_2 * t) - res

def hybrid_nor2_1_0_vout_prime(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, c_1, c_2, res = 0.0):
    return c_1*lambda_1*(alpha + beta)*np.exp(lambda_1*t) + c_2*lambda_2*(alpha - beta)*np.exp(lambda_2*t)

def hybrid_nor2_1_1_initial_condition(v_dd, v_int_in, v_out_in):
    return v_int_in, v_out_in

def hybrid_nor2_1_1_vint(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, c_1, c_2):
    return c_1

def hybrid_nor2_1_1_vout(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, c_1, c_2, res=0.0):
    return c_2 * np.exp((-(1/(c_out*r_3) + 1/(c_out*r_4))) * t * scale_1) - res

def hybrid_nor2_1_1_vout_prime(t, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, c_1, c_2, res=0.0):
    return c_2*scale_1*(-1/(c_out*r_4) - 1/(c_out*r_3))*np.exp(scale_1*t*(-1/(c_out*r_4) - 1/(c_out*r_3)))

def full_output_checks(fsolve_res, full_output):
    if not full_output:
        return fsolve_res
    else:
        x, infodict, ier, mesg = fsolve_res
        my_print((x, infodict, ier, mesg), print_level, print_esc=False)
        return x


