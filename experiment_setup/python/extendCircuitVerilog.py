"""
    
	Involution Tool
	File: generateGates.py
	
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
    if len(sys.argv) == 7: 
        extract_circuit_verilog(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    else:
        my_print("usage: python extendCircuitVerilog.py circuit_file_path gidm_circuit_file_path required_gates input_names structure_file_path port_to_signal_matching_file_path", EscCodes.FAIL)
        sys.exit(1)


module_regex = r".*\s*module\s+(\S*)\s*\("
endmodule_regex = r"\s*endmodule\s*"
instance_name_regex_template = r"(?:\s*(##MODULE##)\s+(\S+)\s*\(.*)"
top_level_module_regex = r"\s*module\s*##TOPLEVELMODULE##\s*\(((\s*[^\)]*)*)\);"
gate_regex_template = r"(?:\s*(##GATE##)\s+([^(|^\s]*)\s*\(.*)"
gate_regex_modified_template = r"(?:\s*##GATE##_(\w*)\s+([^(|^\s]*)\s*\(.*)"

def extract_circuit_verilog(circuit_file_path, gidm_circuit_file_path, required_gates, input_names, structure_file_path, port_to_signal_matching_file_path):

    required_gates = required_gates.split()
    input_names = input_names.split()

    # Read the content of the circuit_file
    content = ""
    with open(circuit_file_path, 'r') as circuit_file:		
        content = circuit_file.read()

    # Modules contains 
    modules = dict()
    parent_modules = dict()

    find_modules(modules, parent_modules, content)

    content_lines = content.splitlines()      

    # contains tuples with the gate name, complete instance name, instance name in     
    unique_gate_name_list = list() 
    rename_gates(content_lines, modules, parent_modules, unique_gate_name_list, required_gates)
    content = "\n".join(content_lines)

    matching = build_matching(content_lines, required_gates, modules, parent_modules)
        
    with open(gidm_circuit_file_path, 'w') as gidm_circuit_file:
        gidm_circuit_file.write(content)    

    with open(port_to_signal_matching_file_path, 'w') as port_to_signal_matching_file:
        json.dump(matching, port_to_signal_matching_file, indent=4)

def find_modules(modules, parent_modules, content):
    matches = re.finditer(module_regex, content, re.MULTILINE)

    for _, match in enumerate(matches, start=1):
        modules[match.group(1)] = ""
        parent_modules[match.group(1)] = ""

    # This assumes that the INSTANCE and the NAME are in the same row
    content_lines = content.splitlines()

    instance_name_regex = ""
    for module in modules:
        instance_name_regex += instance_name_regex_template.replace("##MODULE##", module) + "|"     
    instance_name_regex = instance_name_regex[:-1]
    # Keep track of the current module
    current_module = ""
    for line in content_lines:
        current_module = update_current_module(current_module, line)          
        
        module_name = ""
        instance_name = "" 
        matches = re.finditer(instance_name_regex, line, re.MULTILINE)     
        for _, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                if match.group(groupNum) is not None:
                    module_name = match.group(groupNum)
                    instance_name = match.group(groupNum+1)
                    break  
            
            # print(current_module_list, " - ", instance_name)
            if modules[module_name] != "":
                # We need to check if modules are instantiated multiple times.
                # If this is the case, we also need duplicate the modules 
                # since they are using different gates (depending on the name of the instance)    
                # If this assertion fails, you need to implement the module duplication
                assert(False)

            modules[module_name] = instance_name
            parent_modules[module_name] = current_module
            break

def build_gate_regex(required_gates, use_modified = False):
    gate_regex = ""
    template = gate_regex_template
    if use_modified:
        template = gate_regex_modified_template
    # Build the regex
    for required_gate in required_gates:
        gate_regex += template.replace("##GATE##", required_gate) + "|"     
    gate_regex = gate_regex[:-1]
    return gate_regex

def rename_gates(content_lines, modules, parent_modules, unique_gate_name_list, required_gates):
    # Find all instances of required gates and replace the gate name with 
    # "gate name" + _ + "module names" + "instance name"      
    # Now we find all instances of required gates. 
    # These are the ones that need to be replaced
    gate_regex = build_gate_regex(required_gates)
    
    # Keep track of the current module
    current_module = ""
    for nr, line in enumerate(content_lines):
        current_module = update_current_module(current_module, line) 

        matches = re.finditer(gate_regex, line, re.MULTILINE)

        gate_name = ""
        instance_name = ""                
        for _, match in enumerate(matches, start=1):
            for group_num in range(0, len(match.groups())):
                group_num = group_num + 1
                if match.group(group_num) is not None:
                    gate_name = match.group(group_num)
                    instance_name = match.group(group_num+1)
                    break

            module_name = build_module_name(current_module, modules, parent_modules)                
            complete_instance_name = "_" + convert_instance_name(module_name + "_" + instance_name)
            new_gate_name = gate_name + complete_instance_name
            unique_gate_name_list.append((new_gate_name, complete_instance_name[1:], instance_name))
            content_lines[nr] = content_lines[nr].replace(gate_name, new_gate_name)
            break

def build_module_name(current_module, modules, parent_modules):
    # We need to also add the complete module hierachy to the name 
    parent_module =  current_module

    instances = modules[parent_module]
    instance_list = list()
    while instances != "":
        instance_list.append(instances)
        parent_module = parent_modules[parent_module]
        instances = modules[parent_module]

    module_name = ""
    for instance in reversed(instance_list):
        module_name += "_" + instance

    return module_name

def build_matching(content_lines, required_gates, modules, parent_modules):
    matching = dict()
    instantiation_regex = r"\.(\w*)\s*\(([\w\[\]]*)\)"
    gate_regex = build_gate_regex(required_gates, True)
    current_gate = None
    current_module = ""

    for line in content_lines:        
        current_module = update_current_module(current_module, line)      

        matches = re.finditer(gate_regex, line, re.MULTILINE)

        for _, match in enumerate(matches, start=1):
            for group_num in range(0, len(match.groups())):
                group_num = group_num + 1
                if match.group(group_num) is not None:
                    current_gate = match.group(group_num)
                    # print("Current gate: " + str(current_gate), match.group(group_num), match.group(group_num+1), line)
                    break
        
        
        if current_gate is not None:
            matches = re.finditer(instantiation_regex, line, re.MULTILINE)
            
            for _, match in enumerate(matches, start=1):
                module_name = build_module_name(current_module, modules, parent_modules)
                matching[convert_instance_name(current_gate + match.group(1))] = convert_instance_name(module_name + match.group(2), True)
            
        # If the line matches )); then we need to reset the current gate...
        instantiation_close_regex = r".*\)\s*\)\s*;.*" 
        matched = re.match(instantiation_close_regex, line)
        if bool(matched):
            current_gate = None



    return matching

def update_current_module(current_module, line):
    
    matches = re.finditer(module_regex, line, re.MULTILINE)
    
    for _, match in enumerate(matches, start=1):
        # Push to new module
        return match.group(1)
        
    return current_module



if __name__ == "__main__":
    main()