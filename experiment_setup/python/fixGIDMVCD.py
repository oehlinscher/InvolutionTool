"""
    
	Involution Tool
	File: fixGIDMVCD.py
	
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
import json
from helper import *
from vcdParser import *
from extractCircuitStructure import *


def main():
    if len(sys.argv) == 6:
        fix_gidm_vcd(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        my_print("usage: python fixGIDMVCD.py vcd_input_file_path, vcd_output_file_path tt_folder_path port_to_signal_matching_file_path structure_file_path", EscCodes.FAIL)
        sys.exit(1)


def fix_gidm_vcd(vcd_input_file_path, vcd_output_file_path, tt_folder_path, port_to_signal_matching_file_path, structure_file_path):
    # First we need to parse the signal section from the transition indicator file,
    # so that we have a mapping between signal and char
    (_, signal_to_char_mapping) = generate_vcd_mapping(vcd_input_file_path)
    converted_signal_to_char_mapping = dict()
    for key, value in signal_to_char_mapping.items():
        converted_signal_to_char_mapping[convert_instance_name(key)] = value

    signal_to_char_mapping = converted_signal_to_char_mapping
    
    structure = read_circuit_structure(structure_file_path)    
    

    # The next step is to generate a mapping between tt file names (instance + port) and signal names
    # This should be possible via the matching file 
    # But I dont think thats a good idea, since the matching is between HSPICE and the Verilognames,
    # so this is something completely different
    # Maybe one idea is to prepare another matching file between instance_name + port and the signal name
    port_to_signal_matching = dict()
    with open(port_to_signal_matching_file_path) as port_to_signal_matching_file:
        port_to_signal_matching = json.load(port_to_signal_matching_file)
 
    vcd_data_dict = buid_vcd_data(port_to_signal_matching, signal_to_char_mapping, tt_folder_path)

    # We need to fix the initial values in the VCD, since they are the ones from the TransitionIndicator, and not from the actual signal
    # Therefore we load the initial values from structure[init], or set them hardcoded to 0, if no value is specified there
    # The input string is between a line "$dumpvars" and "$end"
    init_mapping = dict()
    for interconnect in structure.interconnects:
        # There should be a file "interconnect.from_instance + interconnect.from_port + 'complete'""
        port = interconnect.from_instance + interconnect.from_port
        if port in port_to_signal_matching:
            signal = port_to_signal_matching[port]
        else:
            # In this case port must be an input
            continue # We can leave the init as it as

        init_value = '0'
        if interconnect.from_instance in structure.init:
            init_value = structure.init[interconnect.from_instance]


        char = signal_to_char_mapping[signal]
        init_mapping[char] = init_value


    signal_str = ""
    for time, change_list in sorted(vcd_data_dict.items()):
        signal_str += "#" + str(time) + "\n"
        for (signal_name, lvl) in change_list:
            signal_str += str(lvl) + signal_to_char_mapping[signal_name] + "\n"

    dump_vcd(vcd_input_file_path, vcd_output_file_path, init_mapping, signal_str)

def dump_vcd(vcd_input_file_path, vcd_output_file_path, init_mapping, signal_str):
    
    vcd_content = ""
    with open(vcd_input_file_path) as vcd_input_file:
        vcd_content = vcd_input_file.readlines()

    final_vcd_content = ""
    enddefinition = False
    for line_idx, line in enumerate(vcd_content):
        final_vcd_content += line
        if line.startswith("$enddefinitions $end"):
            enddefinition = True
        if enddefinition and line.strip() == "$dumpvars":
            break

    line_idx += 1
    line = vcd_content[line_idx]
    init_str = ""
    while line.strip() != "$end":
        # Try parsing the line, it should be of the format "0Sig", where 0 is a std_logic value, and Sig is the character assigned to the signal
        val = line[0]
        char = line[1:].rstrip()

        if char in init_mapping:
            init_str += init_mapping[char] + char + "\n"
        else:
            init_str += line

        line_idx += 1
        line = vcd_content[line_idx]

    final_vcd_content += init_str
    final_vcd_content += "$end\n"
    final_vcd_content += signal_str

    f = open(vcd_output_file_path, "w")
    f.write(final_vcd_content)
    f.close()

def remove_canceled_transitions(signal_transitions):    
    # We also need to take care to remove canceled transitions (so that we are compatible with vcd standard)
    # Later we can add artificial signals to indicate canceled transitions
    filtered_list = list()
    last_valid_lvl = None
    first_trans = True
    cancel_count = 0

    # We need to check the signal_transition list for cancelations at the beginning, so that we do not initialize last_valid_level false
    while len(signal_transitions) >= 2:
        if signal_transitions[1][0] <= signal_transitions[0][0]:
            # remove the first two elements
            signal_transitions.pop(0)
            signal_transitions.pop(0)
        else:
            # We are done removing cancelled transitions at the beginning
            break


    for (time, lvl) in sorted(signal_transitions):     
        if first_trans:
            last_valid_lvl = lvl
            first_trans = False
        else:
            if last_valid_lvl == lvl:
                cancel_count = cancel_count + 1
                continue
            else:
                if cancel_count == 0:
                    last_valid_lvl = lvl
                else:
                    cancel_count = cancel_count - 1
                    continue
                

        filtered_list.append((time, lvl))

    return filtered_list

def buid_vcd_data(port_to_signal_matching, signal_to_char_mapping, tt_folder_path):
    # vcd_data_dict is a dictionary where the key is the transition time and the value is a list of tuples with signal name and value
    vcd_data_dict = dict()

    for subdir, dirs, files in os.walk(tt_folder_path):
        for file in files:
            if file.endswith((".complete")):
                portname = file[:-len(".complete")]

                # look into the dict
                signal_name = portname
                if portname in port_to_signal_matching:
                    signal_name = port_to_signal_matching[portname]                
                    
                if not signal_name in signal_to_char_mapping:
                    my_print("Could not find a char for signal: " + signal_name, EscCodes.FAIL)

                signal_transitions = read_signal_transitions(os.path.join(subdir, file))

                signal_transitions = remove_canceled_transitions(signal_transitions)

                for (time, lvl) in signal_transitions:
                    if not time in vcd_data_dict:
                        vcd_data_dict[time] = list()

                    vcd_data_dict[time].append((signal_name, lvl))

    return vcd_data_dict

def read_signal_transitions(tt_filepath):
    # Now we can read the .complete file and file the vcd_data 
    signal_transitions = list()
    with open(tt_filepath) as complete_file:
        for line in complete_file:	
            if not line:
                continue

            [time, lvl] = line.split()
            time = int(time)
            lvl = int(lvl.replace("'", ""))

            # We do not need to take care of initialization
            if time == 0:
                continue

            signal_transitions.append((time, lvl))
            
    return signal_transitions

if __name__ == "__main__":
    main()