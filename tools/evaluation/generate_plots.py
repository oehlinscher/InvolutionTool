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
		('total_sum_glitches_inverted_spice_inv','total_sum_glitches_inverted_spice_msim', 'inverted\nsuppressed\nglitches'),\
		('total_pos_area_under_dev_trace_inv_per_spice_transition','total_pos_area_under_dev_trace_msim_per_spice_transition', 'leading\nagainst\nspice per\ntransition [ps]'),\
		('total_neg_area_under_dev_trace_inv_per_spice_transition','total_neg_area_under_dev_trace_msim_per_spice_transition', 'trailing\nagainst\nspice per\ntransition [ps]'),\
		
		
		('total_pos_area_under_dev_trace_inv_per_actual_transition','total_pos_area_under_dev_trace_msim_per_actual_transition', 'leading\nagainst\nactual\ntransition [ps]'),\
		('total_neg_area_under_dev_trace_inv_per_actual_transition','total_neg_area_under_dev_trace_msim_per_actual_transition', 'trailing\nagainst\nactual\ntransition [ps]'),\
		
		
		('total_pos_area_under_dev_trace_inv_per_actual_transition_wo_glitches','total_pos_area_under_dev_trace_msim_per_actual_transition_wo_glitches', 'leading\nagainst\nactual \ntransition\nw.o glitches\n[ps]'),\
		('total_neg_area_under_dev_trace_inv_per_actual_transition_wo_glitches','total_neg_area_under_dev_trace_msim_per_actual_transition_wo_glitches', 'trailing\nagainst\nactual \ntransition\nw.o glitches\n[ps]'),\
		
		('total_sum_glitches_inv_per_transition','total_sum_glitches_msim_per_transition', 'induced\nglitch\npercentage\n[%]'),\
		('total_sum_glitches_orig_inv_per_transition','total_sum_glitches_orig_msim_per_transition', 'induced\norig. glitch\npercentage\n[%]'),\
		('total_sum_glitches_inverted_inv_per_transition','total_sum_glitches_inverted_msim_per_transition', 'induced\ninverted. glitch\npercentage\n[%]'),\
		
		
		('total_sum_glitches_spice_inv_per_transition','total_sum_glitches_spice_msim_per_transition', 'suppressed\nglitch\npercentage\n[%]'),\
		('total_sum_glitches_orig_spice_inv_per_transition','total_sum_glitches_orig_spice_msim_per_transition', 'suppressed\norig. glitch\npercentage\n[%]'),\
		('total_sum_glitches_inverted_spice_inv_per_transition','total_sum_glitches_inverted_spice_msim_per_transition', 'suppressed\ninverted. glitch\npercentage\n[%]'),
				
		('total_pos_area_under_dev_trace_inv_first', 'total_pos_area_under_dev_trace_msim_first', 'first\npos. area under\ndev. trace'),\
		('total_neg_area_under_dev_trace_inv_first', 'total_neg_area_under_dev_trace_msim_first', 'first\nneg. area under\ndev. trace'),\
				
		('total_pos_area_under_dev_trace_inv_wo_glitches', 'total_pos_area_under_dev_trace_msim_wo_glitches', 'pos. area under\ndev. trace\nw.o glitches'),\
		('total_neg_area_under_dev_trace_inv_wo_glitches', 'total_neg_area_under_dev_trace_msim_wo_glitches', 'neg. area under\ndev. trace\nw.o glitches'),\
		
		('total_pos_area_under_dev_trace_inv_transitions_wo_glitches', 'total_pos_area_under_dev_trace_msim_transitions_wo_glitches', 'pos. transitions\ndev. trace\nw.o glitches'),\
		('total_neg_area_under_dev_trace_inv_transitions_wo_glitches', 'total_neg_area_under_dev_trace_msim_transitions_wo_glitches', 'neg. transitions\ndev. trace\nw.o glitches'),\
		
		('total_pos_area_under_dev_trace_inv_per_actual_transition_wo_glitches_first','total_pos_area_under_dev_trace_msim_per_actual_transition_wo_glitches_first', 'first\nleading\nagainst\nactual \ntransition\nw.o glitches\n[ps]'),\
		('total_neg_area_under_dev_trace_inv_per_actual_transition_wo_glitches_first','total_neg_area_under_dev_trace_msim_per_actual_transition_wo_glitches_first', 'first\ntrailing\nagainst\nactual \ntransition\nw.o glitches\n[ps]')]
		
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
	
	fig, axes = plt.subplots(nr_subplots, 1, sharex='col', figsize=(20, 15))
	
	# Hack for indexing when only one plot...
	if nr_subplots == 1:
		axes = [axes]
	
	subplot_index = 0

	# Handle compability with old / new column names:		
	reference_group_col = get_column_name(data, ['reference_group', 'ENVME_reference_group'])
	group_col = get_column_name(data, ['group', 'ENVME_group'])
	n_col = "CWGn"
	mue_col = get_column_name(data, ['mu', 'CWGmue'])
	sigma_col = get_column_name(data, ['sigma', 'CWGsigma'])
	trans_mode_col = get_column_name(data, ['trans_mode', 'CWGcalcnexttransitionmodename'])
	tp_col = get_column_name(data, ['T_P', 'GATEST_P'])
	gate_channel_type_col = get_column_name(data, ['name', 'GATESchannel_type'])
	channel_location_col = get_column_name(data, ['channel_location', 'GATESchannel_location'])
	n_up_col = get_column_name(data, ['n_up', 'GATESn_up'])
	n_do_col = get_column_name(data, ['n_do', 'GATESn_do'])
	x1_up_col = get_column_name(data, ['x_1', 'GATESx_1_up'])
	x1_do_col = get_column_name(data, ['x_1', 'GATESx_1_do'])
	tau1_up_col = get_column_name(data, ['tau_1', 'GATEStau_1_up'])
	tau1_do_col = get_column_name(data, ['tau_1', 'GATEStau_1_do'])
	tau2_up_col = get_column_name(data, ['tau_2', 'GATEStau_2_up'])
	tau2_do_col = get_column_name(data, ['tau_2', 'GATEStau_2_do'])
	vth_col = "v_th"


	
	for (act_col, ref_col, label) in column_names:
		# Find out all unique reference_group values and plot them	 
			
		reference_groups = data[reference_group_col].unique() 
		
		# reset cycler before new plot
		#colorcycler = cycle(['blue', 'green', 'orange', 'red', 'magenta'])
		colorcycler = cycle(['dodgerblue', 'limegreen', 'orange', 'red', 'darkorchid'])
		linecycler = cycle(lines)
		markercycler = cycle(marker)
		
		for ref_group_id in reference_groups:
			if args.ref_group_filter is not None and ref_group_id not in args.ref_group_filter:
				continue
		
			ref_group_data = data.loc[data[reference_group_col] == ref_group_id]	
			label_string = '{0}, {1}, {2}, \n$\mu={3:.1f}ps$, $\sigma={4:.1f}ps${5}{6}'
			local_groups = ref_group_data[group_col].unique()	

			if args.group_filter is not None and len(list(set(args.group_filter) & set(local_groups))) == 0:
				# no groups to show, therefore also do not show the reference
				continue
				
			general_additional_parameter_string = ""
			if vth_col in ref_group_data and ref_group_data[vth_col].iloc[0] is not None and not math.isnan(ref_group_data[vth_col].iloc[0]):
				v_th = "{0:.4f}".format(ref_group_data[vth_col].iloc[0])
				general_additional_parameter_string += "$V_{th}=" + v_th + "$"
				
			if show_reference:			
				temp_label_string = label_string.format('Verilog Inertial', '-', ref_group_data[trans_mode_col].iloc[0], ref_group_data[mue_col].iloc[0] * 1000, ref_group_data[sigma_col].iloc[0] * 1000, general_additional_parameter_string,'')
				#label_string = 'reference, ' + str(ref_group_data['trans_mode'].iloc[0]) + ", mu="+ str(ref_group_data['mu'].iloc[0]) + ", sigma=" + str(ref_group_data['sigma'].iloc[0])
				axes[subplot_index].plot(ref_group_data[tp_col], ref_group_data[ref_col], label=temp_label_string, color=next(colorcycler), linestyle=next(linecycler), marker=next(markercycler)) 
				
			# find all groups for this reference:
			for group_id in local_groups:			
				if args.group_filter is not None and group_id not in args.group_filter:
					continue
				group_data = data.loc[data[group_col] == group_id]
				additional_params_string_list = list()

				n_up_string = build_param_string(n_up_col, group_data, "{0:.1f}")
				n_do_string = build_param_string(n_do_col, group_data, "{0:.1f}")
				x1_up_string = build_param_string(x1_up_col, group_data, "{0:.3f}")
				x1_do_string = build_param_string(x1_do_col, group_data, "{0:.3f}")
				tau1_up_string = build_param_string(tau1_up_col, group_data, "{0:.0f} fs", "{0}")
				tau1_do_string = build_param_string(tau1_do_col, group_data, "{0:.0f} fs", "{0}")
				tau2_up_string = build_param_string(tau2_up_col, group_data, "{0:.0f} fs", "{0}")
				tau2_do_string = build_param_string(tau2_do_col, group_data, "{0:.0f} fs", "{0}")

				add_up_down_string(additional_params_string_list, "n", n_up_string, n_do_string)
				add_up_down_string(additional_params_string_list, "x_1", x1_up_string, x1_do_string)
				add_up_down_string(additional_params_string_list, "\\tau_1", tau1_up_string, tau1_do_string)
				add_up_down_string(additional_params_string_list, "\\tau_2", tau2_up_string, tau2_do_string)			
									
				additional_params_string = ""	
				if len(additional_params_string_list) > 0:
					additional_params_string += ",\n"
				for str in additional_params_string_list:					
					additional_params_string += str + ", "
				additional_params_string = additional_params_string.rstrip(", ")

				channel_type_string = build_param_string(gate_channel_type_col, group_data, "{0}")
				channel_location_string = build_param_string(channel_location_col, group_data, "{0}")

				temp_label_string = label_string.format(channel_type_string, channel_location_string, group_data[trans_mode_col].iloc[0], 
					group_data[mue_col].iloc[0] * 1000, group_data[sigma_col].iloc[0] * 1000, general_additional_parameter_string, additional_params_string)
				handle = axes[subplot_index].plot(group_data[tp_col], group_data[act_col], label=temp_label_string, color=next(colorcycler), linestyle=next(linecycler), marker=next(markercycler)) 	
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
	# plt.savefig("plot2.png")
	# plt.savefig("plot.png", dpi=1000)

