"""
    
	Involution Tool
	File: combineGateGeneration.py
	
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
import json
from helper import my_print, EscCodes, ObjectEncoder
from readGateCfg import read_gate_config

def main():
	# required_gates is optional, if not set, all gates are generated
	if len(sys.argv) != 4: 
		my_print("usage: python combineGateGeneration.py default_config_file circuit_config_file target_config_file", EscCodes.FAIL)
	else:
		combine_gates(sys.argv[1], sys.argv[2], sys.argv[3])	
	
def combine_gates(default_config_file, circuit_config_file, target_config_file):	
	gates = read_gate_config(default_config_file, circuit_config_file)
	
	
	with open(target_config_file, "w") as gate_cfg_file:
		gate_cfg_file.write(json.dumps(gates, cls=ObjectEncoder, indent=2, sort_keys=True))
		
if __name__ == "__main__":
    main()