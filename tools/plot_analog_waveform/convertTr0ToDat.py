"""
    
	Involution Tool
	File: convertTr0ToDat.py
	
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
import matplotlib.pyplot as plt
import json
import sys
import os
import numpy as np
sys.path.append('../../experiment_setup/python')
from readHSPICE import *
from helper import *
from generateSwitchingWaveform import *


def main():
    if len(sys.argv) == 8:
        convert_tr0_to_dat(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    else:
        # python convertTr0ToDat.py inv_t4_d002000000.tr0 f_real_up.dat 5 0 4 100 1.2
        my_print("usage: python convertTr0ToDat.py tr0_file_path output_folder_path var_count time_idx frsw_idx time_divider voltage_divider", EscCodes.FAIL)
        sys.exit(1)

def convert_tr0_to_dat(tr0_file_path, output_folder_path, var_count, time_idx, frsw_idx, time_divider, voltage_divider):
    result = read_hspice(tr0_file_path, int(var_count))
    x_values = [float(x) / float(time_divider) for x in result[int(time_idx)]] 
    y_values = [float(y) / float(voltage_divider) for y in result[int(frsw_idx)]] 

    write_file(output_folder_path, "real", None, x_values, y_values)

if __name__ == "__main__":
    main()