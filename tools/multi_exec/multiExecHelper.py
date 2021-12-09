"""
    
	Involution Tool
	File: multiExecHelper.py
	
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

import os
import json

def single_report_folders():	
	report_folder = os.path.join(os.environ["RESULT_OUTPUT_DIR"], os.environ["ME_REPORT_FOLDER"])	
	list = [name for name in os.listdir(report_folder) if os.path.isdir(os.path.join(report_folder, name)) and name != 'multi_report']
	return sorted(list)
	
def save_folder_mapping(dict):
	with open(os.path.join(os.environ["TARGET_FOLDER"], 'folder_mapping.json'), 'w') as outfile:
		json.dump(dict, outfile)
		
def load_folder_mapping():
	mapping = dict()
	with open(os.path.join(os.environ["TARGET_FOLDER"], 'folder_mapping.json'), 'r') as readfile:
		mapping = json.load(readfile)
	return mapping
	
def load_swapped_folder_mapping():
	mapping = load_folder_mapping()	
	return dict([ (v, k) for k, v in mapping.items( ) ])