"""
    
	Involution Tool
	File: prepareFigureData.py
	
    Copyright (C) 2018-2019  Daniel OEHLINGER <d.oehlinger@outlook.com>

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
import matplotlib
import math
import csv
from helper import *
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from parserHelper import *
from vcdParser import *


def main():
	if len(sys.argv) != 10:
		my_print("usage: python prepareFigureData.py start_out_name crossings_file involution_vcd modelsim_vcd matching_file fig_dir tex_template_file results_file line_template", EscCodes.FAIL)
		sys.exit(1)
	prepareFigureData(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])



vdd = 1.0
vss = 0.0
vth = 0.5
	
def prepareFigureData(start_out_name, crossings_file, involution_vcd, modelsim_vcd, matching_file, fig_dir, tex_template_file, results_file, line_template):
	global vdd, vss, vth
	
	MATCHING = []
		
	fig_folder = fig_dir
	# check if output folder exists
	if not os.path.exists(fig_folder):
		os.makedirs(fig_folder)

	with open(matching_file, 'r') as f:
		for line in f.readlines():
			parts = line.strip(' \t\n\r').split(' ')
			MATCHING.append([parts[0],parts[1]])
			
			
	if "VDD" in os.environ:
		vdd = float(os.environ["VDD"])
		
	if "VTH" in os.environ:
		vth = float(os.environ["VTH"])
		
	if "VSS" in os.environ:
		vss = float(os.environ["VSS"])

	my_print(str(MATCHING))

	with open(crossings_file, 'r') as f:
		spiceData=json.load(f)
		
	involutionData = read_modelsim(involution_vcd, vdd, vth, vss)
	modelsimData = read_modelsim(modelsim_vcd, vdd, vth, vss)
	
	my_print("\ttransition count \t \t \tsum(error(.))")
	my_print("name\tSPICE\tInvolution\tModelsim\tInvolution\tModelsim")
		
	content = ""	
	# extend the results file with the max / sum values
	max_values_dict = dict()
	max_values_dict["max_tc_dev_per_inv"] = 0
	max_values_dict["max_tc_dev_abs_inv"] = 0
	max_values_dict["max_tc_dev_per_msim"] = 0
	max_values_dict["max_tc_dev_abs_msim"] = 0
	
	max_values_dict["total_sum_error_inv"] = 0
	max_values_dict["total_pos_area_under_dev_trace_inv"] = 0
	max_values_dict["total_neg_area_under_dev_trace_inv"] = 0
	max_values_dict["total_pos_area_under_dev_trace_inv_wo_glitches"] = 0
	max_values_dict["total_neg_area_under_dev_trace_inv_wo_glitches"] = 0
	max_values_dict["total_pos_area_under_dev_trace_inv_transitions"] = 0
	max_values_dict["total_neg_area_under_dev_trace_inv_transitions"] = 0
	max_values_dict["total_pos_area_under_dev_trace_inv_transitions_wo_glitches"] = 0
	max_values_dict["total_neg_area_under_dev_trace_inv_transitions_wo_glitches"] = 0
	
	max_values_dict["total_sum_error_msim"] = 0
	max_values_dict["total_pos_area_under_dev_trace_msim"] = 0
	max_values_dict["total_neg_area_under_dev_trace_msim"] = 0
	max_values_dict["total_pos_area_under_dev_trace_msim_wo_glitches"] = 0
	max_values_dict["total_neg_area_under_dev_trace_msim_wo_glitches"] = 0
	max_values_dict["total_pos_area_under_dev_trace_msim_transitions"] = 0
	max_values_dict["total_neg_area_under_dev_trace_msim_transitions"] = 0
	max_values_dict["total_pos_area_under_dev_trace_msim_transitions_wo_glitches"] = 0
	max_values_dict["total_neg_area_under_dev_trace_msim_transitions_wo_glitches"] = 0

	max_values_dict["total_sum_glitches_spice_inv"] = 0
	max_values_dict["total_sum_glitches_orig_spice_inv"] = 0
	max_values_dict["total_sum_glitches_inverted_spice_inv"] = 0

	max_values_dict["total_sum_glitches_inv"] = 0
	max_values_dict["total_sum_glitches_orig_inv"] = 0
	max_values_dict["total_sum_glitches_inverted_inv"] = 0

	max_values_dict["total_sum_glitches_spice_msim"] = 0
	max_values_dict["total_sum_glitches_orig_spice_msim"] = 0
	max_values_dict["total_sum_glitches_inverted_spice_msim"] = 0

	max_values_dict["total_sum_glitches_msim"] = 0
	max_values_dict["total_sum_glitches_orig_msim"] = 0
	max_values_dict["total_sum_glitches_inverted_msim"] = 0 
	
	max_values_dict["total_tc_spice"] = 0
	max_values_dict["total_tc_msim"] = 0
	max_values_dict["total_tc_inv"] = 0
	
	max_values_dict["last_transition_time"] = 0
	max_values_dict["first_transition_time"] = 0
		
	# Define y-axis limits	
	y_margin = 0.2
	ylim_start = vss - y_margin
	ylim_end = vdd + y_margin
	
	# Define x-axis limits (global for all signals, so that we can better compare different plots)
	# we can ignore the "deviation" traces for this part, since the first "transition" is at the first transition
	# of either the trace or the inv / modelsim signal
	x_first = sys.float_info.max
	x_last = sys.float_info.min	
	overlapping = 0.1
	zoom_number = 3	
	
	if "FIGURE_ZOOM_NUMBER" in os.environ:
		zoom_number = int(os.environ["FIGURE_ZOOM_NUMBER"])
	
	if "FIGURE_ZOOM_OVERLAPPING" in os.environ:
		overlapping = float(os.environ["FIGURE_ZOOM_OVERLAPPING"]) 
		
	inv_export_dev_trace_inf = True
	if "FIGURE_INV_EXPORT_DEV_TRACE_INFO" in os.environ:
		inv_export_dev_trace_inf = to_bool(os.environ["FIGURE_INV_EXPORT_DEV_TRACE_INFO"]) 
				
	msim_export_dev_trace_inf = True
	if "FIGURE_MSIM_EXPORT_DEV_TRACE_INFO" in os.environ:
		msim_export_dev_trace_inf = to_bool(os.environ["FIGURE_MSIM_EXPORT_DEV_TRACE_INFO"]) 
	
	round_digits = -1 # next 10e-1, e.g. 0.17 = 0.2, 0.13 = 0.1
		
	
	# before we do anything => convert key to lower()
	for idx, (spice_name, msim_name) in enumerate(MATCHING):
			MATCHING[idx] = (spice_name.lower(), msim_name.lower())
	spiceData['crossing_times'] = dict_key_to_lower_case(spiceData['crossing_times'])
	spiceData['initial_values'] = dict_key_to_lower_case(spiceData['initial_values'])
	involutionData = dict_key_to_lower_case(involutionData)
	modelsimData = dict_key_to_lower_case(modelsimData)
				
	for entry in MATCHING:		
		#print(spiceData['crossing_times'])
		signal_name = entry[1]
		
		if len(spiceData['crossing_times'][entry[0]]) > 1:
			# print spiceData['crossing_times'][entry[0]]
			# print trace[0][1]
		
			x_first = min(x_first, spiceData['crossing_times'][entry[0]][0] * 1e-9)
			x_last = max(x_last, spiceData['crossing_times'][entry[0]][-1] * 1e-9)
		if len(involutionData[signal_name][0]) > 1:
			x_first = min(x_first, involutionData[signal_name][0][1])
			x_last = max(x_last, involutionData[signal_name][0][-1])
		if len(modelsimData[signal_name][0]) > 1:
			x_first = min(x_first, modelsimData[signal_name][0][1])
			x_last = max(x_last, modelsimData[signal_name][0][-1])
	
	# Used for evaluating the overall simulation time	
	max_values_dict["last_transition_time"] = x_last
	max_values_dict["first_transition_time"] = x_first
	
	x_first = math.floor(x_first * pow(10, round_digits * -1)) / (pow(10, round_digits * -1))
	x_last = math.ceil(x_last * pow(10, round_digits * -1)) / (pow(10, round_digits * -1))
	x_last = x_last + 0.2 # "margin" at the right border 
		
	
	for entry in MATCHING:
		signal_name = entry[1]
		
		# get the traces from the various dump files
		trace = get_trace(spiceData['crossing_times'][entry[0]], spiceData['initial_values'][entry[0]]);
		
		dataInv = involutionData[signal_name]	
		dev_trace_inv_results = get_deviation_trace(trace, dataInv, inv_export_dev_trace_inf, fig_folder, 'inv_' + signal_name)			
		
		dataModelsim = modelsimData[signal_name]
		dev_trace_msim_results = get_deviation_trace(trace, dataModelsim, msim_export_dev_trace_inf, fig_folder, 'msim_' + signal_name)
				
		tc_spice = (len(trace[0])-1)/2
		tc_involution = len(dataInv[0])/2
		tc_modelsim = len(dataModelsim[0])/2
		if dataModelsim[1][0] == vth:
			# if the first transition is from X to 0 or 1,
			# ignore this transition, because neither SPICE nor Involution have this transition
			tc_modelsim -= 1
				
		# print the trace "results"
		my_print("%s\t%d\t%d\t\t%d\t\t%.3f\t\t%.3f" %(signal_name, tc_spice , tc_involution, tc_modelsim, dev_trace_inv_results["total_area_under_dev_trace"], dev_trace_msim_results["total_area_under_dev_trace"]))
		
		# prepare the content for the waveform comparison table in the report				
		content += line_template \
		.replace("%##NAME##%", replace_special_chars(signal_name)) \
		.replace("%##TC_SPICE##%", str(tc_spice)) \
		.replace("%##TC_INVOLUTION##%", str(tc_involution)) \
		.replace("%##TC_MSIM##%", str(tc_modelsim)) \
		.replace("%##TOTAL_AREA_UNDER_DEV_TRACE_INV##%", str(dev_trace_inv_results["total_area_under_dev_trace"])) \
		.replace("%##TOTAL_POS_AREA_UNDER_DEV_TRACE_INV##%", str(dev_trace_inv_results["pos_area_under_dev_trace"])) \
		.replace("%##TOTAL_NEG_AREA_UNDER_DEV_TRACE_INV##%", str(dev_trace_inv_results["neg_area_under_dev_trace"])) \
		.replace("%##TOTAL_AREA_UNDER_DEV_TRACE_MSIM##%", str(dev_trace_msim_results["total_area_under_dev_trace"])) \
		.replace("%##TOTAL_POS_AREA_UNDER_DEV_TRACE_MSIM##%", str(dev_trace_msim_results["pos_area_under_dev_trace"]))\
		.replace("%##TOTAL_NEG_AREA_UNDER_DEV_TRACE_MSIM##%", str(dev_trace_msim_results["neg_area_under_dev_trace"])) \
		.replace("%##GLITCHES_SPICE_INV##%", str(dev_trace_inv_results["total_glitches_tr0"])) \
		.replace("%##GLITCHES_ORIG_SPICE_INV##%", str(dev_trace_inv_results["orig_glitches_tr0"])) \
		.replace("%##GLITCHES_INVERTED_SPICE_INV##%", str(dev_trace_inv_results["inverted_glitches_tr0"])) \
		.replace("%##GLITCHES_SPICE_MSIM##%", str(dev_trace_msim_results["total_glitches_tr0"])) \
		.replace("%##GLITCHES_ORIG_SPICE_MSIM##%", str(dev_trace_msim_results["orig_glitches_tr0"])) \
		.replace("%##GLITCHES_INVERTED_SPICE_MSIM##%", str(dev_trace_msim_results["inverted_glitches_tr0"])) \
		.replace("%##GLITCHES_INV##%", str(dev_trace_inv_results["total_glitches_tr1"])) \
		.replace("%##GLITCHES_ORIG_INV##%", str(dev_trace_inv_results["orig_glitches_tr1"])) \
		.replace("%##GLITCHES_INVERTED_INV##%", str(dev_trace_inv_results["inverted_glitches_tr1"])) \
		.replace("%##GLITCHES_MSIM##%", str(dev_trace_msim_results["total_glitches_tr1"])) \
		.replace("%##GLITCHES_ORIG_MSIM##%", str(dev_trace_msim_results["orig_glitches_tr1"])) \
		.replace("%##GLITCHES_INVERTED_MSIM##%", str(dev_trace_msim_results["inverted_glitches_tr1"])) \
		+ "\n"				
		
		# calculate overall values for results.json file				
		max_values_dict["total_sum_error_inv"] += dev_trace_inv_results["total_area_under_dev_trace"]
		max_values_dict["total_pos_area_under_dev_trace_inv"] += dev_trace_inv_results["pos_area_under_dev_trace"]
		max_values_dict["total_neg_area_under_dev_trace_inv"] += dev_trace_inv_results["neg_area_under_dev_trace"]
		
		max_values_dict["total_pos_area_under_dev_trace_inv_wo_glitches"] += dev_trace_inv_results["pos_area_under_dev_trace_wo_glitches"]
		max_values_dict["total_neg_area_under_dev_trace_inv_wo_glitches"] += dev_trace_inv_results["neg_area_under_dev_trace_wo_glitches"]
		max_values_dict["total_pos_area_under_dev_trace_inv_transitions"] += dev_trace_inv_results["pos_area_under_dev_trace_transitions"]
		max_values_dict["total_neg_area_under_dev_trace_inv_transitions"] += dev_trace_inv_results["neg_area_under_dev_trace_transitions"]
		max_values_dict["total_pos_area_under_dev_trace_inv_transitions_wo_glitches"] += dev_trace_inv_results["pos_area_under_dev_trace_transitions_wo_glitches"]
		max_values_dict["total_neg_area_under_dev_trace_inv_transitions_wo_glitches"] += dev_trace_inv_results["neg_area_under_dev_trace_transitions_wo_glitches"]	
				
		max_values_dict["total_sum_error_msim"] += dev_trace_msim_results["total_area_under_dev_trace"]
		max_values_dict["total_pos_area_under_dev_trace_msim"] += dev_trace_msim_results["pos_area_under_dev_trace"]
		max_values_dict["total_neg_area_under_dev_trace_msim"] += dev_trace_msim_results["neg_area_under_dev_trace"]
					
		max_values_dict["total_pos_area_under_dev_trace_msim_wo_glitches"] += dev_trace_msim_results["pos_area_under_dev_trace_wo_glitches"]
		max_values_dict["total_neg_area_under_dev_trace_msim_wo_glitches"] += dev_trace_msim_results["neg_area_under_dev_trace_wo_glitches"]
		max_values_dict["total_pos_area_under_dev_trace_msim_transitions"] += dev_trace_msim_results["pos_area_under_dev_trace_transitions"]
		max_values_dict["total_neg_area_under_dev_trace_msim_transitions"] += dev_trace_msim_results["neg_area_under_dev_trace_transitions"]
		max_values_dict["total_pos_area_under_dev_trace_msim_transitions_wo_glitches"] += dev_trace_msim_results["pos_area_under_dev_trace_transitions_wo_glitches"]
		max_values_dict["total_neg_area_under_dev_trace_msim_transitions_wo_glitches"] += dev_trace_msim_results["neg_area_under_dev_trace_transitions_wo_glitches"]
				
		max_values_dict["total_sum_glitches_spice_inv"] += dev_trace_inv_results["total_glitches_tr0"]
		max_values_dict["total_sum_glitches_orig_spice_inv"] += dev_trace_inv_results["orig_glitches_tr0"]
		max_values_dict["total_sum_glitches_inverted_spice_inv"] += dev_trace_inv_results["inverted_glitches_tr0"]
		
		max_values_dict["total_sum_glitches_inv"] += dev_trace_inv_results["total_glitches_tr1"]
		max_values_dict["total_sum_glitches_orig_inv"] += dev_trace_inv_results["orig_glitches_tr1"]
		max_values_dict["total_sum_glitches_inverted_inv"] += dev_trace_inv_results["inverted_glitches_tr1"]
		
		max_values_dict["total_sum_glitches_spice_msim"] += dev_trace_msim_results["total_glitches_tr0"]
		max_values_dict["total_sum_glitches_orig_spice_msim"] += dev_trace_msim_results["orig_glitches_tr0"]
		max_values_dict["total_sum_glitches_inverted_spice_msim"] += dev_trace_msim_results["inverted_glitches_tr0"]
		
		max_values_dict["total_sum_glitches_msim"] += dev_trace_msim_results["total_glitches_tr1"]
		max_values_dict["total_sum_glitches_orig_msim"] += dev_trace_msim_results["orig_glitches_tr1"]
		max_values_dict["total_sum_glitches_inverted_msim"] += dev_trace_msim_results["inverted_glitches_tr1"]
		
		if abs(max_values_dict["max_tc_dev_abs_inv"]) < abs(tc_spice- tc_involution):
			max_values_dict["max_tc_dev_abs_inv"] = tc_spice- tc_involution	
			
		if abs(max_values_dict["max_tc_dev_abs_msim"]) < abs(tc_spice- tc_modelsim):
			max_values_dict["max_tc_dev_abs_msim"] = tc_spice- tc_modelsim		
		
		# Changed according to https://en.wikipedia.org/wiki/Relative_change_and_difference#Percent_error 
		#dev_per_inv = (tc_spice - tc_involution) / (tc_spice * 1.0)
		dev_per_inv = (tc_involution - tc_spice) / (tc_spice * 1.0)
		if abs(max_values_dict["max_tc_dev_per_inv"]) < abs(dev_per_inv):
			max_values_dict["max_tc_dev_per_inv"] = dev_per_inv
				
		#dev_per_msim = (tc_spice - tc_modelsim) / (tc_spice * 1.0)
		dev_per_msim = (tc_modelsim - tc_spice) / (tc_spice * 1.0)
		if abs(max_values_dict["max_tc_dev_per_msim"]) < abs(dev_per_msim):
			max_values_dict["max_tc_dev_per_msim"] = dev_per_msim		
			
		max_values_dict["total_tc_spice"] += tc_spice
		max_values_dict["total_tc_msim"] += tc_modelsim
		max_values_dict["total_tc_inv"] += tc_involution
		
		# we do not want to generate plots
		if(zoom_number == 0):
			continue
		
		# Fig 1: print the traces (SPICE, Involution, ModelSim)
		name = start_out_name +signal_name

		plt.figure()
		axes = list()
		axes.append(plt.subplot(3, 1, 1))
		plt.plot(trace[0], trace[1], '-r', linewidth=2)    
		plt.title('transition count: SPICE(%d), Involution(%d), Modelsim(%d)'% (tc_spice, tc_involution, tc_modelsim))
		plt.ylabel('SPICE')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()

		axes.append(plt.subplot(3, 1, 2))
		plt.plot(dataInv[0], dataInv[1], '-b', linewidth=2)
		plt.ylabel('Involution')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()

		axes.append(plt.subplot(3, 1, 3))
		plt.plot(dataModelsim[0], dataModelsim[1], '-g', linewidth=2)
		plt.xlabel('time [ns]')
		plt.ylabel('Modelsim')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()	
		
		plt.savefig(fig_folder + name + '.png')
		
		print_zoom_plots(fig_folder + name, '.png', plt, axes, x_first, x_last, zoom_number, overlapping)		
		
		
		# Fig 2: print the deviation traces SPICE vs Involution

		plt.figure()
		axes = list()
		axes.append(plt.subplot(3, 1, 1))
		plt.plot(trace[0], trace[1], '-r', linewidth=2)
		plt.title('sum(error(Involution)) = %.3f, sum(error(Modelsim)) = %.3f'%(dev_trace_inv_results["total_area_under_dev_trace"],dev_trace_msim_results["total_area_under_dev_trace"]))
		plt.ylabel('SPICE')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()

		axes.append(plt.subplot(3, 1, 2))
		plt.plot(dataInv[0], dataInv[1], '-b', linewidth=2)		
		plt.ylabel('Involution')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()

		axes.append(plt.subplot(3, 1, 3))
		plt.plot(dev_trace_inv_results['dev_trace'][0], dev_trace_inv_results['dev_trace'][1], '-r', linewidth=2)
		plt.xlabel('time [ns]')
		plt.ylabel('deviation')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()
		
		plt.savefig(fig_folder+ name + '_devInv.png')		
		
		print_zoom_plots(fig_folder + name, '_devInv.png', plt, axes, x_first, x_last, zoom_number, overlapping)	

		# Fig 3: print the deviation traces SPICE vs Modelsim

		plt.figure()
		axes = list()
		axes.append(plt.subplot(3, 1, 1))
		plt.plot(trace[0], trace[1], '-r', linewidth=2) 
		plt.title('sum(error(Involution)) = %.3f, sum(error(Modelsim)) = %.3f'%(dev_trace_inv_results["total_area_under_dev_trace"],dev_trace_msim_results["total_area_under_dev_trace"]))   
		plt.ylabel('SPICE')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()
		
		axes.append(plt.subplot(3, 1, 2))
		plt.plot(dataModelsim[0], dataModelsim[1], '-g', linewidth=2)		
		plt.ylabel('Modelsim')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()

		axes.append(plt.subplot(3, 1, 3))
		plt.plot(dev_trace_msim_results["dev_trace"][0], dev_trace_msim_results["dev_trace"][1], '-r', linewidth=2)
		plt.xlabel('time [ns]')
		plt.ylabel('deviation')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()

		plt.savefig(fig_folder+ name + '_devModelsim.png')
		
		print_zoom_plots(fig_folder + name, '_devModelsim.png', plt, axes, x_first, x_last, zoom_number, overlapping)	

		
		# Fig 4: deviation traces Involution vs Modelsim
		plt.figure()
		axes = list()
		axes.append(plt.subplot(2, 1, 1))
		plt.title('sum(error(Involution)) = %.3f, sum(error(Modelsim)) = %.3f'%(dev_trace_inv_results["total_area_under_dev_trace"],dev_trace_msim_results["total_area_under_dev_trace"])) 
		plt.plot(dev_trace_inv_results["dev_trace"][0], dev_trace_inv_results["dev_trace"][1], '-b', linewidth=2)
		plt.ylabel('Involution')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()

		axes.append(plt.subplot(2, 1, 2))
		plt.plot(dev_trace_msim_results["dev_trace"][0], dev_trace_msim_results["dev_trace"][1], '-g', linewidth=2)		
		plt.xlabel('time [ns]')
		plt.ylabel('Modelsim')
		plt.ylim([ylim_start,ylim_end])
		plt.xlim([x_first,x_last])
		plt.grid()

		plt.savefig(fig_folder+ name + '_diff.png')
		
		print_zoom_plots(fig_folder + name, '_diff.png', plt, axes, x_first, x_last, zoom_number, overlapping)	
		
	# now write the results in the tex file
	
	# read the content from the template file
	template_content = ""
	with open(tex_template_file, 'r') as infile:		
		template_content = infile.read()
		
	content = template_content.replace("%##LINES##%", content)	
		
	with open(tex_template_file, 'w') as outfile:
		outfile.write(content)
		
	max_values_dict["max_tc_dev_per_inv"] *= 100
	max_values_dict["max_tc_dev_per_msim"] *= 100
	
	max_values_dict["total_tc_deviation_per_msim"] = (max_values_dict["total_tc_msim"] - max_values_dict["total_tc_spice"]) / (max_values_dict["total_tc_spice"] * 1.0) * 100
	max_values_dict["total_tc_deviation_per_inv"] = (max_values_dict["total_tc_inv"] - max_values_dict["total_tc_spice"]) / (max_values_dict["total_tc_spice"] * 1.0) * 100
	
	extend_results(results_file, max_values_dict)
			
#********************************************************************************

def print_zoom_plots(prefix, postfix, plt, axes, x_start, x_end, zoom_number, overlapping):
	if zoom_number < 2:
		return
		
	total_length = x_end - x_start
	leading_zeros_length = 0
	#print total_length
	part_length = (total_length * 1.0 + ((zoom_number - 1) * 1.0) * (overlapping)) / (zoom_number * 1.0)
	
	it = zoom_number * 1.0
	while it < 1:
		it = it / 10
		leading_zeros_length = leading_zeros_length + 1
		
	start = x_start
		
	for part in range(0, zoom_number):
		end = start + part_length
		for axis in axes:
			axis.set_xlim([start,end])
			
		#print "From: " + str(start) + " to: " + str(end)
			
		start = start + part_length - overlapping
		
		plt.savefig(prefix + '_p' + str(part + 1).zfill(leading_zeros_length) + postfix)

#--------------------------------------------------------------------------------

def get_trace(switchingTimes, initialValue):
	data = [[],[]]
		
	value = 0
	
	if initialValue == 0:
		value = vss
	elif initialValue == 1:
		value = vdd
	else:
		my_print("Wrong initial value in crossings.json file", EscCodes.WARNING)		
	
	data[0].append(0)
	data[1].append(value)
	
	for time in switchingTimes:
	
		time *= 1e9
		
		data[0].append(time)
		data[1].append(data[1][-1])
		
		data[0].append(time)
		if value == vss:
			value = vdd
		else:
			value = vss
		
		data[1].append(value)
	
	return data

#--------------------------------------------------------------------------------

def get_deviation_trace(tr0, tr1, export_dev_trace_info, fig_folder, signal_name):

	# res contains the deviation trace
	# res[0][..] contains the times for which deviations (and therefore transitions in the deviation trace) take place
	# res[1][y] contains the value of the deviation trace at time with the index y
	res = [[],[]]

	# start at time=0, and check if there is an initial difference between the traces
	res[0].append(0)	
	res[1].append(abs(tr1[1][0]-tr0[1][0]))
	
	idx0 = 1
	idx1 = 1
	
	same_transition_tolerance = 1e-6 # overall tolerance = 1e-9 * 1e-6 = 1e-15s = 1 femto second

	while (idx0 < len(tr0[0]) and  idx1 < len(tr1[0])):			
		if abs(tr0[0][idx0] - tr1[0][idx1]) > same_transition_tolerance:
		
			if (tr0[0][idx0] < tr1[0][idx1]) :				
				res[0].append(tr0[0][idx0])
				res[1].append(abs(tr0[1][idx0] - tr1[1][idx1]))
				
				idx0 += 1
			elif (tr1[0][idx1] < tr0[0][idx0]):
				res[0].append(tr1[0][idx1])
				res[1].append(abs(tr0[1][idx0] - tr1[1][idx1]))				
				idx1 += 1				
			else:							
				my_print("Check which trace is before the other trace could not find which one is earlier\nShould never be reached,\nsignal: {0}, approx. time: {1}\n".format(signal_name, tr0[0][idx0]), EscCodes.FAIL)
				
		else: # transition on same time instant			
			dev_value = abs(tr0[1][idx0] - tr1[1][idx1])
			if dev_value != 0:
				my_print("Transition happend at the same time: {0} on signal: {1}, but the directions where different".format(tr0[0][idx0], signal_name), EscCodes.WARNING)
			
			idx1 += 1
			idx0 += 1

	if idx0 < len(tr0[0]):
		for i in range(idx0,len(tr0[0])):
			res[0].append(tr0[0][i])
			res[1].append(abs(tr1[1][-1]-tr0[1][i]))
	elif idx1 < len(tr1[0]):
		for i in range(idx1,len(tr1[0])):
			res[0].append(tr1[0][i])
			res[1].append(abs(tr0[1][-1]-tr1[1][i]))
	else:
		# we reached the end of both signals at the same "time"
		# add another point so that the the deviation trace goes until the "end" of the two compared signals
		if abs(tr0[0][idx0-1] - tr1[0][idx1-1]) <= same_transition_tolerance:
			res[0].append(tr1[0][idx1-1])
			res[1].append(abs(tr0[1][idx0-1] - tr1[1][idx1-1]))
			
	# Now take care of the glitch detection
	# 'suppressed' glitches, glitches on the reference signal (tr0), nothing on the actual signal (tr1)	
	total_glitches_tr0 = 0
	orig_glitches_tr0 = 0 # both signals have the same value, two subsequent transitions on tr1, both signals again have the same value
	inverted_glitches_tr0 = 0 # same as abobe but with inverted reference signal
	# 'induced' glitches, vice versa
	total_glitches_tr1 = 0
	orig_glitches_tr1 = 0
	inverted_glitches_tr1 = 0
	
	csv_data = list()	
	header = list()	
	header.append("from")
	header.append("till")
	header.append("dev. value")
	# including the transition which causes the current change of the deviation trace
	header.append("tr0 time last trans. before dev.") 
	header.append("tr1 time last trans. before dev.")
	# We have two points for each transition, one with the old value, and one with the new value, and here we use the OLD value
	header.append("tr0 value last trans. before dev.") 
	header.append("tr1 value last trans. before dev.")	
	# including the transition which causes the current change of the deviation trace
	header.append("tr0 time first trans. after dev.")
	header.append("tr1 time first trans. after dev.")	
	# We have two points for each transition, one with the old value, and one with the new value, and here we use the NEW value
	header.append("tr0 value first trans. after dev.")
	header.append("tr1 value first trans. after dev.")
	
	header.append("deviation start reason")
	header.append("deviation end reason")
	
	header.append("glitches on tr0")
	header.append("orig. glitch on tr0")
	header.append("inv. glitch on tr0")
	header.append("glitches on tr1")
	header.append("orig. glitch on tr1")
	header.append("inv. glitch on tr1")
	
	header.append("area")
	header.append("pos. area")
	header.append("neg. area")
	
	header.append("pos_area_under_dev_trace_wo_glitches")
	header.append("neg_area_under_dev_trace_wo_glitches")
	
	# now iterate over the header, and add the name of the column as the keys, and as value an index:	
	csv_index_dict = dict()
	for idx, caption in enumerate(header):
		csv_index_dict[caption] = idx
		
	
	csv_data.append(header)
	step = -1
	idx0 = 0
	idx1 = 0
			
	total_area_under_dev_trace = 0
	pos_area_under_dev_trace = 0
	neg_area_under_dev_trace = 0
	pos_area_under_dev_trace_wo_glitches = 0
	neg_area_under_dev_trace_wo_glitches = 0
	
	pos_area_under_dev_trace_transitions = 0
	neg_area_under_dev_trace_transitions = 0
	pos_area_under_dev_trace_transitions_wo_glitches = 0
	neg_area_under_dev_trace_transitions_wo_glitches = 0
	
	# we analyze the whole deviation trace
	for dev_idx in range(0, len(res[0])-1):
		step = (step + 1) % 2
		if dev_idx == 0 and res[1][0] == vth:
			# we ignore the first transition from X to 0 or 1, 
			# because only ModelSim does this, 
			# and not Involution or SPICE (they use both an initial value of 0 or 1)
			continue
	
		# only take each second value (necessary because for each transition there are two values at the same time instant (required for plotting)
		# for example 
		# t     | dev. value
		# 0.00  | 0 *
		# 1.15  | 0
		# 1.15  | 1 *
		# 1.20  | 1
		# 1.20  | 0 *
		# 1.30  | 0
		# 1.30  | 1 *
		# we only take "rows" indicated with *
		# and generate something like
		# from | till | dev. value
		# 0    | 1.15 | 0
		# 1.15 | 1.20 | 1
		# 1.20 | 1.30 | 0		
		if step != 0:
			continue
			
		row = [None] * len(header)
		row[csv_index_dict['from']] = res[0][dev_idx]
		row[csv_index_dict['till']] = res[0][dev_idx+1]
		row[csv_index_dict['dev. value']] = res[1][dev_idx]
		
			
		# now we iterate in both traces to the index BEFORE the deviation
		while idx0 < len(tr0[0])-2 and tr0[0][idx0+1] <= res[0][dev_idx]:
			idx0 += 1			
						
		while idx1 < len(tr1[0])-2 and tr1[0][idx1+1] <= res[0][dev_idx]:
			idx1 += 1			

		# now we iterate in both traces to the index AFTER the deviation
		after_idx0 = idx0
		while after_idx0 < len(tr0[0])-2 and tr0[0][after_idx0] < res[0][dev_idx+1]:
			after_idx0 += 1
			
		after_idx1 = idx1
		while after_idx1 < len(tr1[0])-2 and tr1[0][after_idx1] < res[0][dev_idx+1]:
			after_idx1 += 1			
					
		deviation_start_reason = -1
		deviation_end_reason = -1
		
		if tr0[0][idx0] == res[0][dev_idx] and tr1[0][idx1] != res[0][dev_idx]:
			deviation_start_reason = 0 #change on tr0 is the reason for the deviation start
			idx0 -= 1
		elif tr0[0][idx0] != res[0][dev_idx] and tr1[0][idx1] == res[0][dev_idx]: 
			deviation_start_reason = 1 #change on tr1 is the reason for the deviation start
			idx1 -= 1
			
		if tr0[0][after_idx0] == res[0][dev_idx+1] and tr1[0][after_idx1] != res[0][dev_idx+1]:
			deviation_end_reason = 0 #change on tr0 is the reason for the deviation end
			after_idx0 += 1
		elif tr0[0][after_idx0] != res[0][dev_idx+1] and tr1[0][after_idx1] == res[0][dev_idx+1]: 
			deviation_end_reason = 1 #change on tr1 is the reason for the deviation end
			after_idx1 += 1		
		
			
		row[csv_index_dict['tr0 time last trans. before dev.']] = tr0[0][idx0]
		row[csv_index_dict['tr1 time last trans. before dev.']] = tr1[0][idx1] 	
		row[csv_index_dict['tr0 value last trans. before dev.']] = tr0[1][idx0]
		row[csv_index_dict['tr1 value last trans. before dev.']] = tr1[1][idx1] 
		row[csv_index_dict['tr0 time first trans. after dev.']] = tr0[0][after_idx0]
		row[csv_index_dict['tr1 time first trans. after dev.']] = tr1[0][after_idx1]
		row[csv_index_dict['tr0 value first trans. after dev.']] = tr0[1][after_idx0]
		row[csv_index_dict['tr1 value first trans. after dev.']] = tr1[1][after_idx1]
		
		row[csv_index_dict['deviation start reason']] = deviation_start_reason
		row[csv_index_dict['deviation end reason']] = deviation_end_reason
				
		# now we have all the data which is required to decide with type of deviation this is
		# > no glitch
		# > glitch on tr0 / glitch on tr1
		# > original glitch / inverted glitch
		if deviation_start_reason != -1 and deviation_end_reason != -1 and deviation_start_reason == deviation_end_reason:
			# we have a glitch (deviation is started and ended by the same trace)
			glitch_on_tr0 = deviation_start_reason == 0
			glitch_on_tr1 = deviation_start_reason == 1
						
			# now check the type of glitch
			# if start values differ (and also the end values, but this is just a double check)
			start_values_differ = tr0[1][idx0] != tr1[1][idx1]
			end_values_differ = tr0[1][after_idx0] != tr1[1][after_idx1]
			
			inverted_glitch = False
			orig_glitch = False
			if start_values_differ and end_values_differ:
				inverted_glitch = True
			elif not start_values_differ and not end_values_differ:
				orig_glitch = True
			else:				
				my_print("neither original glitch nor inverted glitch --> should never be reached,\nsignal: {0}, approx. time: {1}\nPossible issue: Starting values differ between tr0 and tr1\n".format(signal_name, tr0[0][idx0]), EscCodes.FAIL)
				
			if glitch_on_tr0:
				total_glitches_tr0 += 1
				if orig_glitch:
					orig_glitches_tr0 += 1
				if inverted_glitch:
					inverted_glitches_tr0 += 1
				row[csv_index_dict['glitches on tr0']] = glitch_on_tr0
				row[csv_index_dict['orig. glitch on tr0']] = orig_glitch
				row[csv_index_dict['inv. glitch on tr0']] = inverted_glitch
			
			if glitch_on_tr1:
				total_glitches_tr1 += 1
				if orig_glitch:
					orig_glitches_tr1 += 1
				if inverted_glitch:
					inverted_glitches_tr1 += 1					
				row[csv_index_dict['glitches on tr1']] = glitch_on_tr1
				row[csv_index_dict['orig. glitch on tr1']] = orig_glitch
				row[csv_index_dict['inv. glitch on tr1']] = inverted_glitch
				
		# now we calculate the area under the deviation (total and also signed)
		if row[csv_index_dict['dev. value']] != 0:
			# if deviation value != 0
			area = row[csv_index_dict['dev. value']] * (row[csv_index_dict['till']] - row[csv_index_dict['from']])
			
			row[csv_index_dict['area']] = area
			orig_glitch = row[csv_index_dict['orig. glitch on tr0']] or row[csv_index_dict['orig. glitch on tr1']]
			if deviation_start_reason == 0:
				# tr0 early (* (-1))
				neg_area_under_dev_trace += area * -1
				row[csv_index_dict['neg. area']] = area * -1
				neg_area_under_dev_trace_transitions += 1
				if not orig_glitch:
					neg_area_under_dev_trace_wo_glitches += area * -1
					row[csv_index_dict['neg_area_under_dev_trace_wo_glitches']] = area * -1
					neg_area_under_dev_trace_transitions_wo_glitches += 1
			elif deviation_start_reason == 1:
				# tr1 early (* (+1))
				pos_area_under_dev_trace += area
				row[csv_index_dict['pos. area']] = area
				pos_area_under_dev_trace_transitions += 1
				if not orig_glitch:
					pos_area_under_dev_trace_wo_glitches += area
					row[csv_index_dict['pos_area_under_dev_trace_wo_glitches']] = area
					pos_area_under_dev_trace_transitions_wo_glitches +=1
				
			
			# TODO: We should ignore the deviation between MSIM and SPICE, 
			# since the MSIM outputs are set to X (= VTH) and not to an 
			# initial value like INV / SPICE
			
			total_area_under_dev_trace += area
						
		csv_data.append(row)

		
	if export_dev_trace_info:
		with open(os.path.join(fig_folder, signal_name.replace("/", "_") + '.csv'), 'wb') as f:	
			writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_ALL)
			writer.writerows(csv_data)
	
	result_dictionary = dict()
	result_dictionary["dev_trace"] = res
	result_dictionary["total_area_under_dev_trace"] = total_area_under_dev_trace
	result_dictionary["pos_area_under_dev_trace"] = pos_area_under_dev_trace
	result_dictionary["neg_area_under_dev_trace"] = neg_area_under_dev_trace	
	
	result_dictionary["pos_area_under_dev_trace_wo_glitches"] = pos_area_under_dev_trace_wo_glitches
	result_dictionary["neg_area_under_dev_trace_wo_glitches"] = neg_area_under_dev_trace_wo_glitches
	result_dictionary["pos_area_under_dev_trace_transitions"] = pos_area_under_dev_trace_transitions
	result_dictionary["neg_area_under_dev_trace_transitions"] = neg_area_under_dev_trace_transitions
	result_dictionary["pos_area_under_dev_trace_transitions_wo_glitches"] = pos_area_under_dev_trace_transitions_wo_glitches
	result_dictionary["neg_area_under_dev_trace_transitions_wo_glitches"] = neg_area_under_dev_trace_transitions_wo_glitches	
	
	result_dictionary["total_glitches_tr0"] = total_glitches_tr0
	result_dictionary["orig_glitches_tr0"] = orig_glitches_tr0
	result_dictionary["inverted_glitches_tr0"] = inverted_glitches_tr0
	result_dictionary["total_glitches_tr1"] = total_glitches_tr1
	result_dictionary["orig_glitches_tr1"] = orig_glitches_tr1
	result_dictionary["inverted_glitches_tr1"] = inverted_glitches_tr1
	
	
	return result_dictionary
	
if __name__ == "__main__":
    main()

