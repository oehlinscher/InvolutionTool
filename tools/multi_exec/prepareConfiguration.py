"""
    
	Involution Tool
	File: prepareConfiguration.py
	
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
import shutil
sys.path.append('../../experiment_setup/python')
from helper import *
from prepareCWG import *
from prepareGates import *
from parserHelper import *
from multiExecHelper import *

def main():
	if len(sys.argv) != 1:
		my_print("usage: prepareConfiguration.py", EscCodes.FAIL)
		sys.exit(1)
		
	prepare_configuration()
	
def prepare_configuration():
	# iterate over all folders (execept the multi_exec folder), and generate the configurations
	report_folder = os.path.join(os.environ["RESULT_OUTPUT_DIR"], os.environ["ME_REPORT_FOLDER"])

	config_id_dict = dict()
	
	for name in single_report_folders():
		current_single_report = os.path.join(report_folder, name)
		config_id = ""
		with open(os.path.join(current_single_report, 'config_id'), 'r') as config_id_file:
			config_id = config_id_file.read().strip()	
					
		if int(config_id) in config_id_dict:
			config_id_dict[int(config_id)].append(name)
			continue
			
		config_id_dict[int(config_id)] = [name]
		
		shutil.copy(os.path.join(os.environ["EXPERIMENT_SETUP_DIR"], 'tex/cwg.tex'), os.path.join(os.environ["TARGET_FOLDER"], 'cwg_' + str(config_id) + '.tex'))
		prepare_cwg(os.path.join(current_single_report, 'generate.json'), os.path.join(os.environ["TARGET_FOLDER"], 'cwg_' + str(config_id) + '.tex'), os.path.join(os.environ["EXPERIMENT_SETUP_DIR"], 'tex/cwg_group.tex'))
		prepate_gates(os.path.join(current_single_report, 'gate_config.json'), None, os.path.join(os.environ["EXPERIMENT_SETUP_DIR"], 'tex/gate_config.tex'), os.path.join(os.environ["TARGET_FOLDER"], 'gate_config_' + str(config_id) + '.tex'), os.environ["REQUIRED_GATES"])
			
	
	folder_mapping = dict()
	
	content = "\\newcounter{configurationCounter}\n"
	count = 1
	for key in sorted(config_id_dict):
		content += "\subsection{Config " + str(key) + "}\label{sec:config" + str(key) + "}\n"
		content += "Simulations:\n"
		
		content += "\\begin{enumerate}\n"
		content += "\\setcounter{enumi}{\\value{configurationCounter}}\n"
		for name in config_id_dict[key]:
			content += "\\item \\href{run:./../" + str(name)+ "/report_single.pdf}{" + replace_special_chars(str(name)) + "}\\label{file:" + remove_special_chars(str(name)) + "}\n"
			
			folder_mapping[name] = count
			count = count + 1
			
		content += "\\setcounter{configurationCounter}{\\value{enumi}}\n"
		content += "\\end{enumerate}\n"
			
			
		content += "\subsubsection{Configurable Waveform Generation}\n"
		content += "\input{cwg_" + str(key) + ".tex}\n"
		content += "\subsubsection{Gate configuration}\n"
		content += "\input{gate_config_" + str(key) + ".tex}\n"
		
	with open(os.path.join(os.environ["TARGET_FOLDER"], 'configuration.tex'), 'w') as outfile:
		outfile.write(content)
		
	save_folder_mapping(folder_mapping)	

if __name__ == "__main__":
    main()