def add_up_down_string(params_list, var, up, down):
	if not up and not down:
		return # nothing to do

	if up == down:		
		params_list.append("${0}={1}$".format(var, up))
	else:
		params_list.append("${0}_\\uparrow={1}$".format(var, up))		
		params_list.append("${0}_\\downarrow={1}$".format(var, down))	
	
def build_param_string(column, group_data, format1, format2=None):
	if column in group_data and group_data[column].iloc[0] is not None and group_data[column].iloc[0]:
		val = group_data[column].iloc[0]
		values = []
		try:
			values = val.split(',')
		except:
			values = [val]

		nrValues = len(set(values))
		if nrValues == 1:	
			singleVal = values[0]

			try:
				if math.isnan(singleVal):
					return None
			except:
				pass

			if not singleVal:
				return None
			else:	
				return try_to_format(values[0], format1, format2)
		elif nrValues >= 1:
			strlist = ""
			for val in values:
				strlist.append(try_to_format(val, format1, format2))
			return ','.join(strlist)

	return None

def try_to_format(val, format1, format2):
	try:
		return format1.format(float(val))	
	except:
		try:
			return format1.format(val)
		except:
			try:
				return format2.format(float(val))
			except:
				return format2.format(val)



def get_column_name(data, column_names):
	for column_name in column_names:
		if column_name in data:
			return column_name
	
	return None
	
if __name__ == "__main__":
    main()