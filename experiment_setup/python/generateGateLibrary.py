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

VDD_def=0.8
VTH_def=0.4

def main():
	# required_gates is optional, if not set, all gates are generated
        if len(sys.argv) == 4: 
                generate_library(sys.argv[1], sys.argv[2], sys.argv[3], None)	
	elif len(sys.argv) == 5: 
		generate_library(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])	
	else:
		my_print("usage: python generateGateLibrary.py out_file gate_template_file global_config_file [circuit_config_file]", EscCodes.FAIL)
		sys.exit(1)
		
		
		
def generate_library(out_file, gate_template_file, default_config_file, circuit_config_file):

	gates = read_gate_config(default_config_file, circuit_config_file)
				
	# read template for gate
	gate_template = ""
	with open(gate_template_file, 'r') as template_file:		
		gate_template = template_file.read()
	
	generate_all = True
	content = ""
      
        VDD = os.environ['VDD'] if os.environ.get('VDD') == True else VDD_def;
        VTH = os.environ['VTH'] if os.environ.get('VTH') == True else VTH_def;
        
	# now that we have all the gates we want to create --> create them
	for name, gate in gates.items():	
		if not generate_all and name not in required_gates:
			my_print("Ignoring: " + name) 
			continue # we do not want to generate all gates, if not necessary for the circuit
	
		if len(gate.inputs) == 0:
			my_print("Error at gate: " + name + ". No input defined!", EscCodes.FAIL)
			continue
			
		if len(gate.outputs) != 1:
			my_print("Error at gate: " + name + ". Only one output supported yet!", EscCodes.FAIL)
			continue			

                content += "\n\n\n\n--------------------------------------------\n-- " + name + "\n"
                
                arch_postfix = ""
                function = ""
                output = gate.outputs[0]
                signals = ""
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

                if gate.channel_location == ChannelLocation.INPUT or gate.channel_location == ChannelLocation.INPUT_SWAPPED:
                        my_print("Before")
                        arch_postfix = "_before"

                        function = output + " <= "

                        for input in gate.inputs:
                                function_input_list.append(input + "_del")

                        for input in gate.inputs:
                                signal_list.append(input + "_del")

                        for input in gate.inputs:
                                delay_channel_list.append((input, input + "_del"))

                if gate.channel_location == ChannelLocation.OUTPUT or gate.channel_location == ChannelLocation.OUTPUT_SWAPPED:
                        arch_postfix = "_after"				
                        function = output + "_pre <= "
                        function_input_list = gate.inputs

                        for out in gate.outputs:
                                signal_list.append(out + "_pre")

                        for out in gate.outputs:
                                delay_channel_list.append((out + "_pre", out))

                if len(function_input_list) == 1:
                        function += gate.function + " " + function_input_list[0]
                else:					
                        for input in function_input_list[:-1]:
                                function += input + " " + gate.function + " "
                        function += function_input_list[-1]
                function += ";"	

                for input in gate.inputs:
                        ports += input + " : IN STD_ULOGIC := 'X';\n\t\t"

                for output in gate.outputs:
                        ports += output + " : OUT STD_ULOGIC := 'U';\n\t\t"

                ports = ports[:-4]

                for sig in signal_list:
                        signals += "SIGNAL " + sig + " : STD_ULOGIC := 'X';"
                        signals += "\n\t"

                for elem in entity_generic_list:
                        entity_generic += "tipd_" + elem + " : VitalDelayType01 := (0.0 ns, 0.0 ns);\n\t\t"
                        for out in gate.outputs:
                                entity_generic += "tpd_" + elem + "_" + output + " : VitalDelayType01Z := (OTHERS => 0.0 ns);\n\t\t"

                for channel in delay_channel_list:
                        d_up = ""
                        d_down = ""
                        if gate.channel_location == ChannelLocation.INPUT or gate.channel_location == ChannelLocation.INPUT_SWAPPED:
                                delay_up = "tr01"
                                delay_down = "tr10"
                                if gate.channel_location == ChannelLocation.INPUT_SWAPPED:
                                        delay_up = "tr10"
                                        delay_down = "tr01"

                                d_up = "tpd_" + channel[0] + "_" + output + "(" + delay_up +")"
                                d_down = "tpd_" + channel[0] + "_" + output + "(" + delay_down + ")"
                        if gate.channel_location == ChannelLocation.OUTPUT or gate.channel_location == ChannelLocation.OUTPUT_SWAPPED:
                                delay_up = "tr01"
                                delay_down = "tr10"
                                if gate.channel_location == ChannelLocation.OUTPUT_SWAPPED:
                                        delay_up = "tr10"
                                        delay_down = "tr01"

                                d_down = "("
                                d_up = "("
                                for input in gate.inputs[:-1]:
                                        d_down += "tpd_" + input + "_" + output + "(" + delay_down + ") + "
                                        d_up += "tpd_" + input + "_" + output + "(" + delay_up + ") + "
                                d_down += "tpd_" + gate.inputs[-1] + "_" + output + "(" + delay_down + "))/" + str(len(gate.inputs))
                                d_up += "tpd_" + gate.inputs[-1] + "_" + output + "(" + delay_up + "))/" + str(len(gate.inputs))

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
                                my_print("Unkown channel type: " + str(gate.channel_type), EscCodes.FAIL)

                        channel_parameters = ""
                        gate_specific_parameters = ""
                        for param_key, param_value in gate.channel_parameters.iteritems():
                                channel_parameters += ",\n\t\t" + str(param_key) + " => " + str(param_value)

                        delay_channel += ("" + 
                                "delay_" + channel[0] + " : " + channel_name + "\n"
                                "\tgeneric map(\n" + 
                                "\t\tD_UP => "+ d_up +",\n" +
                                "\t\tD_DO => " + d_down + ",\n" + 
                                "\t\tT_P => " + str(gate.T_P) + " ps" + channel_parameters + ",\n" + 
                                "\t\tV_DD => " + str(VDD) + ",\n" + 
                                "\t\tV_TH => " + str(VTH) + ")\n" + 
                                "\tport map(\n" + 
                                "\t\tinput => " + channel[0] + ",\n" +
                                "\t\toutput => " + channel[1] + ");\n" +
                                "\n\t")



                arch_name = gate.channel_type + '_'+ gate.channel_location

                content += gate_template.replace("##ENTITY_NAME##", gate.entity_name).replace("##ARCH_NAME##", arch_name).replace("##ARCH_FUNCTION##", function).replace("##ARCH_SIGNALS##", signals).replace("##ENTITY_GENERIC##", entity_generic).replace("##ARCH_DELAY_CHANNEL##", delay_channel).replace("##PORTS##", ports).replace("##GATE_SPECIFIC_PARAMETERS##", gate_specific_parameters)

	with open(out_file, "w") as gate_file:                
                gate_file.write(content)
		
	
if __name__ == "__main__":
    main()
