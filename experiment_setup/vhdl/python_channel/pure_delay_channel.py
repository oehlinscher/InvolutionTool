"""
    
	Involution Tool
	File: pure_delay_channel.py
	
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

sys.path.append('vhdl/python_channel')
from python_channel_base import std_logic_t

def pure_delay_channel_idm(input_level, d_up, d_do, t_p, t_p_percent, t_p_mode, v_dd, v_th, now, last_output_time, first_transition, channel_parameters_dict):
    delay = 0
    if input_level == std_logic_t.STD_LOGIC_1:
        delay = d_up
    elif input_level == std_logic_t.STD_LOGIC_0:
        delay = d_do
    else:
        assert(False)

    return (delay, now + delay, 0)