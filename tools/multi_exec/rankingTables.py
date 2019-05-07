"""
    
	Involution Tool
	File: rankingTables.py
	
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
		my_print("usage: rankingTables.py table_template line_template", EscCodes.FAIL)
		sys.exit(1)
		
	ranking_tables(sys.argv[1], sys.argv[2])
	
def ranking_tables(table_template, line_template):		
	report_folder = os.path.join(os.environ["RESULT_OUTPUT_DIR"], os.environ["ME_REPORT_FOLDER"])
	
	# load a list with all the dictionaries
	values_dict = dict()
	for name in single_report_folders():	
		values_dict[name] = read_results(os.path.join(report_folder, name, 'results.json'))
		
	# get a set with all keys (from all inner dictionaries, it may be possible that some dictionaries have different keys)
	key_set = set()	
	for key in values_dict.keys():
		key_set.update(values_dict[key].keys())
		
	ranking_props = list()
	if "ME_RANKING_PROPERTIES" in os.environ:
		ranking_props = parse_csv_string(os.environ["ME_RANKING_PROPERTIES"])
		
	template_content = ""
	with open(table_template, 'r') as infile:		
		template_content = infile.read()
		
	tables_content = ""
		
	# now iterate over this set and 
	for ranking_property in ranking_props:
		for dict_prop in sorted(apply_regex_to_list(key_set, ranking_property)):
			#print "Ranking prop: " + ranking_property + " Dict prop: " + dict_prop
			# Get all values from all dicts (print warning if a dict has no key)
			try:
				value_tuple = [(key, value[dict_prop]) for key,value in values_dict.items()]
			except KeyError:
				my_print("At least one of the value dictionaries does not have the key: " + dict_prop)
				continue # ignore the key (this exception should never happen, as long each single report has the same keys, which is currently the case)
			value_tuple.sort(key=lambda x: x[1])
			#print value_tuple
			# Now print the sorted values in a table form, template required!
			line_content = ""
			for file, value in value_tuple:
				line_content += line_template.replace("%##NAME##%", "\\ref{file:" + remove_special_chars(file) + "}").replace("%##VALUE##%", str(value)) + "\\\\\n"
			
			tables_content += template_content.replace("%##LINES##%", line_content).replace("||PROPERTY||", replace_special_chars(dict_prop))	+ "\n\n"
			
	if tables_content != "":	
		# add section header
		tables_content = "\section{Rankings}\n" + tables_content 				
		
	multi_report_folder = os.path.join(report_folder, 'multi_report')
	with open(os.path.join(multi_report_folder, 'ranking.tex'), 'w') as outfile:
		outfile.write(tables_content)
		
if __name__ == "__main__":
	main() 