"""
    
	Involution Tool
	File: python_channel_base.py
	
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

from enum import Enum

# Set to true, if you want to ensure to get the same results as with the VHDL implementation
# Results are more accurate when not using rounding
# Only useful for EXP_CHANNEL implementation (and HILL_CHANNEL), 
# since there we do not need to incorporate fsolve and can calculate everything exactly
round_results = False

class std_logic_t(Enum):
    STD_LOGIC_U = 0
    STD_LOGIC_X = 1
    STD_LOGIC_0 = 2
    STD_LOGIC_1 = 3
    STD_LOGIC_Z = 4
    STD_LOGIC_W = 5
    STD_LOGIC_L = 6
    STD_LOGIC_H = 7
    STD_LOGIC_D = 8

class tp_mode(Enum):
    ABSOLUTE = 0
    PERCENT = 1
    

def calc_tp(t_p, t_p_percent, t_p_mode, d_inf):
    # print("Mode: ", t_p_mode)
    if t_p_mode == tp_mode.ABSOLUTE:
        return t_p
    elif t_p_mode == t_p_mode.PERCENT:
        return d_inf * t_p_percent
    else:
        assert(False)
        
def convert_fsolve_result(res):
    assert(len(res) == 1)
    return res[0]