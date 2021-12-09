"""

	Involution Tool
	File: prepareTestbenchGIDM.py

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
from readGateCfg import *
from extractCircuitStructure import *


def main():
    if len(sys.argv) == 7:
        prepare_testbench_gidm(
            sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    else:
        my_print("usage: python prepareTestbenchGIDM.py circuit_file_in circuit_out_file_path process_template_file_path input_names circuit_structure_file_path tt_file_path", EscCodes.FAIL)
        sys.exit(1)


def prepare_testbench_gidm(circuit_template_file_path, circuit_out_file_path, process_template_file_path, input_names, circuit_structure_file_path, tt_file_path):
    my_print("prepare_testbench_gidm ")

    # gates = read_gate_config(default_gate_config_file, circuit_gate_config_file)

    circuit_template = ""
    with open(circuit_template_file_path, 'r') as circuit_template_file:
        circuit_template = circuit_template_file.read()

    process_template = ""
    with open(process_template_file_path, 'r') as process_template_file:
        process_template = process_template_file.read()

    input_list = input_names.split(" ")
    input_list = [x.strip(" \r\t\n") for x in input_list if x.strip(" \r\n\t")]

    # we do not iterate over the input_list (or the vector_names)
    # we rather need to iterate over the structure.json, 
    # and generate for each element in the list where the FromInstance 
    # matches exactly with a signal from the input list a process
    input_process_content = ""

    for input_sig in input_list:
        tt_file_path_complete = tt_file_path + "/" + input_sig

        input_process_content += process_template.replace(
            "##SIGNALNAME##", input_sig).replace("##VECTORNAME##", "vectors_" + input_sig).replace("##TT_FILE_PATH##", tt_file_path_complete)
        input_process_content += "\n\n\n"
    

    input_process_content = """
		init_proc : PROCESS
		BEGIN
			init_wrapper;
			initialized <= '1';
			WAIT;
		END PROCESS;


        """.format() + input_process_content

    all_inputs_done = " AND ".join(["{input}_done = '1'".format(input = input) for input in input_list])

    input_process_content = input_process_content + """


		clean_process : PROCESS
		BEGIN
			WAIT UNTIL {all_done};
			WAIT for 10 sec; -- This is to ensure that clean_wrapper is definitely called after all transitions have been handled
			clean_wrapper;
			WAIT;
		END PROCESS;
		""".format(all_done = all_inputs_done)



    content_to_write = circuit_template.replace(
        "##INPUT_PROCESS##", input_process_content)

    with open(circuit_out_file_path, 'w') as circuit_out_file:
        circuit_out_file.write(content_to_write)


if __name__ == "__main__":
    main()
