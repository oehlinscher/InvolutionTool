"""
    
	Involution Tool
	File: extractCircuitStructure.py
	
    Copyright (C) 2018-2020  Daniel OEHLINGER <d.oehlinger@outlook.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See ther
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import re
import json
from json import JSONEncoder
from helper import my_print, EscCodes, convert_instance_name, convert_port_name

def main():
	if len(sys.argv) == 3: 
		extract_circuit_structure(sys.argv[1], sys.argv[2])	
	else:
		my_print("usage: python extractCircuitStructure.py ", EscCodes.FAIL)
		sys.exit(1)

def read_circuit_structure(structure_file_path):
    circuit_structure = CircuitStructure()

    with open(structure_file_path, "r") as structure_file:
        try:
            jsonobject = json.load(structure_file)
            for cell in jsonobject["cells"]:
                cell_obj = Cell()
                cell_obj.__dict__ = cell
                circuit_structure.cells.append(cell_obj)

            for interconnect in jsonobject["interconnects"]:
                interconnect_obj = Interconnect()
                interconnect_obj.__dict__ = interconnect
                circuit_structure.interconnects.append(interconnect_obj)

            if 'init' in jsonobject:
                circuit_structure.init = jsonobject['init']
            else:
                circuit_structure.init = dict()
        except ValueError:
            my_print("No valid json object found in structure_file_path", EscCodes.FAIL)

    return circuit_structure
		
		
		
def extract_circuit_structure(sdf_file_path, structure_file_path):
    # Read sdf file and parse interconnect section
    structure = CircuitStructure()

    sdf_file = open(sdf_file_path)
    lines = sdf_file.readlines()

    for line in lines:
        if line.count('INTERCONNECT') > 0:       
            parts = line.split(' ')
            parts = [part for part in parts if part != ""]
            interconnect = Interconnect()
            split_interconnect_name(parts[1], interconnect, "from")
            split_interconnect_name(parts[2], interconnect, "to")

            structure.interconnects.append(interconnect)

    # Now we read all the cells from the sdf file    
    last_celltype = ""

    for line in lines:
        
        matches = re.finditer(r".*\(CELLTYPE  \"(.*)\"\).*", line, re.MULTILINE)        
        for _, match in enumerate(matches, start=1):            
            last_celltype = match.group(1) 
            break   

        matches = re.finditer(r".*\(INSTANCE\s*(.+)\).*", line, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            cell = Cell()
            cell.instance = convert_instance_name(match.group(1))
            cell.cell_type = last_celltype
            structure.cells.append(cell)

            break   
    
    save_circuit_structure(structure_file_path, structure)

def save_circuit_structure(structure_file_path, structure):    
    with open(structure_file_path, 'w') as structure_file:
        json.dump(structure.__dict__, structure_file,  sort_keys=True, indent=4, cls=CircuitStructureEncoder)



def split_interconnect_name(interconnect_name, interconnect, prefix):
    if "/" in interconnect_name:
        parts = interconnect_name.split('/')
        setattr(interconnect, prefix + "_instance", convert_instance_name("/".join(parts[:-1])))
        setattr(interconnect, prefix + "_port", convert_port_name(parts[-1]))
    else:
        
        setattr(interconnect, prefix + "_instance", convert_instance_name(interconnect_name))
        setattr(interconnect, prefix + "_port", convert_port_name(""))

class CircuitStructure:
    def __init__(self):
        self.interconnects = list()
        self.cells = list()
        self.init = dict()

    def __str__(self):
        return "interconnects: {interconnects}, cells: {cells}, init: {init}".format(interconnects = self.interconnects, cells = self.cells, init = self.init)


class CircuitStructureEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Interconnect:
        
    def __init__(self, from_instance = "", from_port = "", to_instance = "", to_port = ""):
        self.from_instance = from_instance
        self.from_port = from_port
        self.to_instance = to_instance
        self.to_port = to_port

    def __eq__(self, interconnect2):
        return (self.from_instance, self.from_port, self.to_instance, self.to_port) == (interconnect2.from_instance, interconnect2.from_port, interconnect2.to_instance, interconnect2.to_port) 

    def __gt__(self, interconnect2):
        return (self.from_instance, self.from_port, self.to_instance, self.to_port) > (interconnect2.from_instance, interconnect2.from_port, interconnect2.to_instance, interconnect2.to_port) 
        
    def __str__(self):
        return "from_instance: {from_instance}, from_port: {from_port}, to_instance: {to_instance}, to_port: {to_port}".format(from_instance = self.from_instance, from_port = self.from_port, to_instance = self.to_instance, to_port = self.to_port)

class Cell:
    def __init__(self):
        self.instance = ""
        self.cell_type = ""
        # TODO: Find a better way how to specify the pure delay
        # We need this information here because 
        self.pure_delay_up = "0.5 ps"
        self.pure_delay_down = "0.5 ps"
        self.pure_delay = "0.5 ps"
        self.channel_params = dict()
        self.hybrid_channel_params = dict()

    
    def __str__(self):
        return "instance: {instance}, cell_type: {cell_type}, pure_delay_up: {pure_delay_up}, pure_delay_down: {pure_delay_down}, pure_delay: {pure_delay}".format(instance = self.instance, cell_type = self.cell_type, pure_delay_up = get_property_fallback(self, 'pure_delay_up'), pure_delay_down = get_property_fallback(self, 'pure_delay_down'), pure_delay = get_property_fallback(self, 'pure_delay'))

def get_property_fallback(obj, prop):
    if hasattr(obj, prop):
        return obj.__dict__[prop]
    return None

if __name__ == "__main__":
    main()