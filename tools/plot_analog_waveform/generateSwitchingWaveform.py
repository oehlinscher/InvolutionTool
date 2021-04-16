"""
    
	Involution Tool
	File: generateSwitchingWaveform.py
	
    Copyright (C) 2018-2020  Daniel OEHLINGER <d.oehlinger@outlook.com>

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
import os
import json
import math
import numpy as np
from scipy.optimize import fsolve
sys.path.append('../../experiment_setup/python')
from helper import *
from readGateCfg import *


def main():
    if len(sys.argv) == 5:
        generate_switching_waveform(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        # Example how to pass dictionary via command line
        # python generateSwitchingWaveform.py EXP_CHANNEL '{"tau_up" : 1.5e-12,"tau_down" : 1.2e-12}' "" f_exp
        # python generateSwitchingWaveform.py SUMEXP_CHANNEL '{"x_1_up" : 0.25, "x_1_down" : 0.25, "tau_1_up" : 43e-15, "tau_1_down": 43e-15, "tau_2_up" : 4300e-15, "tau_2_down" : 4300e-15 }' "" f_sumexp
        # python generateSwitchingWaveform.py HILL_CHANNEL '{"n_up" : 1, "n_down" : 1, "k_up" : 1, "k_down": 1}' "" f_hill
        my_print("usage: python generateSwitchingWaveform.py channel_type parameter_dict output_folder_path prefix", EscCodes.FAIL)
        sys.exit(1)

# Generates up and down switching waveform table 
# Left column: time, right column: value
def generate_switching_waveform(channel_type, parameter_dict, output_folder_path, prefix):

    nr_of_samples = 50000
    difference_to_end = 0.00001 # For the rising EXP_CHANNEL we generate evenly spaced values from 0 to 1-difference_to_end
    parameter_dict = json.loads(parameter_dict)

    if channel_type == ChannelType.EXP_CHANNEL:
        # For the exp channel we expect the following parameters: tau_up, tau_down
        tau_up = parameter_dict["tau_up"]
        tau_down = parameter_dict["tau_down"]
        
        x_start = 0

        # Calculate f_up
        y_end = 1 - difference_to_end
        x_end = - tau_up * math.log(1 - y_end)
        x_values = np.linspace(x_start, x_end, nr_of_samples)
        y_values = 1 - np.exp(-x_values / tau_up)
        write_file(output_folder_path + prefix + "_up.dat", channel_type, parameter_dict, x_values, y_values)    

        # Calculate f_down
        y_end = 0 + difference_to_end
        x_end = - tau_down * math.log(y_end)
        x_values = np.linspace(x_start, x_end, nr_of_samples)
        y_values = np.exp(-x_values / tau_down)
        write_file(output_folder_path + prefix + "_down.dat", channel_type, parameter_dict, x_values, y_values)  

    elif channel_type == ChannelType.HILL_CHANNEL:
         # For the exp channel we expect the following parameters: n_up, n_do, k_up, k_do

        n_up = parameter_dict["n_up"]
        n_do = parameter_dict["n_down"]
        
        k_up = parameter_dict["k_up"]
        k_do = parameter_dict["k_down"]

        difference_to_end_hill = 1e-2 # should not be too small, since the function slowly approaches the end value

        x_start = 0

        # Calculate f_up
        y_end = 1 -  difference_to_end_hill
        x_end = math.pow((y_end * math.pow(k_do, n_do)) / (1 - y_end), 1/n_do)
        x_values = np.linspace(x_start, x_end, nr_of_samples)
        y_values = np.power(x_values, n_do) / (np.power(k_do, n_do) + np.power(x_values, n_do))
        write_file(output_folder_path + prefix + "_up.dat", channel_type, parameter_dict, x_values, y_values)   

        # Calculate f_down
        y_end = 0 +  difference_to_end_hill
        x_end = math.pow(((1 - y_end) * math.pow(k_up, n_up)) / (y_end), 1/n_up)
        x_values = np.linspace(x_start, x_end, nr_of_samples)
        y_values = 1 - np.power(x_values, n_up) / (np.power(k_up, n_up) + np.power(x_values, n_up))
        write_file(output_folder_path + prefix + "_down.dat", channel_type, parameter_dict, x_values, y_values)    

    elif channel_type == ChannelType.SUMEXP_CHANNEL:
        
        # For the exp channel we expect the following parameters: x_1_up, tau_1_up, tau_2_up, x_1_down, tau_1_down, tau_2_down
        x_1_up = parameter_dict["x_1_up"]
        tau_1_up = parameter_dict["tau_1_up"]
        tau_2_up = parameter_dict["tau_2_up"]
        x_1_down = parameter_dict["x_1_down"]
        tau_1_down = parameter_dict["tau_1_down"]
        tau_2_down = parameter_dict["tau_2_down"]

        x_start = 0

        # Calculate f_up
        y_end = 1 - difference_to_end
        x_end = fsolve(sum_exp_frsw_up_y, 1.0 ,args=(x_1_up, tau_1_up*1e20, tau_2_up*1e20, y_end))
        x_end = x_end[0] * 1e-20
        x_values = np.linspace(x_start, x_end, nr_of_samples)
        y_values = sum_exp_frsw_up(x_values, x_1_up, tau_1_up, tau_2_up)
        write_file(output_folder_path + prefix + "_up.dat", channel_type, parameter_dict, x_values, y_values)    

        # Calculate f_down
        y_end = 0 + difference_to_end
        x_end = fsolve(sum_exp_frsw_down_y, 1.0 ,args=(x_1_down, tau_1_down*1e20, tau_2_down*1e20, y_end))
        x_end = x_end[0] * 1e-20
        x_values = np.linspace(x_start, x_end, nr_of_samples)
        y_values = sum_exp_frsw_down(x_values, x_1_down, tau_1_down, tau_2_down)
        write_file(output_folder_path + prefix + "_down.dat", channel_type, parameter_dict, x_values, y_values)  

    else:
        my_print("Channel type not supported yet!", EscCodes.FAIL)

def sum_exp_frsw_up_y(x_values, x_1_down, tau_1_down, tau_2_down, y):
    return 1 - sum_exp_frsw_down_y(x_values, x_1_down, tau_1_down, tau_2_down, -y)

def sum_exp_frsw_up(x_values, x_1_down, tau_1_down, tau_2_down):
    return 1 - sum_exp_frsw_down_y(x_values, x_1_down, tau_1_down, tau_2_down, 0)

def sum_exp_frsw_down_y(x_values, x_1_down, tau_1_down, tau_2_down, y):
    return x_1_down*np.exp(-x_values / tau_1_down) + (1-x_1_down)*np.exp(-x_values / tau_2_down) - y

def sum_exp_frsw_down(x_values, x_1_down, tau_1_down, tau_2_down):
    return sum_exp_frsw_down_y(x_values, x_1_down, tau_1_down, tau_2_down, 0)

def write_file(filepath, channel_type, parameter_dict, x_values, y_values):     
    with open(filepath, "w") as f:
        f.write("#" + str(channel_type) + "\n")
        f.write("#" + str(parameter_dict) + "\n")
        #   
    with open(filepath, "ab") as f:
        np.savetxt(f, np.array(list(zip(x_values,y_values))))


if __name__ == "__main__":
    main()