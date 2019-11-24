"""
    
	Involution Tool
	File: extendResults.py
	
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
from parserHelper import *


def add_key_value(output_file, key, value):
	toExtend = dict()
	toExtend[key] = value
	extend_results(output_file, toExtend)
	
def add_dict_to_dict(target_file, dict_to_add_file):
	dict_to_add = read_results(dict_to_add_file)
	extend_results(target_file, dict_to_add)
	

if __name__ == "__main__":
	if len(sys.argv) == 4:
		add_key_value(sys.argv[1], sys.argv[2], sys.argv[3]) # add a simple key and value to an already existing dictionary file
	elif len(sys.argv) == 3:
		add_dict_to_dict(sys.argv[1], sys.argv[2]) # add the second dictionary to the first (both specified by their filename)
