"""
    
	Involution Tool
	File: multiReportVars.py
	
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
sys.path.append('../../experiment_setup/python')
from helper import *
from parserHelper import *
from multiExecHelper import *

def main():

	if len(sys.argv) != 1:
		my_print("usage: multiReportVars.py", EscCodes.FAIL)
		sys.exit(1)
		
	multi_report_vars()
	
def multi_report_vars():
	
	# contains the relative path from $RESULT_OUTPUT_DIR, can be set
	# a. by executing the make all command
	# b. passing the relative path via make report ME_REPORT_FOLDER="folder_name"
	report_folder = os.path.join(os.environ["RESULT_OUTPUT_DIR"], os.environ["ME_REPORT_FOLDER"])
	
	# read the copy properties from cfg File
	copy_properties = parse_csv_string(os.environ["ME_COPY_PROPERTIES"])
	copy_folder = None
	
	for name in single_report_folders():
		copy_folder = os.path.join(report_folder, name)
		break
			
	if copy_folder is None:
		my_print("No sub_folders found in the $ME_REPORT_FOLDER")
		return
	
	source_dict = read_results(os.path.join(copy_folder, 'results.json'))
	multi_report_dict = dict()
	
	# now iterate over the properties we want to copy 1:1
	for copy_property in copy_properties:
		# check if we find the property in the list of keys (regex can be used)
		regex = re.compile(copy_property, re.IGNORECASE)
		found = False
		for key in apply_regex_to_list(source_dict.keys(), copy_property):		
			found = True
			multi_report_dict[key] = source_dict[key]
			#break # no break, because regeex could match for multiple properties in the source_dict
		
		if not found:
			my_print("[COPY_PROPERTY] Could not find a match for the following regex: " + copy_property, EscCodes.WARNING)
			
	# Create a dictionary with MIN_value / MIN_ref / MAX_value / MAX_ref / AVG_value of 
	calc_properties = parse_csv_string(os.environ["ME_CALC_PROPERTIES"])
	# iterate over all calc_properties
	for calc_property in calc_properties:
		# iterate over the copy "source_dict" (assume that all folders contain the same keys)
		# if not --> do error handling during iteration over result folder)
		# needed to change the two loops, so that regex are working
		found = False
		
		for key in apply_regex_to_list(source_dict.keys(), calc_property):	
			found = True # found at least one match for the calc_property
			min_value = 0.0
			min_value_ref = ""
			min_value_abs = 0.0
			min_value_abs_ref = ""
			max_value = 0.0
			max_value_ref = ""
			max_value_abs = 0.0
			max_value_abs_ref = ""
			total_value = 0.0
			total_value_abs = 0.0
			count = 0
			error = False
			for name in single_report_folders():							
				value_source_dict = read_results(os.path.join(report_folder, name, 'results.json'))
				
				if key not in value_source_dict:
					# key was in at least one dictionary present, but not in the dictionary of this folder
					# should never happen --> ignore key and print a fail message
					my_print("CALC_PROPERTY] Key " + key + " was not present in the dict of the folder: " + os.path.join(report_folder, name), EscCodes.FAIL)
					error = True
					break;
					
				try:
					float(value_source_dict[key])
				except ValueError:
					my_print("CALC_PROPERTY] Key " + key + " is not a float in the folder: " + os.path.join(report_folder, name), EscCodes.FAIL)
					error = True
					break;
			
				value = float(value_source_dict[key])
				count = count + 1
				total_value = total_value + value
				total_value_abs = total_value_abs + abs(value)
				if count == 1:
					min_value = value
					max_value = value
					min_value_abs = abs(value)
					max_value_abs = abs(value)
					min_value_ref = name
					max_value_ref = name
					min_value_abs_ref = name
					max_value_abs_ref = name
				else:
					if value < min_value:
						min_value = value
						min_value_ref = name
					if value > max_value:
						max_value = value
						max_value_ref = name
					if abs(value) < abs(min_value_abs):
						min_value_abs = abs(value)
						min_value_abs_ref = name
					if abs(value) > abs(max_value_abs):
						max_value_abs = abs(value)
						max_value_abs_ref = name
				
				# after calculating MIN / MAX / AVG --> store into dictionary
				if not error:
					my_print("Adding key " + key + " to dict")
					prefix = "me_multi_"
					ref_prefix = "file:"
					multi_report_dict[prefix + "min_value_" + key] = min_value 
					multi_report_dict[prefix + "min_value_ref_" + key] = ref_prefix + remove_special_chars(min_value_ref)
					multi_report_dict[prefix + "min_value_abs_" + key] = min_value_abs 
					multi_report_dict[prefix + "min_value_abs_ref_" + key] = ref_prefix + remove_special_chars(min_value_abs_ref)
					
					multi_report_dict[prefix + "max_value_" + key] = max_value
					multi_report_dict[prefix + "max_value_ref_" + key] = ref_prefix + remove_special_chars(max_value_ref)
					multi_report_dict[prefix + "max_value_abs_" + key] = max_value_abs 
					multi_report_dict[prefix + "max_value_abs_ref_" + key] = ref_prefix + remove_special_chars(max_value_abs_ref)
					
					multi_report_dict[prefix + "avg_value_" + key] = total_value / float(count)
					multi_report_dict[prefix + "avg_value_abs_" + key] = total_value_abs / float(count)
		
		if not found:			
			my_print("[CALC_PROPERTY] Could not find a match for the following regex: " + calc_property, EscCodes.WARNING)
								
	
	# Save the values in a new results.json dictionary
	multi_report_folder = os.path.join(report_folder, "multi_report")
	extend_results(os.path.join(multi_report_folder, 'results.json'), multi_report_dict)
	

if __name__ == "__main__":
    main() 