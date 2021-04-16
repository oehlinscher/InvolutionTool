"""
    
	Involution Tool
	File: convertSDFFileGIDM.py
	
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
import os
import re
from helper import *


def main():
    if len(sys.argv) == 4:
        convert_sdf_file_gidm(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        my_print("usage: python convertSDFFileGIDM.py sdf_input_file_path, sdf_output_file_path required_gates", EscCodes.FAIL)
        sys.exit(1)


def convert_sdf_file_gidm(sdf_input_file_path, sdf_output_file_path, required_gates):
    required_gates = required_gates.split()
    regex = r"CELLTYPE\s+\"(\w+)\"\s*\)\s*\(INSTANCE\s+([^)]*)"

    
    sdf_content = ""
    with open(sdf_input_file_path) as sdf_input_file:
        sdf_content = sdf_input_file.read()

    matches = re.finditer(regex, sdf_content, re.MULTILINE)

    celltype = ""
    instance = ""
    match_str = ""
    for _, match in enumerate(matches, start=1):
        match_str = match.group()

        for _ in range(0, len(match.groups())):
            celltype = match.group(1)
            instance = match.group(2)
            break

        if celltype in required_gates:
            replaced_match_str = match_str.replace(celltype, celltype + "_" + convert_instance_name(instance))
            sdf_content = sdf_content.replace(match_str, replaced_match_str)
            
    f = open(sdf_output_file_path, "w")
    f.write(sdf_content)
    f.close()

if __name__ == "__main__":
    main()