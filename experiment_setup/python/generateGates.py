"""
    
	Involution Tool
	File: generateGates.py
	
    Copyright (C) 2018-2021  Daniel OEHLINGER <d.oehlinger@outlook.com>

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
from readGateCfg import read_gate_config, ChannelLocation, ImplementationType, ChannelType
from helper import my_print, EscCodes, to_bool
from extractCircuitStructure import read_circuit_structure, CircuitStructure


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
    else:
        # This case is obsolete, we do not want to maintain this option any more.
        # Simply switch to GIDM or to generate_gate_per_instance
        # There is no function reduction, only a little performance sacrifice
        my_print("Gate generation configuration not supported any more!", EscCodes.FAIL)

    # now that we have all the gates we want to create --> create them
    for name, gate in gates.items():
        if not check_gate_creation(generate_all, name, required_gates, gate):
            continue

        output = gate.outputs[0]

        function, function_input_list, delay_channel_list, signal_list = build_function(use_gidm, gate, output)

        entity_generic = build_entity_generic(gate)

        channel, d_up, d_down = build_channel_parameters(delay_channel_list, gate, output, use_gidm)

        arch_name = build_arch_name(use_gidm, gate)

        # Replace stuff that is independent of GIDM / IDM, and the ImplementationType
        content = gate_template.replace("##ARCH_NAME##", arch_name).replace("##ARCH_FUNCTION##", function).replace(
            "##ENTITY_GENERIC##", entity_generic).replace("##GATE_SPECIFIC_PARAMETERS##", "")

        if use_gidm:
            generate_gate_gidm(gate, content, structure, name, channel, gate_dir, gate_input_process_template, tt_file_path, function_input_list, output, vectors_dir_file_path)
        else:
            generate_gate_idm(gate, content, structure, name, channel, gate_dir, d_up, d_down, signal_list, generate_all, required_gates)
   
def check_gate_creation(generate_all, name, required_gates, gate):
    if not generate_all and name not in required_gates:
        my_print("Ignoring: " + name)
        return False  # we do not want to generate all gates, if not necessary for the circuit

    if len(gate.inputs) == 0:
        my_print("Error at gate: " + name +
                    ". No input defined!", EscCodes.FAIL)
        return False

    if len(gate.outputs) != 1:
        my_print("Error at gate: " + name +
                    ". Only one output supported yet!", EscCodes.FAIL)
        return False
    
    return True

def build_function(use_gidm, gate, output):
    signal_list = list()    
    delay_channel_list = list()
    function_input_list = list()
    function = ""

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

    return function, function_input_list, delay_channel_list, signal_list

def build_channel_parameters(delay_channel_list, gate, output, use_gidm):
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

    return channel, d_up, d_down

def build_channel_name(gate, use_gidm):
    channel_name = ""
    if gate.channel_type == ChannelType.EXP_CHANNEL:
        channel_name = "exp_channel"
    elif gate.channel_type == ChannelType.HILL_CHANNEL:
        channel_name = "hill_channel"
    elif gate.channel_type == ChannelType.SUMEXP_CHANNEL:
        channel_name = "sumexp_channel"
    elif gate.channel_type == ChannelType.PUREDELAY_CHANNEL:
        channel_name = "puredelay_channel"
    elif gate.channel_type == ChannelType.HYBRID_CHANNEL:
        channel_name = "hybrid_channel"
    else:
        my_print("Unkown channel type: " +
                    str(gate.channel_type), EscCodes.FAIL)

    if use_gidm:
        channel_name = "gidm_" + channel_name

    return channel_name.lower()

def merge_channel_parameters(gate_channel_parameters, cell):
    if hasattr(cell, 'channel_params'):
        gate_channel_parameters.update(cell.channel_params)
    return gate_channel_parameters

def build_channel_parameters_vhdl(channel_parameters):
    channel_parameters_str = ""
    for param_key, param_value in channel_parameters.items():
        channel_parameters_str += "{param} => {value},\n\t\t\t\t".format(param=param_key, value=param_value)

    return channel_parameters_str


def build_channel_parameters_python(channel_parameters):
    channel_parameters_str = ", {count}".format(count = len(channel_parameters))
    # Needs to be in a sorted order, otherwise we have a hard time of parsing the variadic arguments in c
    for _, param_value in sorted(channel_parameters.items()):
        channel_parameters_str += ", {value}".format(value = param_value)

    return channel_parameters_str



def build_entity_generic(gate):
    entity_generic = ""

    for elem in gate.inputs:
        entity_generic += "tipd_" + elem + " : VitalDelayType01 := (0.0 ns, 0.0 ns);\n\t\t"

        for out in gate.outputs:
            entity_generic += "tpd_" + elem + "_" + out + " : VitalDelayType01Z := (OTHERS => 0.0 ns);\n\t\t"
    
    return entity_generic
    

def build_arch_name(use_gidm, gate):
    if use_gidm:
        arch_name = "{channel_type}_GIDM".format(channel_type = gate.channel_type)
    else:
        arch_name = "{channel_type}_{channel_location}".format(channel_type = gate.channel_type, channel_location = gate.channel_location)
    return arch_name

def generate_gate_gidm(gate, content, structure, name, channel, gate_dir, gate_input_process_template, tt_file_path, function_input_list, output, vectors_dir_file_path):
    # For GIDM, we need to initialize both, the input and output ports with 0, because that is how the toggle indicator is initialized
    ports = ""
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
                input_processes += "\n\n" + gate_input_process_template.replace("##INPUT##", input)
                # For the tt_file path, we need to look who is our predecessor
                pred_interconnect = find_pred_interconnect(structure, cell, input)
                assert (pred_interconnect is not None)
                tt_file = tt_file_path + "/" + pred_interconnect.from_instance + pred_interconnect.from_port
                input_processes = input_processes.replace(
                    "##TT_FILE##", tt_file)

                pure_delay_code = build_pure_delay_code(gate.function, cell.delta_plus, cell.delta_minus, input + "AfterDelta", function_input_list)

                input_processes = input_processes.replace("##PURE_DELAY_CALC##", pure_delay_code)

            # Iterate over all the interconnects
            # which are after this gate instance
            # + one delay channel used for comparison

            # Sum up the input delays
            # TODO: Find a better way, once the theory how to do is is clear
            (d_up, d_down) = generate_multiinput_delay_strings(gate, output, "tr01", "tr10")

            succ_interconnect = find_succ_interconnect(structure, cell, gate.outputs[0])	
            assert succ_interconnect is not None

            # This is now the process for the output which we use for comparison
            tt_file = tt_file_path + "/" + succ_interconnect.from_instance + succ_interconnect.from_port
            
            delay_channel = ""
            channel_parameters = merge_channel_parameters(gate.channel_parameters, cell)
            if gate.implementation_type == ImplementationType.VHDL:               
                channel_parameters = build_channel_parameters_vhdl(channel_parameters)
                delay_channel = build_delay_channel_string_vhdl_gidm(gate, d_up, d_down, cell, channel[0], channel_parameters, tt_file)
            elif gate.implementation_type == ImplementationType.PYTHON:
                channel_parameters = build_channel_parameters_python(channel_parameters)
                delay_channel = build_delay_channel_string_python(gate, d_up, d_down, cell, channel[0], output, channel_parameters, True, tt_file=tt_file)
            else:
                assert(False)

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

def build_idm_signals(structure, cell, signal_list, init_value_out):           

    signals = ""
    for sig in signal_list:
        signals += "SIGNAL " + sig + " : STD_ULOGIC := '" + init_value_out + "';" 
        signals += "\n\t"

    return signals

def generate_gate_idm(gate, content, structure, name, channel, gate_dir, d_up, d_down, signal_list, generate_all, required_gates):
    for cell in structure.cells: 
        # First we need to check if this is one of the cells we need to generate  
        if cell.cell_type != gate.entity_name:
            continue

        # Correct initialization only implement for this ChannelLocation, other ChannelLocations are not really used any more, since they do not correspond to the model
        assert gate.channel_location == ChannelLocation.OUTPUT

        # For channel location OUTPUT, this is basically one signal, which is the value after the gate output. This needs to be set according to the init value
        assert(len(signal_list) == 1)
        
        init_value_out = "0" # We simply fix the init value to 0. If specified, we overwrite this value. 
        if cell.instance in structure.init:
            init_value_out = structure.init[cell.instance]            

        signals = build_idm_signals(structure, cell, signal_list, init_value_out)

        ports = ""
        for input in gate.inputs:

            # For IDM, we need to initialize both, the input and output ports with 0, because that is how the toggle indicator is initialized                          
            init_value_in = "0"                      
            pred_interconnect = find_pred_interconnect(structure, cell, input)

            if pred_interconnect is None:
                my_print("Cell: {cell}, Input: {input}".format(cell = cell, input = input), EscCodes.FAIL)
                assert(False)

            if pred_interconnect.from_instance in structure.init:
                init_value_in = structure.init[pred_interconnect.from_instance]

            ports += input + " : IN STD_ULOGIC := '" + init_value_in + "';\n\t\t"

        # The output is set to our init value (if specified)
        init_value = "0"
        if cell.instance in structure.init:
            init_value = structure.init[cell.instance]
        for out in gate.outputs:
            ports += out + " : OUT STD_ULOGIC := '" + init_value + "';\n\t\t"

        ports = ports[:-4]

        delay_channel = build_delay_channel_idm(gate, channel[0], channel[1], d_up, d_down, cell, init_value_out)


        content_repl = content.replace("##ENTITY_NAME##", gate.entity_name + "_" + cell.instance).replace(
            "##ARCH_INPUT_PROCESSES##", "").replace("##ARCH_DELAY_CHANNEL##", delay_channel).replace("##PORTS##", ports).replace("##ARCH_SIGNALS##", signals)
        with open(os.path.join(gate_dir, name + "_" + cell.instance + ".vhd"), "w") as gate_file:
            gate_file.write(content_repl)

def build_delay_channel_idm(gate, input, output, d_up, d_down, cell, init_value_out):
    delay_channel = ""
    
    channel_parameters = merge_channel_parameters(gate.channel_parameters, cell)

    if gate.implementation_type == ImplementationType.VHDL:
        channel_parameters = build_channel_parameters_vhdl(channel_parameters)
        delay_channel = build_delay_channel_string_vhdl_idm(gate, d_up, d_down, cell, input, output, channel_parameters, init_value_out)
    elif gate.implementation_type == ImplementationType.PYTHON:
        channel_parameters = build_channel_parameters_python(channel_parameters)
        delay_channel = build_delay_channel_string_python(gate, d_up, d_down, cell, input, output, channel_parameters, False)
    else:
        my_print("Unexpected implementation type: " + gate.implementation_type, EscCodes.FAIL)

    return delay_channel


def build_delay_channel_string_vhdl_gidm(gate, d_up, d_down, cell, input, channel_parameters, tt_file):
    delay_channel = """
        delay_{input} : {channel_name}
        generic map(
            D_INF_UP => {d_up},
            D_INF_DO => {d_do},
            V_DD => {v_dd},
            V_TH => {v_th},
            {channel_parameters}
            D_MIN => {d_min},
            DELTA_PLUS => {delta_plus},
            DELTA_MINUS => {delta_minus},
            TRANSITION_TIME_FILE_PATH => "{tt_file}"
        )
        port map(
            input => {input},
            output => {output}
        );
    """.format(
        channel_name = build_channel_name(gate, True),         
        d_up = d_up, 
        d_do = d_down, 
        d_min = cell.pure_delay, 
        v_dd = os.environ['VDD'], 
        v_th = os.environ['VTH'], 
        delta_plus = cell.delta_plus,
        delta_minus = cell.delta_minus,
        tt_file = tt_file,
        input = input,
        output = gate.outputs[0],
        channel_parameters = channel_parameters
    )
    return delay_channel


def build_delay_channel_string_vhdl_idm(gate, d_up, d_down, cell, input, output, channel_parameters, init_value):
    delay_channel = """
        delay_{input} : {channel_name}
        generic map(
            D_UP => {d_up},
            D_DO => {d_do},
            T_P => {t_p},
            T_P_PERCENT => {t_p_percent},
            T_P_MODE => {t_p_mode},
            {channel_parameters}
            V_DD => {v_dd},
            V_TH => {v_th},
            INIT_VALUE => '{init_value}'
        )
        port map(
            input => {input},
            output => {output}
        );
    """.format(    
        channel_name = build_channel_name(gate, False),         
        d_up = d_up, 
        d_do = d_down, 
        t_p = cell.pure_delay, 
        t_p_percent = gate.T_P_percent, 
        t_p_mode = gate.T_P_mode, 
        v_dd = os.environ['VDD'], 
        v_th = os.environ['VTH'], 
        input = input, 
        output = output,
        channel_parameters = channel_parameters,
        init_value = init_value)
    return delay_channel

def build_delay_channel_string_python(gate, d_up, d_down, cell, input, output, channel_parameters, use_gidm, tt_file = None):        
    delay_channel = ""
    if gate.channel_type == ChannelType.HYBRID_CHANNEL:
        assert(len(gate.inputs) == 2) # Currently only 2-input gates supported

        process_variables = """        
            VARIABLE delay : time := 0 sec;
            VARIABLE input_1_old : std_logic := '0';
            VARIABLE input_2_old : std_logic := '0';
            VARIABLE last_input_switch_time : time := 0 sec;
            VARIABLE v_int : real := 0.0;
            VARIABLE v_out : real := 0.0;
            VARIABLE delay_valid : bit;

            -- Slowdown detection variables
            VARIABLE last_transition_level : std_logic := '0';
            VARIABLE last_transition_time : time := 0 sec;

            VARIABLE transition_level : std_logic := '0';
            VARIABLE transition_time : time := 0 sec;

            VARIABLE first_transition : bit := '1';


        """.format()

        process = """
            input_1_old := {input_1};
            input_2_old := {input_2};

            IF (delay < 0 fs) THEN
                report "Delay smaller 0 fs, this should not happen in the hybrid model";
                delay := 0 fs;
            END IF;

            -- report "delay: "  & time'IMAGE(delay) & ", delay_valid: " & bit'IMAGE(delay_valid);

            
            transition_level := {input_1} {gate_function} {input_2};

            IF last_transition_level /= transition_level and delay_valid = '0' THEN
                -- Check if the previous transition was able to cross the threshold
                report "Need to cancel previous transition";
                {output} <= TRANSPORT not last_transition_level AFTER last_transition_time - now;    
            END IF;


            IF delay_valid = '1' THEN
                
                -- Cancellation in case of delay slowdown
                IF first_transition = '0' and last_transition_time < now + delay and last_transition_level = transition_level THEN                
                    -- We have the same transition level twice in a row, and the second transition is after the first one (slow down).
                    -- Therefore we need to cancel the first one and schedule the seconde one
                    report "Slowdown. last_transition_time: " & time'IMAGE(last_transition_time) & ", last_transition_level: " & std_logic'IMAGE(last_transition_level) & ", transition_level: " & std_logic'IMAGE(transition_level);
                    {output} <= TRANSPORT not last_transition_level AFTER last_transition_time - now;                    
                END IF;

                {output} <= TRANSPORT transition_level AFTER delay;

                last_transition_time := now + delay;
            END IF;

            last_transition_level := transition_level;
            first_transition := '0';
        """.format(
            gate_function = gate.function,
            input_1 = gate.inputs[0],
            input_2 = gate.inputs[1],
            output = output
        )

        procedure_call = """calculate_delay_hybrid_2in("{gate_function}", input_1_old, input_2_old, {input_1}, {input_2}, {r_1:.10E}, {r_2:.10E}, {r_3:.10E}, {r_4:.10E}, {c_int:.10E}, {c_out:.10E}, {scale_1:.10E}, {pure_delay}, {v_dd}, {v_th}, now, first_transition, last_input_switch_time, v_int, v_out, delay, delay_valid);""".format(
            gate_function = gate.function, 
            v_dd = os.environ['VDD'], 
            v_th = os.environ['VTH'], 
            r_1 = cell.hybrid_channel_params["r_1"],
            r_2 = cell.hybrid_channel_params["r_2"], 
            r_3 = cell.hybrid_channel_params["r_3"], 
            r_4 = cell.hybrid_channel_params["r_4"], 
            c_int = cell.hybrid_channel_params["c_int"], 
            c_out = cell.hybrid_channel_params["c_out"],
            scale_1 = cell.hybrid_channel_params["scale_1"],
            pure_delay = cell.hybrid_channel_params["pure_delay"],
            input_1 = gate.inputs[0],
            input_2 = gate.inputs[1],
        );     


        delay_channel = """
        channel_process: PROCESS ({input_1}, {input_2})
            {process_variables}
        BEGIN
            IF ({input_1}'EVENT and ({input_1} = '1' OR {input_1} = '0')) OR ({input_2}'EVENT and ({input_2} = '1' OR {input_2} = '0')) THEN
                {procedure_call}       
                {process}
            END IF;
        END PROCESS;
        """.format(
            input_1 = gate.inputs[0], 
            input_2 = gate.inputs[1], 
            process = process,
            process_variables = process_variables,
            procedure_call = procedure_call            
        )
    else: 
        idm_process = ""
        gidm_process = ""
        idm_process_variables = ""
        gidm_process_variables = ""     

        procedure_call = ""

        if use_gidm:        
            gidm_process_variables = """        
                FILE tt_file : text;
                VARIABLE tt_line : line;
                VARIABLE tt_level : std_logic;
            """

            procedure_call = """calculate_delay_gidm("{channel_type}", {input}, {d_up}, {d_do}, {v_dd}, {v_th}, {d_min}, {delta_plus}, {delta_minus}, now, last_output_time, first_transition, delay{channel_parameters});""".format(
                channel_type = build_channel_name(gate, use_gidm), 
                input = input, 
                d_up = d_up, 
                d_do = d_down,             
                v_dd = os.environ['VDD'], 
                v_th = os.environ['VTH'], 
                d_min = cell.pure_delay,
                delta_plus = cell.delta_plus,
                delta_minus = cell.delta_minus, 
                channel_parameters = channel_parameters
            );     

            gidm_process = """            
                IF {input} = '1' THEN
                    tt_level := '1';
                ELSE
                    tt_level := '0';
                END IF;

                write(tt_line, integer'image(integer((now + delay) / 1 fs)));
                write(tt_line, string'(" "));
                write(tt_line, std_logic'image(tt_level));
                file_open(tt_file, "{tt_file}", WRITE_MODE);
                writeline(tt_file, tt_line);
                file_close(tt_file);	

                write(tt_line, integer'image(integer((now + delay) / 1 fs)));
                write(tt_line, string'(" "));
                write(tt_line, std_logic'image(tt_level));
                file_open(tt_file, "{tt_file}.complete", APPEND_MODE);
                writeline(tt_file, tt_line);
                file_close(tt_file);	

                {output} <= not {output};
            """.format(
                input = input,
                tt_file = tt_file,
                output = output
            )
        else:
            idm_process = """
                IF (delay < 0 fs) THEN
                    delay := 0 fs;
                END IF;

                IF {input} = '1' THEN
                    {output} <= TRANSPORT '1' AFTER delay;
                ELSE
                    {output} <= TRANSPORT '0' AFTER delay;
                END IF;
            """.format(
                input = input,
                output = output
            )

            procedure_call = """calculate_delay_idm("{channel_type}", {input}, {d_up}, {d_do}, {t_p}, {t_p_percent}, {t_p_mode}, {v_dd}, {v_th}, now, last_output_time, first_transition, delay{channel_parameters});""".format(
                channel_type = build_channel_name(gate, use_gidm), 
                input = input, 
                d_up = d_up, 
                d_do = d_down, 
                t_p = cell.pure_delay, 
                t_p_percent = gate.T_P_percent, 
                t_p_mode = gate.T_P_mode, 
                v_dd = os.environ['VDD'], 
                v_th = os.environ['VTH'], 
                channel_parameters = channel_parameters
            );     


        delay_channel = """
        channel_process: PROCESS ({input})
            VARIABLE last_output_time : time := -1 sec;
            VARIABLE delay : time := 10 ps;
            VARIABLE first_transition : bit := '1';
            -- VARIABLE prev_last_output_time : time;
            {idm_process_variables}
            {gidm_process_variables}
        BEGIN
            IF {input}'EVENT and ({input} = '1' OR {input} = '0') THEN
                --prev_last_output_time := last_output_time;
                {procedure_call}       
                -- report "level: " & std_logic'IMAGE({input}) & ", input transition at: " & time'IMAGE(now) & ", last_output_time: " & time'IMAGE(prev_last_output_time) & ",  delay " & time'IMAGE(delay) & ", d_up: " & time'IMAGE({d_up}) & ", d_do: " & time'IMAGE({d_do});	
                
                {idm_process}
                {gidm_process}
            END IF;
        END PROCESS;
        """.format(
            d_up = d_up, 
            d_do = d_down, 
            input = input, 
            idm_process = idm_process,
            gidm_process = gidm_process,
            idm_process_variables = idm_process_variables,
            gidm_process_variables = gidm_process_variables,
            procedure_call = procedure_call            
        )

    return delay_channel


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
        return "0.001 ps" # We need to be strictly > 0, otherwise we are not causal any more
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
    for _, match in enumerate(matches, start=1):            
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
