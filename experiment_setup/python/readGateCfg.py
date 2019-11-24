"""
    
	Involution Tool
	File: readGateCfg.py
	
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
from helper import *

def read_gate_config(default_config_file, circuit_config_file):
	gates = dict()

	# ugly, better use pickle for (de)serialization?
	if os.path.isfile(default_config_file):
		with open(default_config_file, "r") as default_config:
			try:
				jsonobject = json.load(default_config)
			except ValueError:
				my_print("No valid json object found in default_config", EscCodes.FAIL)
			for key, value in jsonobject.items():
				gate = Gate()
				gate.__dict__.update(value);
				gates[gate.entity_name] = gate	

	if circuit_config_file != None and os.path.isfile(circuit_config_file):
		with open(circuit_config_file, "r") as circuit_config:		
			try:
				jsonobject = json.load(circuit_config)
			except ValueError:
				my_print("No valid json object found in circuit_config", EscCodes.WARNING)
			for key, value in jsonobject.items():
				gate = Gate()
				gate.__dict__.update(value);
				gates[gate.entity_name] = gate		
		
	return gates
	

class Gate:
	def __init__(self):
		self.entity_name = ""
		self.inputs = list()
		self.outputs = list()
		self.T_P = 1 # in ps
		self.function = ""
		self.channel_location = ChannelLocation.OUTPUT # Default Output, since VHDl Vital also places the delay at the output
		self.channel_type = ChannelType.EXP_CHANNEL
		self.channel_parameters = dict()
		
class ChannelType():
	EXP_CHANNEL = "EXP_CHANNEL"
	HILL_CHANNEL = "HILL_CHANNEL"
	SUMEXP_CHANNEL = "SUMEXP_CHANNEL"
	PUREDELAY_CHANNEL = "PUREDELAY_CHANNEL"
		
class ChannelLocation():
	INPUT = "INPUT"
	INPUT_SWAPPED = "INPUT_SWAPPED"
	OUTPUT = "OUTPUT"
	OUTPUT_SWAPPED = "OUTPUT_SWAPPED"
		
		
if __name__ == "__main__":
    main()