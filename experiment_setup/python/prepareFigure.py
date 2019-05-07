"""
    
	Involution Tool
	File: prepareFigure.py
	
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
import re
from helper import *
from parserHelper import *
from shutil import copyfile

def main():
	if len(sys.argv) != 5:
		my_print("usage: python prepareFigure.py file figure_group_template figure_template config_file", EscCodes.FAIL)
		sys.exit(1)
	prepare_figure(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

def prepare_figure(file, figure_group_template_file, figure_template_file, config_file):	
	result_path = os.path.split(file)[0]
		
	config = read_config_file(config_file)
	if "FIGURES" not in config:
		my_print("No figures for printing configured in report.cfg")
		# just print empty tex file..
		
		with open(file, 'w') as outfile:
			outfile.write("% No figures defined in report.cfg")
		return
		
	figures = parse_csv_string(config["FIGURES"]);
	
	figure_group_template = ""
	with open(figure_group_template_file, 'r') as tempfile:
		figure_group_template = tempfile.read()
		
	figure_template = ""
	with open(figure_template_file, 'r') as tempfile:
		figure_template = tempfile.read()
	
	content = ""
	groups_content = ""
	group_content = figure_group_template
		
	with open(file, 'w') as outfile:
		for fig in figures:
			if not fig.strip():
				continue
				
			# we need to copy the figures into the result folder (because the figures change from simulation to simulation...)
			#copyfile(os.path.join(figure_path, fig.strip()), os.path.join(result_path, fig.strip()))
			
			fig_content = figure_template.replace("%##PATH##%", "fig/" + fig.strip()).replace("%##CAPTION##%", replace_special_chars(fig))
		
			if "##FIGURE##" not in group_content:
				# append the "finished" row to the content
				content += group_content
				content += "\n"
				group_content = figure_group_template
			group_content = group_content.replace("%##FIGURE##%", fig_content, 1)
			
		# remove placeholders and append...
		group_content = group_content.replace("%##FIGURE##%", "")
		content += group_content
		content += "\n"
		
		# remove first \ContinuedFloat (otherwise the numbering starts with 0)
		content = content.replace("\ContinuedFloat", "", 1)
		
		
		# now replace all %##GROUPCAPTION##% with phantomcaption, and the last with the real caption 
		count = content.count("%##GROUPCAPTION##%")
		content = content.replace("%##GROUPCAPTION##%", "\phantomcaption", count - 1)
		content = content.replace("%##GROUPCAPTION##%", "\caption{Waveform comparison}")
		
		outfile.write(content)

	
if __name__ == "__main__":
    main()