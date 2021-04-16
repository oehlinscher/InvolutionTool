import sys
import matplotlib.pyplot as plt
import json
import sys
import os
import numpy as np
import shutil
import subprocess
import time
sys.path.append('../../experiment_setup/python')
from helper import *
from rawread import *
from vcdParser import *
from fixGIDMVCD import read_signal_transitions
sys.path.append('../plot_analog_waveform')
from generateTrace import *

circuit_file_path = "../../circuits/hlth_chain_L_15nm"

def main():
    # input_str = "0ns 0.0 1.100ns 0.0 1.101ns 0.5 1.107ns 0.5 1.108ns 0.3 1.114ns 0.3 1.115ns 0.5 1.119ns 0.5 1.120ns 0.3 1.123ns 0.3 1.124ns 0.6 1.127ns 0.6"

    # if input_str is not None:
    #     fin = open(circuit_file_path + "/main_new_orig.sp", "r")
    #     #output file to write the result to
    #     fout = open(circuit_file_path + "/main_new.sp", "w")
    #     #for each line in the input file
    #     for line in fin:
    #         #read replace the string and write to output file
    #         fout.write(line.replace('<I>', input_str))
    #         #close input and output files
    #     fin.close()
    #     fout.close()

    # Overwrite vectors_I file in vectors dir
    # dig_transitions = [(0, 0), (1000500, 1), (1002500, 0), (1004000, 1), (1005500, 0), (1007000, 1), (1008500, 0), (1010000, 1), (1011500, 0)]
    # delays = [3500, 2300, 2000, 1800, 1500]
    # delays = [0, 1570, 7000, 1550, 7000, 7000, 1550, 7000, 7000, 7000, 1500, 7000]
    # delays = [0, 8000, 1540, 8000] # Example input for cancelation of down pulse on B1 and canceled pulse on B2 (but the difference between the pure delays is not sufficient to decancel)
    # delays = [0, 12000, 4225, 12000] B4 / B5
    # delays = [0, 5000, 3000, 25000, 20000] # B4 / B5

    # THIS DELAY DOES SOMETHING INTERESTING
    # hlth_chain_L_15nm B6 / B7 # check 
    # delays = [0, 60000, 60000, 80000, 5780, 80000, 80000]     
    # delays = [0, 80000, 80000, 70000, 5600, 80000, 80000] 
    
    # lower bound
    # delays = [0, 80000, 80000, 70000, 8000, 80000, 80000] 
 
    # check
    # delays = [0, 80000, 80000, 70000, 9180, 70000, 70000, 80000] # WORKING
    # delays = [0, 80000, 80000, 50000, 7125, 70000, 70000, 80000] # EVEN BETTER
    # delays = [0, 80000, 80000, 50000, 7125, 25000, 6900, 80000, 80000] # MULTIPLE PULSES
    delays = [0, 80000, 80000, 50000, 7125, 25000, 6900, 25000, 6900, 80000, 80000] # MULTIPLE PULSES
    # delays = [0, 80000, 80000, 70000, 9180, 70000, 10250, 70000, 80000] # WORKING, multiple pulses

    # upper bound
    # delays = [0, 80000, 80000, 70000, 10000, 80000, 80000] 

    fout = open(circuit_file_path + "/vectors/vectors_I", "w")
    t = 1000500
    val = 1
    fout.write(str(0) + " " + str(1-val) + "\n")
    for delay in delays:
        t += delay
        fout.write(str(t) + " " + str(val) + "\n")
        val = 1 - val
    fout.close()

    # fout = open(circuit_file_path + "/vectors/vectors_I", "w")
    # for (t, value) in dig_transitions:
    #     fout.write(str(t) + " " + str(value) + "\n")
    # fout.close()


    results_folder = time.strftime("results/%Y%m%d_%H%M%S")
    if not os.path.exists("results"):
        os.mkdir("results")
    os.mkdir(results_folder)
    
    # execute_cmd("make clean")		
    os.environ["USE_GIDM"] = "True"
    os.environ["STRUCTURE_FILE"] = "structure.fix.json"
    os.environ["SDF_FILE"] = "hlth_L_custom.sdf"
    os.environ["SDF_FILE_GIDM"] = "hlth_L_fitting_gidm.sdf"
    

    # execute_cmd("make clean")	
    # execute_cmd("make spice")	
    execute_cmd("rm -rf modelsim")
    execute_cmd("rm -rf gates")
    execute_cmd("make sim")	
    # SPICE
    shutil.copy(circuit_file_path + "/generate.json", "./" + results_folder + "/")
    shutil.copy(circuit_file_path + "/input/main_new_exp.sp", "./" + results_folder + "/")
    shutil.copy(circuit_file_path + "/spice/main_new_exp.raw", "./" + results_folder + "/")
    shutil.copy(circuit_file_path + "/spice/main_new_exp.vcd0", "./" + results_folder + "/spice.vcd")
    # GIDM
    shutil.copy(circuit_file_path + "/modelsim/involution.vcd", "./" + results_folder + "/involution_gidm.vcd")
    shutil.move(circuit_file_path + "/tt", "./" + results_folder + "/")
    
    
    execute_cmd("rm -rf modelsim")
    execute_cmd("rm -rf gates")
    os.environ["USE_GIDM"] = "False"
    os.environ["STRUCTURE_FILE"] = "structure.fix.json"
    os.environ["SDF_FILE"] = "hlth_L_custom.sdf"
    os.environ["SDF_FILE_GIDM"] = "hlth_L_fitting_idm_fix.sdf"
    execute_cmd("make sim")	
    # IDM
    shutil.copyfile(circuit_file_path + "/modelsim/involution.vcd", "./" + results_folder + "/involution_idm.vcd")

    # results_folder = "20201116_171924"
    print(results_folder)		

    # Read the SPICE / GIDM and IDM Trace and plot it for each input:
    
    matching_dict = matching_file_to_dict(circuit_file_path + "/matching.json")
    darr, mdata = rawread(results_folder + "/main_new_exp.raw")
    
    spice_sig_to_raw_matching = {}
    for mytuple in darr[0].dtype.descr:
        if mytuple[0].endswith('_prime'):
            continue
        if mytuple[0] == 'time':
            continue

        if mytuple[0][2:-1].lower() not in matching_dict:
            continue

        spice_sig_to_raw_matching[mytuple[0][2:-1].lower()] = mytuple[0]


    spice_dig = dict_to_lower(read_modelsim(results_folder + "/spice.vcd", 0.8, 0.4, 0.0))
    gidm = dict_to_lower(read_modelsim(results_folder + "/involution_gidm.vcd", 0.8, 0.4, 0.0))
    idm = dict_to_lower(read_modelsim(results_folder + "/involution_idm.vcd", 0.8, 0.4, 0.0))

    port_to_signal_matching = dict()
    with open(circuit_file_path + "/port_to_signal_matching.json") as port_to_signal_matching_file:
        port_to_signal_matching = json.load(port_to_signal_matching_file)
 


    for spice_name, dig_name in matching_dict.items():
        # fig, axs = plt.subplots(4,figsize=(8,6), sharex=True)
        # offset = 0
        fig, axs = plt.subplots(3,figsize=(6,6), sharex=True)
        offset = -1
        # time_spice = darr[0]['time']
        # y_spice = darr[0][spice_sig_to_raw_matching[spice_name]]

        xlim = (1.05e-9, 1.45e-9)

        # axs[0].plot(time_spice, y_spice, label='SPICE')
        # axs[0].plot(np.array(spice_dig[spice_name][0])*1e-9, spice_dig[spice_name][1], label='SPICE dig', linestyle="--", alpha=0.7)
        # axs[0].hlines(y=0.4, xmin=xlim[0], xmax=xlim[1], color='black', linestyle=":", alpha=0.5)
        # axs[0].set_xlim(xlim)
        # axs[0].legend(loc='lower right')

        axs[1+offset].plot(np.array(gidm[dig_name][0])*1e-9, gidm[dig_name][1], label='GIDM')
        axs[1+offset].set_xlim(xlim)
        axs[1+offset].legend(loc='lower right')

        # read the transition information from the corresponding tt file
        signal_transitions = None
        for port, signal in port_to_signal_matching.items():
            if signal.lower() == dig_name.replace("]", "").replace("[", "").lower():
                # Check if there is a .complete file for port.lower
                tt_file_path = results_folder + "/tt/" + port + ".complete"
                if os.path.isfile(tt_file_path): 
                    signal_transitions = read_signal_transitions(tt_file_path) # The time is here in fs
                    break

                tt_file_path = results_folder + "/tt/" + dig_name.upper() + ".complete"
                if os.path.isfile(tt_file_path):  
                    signal_transitions = read_signal_transitions(tt_file_path) # The time is here in fs
                    break

        if signal_transitions is None:
            print("Could not find transition times for signal: ", dig_name)
        else:
            for trans in signal_transitions:
                color = None
                if trans[1] == 1:
                    color = 'red'
                else:
                    color = 'blue'
                axs[2+offset].axvline(x=trans[0] * 1e-15, ymin=0, ymax=1, color=color, linestyle="--", alpha=0.7)
                axs[2+offset].set_xlim(xlim)

            
            waveform = generate_waveform("../plot_analog_waveform/f_exp_up.dat", "../plot_analog_waveform/f_exp_down.dat", signal_transitions)
            
            axs[2+offset].plot(waveform[:,0], waveform[:,1]*0.8, label='GIDM / Exp')
            axs[2+offset].hlines(y=0.4, xmin=xlim[0], xmax=xlim[1], color='black', linestyle=":", alpha=0.5)
            axs[2+offset].legend(loc='lower right')
                   


        axs[3+offset].plot(np.array(idm[dig_name][0])*1e-9, idm[dig_name][1], label='IDM')
        axs[3+offset].set_xlim(xlim)
        axs[3+offset].legend(loc='lower right')

        
        plt.setp(axs[3+offset], xlabel='[s]')
        
        plt.savefig(results_folder + "/" + dig_name + ".pdf")


def execute_cmd(cmd):		
	
	make_process = subprocess.Popen(cmd, shell=True, cwd=circuit_file_path)
	if make_process.wait() != 0:
		my_print (cmd + " failed!", EscCodes.FAIL)
	else:
		my_print(cmd + " succeeded!", EscCodes.OKGREEN)

def dict_to_lower(dictionary):
	temp_dict = dict()
	for key, value in dictionary.items():
		temp_dict[key.lower()] = value
	dictionary = temp_dict
	return dictionary

if __name__ == "__main__":
    main()