"""
    @file buildInstanceMapping.py

	@brief Script for building the mapping between instance name
    of the fitting file and the name in the sdf file

	@author Daniel OEHLINGER <d.oehlinger@outlook.com>
	@date 2021

	@copyright
	@parblock
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
	@endparblock	
""" 

import sys
import re
import os
import json
sys.path.append('../../experiment_setup/python')
from helper import my_print, EscCodes

# python buildInstanceMapping.py ../../circuits/mips_clock_15nm/ clk_own_gidm.sdf instance_mapping.json

def main():    
    if len(sys.argv) != 4:
        my_print("usage: python buildInstanceMapping.py circuit_folder sdf_file_path instance_mapping_path", EscCodes.FAIL)
    else:
        build_instance_mapping(sys.argv[1], sys.argv[2], sys.argv[3])

def build_instance_mapping(circuit_folder, sdf_file_path, instance_mapping_path):
    instance_mapping = dict()
    sdf_file_path = os.path.join(circuit_folder, sdf_file_path)
    instance_mapping_path = os.path.join(circuit_folder, instance_mapping_path)

    sdf_file = open(sdf_file_path, 'r')
    lines = sdf_file.readlines()

    for line in lines:
        search_result = re.search(r"\(INSTANCE\s+(.*)\)", line)
        if search_result:
            instance_name = search_result.group(1)

            instance_name_clean = instance_name.replace('_', '').replace('\\', '').replace('/', '').replace('[', '').replace(']', '')

            assert(not instance_name_clean in instance_mapping)

            instance_mapping[instance_name_clean] = instance_name

    print(instance_mapping_path)
    print(instance_mapping)
    
    with open(instance_mapping_path, 'w') as instance_mapping_file:
        json.dump(instance_mapping, instance_mapping_file, sort_keys=True, indent=4)
        
if __name__ == "__main__":
    main()
