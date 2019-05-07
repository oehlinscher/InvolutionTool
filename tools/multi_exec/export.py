"""
    
	Involution Tool
	File: export.py
	
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
	if len(sys.argv) != 1:
		my_print("usage: export.py", EscCodes.FAIL)
		sys.exit(1)
		
	export()
	
def export():
	report_folder = os.path.join(os.environ["RESULT_OUTPUT_DIR"], os.environ["ME_REPORT_FOLDER"])
	
	export_dict = dict()
	export_dict["folder_name"] = list()
	export_dict["me_config_id"] = list()
	count = 0
	
	for name in single_report_folders():	
		folder_dict = read_results(os.path.join(report_folder, name, 'results.json'))
		export_dict["folder_name"].append(name)
		config_id = ""
		with open(os.path.join(report_folder, name, 'config_id'), 'r') as config_id_file:
			config_id = config_id_file.read().strip()	
		export_dict["me_config_id"].append(int(config_id))
		for key in folder_dict:
			if key in export_dict:
				export_dict[key].append(folder_dict[key])
			else:
				if count == 0:
					export_dict[key] = [folder_dict[key]]
				else:
					# found a key, which was not present in previous folders
					my_print("Found a key: " + key + " which was not present in previous folders, fill up list with empty strings", EscCodes.WARNING)
					export_dict[key] = list()
					for i in range(0, count):
						export_dict[key].append("")
						
					# now add the "new" value
					export_dict[key].append(folder_dict[key])
					
		count = count + 1			
							
	# create a list of the header names		
	temp = ""
	if "ME_CSV_PROPERTY_ORDER" in os.environ:
		temp = os.environ["ME_CSV_PROPERTY_ORDER"]
	property_order_list = parse_csv_string(temp)
	final_order = list()
	for property in property_order_list:
		properties_to_add = apply_regex_to_list(export_dict.keys(), property)
		if properties_to_add is None or len(properties_to_add) == 0:
			my_print("No matches found for regex: " + property, EscCodes.WARNING)
			continue
			
		final_order.extend(sorted(properties_to_add)) # sort alphabetically (especially required when the regex matches multiple columns, so that we always have a defined order)				
		
	all_props = True
	if "ME_CSV_EXPORT_ALL_PROPERTIES" in os.environ:
		all_props = to_bool(os.environ["ME_CSV_EXPORT_ALL_PROPERTIES"])
		
	if all_props:
		# now add the rest of the keys in an alphabetical order
		final_order.extend([x for x in sorted(export_dict.keys()) if x not in final_order])
			
	# now build a list of list, which can be used with writerows
	csv_data = list()
	csv_data.append(final_order)
	value_list = list()
	for key in final_order:
		value_list.append(export_dict[key])
		
	csv_data.extend(zip(*value_list))	
	
	multi_report_folder = os.path.join(report_folder, "multi_report")	
	with open(os.path.join(multi_report_folder, 'values.csv'), 'wb') as f:	
		writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_ALL)
		writer.writerows(csv_data)
	

if __name__ == "__main__":
	main() 