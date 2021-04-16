"""
    
	Involution Tool
	File: convertMatching.py
	
    Copyright (C) 2018-2020  Daniel OEHLINGER <d.oehlinger@outlook.com>

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
import re
import json
from helper import *

def main():
    if len(sys.argv) == 3: 
        convert_matching(sys.argv[1], sys.argv[2])
    else:
        my_print("usage: python convertMatching.py matching_in_file_path matching_out_file_path", EscCodes.FAIL)
        sys.exit(1)


def convert_matching(matching_in_file_path, matching_out_file_path):
    matching = matching_file_to_dict(matching_in_file_path)		
   
    with open(matching_out_file_path, 'w') as matching_out_file:
        json.dump(matching, matching_out_file, indent=4)	


if __name__ == "__main__":
    main()