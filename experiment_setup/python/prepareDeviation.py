"""
    
	Involution Tool
	File: prepareDeviation.py
	
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
from helper import *
from parserHelper import *

def main():
	# required_gates is optional, if not set, all gates are generated
	if len(sys.argv) != 2: 
		my_print("usage: python prepareDeviation.py results_file", EscCodes.FAIL)
	else:
		prepare_deviation(sys.argv[1])	
	
def prepare_deviation(results_file):	
	results = read_results(results_file)

	deviation_dict = dict()
	
	for ref in ["spice", "column"]:
		for delay_model in ["SPICE", "MODELSIM", "INVOLUTION"]:
			if ref == "column" and delay_model == "spice":
				continue
				
			for sim_type in ["DC", "PT_AVG", "PT_TIM"]:			
				# get the reference_value			
				reference_value = 0;
				actual_value = 0;
				if ref == "spice":
					reference_value = float(results["SPICEpwr_avg"])
				elif ref == "column":
					if sim_type == "DC":
						reference_value = float(results["SPICE_" + sim_type + "Total_Total"])
					else:
						reference_value = float(results["SPICE_" + sim_type + "_total power"])
							
				# get the actual_value			
				if sim_type == "DC":
					actual_value = float(results[delay_model + "_" + sim_type + "Total_Total"]);
				else:
					actual_value = float(results[delay_model + "_" + sim_type + "_total power"]);
								
				# Changed deviation calculation (according to https://en.wikipedia.org/wiki/Relative_change_and_difference#Percent_error)  
				# see section Percent Error
				# for old results (<= 28.02.2018 16.00, the sign of the value has to be changed)
				# deviation_dict["avgperspice" + ref + delay_model + sim_type] = ((reference_value - actual_value) / reference_value) * 100
				deviation_dict["avgperspice" + ref + delay_model + sim_type] = ((actual_value - reference_value) / reference_value) * 100
				
				
	extend_results(results_file, deviation_dict)
		
		
if __name__ == "__main__":
    main()