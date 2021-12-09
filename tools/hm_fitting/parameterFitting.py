"""
    @file parameterFitting.py

	@brief Script for fitting the parameters of the hybrid delay model

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


import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import optimize
from scipy.optimize import LinearConstraint
import sympy as sp
from sympy import symbols, Symbol, solve, Poly, Eq, Function, exp, diff
import time
import math
import json
import sys


sys.path.append('../../experiment_setup/python')
from helper import to_bool

sys.path.append('../../experiment_setup/vhdl/python_channel')
from hybrid_nor2_delay_channel import *

c_factor = 1e-19
delay_factor = 1

# Main
def main():
    v_dd = 0.8
    v_th = 0.4

    # # nor_gate_15nm
    r_1 = 50000
    r_2 = 50000
    r_3 = 50000
    r_4 = 50000
    c_int = 1e-16 / c_factor
    c_out = 1e-15 / c_factor
    scale_1 = 1

    # Rising
    delay_1_0_to_0_0 = 5.499640386871877e-11 # Left
    delay_1_1_to_0_0 = 5.654233219903415e-11 # Center  
    delay_0_1_to_0_0 = 5.274166471655068e-11 # Right

    delay_0_0_to_0_1 = 3.886266628430315e-11 # Left
    delay_0_0_to_1_1 = 2.7966592079856073e-11 # Center
    delay_0_0_to_1_0 = 3.907790746216297e-11 # Right

    pd = 1.8e-11

    use_pd = False

    fitting_folder = "../../circuits/nor_gate_15nm/hm_fitting/"
    postfix = "_with_dmin"


    ###############

    t_min = 0
    t_max = 1000e-12
    
    # res = optimize.root(v_outs_fun, x0=(r_1, r_2, r_3, r_4, c_int, c_out), args=(v_dd, v_th, delay_0_1_to_0_0, delay_1_0_to_0_0, delay_1_1_to_0_0, delay_0_0_to_0_1, delay_0_0_to_1_0, delay_0_0_to_1_1, funs, grads), jac=v_outs_jac)    
    # res = optimize.root(v_outs_fun, x0=(r_1, r_2, r_3, r_4, c_int, c_out), args=(v_dd, v_th, delay_0_1_to_0_0, delay_1_0_to_0_0, delay_1_1_to_0_0, delay_0_0_to_0_1, delay_0_0_to_1_0, delay_0_0_to_1_1, funs, grads))    
        
    if use_pd:
        funs, grads  = v_outs(v_dd, v_th, delay_0_1_to_0_0, delay_1_0_to_0_0, delay_1_1_to_0_0, delay_0_0_to_0_1, delay_0_0_to_1_0, delay_0_0_to_1_1, use_pd)
        bounds = ([1, 1, 1, 1, 1e-30/c_factor, 1e-30/c_factor, 1e-5, 17e-12], [1e12, 1e12, 1e12, 1e12, 1e-8/c_factor, 1e-8/c_factor, 1e5, 19e-12])
        res = optimize.least_squares(v_outs_fun, x0=(r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pd), args=(v_dd, v_th, delay_0_1_to_0_0, delay_1_0_to_0_0, delay_1_1_to_0_0, delay_0_0_to_0_1, delay_0_0_to_1_0, delay_0_0_to_1_1, funs, grads, use_pd), bounds=bounds, xtol=2.5e-40, ftol=2.5e-16, gtol=2.5e-16)    
        r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pd = res.x
    else:        
        delay_0_1_to_0_0 = delay_0_1_to_0_0 - pd
        delay_1_0_to_0_0 = delay_1_0_to_0_0 - pd
        delay_1_1_to_0_0 = delay_1_1_to_0_0 - pd
        delay_0_0_to_0_1 = delay_0_0_to_0_1 - pd
        delay_0_0_to_1_0 = delay_0_0_to_1_0 - pd
        delay_0_0_to_1_1 = delay_0_0_to_1_1 - pd
        funs, grads  = v_outs(v_dd, v_th, delay_0_1_to_0_0, delay_1_0_to_0_0, delay_1_1_to_0_0, delay_0_0_to_0_1, delay_0_0_to_1_0, delay_0_0_to_1_1, use_pd)
        bounds = ([1, 1, 1, 1, 1e-30/c_factor, 1e-30/c_factor, 1e-5], [1e12, 1e12, 1e12, 1e12, 1e-8/c_factor, 1e-8/c_factor, 1e5])
        res = optimize.least_squares(v_outs_fun, x0=(r_1, r_2, r_3, r_4, c_int, c_out, scale_1), args=(v_dd, v_th, delay_0_1_to_0_0, delay_1_0_to_0_0, delay_1_1_to_0_0, delay_0_0_to_0_1, delay_0_0_to_1_0, delay_0_0_to_1_1, funs, grads, use_pd), bounds=bounds, xtol=2.5e-40, ftol=2.5e-16, gtol=2.5e-16)    
        r_1, r_2, r_3, r_4, c_int, c_out, scale_1 = res.x

    print(res)

    c_int = c_int * c_factor
    c_out = c_out * c_factor
    delay_0_1_to_0_0 = delay_0_1_to_0_0 * delay_factor
    delay_1_0_to_0_0 = delay_1_0_to_0_0 * delay_factor
    delay_1_1_to_0_0 = delay_1_1_to_0_0 * delay_factor
    delay_0_0_to_0_1 = delay_0_0_to_0_1 * delay_factor
    delay_0_0_to_1_0 = delay_0_0_to_1_0 * delay_factor
    delay_0_0_to_1_1 = delay_0_0_to_1_1 * delay_factor



    t = np.arange(2e-11, t_max, 1e-11)

    # System 0,1 -> 0,0
    v_int_in, v_out_in = v_dd, 0
    alpha, beta, gamma, lambda_1, lambda_2 = hybrid_nor2_0_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out)
    c_1, c_2 = hybrid_nor2_0_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, v_int_in, v_out_in)
    nor2_0_0_vout =  np.array([hybrid_nor2_0_0_vout(ti, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2) for ti in t])
    level_0_1_to_0_0 = hybrid_nor2_0_0_vout(delay_0_1_to_0_0, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2) 
    plt.plot(t, nor2_0_0_vout, label='0,1 to 0,0', color='blue', marker='o')
    plt.vlines(delay_0_1_to_0_0, 0, 0.8, color='blue', linestyles='dashed')

    
    # System 1,0 -> 0,0
    v_int_in, v_out_in = 0, 0
    alpha, beta, gamma, lambda_1, lambda_2 = hybrid_nor2_0_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out)
    c_1, c_2 = hybrid_nor2_0_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, v_int_in, v_out_in)
    nor2_0_0_vout =  np.array([hybrid_nor2_0_0_vout(ti, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2) for ti in t])
    level_1_0_to_0_0 = hybrid_nor2_0_0_vout(delay_1_0_to_0_0, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2) 
    plt.plot(t, nor2_0_0_vout, label='1,0 to 0,0', color='magenta', marker='v')
    plt.vlines(delay_1_0_to_0_0, 0, 0.8, color='magenta', linestyles='dashed')

    
    # System 1,1 -> 0,0
    v_int_in, v_out_in = 0, 0
    alpha, beta, gamma, lambda_1, lambda_2 = hybrid_nor2_0_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out)
    c_1, c_2 = hybrid_nor2_0_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, v_int_in, v_out_in)
    nor2_0_0_vout =  np.array([hybrid_nor2_0_0_vout(ti, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2) for ti in t])
    level_1_1_to_0_0 = hybrid_nor2_0_0_vout(delay_1_1_to_0_0, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, gamma, lambda_1, lambda_2, c_1, c_2) 
    plt.plot(t, nor2_0_0_vout, label='1,1 to 0,0', color='indigo', marker='s')
    plt.vlines(delay_1_1_to_0_0, 0, 0.8, color='indigo', linestyles='dashed')


    # System 0,0 -> 1,0
    v_int_in, v_out_in = v_dd, v_dd
    alpha, beta, lambda_1, lambda_2 = hybrid_nor2_1_0_helper(v_dd, r_1, r_2, r_3, r_4, c_int, c_out)
    c_1, c_2 = hybrid_nor2_1_0_initial_condition(v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, v_int_in, v_out_in)
    nor2_1_0_vout = np.array([hybrid_nor2_1_0_vout(ti, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, c_1, c_2) for ti in t])
    level_1_0 = hybrid_nor2_1_0_vout(delay_0_0_to_1_0, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, alpha, beta, lambda_1, lambda_2, c_1, c_2) 
    plt.plot(t, nor2_1_0_vout, label='0,0 to 1,0', color='orange', marker='1')
    plt.vlines(delay_0_0_to_1_0, 0, 0.8, color='orange', linestyles='dashed')

    # System 0,0 -> 0,1
    v_int_in, v_out_in = v_dd, v_dd
    c_1, c_2 = hybrid_nor2_0_1_initial_condition(v_dd, v_int_in, v_out_in)
    nor2_0_1_vout = np.array([hybrid_nor2_0_1_vout(ti, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, c_1, c_2) for ti in t])
    level_0_1 = hybrid_nor2_0_1_vout(delay_0_0_to_0_1, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, c_1, c_2) 
    plt.plot(t, nor2_0_1_vout, label='0,0 to 0,1', color='red', marker='|')
    plt.vlines(delay_0_0_to_0_1, 0, 0.8, color='red', linestyles='dashed')

    # System 0,0 -> 1,1
    v_int_in, v_out_in = v_dd, v_dd
    c_1, c_2 = hybrid_nor2_1_1_initial_condition(v_dd, v_int_in, v_out_in)
    nor2_1_1_vout = np.array([hybrid_nor2_1_1_vout(ti, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, c_1, c_2) for ti in t])
    level_1_1 = hybrid_nor2_1_1_vout(delay_0_0_to_1_1, v_dd, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, c_1, c_2) 
    plt.plot(t, nor2_1_1_vout, label='0,0 to 1,1', color='green', marker='*')
    plt.vlines(delay_0_0_to_1_1, 0, 0.8, color='green', linestyles='dashed')

    # Calculate the deviation for all 4 systems
    print("0,1->0/0: {level_0_1_to_0_0}\n1/0->0/0: {level_1_0_to_0_0}\n1/1->0/0: {level_1_1_to_0_0}\n1/0: {level_1_0}\n0/1: {level_0_1}\n1/1: {level_1_1}".format(level_0_1_to_0_0 = level_0_1_to_0_0, level_1_0_to_0_0 = level_1_0_to_0_0, level_1_1_to_0_0 = level_1_1_to_0_0, level_0_1 = level_0_1, level_1_0 = level_1_0, level_1_1 = level_1_1))
    dev_0_1_to_0_0 = v_th - level_0_1_to_0_0
    dev_1_0_to_0_0 = v_th - level_1_0_to_0_0
    dev_1_1_to_0_0 = v_th - level_1_1_to_0_0
    dev_1_0 = v_th - level_1_0
    dev_0_1 = v_th - level_0_1
    dev_1_1 = v_th - level_1_1
    total_dev = abs(dev_0_1_to_0_0) + abs(dev_1_0_to_0_0) + abs(dev_1_1_to_0_0) + abs(dev_1_0) + abs(dev_0_1) + abs(dev_1_1)
    print(r_1, r_2, r_3, r_4, c_int, c_out)
    print("Deviations:\n0/1->0/0:{dev_0_1_to_0_0}\n1/0->0/0:{dev_1_0_to_0_0}\n1/1->0/0:{dev_1_1_to_0_0}\n1/0:{dev_1_0}\n0/1:{dev_0_1}\n1/1:{dev_1_1}\n{total_dev}".format(dev_0_1_to_0_0 = dev_0_1_to_0_0, dev_1_0_to_0_0 = dev_1_0_to_0_0, dev_1_1_to_0_0 = dev_1_1_to_0_0, dev_1_0 = dev_1_0, dev_0_1 = dev_0_1, dev_1_1 = dev_1_1, total_dev = total_dev))

    plt.hlines(v_th, t_min, t_max)

    plt.xlabel('$t [s]$')
    plt.ylabel('$V_{out} [V]$')
    plt.legend()
    plt.xlim((0, 0.4e-9))
    # plt.xlim((0, 0.4e-10))
    # plt.show()

    
    plt.savefig(fitting_folder + "fitting_plot" + postfix + ".png", dpi=1000)

    
    print("r_1 = {}".format(r_1))
    print("r_2 = {}".format(r_2))
    print("r_3 = {}".format(r_3))
    print("r_4 = {}".format(r_4))
    print("c_int = {}".format(c_int))
    print("c_out = {}".format(c_out))
    print("scale_1 = {}".format(scale_1))
    print("pd = {}".format(pd))

    
    with open(fitting_folder + 'fitting_result' + postfix + ".json", 'w') as outfile:
        json.dump((r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pd), outfile)


# Helpers
def v_outs(v_dd, v_th, delay_0_1_to_0_0, delay_1_0_to_0_0, delay_1_1_to_0_0, delay_0_0_to_0_1, delay_0_0_to_1_0, delay_0_0_to_1_1, use_pd):
    # Symbols for our parameters
    r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pd = symbols('r_1 r_2 r_3 r_4 c_int c_out scale_1 pd')

    # System 0,0 -> 0,1
    v_int_in_0_1, v_out_in_0_1 = v_dd, v_dd
    c_2_0_1 = v_out_in_0_1
    t = delay_0_0_to_0_1
    if use_pd:
         t = delay_0_0_to_0_1 + pd
    fun_0_0_to_0_1 = c_2_0_1 * exp(-(t) * delay_factor / ((c_out * c_factor) * r_4))

    # System 0,0 -> 1,1
    v_int_in_1_1, v_out_in_1_1 = v_dd, v_dd
    c_2_1_1 = v_out_in_1_1
    # fun_0_0_to_1_1 = c_2_1_1 * exp((-(1/(c_out * c_factor*r_3) + 1/(c_out * c_factor*r_4))) * delay_0_0_to_1_1 * delay_factor * scale_1)
    t = delay_0_0_to_1_1
    if use_pd:
         t = delay_0_0_to_1_1 + pd
    fun_0_0_to_1_1 = c_2_1_1 * exp((-(1/(c_out * c_factor*r_3) + 1/(c_out * c_factor*r_4))) * (t) * delay_factor)

    # System 0,0 -> 1,0
    v_int_in_1_0, v_out_in_1_0 = v_dd, v_dd # TODO Check with smaller V_int?
    alpha = (c_out * c_factor * r_3 - c_int * c_factor*(r_2 + r_3)) / (2*c_out * c_factor*c_int * c_factor*r_2*r_3)
    beta = sp.sqrt((c_out * c_factor*r_3 + c_int * c_factor*(r_2 + r_3))**2 - 4 * c_out * c_factor * c_int * c_factor * r_2 * r_3) / (2*c_out * c_factor*c_int * c_factor *r_2*r_3)
    lambda_base = -(c_out * c_factor * r_3 + c_int * c_factor*(r_2 + r_3)) / (2 * c_out * c_factor * c_int * c_factor * r_2 * r_3)
    lambda_1 = lambda_base + beta
    lambda_2 = lambda_base - beta
    c_1 = (-alpha*c_int * c_factor*r_2*v_int_in_1_0 + beta*c_int * c_factor*r_2*v_int_in_1_0 + v_out_in_1_0)/(2*beta)
    c_2 = (alpha*c_int * c_factor*r_2*v_int_in_1_0 + beta*c_int * c_factor*r_2*v_int_in_1_0 - v_out_in_1_0)/(2*beta)
    t = delay_0_0_to_1_0
    if use_pd:
         t = delay_0_0_to_1_0 + pd
    fun_0_0_to_1_0 = (c_1 * (alpha + beta)) * exp(lambda_1 * (t) * delay_factor) + c_2 * (alpha - beta) * exp(lambda_2 * (t) * delay_factor)
    
    # System 0,1 -> 0,0
    v_int_in_0_0, v_out_in_0_0 = v_dd, 0
    denominator = (2 * c_out * c_factor * c_int * c_factor * r_1 * r_2)
    alpha = (c_out * c_factor * (r_1 + r_2) - c_int * c_factor * r_1) / denominator
    beta = sp.sqrt((c_int * c_factor * r_1 + c_out * c_factor * (r_1 + r_2))**2 - 4 * c_out * c_factor * c_int * c_factor * r_1 * r_2) / denominator
    gamma = -(c_int * c_factor * r_1 + c_out * c_factor * (r_1 + r_2)) / denominator
    lambda_1 = gamma + beta
    lambda_2 = gamma - beta
    c_1 = (-alpha*beta*c_int * c_factor*r_1*r_2*v_int_in_0_0 - alpha*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 - alpha*r_2*v_dd + beta**2*c_int * c_factor*r_1*r_2*v_int_in_0_0 + beta*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 + beta*r_1*v_out_in_0_0 + beta*r_2*v_dd + gamma*r_1*v_out_in_0_0)/(2*beta**2*r_1 + 2*beta*gamma*r_1)
    c_2 = (alpha*beta*c_int * c_factor*r_1*r_2*v_int_in_0_0 - alpha*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 - alpha*r_2*v_dd + beta**2*c_int * c_factor*r_1*r_2*v_int_in_0_0 - beta*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 - beta*r_1*v_out_in_0_0 - beta*r_2*v_dd + gamma*r_1*v_out_in_0_0)/(2*beta**2*r_1 - 2*beta*gamma*r_1)
    t = delay_0_1_to_0_0
    if use_pd:
         t = delay_0_1_to_0_0 + pd
    fun_0_1_to_0_0 = (c_1 * (alpha + beta)) * exp(lambda_1 * (t) * delay_factor) + (c_2 * (alpha - beta)) * exp(lambda_2 * (t) * delay_factor) + (v_dd * (-(alpha*alpha)+beta*beta)*r_2) / (r_1 * (gamma * gamma - beta * beta))
    
    # System 1,0 -> 0,0
    v_int_in_0_0, v_out_in_0_0 = 0, 0
    denominator = (2 * c_out * c_factor * c_int * c_factor * r_1 * r_2)
    alpha = (c_out * c_factor * (r_1 + r_2) - c_int * c_factor * r_1) / denominator
    beta = sp.sqrt((c_int * c_factor * r_1 + c_out * c_factor * (r_1 + r_2))**2 - 4 * c_out * c_factor * c_int * c_factor * r_1 * r_2) / denominator
    gamma = -(c_int * c_factor * r_1 + c_out * c_factor * (r_1 + r_2)) / denominator
    lambda_1 = gamma + beta
    lambda_2 = gamma - beta
    c_1 = (-alpha*beta*c_int * c_factor*r_1*r_2*v_int_in_0_0 - alpha*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 - alpha*r_2*v_dd + beta**2*c_int * c_factor*r_1*r_2*v_int_in_0_0 + beta*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 + beta*r_1*v_out_in_0_0 + beta*r_2*v_dd + gamma*r_1*v_out_in_0_0)/(2*beta**2*r_1 + 2*beta*gamma*r_1)
    c_2 = (alpha*beta*c_int * c_factor*r_1*r_2*v_int_in_0_0 - alpha*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 - alpha*r_2*v_dd + beta**2*c_int * c_factor*r_1*r_2*v_int_in_0_0 - beta*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 - beta*r_1*v_out_in_0_0 - beta*r_2*v_dd + gamma*r_1*v_out_in_0_0)/(2*beta**2*r_1 - 2*beta*gamma*r_1)
    t = delay_1_0_to_0_0
    if use_pd:
         t = delay_1_0_to_0_0 + pd
    fun_1_0_to_0_0 = (c_1 * (alpha + beta)) * exp(lambda_1 * (t) * delay_factor) + (c_2 * (alpha - beta)) * exp(lambda_2 * (t) * delay_factor) + (v_dd * (-(alpha*alpha)+beta*beta)*r_2) / (r_1 * (gamma * gamma - beta * beta))

    # System 1,1 -> 0,0
    v_int_in_0_0, v_out_in_0_0 = 0, 0
    denominator = (2 * c_out * c_factor * c_int * c_factor * r_1 * r_2)
    alpha = (c_out * c_factor * (r_1 + r_2) - c_int * c_factor * r_1) / denominator
    beta = sp.sqrt((c_int * c_factor * r_1 + c_out * c_factor * (r_1 + r_2))**2 - 4 * c_out * c_factor * c_int * c_factor * r_1 * r_2) / denominator
    gamma = -(c_int * c_factor * r_1 + c_out * c_factor * (r_1 + r_2)) / denominator
    lambda_1 = gamma + beta
    lambda_2 = gamma - beta
    c_1 = (-alpha*beta*c_int * c_factor*r_1*r_2*v_int_in_0_0 - alpha*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 - alpha*r_2*v_dd + beta**2*c_int * c_factor*r_1*r_2*v_int_in_0_0 + beta*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 + beta*r_1*v_out_in_0_0 + beta*r_2*v_dd + gamma*r_1*v_out_in_0_0)/(2*beta**2*r_1 + 2*beta*gamma*r_1)
    c_2 = (alpha*beta*c_int * c_factor*r_1*r_2*v_int_in_0_0 - alpha*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 - alpha*r_2*v_dd + beta**2*c_int * c_factor*r_1*r_2*v_int_in_0_0 - beta*c_int * c_factor*gamma*r_1*r_2*v_int_in_0_0 - beta*r_1*v_out_in_0_0 - beta*r_2*v_dd + gamma*r_1*v_out_in_0_0)/(2*beta**2*r_1 - 2*beta*gamma*r_1)
    t = delay_1_1_to_0_0
    if use_pd:
         t = delay_1_1_to_0_0 + pd
    fun_1_1_to_0_0 = (c_1 * (alpha + beta)) * exp(lambda_1 * (t) * delay_factor) + (c_2 * (alpha - beta)) * exp(lambda_2 * (t) * delay_factor) + (v_dd * (-(alpha*alpha)+beta*beta)*r_2) / (r_1 * (gamma * gamma - beta * beta))


    f_empty = v_th

    f_3_l = f_empty
    f_3_c = f_empty
    f_3_r = f_empty
    f_5_l = f_empty
    f_5_c = f_empty
    f_5_r = f_empty

    # Select points to optimize
    f_3_l = fun_0_0_to_0_1
    # f_3_c = fun_0_0_to_1_1
    f_3_r = fun_0_0_to_1_0

    f_5_l = fun_1_0_to_0_0
    # f_5_c = fun_1_1_to_0_0
    f_5_r = fun_0_1_to_0_0

    funs = list()
    grads = list()
    for f in [f_3_l, f_3_c, f_3_r, f_5_l, f_5_c, f_5_r]:    
        if use_pd:
            funs.append(sp.lambdify([r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pd], f - v_th, 'numpy'))
            gf = [sp.diff(f - v_th, var) for var in (r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pd)]
            grads.append(sp.lambdify([r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pd], gf, 'numpy'))
        else:
            funs.append(sp.lambdify([r_1, r_2, r_3, r_4, c_int, c_out, scale_1], f - v_th, 'numpy'))
            gf = [sp.diff(f - v_th, var) for var in (r_1, r_2, r_3, r_4, c_int, c_out, scale_1)]
            grads.append(sp.lambdify([r_1, r_2, r_3, r_4, c_int, c_out, scale_1], gf, 'numpy'))
    
    print("Necessary functions calculated.")

    return funs, grads

def v_outs_fun(params, v_dd, v_th, delay_0_1_to_0_0, delay_1_0_to_0_0, delay_1_1_to_0_0, delay_0_0_to_0_1, delay_0_0_to_1_0, delay_0_0_to_1_1, funs, grads, use_pd):  
    if use_pd:
        p_r_1, p_r_2, p_r_3, p_r_4, p_c_int, p_c_out, p_scale_1, pd = params
    else:
        p_r_1, p_r_2, p_r_3, p_r_4, p_c_int, p_c_out, p_scale_1 = params
    vals = list()
    for f in funs:
        if use_pd:
            vals.append(f(p_r_1, p_r_2, p_r_3, p_r_4, p_c_int, p_c_out, p_scale_1, pd))
        else:
            vals.append(f(p_r_1, p_r_2, p_r_3, p_r_4, p_c_int, p_c_out, p_scale_1))

    print("Fun: ", vals)
    
    return np.array(vals)

def v_outs_jac(params, v_dd, v_th, delay_0_1_to_0_0, delay_1_0_to_0_0, delay_1_1_to_0_0, delay_0_0_to_0_1, delay_0_0_to_1_0, delay_0_0_to_1_1, funs, grads, use_pd):   
    if use_pd:
        p_r_1, p_r_2, p_r_3, p_r_4, p_c_int, p_c_out, p_scale_1, pd = params
    else:
        p_r_1, p_r_2, p_r_3, p_r_4, p_c_int, p_c_out, p_scale_1 = params
    vals = list()
    for g in grads:
        if use_pd:
            vals.append(g(p_r_1, p_r_2, p_r_3, p_r_4, p_c_int, p_c_out, p_scale_1, pd))
        else:            
            vals.append(g(p_r_1, p_r_2, p_r_3, p_r_4, p_c_int, p_c_out, p_scale_1))

    print("Grads: ", vals)
    
    return np.array(vals)

if __name__ == "__main__":
    main()