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
from helper import my_print, EscCodes
from enum import Enum


def read_gate_config(default_config_file, circuit_config_file):
    gates = dict()

    # ugly, better use pickle for (de)serialization?
    if os.path.isfile(default_config_file):
        with open(default_config_file, "r") as default_config:
            try:
                jsonobject = json.load(default_config)
            except ValueError:
                my_print(
                    "No valid json object found in default_config", EscCodes.FAIL)
            for _, value in jsonobject.items():
                gate = Gate()
                gate.__dict__.update(value)
                gates[gate.entity_name] = gate

    if circuit_config_file != None and os.path.isfile(circuit_config_file):
        with open(circuit_config_file, "r") as circuit_config:
            try:
                jsonobject = json.load(circuit_config)
            except ValueError:
                my_print("No valid json object found in circuit_config",
                         EscCodes.WARNING)
            for key, value in jsonobject.items():
                gate = Gate()
                gate.__dict__.update(value)
                gates[gate.entity_name] = gate

    # Need to convert all string into enums
    for gate in gates.values():
        if not isinstance(gate.channel_location, ChannelLocation):
            gate.channel_location = ChannelLocation(gate.channel_location)
        gate.T_P_mode = ParameterMode(gate.T_P_mode)
        gate.channel_type = ChannelType(gate.channel_type)
        gate.implementation_type = ImplementationType(gate.implementation_type)

    return gates


class Gate:
    def __init__(self):
        self.entity_name = ""
        self.inputs = list()
        self.outputs = list()
        self.T_P = 1  # in ps
        self.T_P_percent = 0.0
        self.T_P_mode = ParameterMode.ABSOLUTE
        self.function = ""
        # Default Output, since VHDl Vital also places the delay at the output
        self.channel_location = ChannelLocation.OUTPUT
        self.channel_type = ChannelType.EXP_CHANNEL
        self.channel_parameters = dict()
        self.implementation_type = ImplementationType.VHDL

    def __str__(self):
        return "entity_name: {entity_name}, inputs: {inputs}, outputs: {outputs}, T_P: {T_P}, T_P_percent: {T_P_percent}, T_P_mode: {T_P_mode}, function: {function}, channel_location: {channel_location}, channel_type: {channel_type}, channel_type: {channel_type}, channel_parameters: {channel_parameters}, implementation_type: {implementation_type}".format(entity_name=self.entity_name, inputs=self.inputs, outputs=self.outputs, T_P=self.T_P, T_P_percent=self.T_P_percent, T_P_mode=self.T_P_mode, function=self.function, channel_location=self.channel_location, channel_type=self.channel_type, channel_parameters=self.channel_parameters, implementation_type=self.implementation_type)


class ParameterMode(Enum):
    ABSOLUTE = "ABSOLUTE"
    PERCENT = "PERCENT"

    def to_json(self):
        return str(self)

    def __str__(self):
        return str(self.value)


class ChannelType(Enum):
    EXP_CHANNEL = "EXP_CHANNEL"
    HILL_CHANNEL = "HILL_CHANNEL"
    SUMEXP_CHANNEL = "SUMEXP_CHANNEL"
    PUREDELAY_CHANNEL = "PUREDELAY_CHANNEL"
    HYBRID_CHANNEL = "HYBRID_CHANNEL"

    def to_json(self):
        return str(self)
    
    def __str__(self):
        return str(self.value)


class ChannelLocation(Enum):
    INPUT = "INPUT"
    INPUT_SWAPPED = "INPUT_SWAPPED"
    OUTPUT = "OUTPUT"
    OUTPUT_SWAPPED = "OUTPUT_SWAPPED"

    def to_json(self):
        return str(self)

    def __str__(self):
        return str(self.value)


class ImplementationType(Enum):
    VHDL = "vhdl"
    PYTHON = "python"
    
    def to_json(self):
        return str(self)
    
    def __str__(self):
        return str(self.value)
