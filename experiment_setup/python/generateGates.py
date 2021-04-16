"""
    
	Involution Tool
	File: generateGates.py
	
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
import os
from readGateCfg import *
from helper import *
from extractCircuitStructure import *


def main():
    # required_gates is optional, if not set, all gates are generated
    if len(sys.argv) == 11:
        generate_gates(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                       sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], None)
    elif len(sys.argv) == 12:
        generate_gates(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                       sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
    else:
        my_print("usage: python generateGates.py default_config_file circuit_config_file gate_dir gate_template_file gate_input_process_template_file use_gidm structure_file tt_file_path generate_gate_per_instance required_gates", EscCodes.FAIL)
        sys.exit(1)


def generate_gates(default_config_file, circuit_config_file, gate_dir, gate_template_file, gate_input_process_template_file, use_gidm, structure_file, tt_file_path, generate_gate_per_instance, vectors_dir_file_path, required_gates):

    gates = read_gate_config(default_config_file, circuit_config_file)
    use_gidm = to_bool(use_gidm)
    generate_gate_per_instance = to_bool(generate_gate_per_instance)

    # read template for gate
    gate_template = ""
    with open(gate_template_file, 'r') as template_file:
        gate_template = template_file.read()

    # read template for gate input process
    gate_input_process_template = ""
    with open(gate_input_process_template_file, 'r') as template_file:
        gate_input_process_template = template_file.read()

    generate_all = required_gates is None or "ALL" in required_gates

    structure = CircuitStructure()
    if use_gidm or generate_gate_per_instance:
        # now we need to read the structure.json file and generate
        structure = read_circuit_structure(structure_file)

    # now that we have all the gates we want to create --> create them
    for name, gate in gates.items():
        if not generate_all and name not in required_gates:
            my_print("Ignoring: " + name)
            continue  # we do not want to generate all gates, if not necessary for the circuit

        if len(gate.inputs) == 0:
            my_print("Error at gate: " + name +
                     ". No input defined!", EscCodes.FAIL)
            continue

        if len(gate.outputs) != 1:
            my_print("Error at gate: " + name +
                     ". Only one output supported yet!", EscCodes.FAIL)
            continue

        function = ""
        output = gate.outputs[0]
        entity_generic = ""
        delay_channel = ""

        signal_list = list()
        entity_generic_list = list()
        delay_channel_list = list()
        function = ""
        function_input_list = list()
        ports = ""

        for input in gate.inputs:
            entity_generic_list.append(input)

        if not use_gidm and (gate.channel_location == ChannelLocation.INPUT or gate.channel_location == ChannelLocation.INPUT_SWAPPED):
            my_print("Before")

            function = output + " <= "

            for input in gate.inputs:
                function_input_list.append(input + "_del")

            for input in gate.inputs:
                signal_list.append(input + "_del")

            for input in gate.inputs:
                delay_channel_list.append((input, input + "_del"))

        if not use_gidm and (gate.channel_location == ChannelLocation.OUTPUT or gate.channel_location == ChannelLocation.OUTPUT_SWAPPED):
            my_print("After")
            function = output + "_pre <= "
            function_input_list = gate.inputs

            for out in gate.outputs:
                signal_list.append(out + "_pre")

            for out in gate.outputs:
                delay_channel_list.append((out + "_pre", out))

        if use_gidm:
            # the function is built different when using GIDM
            # we ignore the ChannelLocation fpr GIDM
            # Currently just one output supported
            function = gate.outputs[0] + "PreDelay <= "
            for input in gate.inputs:
                function_input_list.append(input + "AfterDelta")

            for out in gate.outputs:
                delay_channel_list.append((out + "PreDelay", out))

        if len(function_input_list) == 1:
            function += gate.function + " " + function_input_list[0]
        else:
            for input in function_input_list[:-1]:
                function += input + " " + gate.function + " "
            function += function_input_list[-1]
        function += ";"

        for elem in entity_generic_list:
            entity_generic += "tipd_" + elem + \
                " : VitalDelayType01 := (0.0 ns, 0.0 ns);\n\t\t"
            for out in gate.outputs:
                entity_generic += "tpd_" + elem + "_" + out + \
                    " : VitalDelayType01Z := (OTHERS => 0.0 ns);\n\t\t"

        for channel in delay_channel_list:
            d_up = ""
            d_down = ""
            if gate.channel_location == ChannelLocation.INPUT or gate.channel_location == ChannelLocation.INPUT_SWAPPED:
                delay_up = "tr01"
                delay_down = "tr10"
                if gate.channel_location == ChannelLocation.INPUT_SWAPPED:
                    delay_up = "tr10"
                    delay_down = "tr01"

                d_up = "tpd_" + channel[0] + "_" + \
                    output + "(" + delay_up + ")"
                d_down = "tpd_" + channel[0] + "_" + \
                    output + "(" + delay_down + ")"
            if gate.channel_location == ChannelLocation.OUTPUT or gate.channel_location == ChannelLocation.OUTPUT_SWAPPED:
                delay_up = "tr01"
                delay_down = "tr10"
                if gate.channel_location == ChannelLocation.OUTPUT_SWAPPED:
                    delay_up = "tr10"
                    delay_down = "tr01"

                (d_up, d_down) = generate_multiinput_delay_strings(
                    gate, output, delay_up, delay_down)

            channel_name = ""
            if gate.channel_type == ChannelType.EXP_CHANNEL:
                channel_name = "exp_channel"
            elif gate.channel_type == ChannelType.HILL_CHANNEL:
                channel_name = "hill_channel"
            elif gate.channel_type == ChannelType.SUMEXP_CHANNEL:
                channel_name = "sumexp_channel"
            elif gate.channel_type == ChannelType.PUREDELAY_CHANNEL:
                channel_name = "puredelay_channel"
            else:
                my_print("Unkown channel type: " +
                         str(gate.channel_type), EscCodes.FAIL)

            if use_gidm:
                channel_name = "gidm_" + channel_name

            channel_parameters = ""
            for param_key, param_value in gate.channel_parameters.iteritems():
                channel_parameters += ",\n\t\t" + \
                    str(param_key) + " => " + str(param_value)

        arch_name = ""
        if use_gidm:
            arch_name = gate.channel_type + '_GIDM'
        else:
            arch_name = gate.channel_type + '_' + gate.channel_location

        content = gate_template.replace("##ARCH_NAME##", arch_name).replace("##ARCH_FUNCTION##", function).replace(
            "##ENTITY_GENERIC##", entity_generic).replace("##GATE_SPECIFIC_PARAMETERS##", "")
        if use_gidm:
            # For GIDM, we need to initialize both, the input and output ports with 0, because that is how the toggle indicator is initialized
            for input in gate.inputs:
                ports += input + " : IN STD_ULOGIC := '0';\n\t\t"

            for out in gate.outputs:
                ports += out + " : OUT STD_ULOGIC := '0';\n\t\t"

            ports = ports[:-4]

            content = content.replace("##PORTS##", ports)


            # now we need to read the structure.json file and generate
            for cell in structure.cells:
                if cell.cell_type == name:
                    input_processes = ""

                    # We need to check if the cell has a pure_delay set, and if not, we need to assign a pure delay > 0 to it
                    if 'pure_delay' not in cell.__dict__:
                        cell.pure_delay = estimate_pure_delay(cell)
                    
                    # Set the values for the pure delay shifter at the inputs
                    set_delta(cell)

                    # For each input
                    for input in gate.inputs:
                        input_processes += gate_input_process_template.replace("##INPUT##", input)
                        # For the tt_file path, we need to look who is our predecessor
                        pred_interconnect = find_pred_interconnect(structure, cell, input)
                        assert (pred_interconnect is not None)
                        tt_file = tt_file_path + "/" + pred_interconnect.from_instance + pred_interconnect.from_port
                        input_processes = input_processes.replace(
                            "##TT_FILE##", tt_file)

                        pure_delay_code = build_pure_delay_code(gate.function, cell.delta_plus, cell.delta_minus, input + "AfterDelta", function_input_list)

                        # if gate.function.lower() == "not":
                        #     # for an inverter we need to swap both pure delays (see discussion with Juergen from)
                        #     pure_delay_up = cell.pure_delay_down
                        #     pure_delay_down = cell.pure_delay_up
                        # else:   
                        #     ##PURE_DELAY_CALC##                         
                        #     pure_delay_up = average_pure_delay(cell.pure_delay_up, cell.pure_delay_down)
                        #     pure_delay_down = pure_delay_up
                        #     my_print("Pure Delay handling for gate function " + gate.function + " not specified. We simply use the average of both pure delays", EscCodes.WARNING)
                        input_processes = input_processes.replace("##PURE_DELAY_CALC##", pure_delay_code)

                    # Iterate over all the interconnects
                    # which are after this gate instance
                    # + one delay channel used for comparison
                    delay_channel = ""

                    # Sum up the input delays
                    # TODO: Find a better way, once the theory how to do is is clear
                    (d_up, d_down) = generate_multiinput_delay_strings(	gate, output, "tr01", "tr10")

                    succ_interconnect = find_succ_interconnect(structure, cell, gate.outputs[0])	
                    assert succ_interconnect is not None

                    # This is now the process for the output which we use for comparison
                    tt_file = tt_file_path + "/" + succ_interconnect.from_instance + succ_interconnect.from_port
                    delay_channel += ("" +
                                        "delay_" + channel[0] +
                                        " : " + channel_name + "\n"
                                        "\tgeneric map(\n" +
                                        "\t\tD_INF_UP => " + d_up + ",\n" +
                                        "\t\tD_INF_DO => " + d_down + ",\n" +
                                        "\t\tV_DD => " + os.environ['VDD'] + ",\n" +
                                        "\t\tV_TH => " + os.environ['VTH'] +
                                        # How to set the following two parameters? To 0? Or to the average? Or to our own pure delay?
                                        # Discussed with Juergen: We need to use our own pure delay
                                        # (then we can also ensure backwards compatibility with IDM)
                                        channel_parameters + ",\n" +
                                        "\t\tD_MIN => " + cell.pure_delay + ",\n" +
                                        "\t\tDELTA_PLUS => " + cell.delta_plus + ",\n" +
                                        "\t\tDELTA_MINUS => " + cell.delta_minus + ",\n" +
                                        "\t\tTRANSITION_TIME_FILE_PATH => \"" + tt_file + "\")\n" +
                                        "\tport map(\n" +
                                        "\t\tinput => " + channel[0] + ",\n" +
                                        "\t\toutput => " + gate.outputs[0] + ");\n" +
                                        "\n\t")

                    # Signals
                    signals = ""
                    for input in gate.inputs:     
                        init_value = "0"                      
                        pred_interconnect = find_pred_interconnect(structure, cell, input)
                        if pred_interconnect.from_instance in structure.init:
                            init_value = structure.init[pred_interconnect.from_instance]

                        if pred_interconnect.from_port == "":
                            # We have an input here. For an input, we need to set the value to the one specified in vectors dir
                            # Otherwise it might happen that we toggle a transition indicator twice at the same t, which leads to a lost transition
                            # Look into the vectors dir, and find a file called "vector"_ + pred_interconnect.from_instance and read the first line without a comment

                            with open(vectors_dir_file_path + "/vectors_" + pred_interconnect.from_instance) as vectors_dir_file:
                                for line in vectors_dir_file:
                                    if line.startswith("#"):
                                        continue
                                    else:
                                        (t, v) = line.split()
                                        assert(int(t) == 0)
                                        init_value = str(int(v))
                                        break



                        signals += "SIGNAL " + input + "AfterDelta : STD_ULOGIC := '" + init_value + "';"
                        signals += "\n\t"
             
                    for out in gate.outputs:                
                        init_value = "0" # We simply fix the init value to 0. If specified, we overwrite this value. 
                        if cell.instance in structure.init:
                            init_value = structure.init[cell.instance]

                        signals += "SIGNAL " + out + "PreDelay : STD_ULOGIC := '" + init_value + "';"
                        signals += "\n\t"

                    content_repl = content.replace("##ENTITY_NAME##", gate.entity_name + "_" + cell.instance).replace("##ARCH_INPUT_PROCESSES##", input_processes).replace("##ARCH_DELAY_CHANNEL##", delay_channel).replace("##ARCH_SIGNALS##", signals)
                    with open(os.path.join(gate_dir, name + "_" + cell.instance + ".vhd"), "w") as gate_file:
                        gate_file.write(content_repl)
        else:
            if generate_gate_per_instance:

                for cell in structure.cells:                    
                     # Correct initialization only implement for this ChannelLocation, other ChannelLocations are not really used any more, since they do not correspond to the model
                    assert gate.channel_location == ChannelLocation.OUTPUT

                    # For channel location OUTPUT, this is basically one signal, which is the value after the gate output. This needs to be set according to the init value
                    assert(len(signal_list) == 1)

                    init_value_out = "0" # We simply fix the init value to 0. If specified, we overwrite this value. 
                    if cell.instance in structure.init:
                        init_value_out = structure.init[cell.instance]                        

                    signals = ""
                    for sig in signal_list:
                        signals += "SIGNAL " + sig + " : STD_ULOGIC := '" + init_value_out + "';" 
                        signals += "\n\t"

                    # For IDM, we need to initialize both, the input and output ports with 0, because that is how the toggle indicator is initialized                          
                    init_value_in = "0"                      
                    pred_interconnect = find_pred_interconnect(structure, cell, input)
                    if pred_interconnect.from_instance in structure.init:
                        init_value_in = structure.init[pred_interconnect.from_instance]

                    ports = ""
                    for input in gate.inputs:
                        ports += input + " : IN STD_ULOGIC := '" + init_value_in + "';\n\t\t"

                    delay_channel = ("" +
                                  "delay_" + channel[0] +
                                  " : " + channel_name + "\n"
                                  "\tgeneric map(\n" +
                                  "\t\tD_UP => " + d_up + ",\n" +
                                  "\t\tD_DO => " + d_down + ",\n" +
                                  "\t\tT_P => " + cell.pure_delay + ",\n"
                                  "\t\tT_P_PERCENT => " +
                                  str(gate.T_P_percent) + ",\n"
                                  "\t\tT_P_MODE => " + str(gate.T_P_mode) +
                                  channel_parameters + ",\n" +
                                  "\t\tV_DD => " + os.environ['VDD'] + ",\n" +
                                  "\t\tV_TH => " + os.environ['VTH'] + ",\n" +
                                  "\t\tINIT_VALUE => '" + init_value_out + "')\n"
                                  "\tport map(\n" +
                                  "\t\tinput => " + channel[0] + ",\n" +
                                  "\t\toutput => " + channel[1] + ");\n" +
                                  "\n\t")
                    
                    # The output is set to our init value (if specified)
                    init_value = "0"
                    if cell.instance in structure.init:
                            init_value = structure.init[cell.instance]
                    for out in gate.outputs:
                        ports += out + " : OUT STD_ULOGIC := '" + init_value + "';\n\t\t"

                    ports = ports[:-4]

                    content_repl = content.replace("##ENTITY_NAME##", gate.entity_name + "_" + cell.instance).replace(
                        "##ARCH_INPUT_PROCESSES##", "").replace("##ARCH_DELAY_CHANNEL##", delay_channel).replace("##PORTS##", ports).replace("##ARCH_SIGNALS##", signals)
                    with open(os.path.join(gate_dir, name + "_" + cell.instance + ".vhd"), "w") as gate_file:
                        gate_file.write(content_repl)
            else:  
                assert gate.channel_location == ChannelLocation.OUTPUT

                # For channel location OUTPUT, this is basically one signal, which is the value after the gate output. This needs to be set according to the init value
                assert(len(signal_list) == 1)        

                signals = ""
                for sig in signal_list:
                    signals += "SIGNAL " + sig + " : STD_ULOGIC := '0';" 
                    signals += "\n\t"

                # If we have no possibility to set the initialization for each gate individually, set all to 0
                for input in gate.inputs:
                    ports += input + " : IN STD_ULOGIC := '0';\n\t\t"

                for out in gate.outputs:
                    ports += out + " : OUT STD_ULOGIC := '0';\n\t\t"

                ports = ports[:-4]

                delay_channel += ("" +
                                  "delay_" + channel[0] +
                                  " : " + channel_name + "\n"
                                  "\tgeneric map(\n" +
                                  "\t\tD_UP => " + d_up + ",\n" +
                                  "\t\tD_DO => " + d_down + ",\n" +
                                  "\t\tT_P => " + str(gate.T_P) + " ps" + ",\n"
                                  "\t\tT_P_PERCENT => " +
                                  str(gate.T_P_percent) + ",\n"
                                  "\t\tT_P_MODE => " + str(gate.T_P_mode) +
                                  channel_parameters + ",\n" +
                                  "\t\tV_DD => " + os.environ['VDD'] + ",\n" +
                                  "\t\tV_TH => " + os.environ['VTH'] + ")\n" +
                                  "\tport map(\n" +
                                  "\t\tinput => " + channel[0] + ",\n" +
                                  "\t\toutput => " + channel[1] + ");\n" +
                                  "\n\t")

                content = content.replace("##ENTITY_NAME##", gate.entity_name).replace(
                    "##ARCH_INPUT_PROCESSES##", "").replace("##ARCH_DELAY_CHANNEL##", delay_channel).replace("##PORTS##", ports).replace("##ARCH_SIGNALS##", signals)
                with open(os.path.join(gate_dir, name + ".vhd"), "w") as gate_file:
                    gate_file.write(content)

def find_pred_interconnect(structure, current_cell, input):
    for interconnect in structure.interconnects:
        if interconnect.to_instance == current_cell.instance and interconnect.to_port == input:
            return interconnect
    return None

def find_succ_interconnect(structure, current_cell, output):
    for interconnect in structure.interconnects:
        if interconnect.from_instance == current_cell.instance and interconnect.from_port == output:
            return interconnect
    return None

def estimate_pure_delay(cell):
    
    (pd_up_val, pd_up_unit) = parse_pure_delay(cell.pure_delay_up)
    (pd_down_val, pd_down_unit) = parse_pure_delay(cell.pure_delay_down)
    
    assert pd_up_unit == pd_down_unit
    
    pure_delay = max((pd_up_val + pd_down_val) / 2, 0.0)
    if pure_delay == 0:
        return "1 fs" # We need to be strictly > 0, otherwise we are not causal any more
    else:
        return build_pure_delay_string(pure_delay, pd_up_unit)

def set_delta(cell):    
    (pd_up_val, pd_up_unit) = parse_pure_delay(cell.pure_delay_up)
    (pd_down_val, pd_down_unit) = parse_pure_delay(cell.pure_delay_down)
    (pd_val, pd_unit) = parse_pure_delay(cell.pure_delay)

    assert(pd_up_unit == pd_down_unit)
    assert(pd_down_unit == pd_unit)

    cell.delta_plus = build_pure_delay_string(pd_up_val - pd_val, pd_up_unit)
    cell.delta_minus = build_pure_delay_string(pd_down_val - pd_val, pd_down_unit)

def build_pure_delay_code(func, pure_delay_up, pure_delay_down, current_input, all_inputs):
    (pd_up_val, pd_up_unit) = parse_pure_delay(pure_delay_up)
    (pd_down_val, pd_down_unit) = parse_pure_delay(pure_delay_down)
    
    code = ""

    if func.lower() == "not":
        code = ("if tt_level = '1' then" + "\n" + 
		"\t\t\t\tpure_delay := " + build_pure_delay_string(pd_down_val, pd_down_unit)	+ ";\n" + 			
        "\t\t\telse" + "\n" +
		"\t\t\t\tpure_delay := " + build_pure_delay_string(pd_up_val, pd_up_unit)	+ ";\n" + 
		"\t\t\tend if;")
    elif func.lower() == "":
        # Buffer
        code = ("if tt_level = '1' then" + "\n" + 
		"\t\t\t\tpure_delay := " + build_pure_delay_string(pd_up_val, pd_up_unit)	+ ";\n" + 			
        "\t\t\telse" + "\n" +
		"\t\t\t\tpure_delay := " + build_pure_delay_string(pd_down_val, pd_down_unit)	+ ";\n" + 
		"\t\t\tend if;")
    elif func.lower() == "nand" and len(all_inputs) == 2:
        # current_input = 
        if(all_inputs[0] == current_input):
            other_input = all_inputs[1]
        else:
            other_input = all_inputs[0]

        # We only use \ddomin when we can get a falling transition on the output
        # Otherwise, we use \dupmin.
        # Note that this is still not an optimal solution, since it does not consider the Charlie effect for example.
        # Another thing is how to delay an input, if it would cause no transition after the gate, for example
        # if one input is 0, and the other one toggles? The output still remains the same (1).
        code = ("if tt_level = '1' and " + other_input + " = '1' then" + "\n" + 
		"\t\t\t\tpure_delay := " + build_pure_delay_string(pd_down_val, pd_down_unit)	+ ";\n" + 			
        "\t\t\telse" + "\n" +
		"\t\t\t\tpure_delay := " + build_pure_delay_string(pd_up_val, pd_up_unit)	+ ";\n" + 
		"\t\t\tend if;")
    else:
        assert pd_up_unit == pd_down_unit and pd_up_val == pd_down_val
        my_print("No special pure delay calculation implemented for " + func + ". Either implement how you want to handle the specific function, or use equal pure delays!", EscCodes.WARNING)
        code = "pure_delay := " + build_pure_delay_string(pd_up_val, pd_up_unit) + ";"
    return code

def build_pure_delay_string(val, unit):
    return str(val) + " " + unit

def average_pure_delay(pure_delay_up, pure_delay_down):    
    (pd_up_val, pd_up_unit) = parse_pure_delay(pure_delay_up)
    (pd_down_val, pd_down_unit) = parse_pure_delay(pure_delay_down)

    return str((pd_up_val + pd_down_val) / 2) + " " + pd_up_unit



def parse_pure_delay(pure_delay_str):
    pure_delay_regex = r"(.*)\s+(.?s)"
    matches = re.finditer(pure_delay_regex, pure_delay_str, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):            
        return (float(match.group(1)), match.group(2))


def generate_multiinput_delay_strings(gate, output, delay_up, delay_down):
    d_down = "("
    d_up = "("
    for input in gate.inputs[:-1]:
        d_down += "tpd_" + input + "_" + output + "(" + delay_down + ") + "
        d_up += "tpd_" + input + "_" + output + "(" + delay_up + ") + "
    d_down += "tpd_" + gate.inputs[-1] + "_" + output + \
        "(" + delay_down + "))/" + str(len(gate.inputs))
    d_up += "tpd_" + gate.inputs[-1] + "_" + output + \
        "(" + delay_up + "))/" + str(len(gate.inputs))
    return (d_up, d_down)


if __name__ == "__main__":
    main()
