"""
    
	Involution Tool
	File: generate_plots.py
	
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

import matplotlib.pyplot as plt
import pandas as pd 
import sys
import os
from argparse import ArgumentParser
from itertools import cycle
from matplotlib.pyplot import figure
import math

def main():
	# gcd(lines, marker) should be large, so that we get the most possible different combinations
	lines = ["-","--","-.",":"]
	marker = [".","*","x","+","s"]
	show_reference = True
	# Contains the name of the involution_column, modelsim_column, label
	column_names = [\
		('avgperspicecolumnINVOLUTIONPT_TIM', 'avgperspicecolumnMODELSIMPT_TIM', 'power dev.\n[%]'),\
		('max_tc_dev_per_inv', 'max_tc_dev_per_msim', 'max.\ntrans. count\ndev. [%]'),\
		('total_tc_deviation_per_inv', 'total_tc_deviation_per_msim', 'avg.\ntrans. count\ndev. [%]'),\
		('total_sum_error_inv', 'total_sum_error_msim', 'area under\ndev. trace'),\
		('total_pos_area_under_dev_trace_inv', 'total_pos_area_under_dev_trace_msim', 'pos. area under\ndev. trace'),\
		('total_neg_area_under_dev_trace_inv', 'total_neg_area_under_dev_trace_msim', 'neg. area under\ndev. trace'),\
		('total_sum_glitches_inv', 'total_sum_glitches_msim', 'induced\nglitches'),\
		('total_sum_glitches_orig_inv', 'total_sum_glitches_orig_msim', 'original\ninduced\nglitches'),\
		('total_sum_glitches_inverted_inv', 'total_sum_glitches_inverted_msim', 'inverted\ninduced\nglitches'),\
		('total_sum_glitches_spice_inv','total_sum_glitches_spice_msim', 'suppressed\nglitches'),\
		('total_sum_glitches_orig_spice_inv','total_sum_glitches_orig_spice_msim', 'original\nsuppressed\nglitches'),\
		('total_sum_glitches_inverted_spice_inv','total_sum_glitches_inverted_spice_msim', 'inverted\suppressed\nglitches'),\
		('total_pos_area_under_dev_trace_inv_per_spice_transition','total_pos_area_under_dev_trace_msim_per_spice_transition', 'leading\nagainst\nspice per\ntransition [ps]'),\
		('total_neg_area_under_dev_trace_inv_per_spice_transition','total_neg_area_under_dev_trace_msim_per_spice_transition', 'trailing\nagainst\nspice per\ntransition [ps]'),\
		
		
		('total_pos_area_under_dev_trace_inv_per_actual_transition','total_pos_area_under_dev_trace_msim_per_actual_transition', 'leading\nagainst\nactual\ntransition [ps]'),\
		('total_neg_area_under_dev_trace_inv_per_actual_transition','total_neg_area_under_dev_trace_msim_per_actual_transition', 'trailing\nagainst\nactual\ntransition [ps]'),\
		
		
		('total_pos_area_under_dev_trace_inv_per_actual_transition_wo_glitches','total_pos_area_under_dev_trace_msim_per_actual_transition_wo_glitches', 'leading\nagainst\nactual \ntransition\nw.o glitches\n[ps]'),\
		('total_neg_area_under_dev_trace_inv_per_actual_transition_wo_glitches','total_neg_area_under_dev_trace_msim_per_actual_transition_wo_glitches', 'trailing\nagainst\nactual \ntransition\nw.o glitches\n[ps]'),\
		
		('total_sum_glitches_inv_per_transition','total_sum_glitches_msim_per_transition', 'induced\nglitch\npercentage\n[%]'),\
		('total_sum_glitches_orig_inv_per_transition','total_sum_glitches_orig_msim_per_transition', 'induced\norig. glitch\npercentage\n[%]'),\
		('total_sum_glitches_inverted_inv_per_transition','total_sum_glitches_inverterd_msim_per_transition', 'induced\ninverted. glitch\npercentage\n[%]'),\
		
		
		('total_sum_glitches_spice_inv_per_transition','total_sum_glitches_spice_msim_per_transition', 'suppressed\nglitch\npercentage\n[%]'),\
		('total_sum_glitches_orig_spice_inv_per_transition','total_sum_glitches_orig_spice_msim_per_transition', 'suppressed\norig. glitch\npercentage\n[%]'),\
		('total_sum_glitches_inverted_spice_inv_per_transition','total_sum_glitches_inverterd_spice_msim_per_transition', 'suppressed\ninverted. glitch\npercentage\n[%]')]
		
	parser = ArgumentParser()
	parser.add_argument("-f", "--file", metavar='filename')
	parser.add_argument("-d", "--description", metavar='description')
	parser.add_argument("-p", "--path", metavar='path')
	parser.add_argument("-g", "--group_filter", metavar='list', nargs='+', type=int)
	parser.add_argument("-r", "--ref_group_filter", metavar='list', nargs='+', type=int)
	parser.add_argument("-m", "--metrics", metavar='metric_list', nargs='+', type=int)
	
	args = parser.parse_args()
			
	if args.metrics is not None:
		column_names = [column_names[i] for i in list(args.metrics)]	
		
	data = None
	if args.path is not None:
		data = pd.read_csv(os.path.join(args.path, 'evaluation.csv'), sep=';')
	elif args.file is not None:
		data = pd.read_csv(args.file, sep=';')
	else:
		raise Exception("No path to the evaluation file supplied!")
	
	# check if all the columns exists in the evaluation file (compatibility reasons, some metrics have been added later)
	# if we can't find the column --> remove it from the list
	column_names = [column_names[i] for i, (inv_col, msim_col, _) in enumerate(column_names) if set([inv_col, msim_col]).issubset(data.columns)]
	
	nr_subplots = len(column_names)
	
	fig, axes = plt.subplots(nr_subplots, 1, sharex='col')
	
	# Hack for indexing when only one plot...
	if nr_subplots == 1:
		axes = [axes]
	
	subplot_index = 0
	
	for (act_col, ref_col, label) in column_names:
		# Find out all unique reference_group values and plot them		
		reference_groups = data.reference_group.unique() 
		
		# reset cycler before new plot
		linecycler = cycle(lines)
		markercycler = cycle(marker)
		
		for ref_group_id in reference_groups:
			if args.ref_group_filter is not None and ref_group_id not in args.ref_group_filter:
				continue
		
			ref_group_data = data.loc[data['reference_group'] == ref_group_id]	
			label_string = '{0}, {1}, {2}, \n$\mu={3:.1f}ps$, $\sigma={4:.1f}ps${5}'
			local_groups = ref_group_data.group.unique()			
			if args.group_filter is not None and len(list(set(args.group_filter) & set(local_groups))) == 0:
				# no groups to show, therefore also do not show the reference
				continue
				
			if show_reference:
				temp_label_string = label_string.format('standard ModelSim', '-', ref_group_data['trans_mode'].iloc[0], ref_group_data['mu'].iloc[0] * 1000, ref_group_data['sigma'].iloc[0] * 1000, '')
			
				#label_string = 'reference, ' + str(ref_group_data['trans_mode'].iloc[0]) + ", mu="+ str(ref_group_data['mu'].iloc[0]) + ", sigma=" + str(ref_group_data['sigma'].iloc[0])
				axes[subplot_index].plot(ref_group_data['T_P'], ref_group_data[ref_col], label=temp_label_string, linestyle=next(linecycler), marker=next(markercycler)) 
				
			# find all groups for this reference:
			for group_id in local_groups:			
				if args.group_filter is not None and group_id not in args.group_filter:
					continue
				group_data = data.loc[data['group'] == group_id]
				additional_params_string = ""	
				if group_data['n_up'].iloc[0] is not None and not math.isnan(group_data['n_up'].iloc[0]):
					additional_params_string+="$n_\\uparrow={0:.1f}$".format(group_data['n_up'].iloc[0])
				if group_data['n_do'].iloc[0] is not None and not math.isnan(group_data['n_do'].iloc[0]):
					additional_params_string+=", $n_\\downarrow={0:.1f}$".format(group_data['n_do'].iloc[0])
				if additional_params_string != "":
					additional_params_string = ",\n" + additional_params_string
				temp_label_string = label_string.format(group_data['name'].iloc[0], group_data['channel_location'].iloc[0], group_data['trans_mode'].iloc[0], group_data['mu'].iloc[0] * 1000, group_data['sigma'].iloc[0] * 1000, additional_params_string)
				handle = axes[subplot_index].plot(group_data['T_P'], group_data[act_col], label=temp_label_string, linestyle=next(linecycler), marker=next(markercycler)) 	
		axes[subplot_index].set_ylabel(label)
		subplot_index += 1
	
	axes[-1].set_xlabel(r"$T_P [ps]$")
	handles, labels = axes[-1].get_legend_handles_labels()
	
	# number_of_columns = len(data.reference_group.unique())
	# if args.ref_group_filter is not None:
		# number_of_columns = len(args.ref_group_filter)
		
		
	filepath = None
	if args.path is not None:
		filepath = os.path.join(args.path, 'README.txt')
	elif args.description is not None:
		filepath = args.description
		
	if filepath is not None and os.path.isfile(filepath):
		with open(filepath, 'r') as content_file:
			content = content_file.read()
			fig.suptitle(content, fontsize=14)
		plt.subplots_adjust(bottom=0.2, top=0.85)
	else:
		# we can use the space at the top
		plt.subplots_adjust(bottom=0.2, top=0.95)
		
	number_of_columns = 3
	fig.legend(handles, labels, loc='lower center', ncol=number_of_columns)
	
	plt.show()
	
if __name__ == "__main__":
    main()