"""
    
	Involution Tool
	File: prepareWaveformComparison.py
	
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
import csv
sys.path.append('../../experiment_setup/python')
from helper import *
from parserHelper import *
from multiExecHelper import *

def main():
	if len(sys.argv) != 3:
		my_print("usage: prepareWaveformComparison.py tempate_file line_template", EscCodes.FAIL)
		sys.exit(1)
		
	prepareWaveformComparison(sys.argv[1], sys.argv[2])
	
def prepareWaveformComparison(tempate_file, line_template):
	# read the content from the template file
	template_content = ""
	with open(tempate_file, 'r') as infile:		
		template_content = infile.read()
	
	
	report_folder = os.path.join(os.environ["RESULT_OUTPUT_DIR"], os.environ["ME_REPORT_FOLDER"])	
	multi_report_folder = os.path.join(report_folder, 'multi_report')
	line_content = ""
		
	dict = load_swapped_folder_mapping()
		
	# sort the folders in ascending order (file number in report)
	for key in sorted(dict.keys()):		
		name = dict[key]
		value_dict = read_results(os.path.join(report_folder, name, 'results.json'))
		# not present in older versions of reporting, therefore we use a fallback value
		glitches_spice_inv = "-"
		if "total_sum_glitches_spice_inv" in value_dict:
			glitches_spice_inv = value_dict["total_sum_glitches_spice_inv"]
		glitches_inv = "-"
		if "total_sum_glitches_inv" in value_dict:
			glitches_inv = value_dict["total_sum_glitches_inv"]
		glitches_spice_msim = "-"
		if "total_sum_glitches_spice_msim" in value_dict:
			glitches_spice_msim = value_dict["total_sum_glitches_spice_msim"]
		glitches_msim = "-"	
		if "total_sum_glitches_msim" in value_dict:
			glitches_msim = value_dict["total_sum_glitches_msim"]
		
		line_content += line_template.replace("%##NAME##%", "\\ref{file:" + remove_special_chars(name) + "}").replace("%##MSIM_ABS##%", str(value_dict["max_tc_dev_abs_msim"])).replace("%##MSIM_REL##%", str(value_dict["max_tc_dev_per_msim"])).replace("%##MSIM_SUM##%", str(value_dict["total_sum_error_msim"])).replace("%##INV_ABS##%", str(value_dict["max_tc_dev_abs_inv"])).replace("%##INV_REL##%", str(value_dict["max_tc_dev_per_inv"])).replace("%##INV_SUM##%", str(value_dict["total_sum_error_inv"])).replace("%##GLITCHES_SPICE_INV##%", str(glitches_spice_inv)).replace("%##GLITCHES_INV##%", str(glitches_inv)).replace("%##GLITCHES_SPICE_MSIM##%", str(glitches_spice_msim)).replace("%##GLITCHES_MSIM##%", str(glitches_msim)) + "\n"
				

	content = template_content.replace("%##LINES##%", line_content)	
	
	with open(os.path.join(multi_report_folder, 'waveform_comparison.tex'), 'w') as outfile:
		outfile.write(content)

if __name__ == "__main__":
	main()