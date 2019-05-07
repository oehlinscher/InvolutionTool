"""
    
	Involution Tool
	File: extractSdf.py
	
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
sys.path.append('../../experiment_setup/python')
from vcdParser import *

def main():		
	# TODO: Define timescale and matching dict for each circuit 
	# TODO: Scaling not properly working yet
	vcd_timescale = 1 # in femto seconds
	subsequent_transition_range = 1e6 / 2 # in femto seconds, use for example mu/2 from generate.json
	sdf_output_scale = 1e3 # in femto seconds
	
	warning_delay_change = 10
	
	matching_dict = dict()
	# (start, stop, rising, falling, nr_rising, nr_falling)
	
	# inv_tree (65nm)
	# matching_dict['g10'] = (['din', 'xmycir.g10:z', -1, -1, 0, 0])
	# matching_dict['g11'] = (['xmycir.g10:z', 'xmycir.g11:z', -1, -1, 0, 0])
	# matching_dict['g12'] = (['xmycir.g11:z', 'xmycir.g12:z', -1, -1, 0, 0])
	# matching_dict['g13'] = (['xmycir.g12:z', 'xmycir.g13:z', -1, -1, 0, 0])
	# matching_dict['g14'] = (['xmycir.g13:z', 'xmycir.g14:z', -1, -1, 0, 0])
	# matching_dict['g15'] = (['xmycir.g14:z', 'xmycir.g15:z', -1, -1, 0, 0])
	# matching_dict['g16'] = (['xmycir.g14:z', 'xmycir.g16:z', -1, -1, 0, 0])
	# matching_dict['g17'] = (['xmycir.g15:z', 'dout1', -1, -1, 0, 0])
	# matching_dict['g18'] = (['xmycir.g15:z', 'dout2', -1, -1, 0, 0])
	# matching_dict['g19'] = (['xmycir.g16:z', 'dout3', -1, -1, 0, 0])
	# matching_dict['g20'] = (['xmycir.g16:z', 'dout4', -1, -1, 0, 0])
	
	# inv_tree (15nm)
	matching_dict['g10'] = (['din', 'Xmycir.g10:ZN', -1, -1, 0, 0])
	matching_dict['g11'] = (['Xmycir.g10:ZN', 'Xmycir.g11:ZN', -1, -1, 0, 0])
	matching_dict['g12'] = (['Xmycir.g11:ZN', 'Xmycir.g12:ZN', -1, -1, 0, 0])
	matching_dict['g13'] = (['Xmycir.g12:ZN', 'Xmycir.g13:ZN', -1, -1, 0, 0])
	matching_dict['g14'] = (['Xmycir.g13:ZN', 'Xmycir.g14:ZN', -1, -1, 0, 0])
	matching_dict['g15'] = (['Xmycir.g14:ZN', 'Xmycir.g15:ZN', -1, -1, 0, 0])
	matching_dict['g16'] = (['Xmycir.g14:ZN', 'Xmycir.g16:ZN', -1, -1, 0, 0])
	matching_dict['g17'] = (['Xmycir.g15:ZN', 'dout1', -1, -1, 0, 0])
	matching_dict['g18'] = (['Xmycir.g15:ZN', 'dout2', -1, -1, 0, 0])
	matching_dict['g19'] = (['Xmycir.g16:ZN', 'dout3', -1, -1, 0, 0])
	matching_dict['g20'] = (['Xmycir.g16:ZN', 'dout4', -1, -1, 0, 0])
	
	# c17_slack (15nm)
	# matching_dict['inst_0 A'] = (['nx3', 'Xmycir.inst_0:ZN', -1, -1, 0, 0])
	# matching_dict['inst_0 B'] = (['nx6', 'Xmycir.inst_0:ZN', -1, -1, 0, 0])
	# matching_dict['inst_1 A'] = (['nx1', 'Xmycir.inst_1:ZN', -1, -1, 0, 0])
	# matching_dict['inst_1 B'] = (['nx3', 'Xmycir.inst_1:ZN', -1, -1, 0, 0])
	# matching_dict['inst_2 A'] = (['nx7', 'Xmycir.inst_2:ZN', -1, -1, 0, 0])
	# matching_dict['inst_2 B'] = (['Xmycir.inst_0:ZN', 'Xmycir.inst_2:ZN', -1, -1, 0, 0])
	# matching_dict['inst_3 A'] = (['nx2', 'Xmycir.inst_3:ZN', -1, -1, 0, 0])
	# matching_dict['inst_3 B'] = (['Xmycir.inst_0:ZN', 'Xmycir.inst_3:ZN', -1, -1, 0, 0])
	# matching_dict['inst_4 A'] = (['Xmycir.inst_3:ZN', 'nx23', -1, -1, 0, 0])
	# matching_dict['inst_4 B'] = (['Xmycir.inst_2:ZN', 'nx23', -1, -1, 0, 0])
	# matching_dict['inst_5 A'] = (['Xmycir.inst_1:ZN', 'nx22', -1, -1, 0, 0])
	# matching_dict['inst_5 B'] = (['Xmycir.inst_3:ZN', 'nx22', -1, -1, 0, 0])
	
	# mips_clock (15nm)
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_1'] = (['Xmycir.dp/FE_USKC131_CTS_210:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_1:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC168_CTS_248'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_12:ZN', 'Xmycir.dp/FE_USKC168_CTS_248:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L4_10'] = (['Xmycir.dp/rf/FE_USKC153_CTS_164:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_10:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC177_CTS_159'] = (['Xmycir.dp/rf/FE_USKC176_CTS_159:ZN', 'Xmycir.dp/rf/FE_USKC177_CTS_159:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC162_CTS_156'] = (['Xmycir.dp/rf/FE_USKC254_CTS_156:ZN', 'Xmycir.dp/rf/FE_USKC162_CTS_156:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L2_4'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L1_2:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L2_4:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L5_17'] = (['Xmycir.dp/rf/FE_USKC256_CTS_156:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_17:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC151_CTS_238'] = (['Xmycir.dp/FE_USKC250_CTS_238:ZN', 'Xmycir.dp/FE_USKC151_CTS_238:ZN', -1, -1, 0, 0])
	# matching_dict['dp/ir3/CTS_ccl_INV_clk_G0_L6_13'] = (['Xmycir.dp/ir3/CTS_ccl_INV_clk_G0_L5_7:ZN', 'Xmycir.dp/ir3/CTS_ccl_INV_clk_G0_L6_13:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L5_12'] = (['Xmycir.dp/rf/FE_USKC212_CTS_146:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_12:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC285_CTS_270'] = (['Xmycir.dp/FE_USKC284_CTS_270:ZN', 'Xmycir.dp/FE_USKC285_CTS_270:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L5_10'] = (['Xmycir.dp/rf/FE_USKC214_CTS_139:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_10:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC192_CTS_210'] = (['Xmycir.dp/FE_USKC191_CTS_210:ZN', 'Xmycir.dp/FE_USKC192_CTS_210:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC248_CTS_250'] = (['Xmycir.dp/FE_USKC247_CTS_250:ZN', 'Xmycir.dp/FE_USKC248_CTS_250:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC283_CTS_218'] = (['Xmycir.dp/FE_USKC282_CTS_218:ZN', 'Xmycir.dp/FE_USKC283_CTS_218:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC204_CTS_147'] = (['Xmycir.dp/rf/FE_USKC203_CTS_147:ZN', 'Xmycir.dp/rf/FE_USKC204_CTS_147:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC178_CTS_155'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_18:ZN', 'Xmycir.dp/rf/FE_USKC178_CTS_155:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_2'] = (['Xmycir.dp/FE_USKC131_CTS_210:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_2:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_2'] = (['Xmycir.dp/FE_USKC283_CTS_218:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_2:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC191_CTS_210'] = (['Xmycir.dp/FE_USKC130_CTS_210:ZN', 'Xmycir.dp/FE_USKC191_CTS_210:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L4_13'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L3_7:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_13:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L5_19'] = (['Xmycir.dp/rf/FE_USKC161_CTS_163:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_19:ZN', -1, -1, 0, 0])
	# matching_dict['CTS_ccl_INV_clk_G0_L4_4'] = (['Xmycir.CTS_ccl_INV_clk_G0_L3_2:ZN', 'Xmycir.CTS_ccl_INV_clk_G0_L4_4:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_59'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_30:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_59:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_58'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_29:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_58:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_19'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_10:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_19:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_53'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_27:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_53:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC153_CTS_164'] = (['Xmycir.dp/rf/FE_USKC152_CTS_164:ZN', 'Xmycir.dp/rf/FE_USKC153_CTS_164:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_57'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_29:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_57:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC290_CTS_217'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_2:ZN', 'Xmycir.dp/FE_USKC290_CTS_217:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_55'] = (['Xmycir.dp/FE_USKC141_CTS_259:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_55:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_54'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_27:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_54:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC179_CTS_155'] = (['Xmycir.dp/rf/FE_USKC178_CTS_155:ZN', 'Xmycir.dp/rf/FE_USKC179_CTS_155:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC207_CTS_139'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_5:ZN', 'Xmycir.dp/rf/FE_USKC207_CTS_139:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L2_3'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L1_2:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L2_3:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L2_2'] = (['Xmycir.CTS_ccl_INV_clk_G0_L1_1:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L2_2:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC254_CTS_156'] = (['Xmycir.dp/rf/FE_USKC253_CTS_156:ZN', 'Xmycir.dp/rf/FE_USKC254_CTS_156:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC159_CTS_237'] = (['Xmycir.dp/FE_USKC158_CTS_237:ZN', 'Xmycir.dp/FE_USKC159_CTS_237:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_8'] = (['Xmycir.dp/FE_USKC159_CTS_237:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_8:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_1'] = (['Xmycir.dp/FE_USKC283_CTS_218:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_1:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC246_CTS_270'] = (['Xmycir.dp/FE_USKC285_CTS_270:ZN', 'Xmycir.dp/FE_USKC246_CTS_270:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC181_CTS_152'] = (['Xmycir.dp/rf/FE_USKC180_CTS_152:ZN', 'Xmycir.dp/rf/FE_USKC181_CTS_152:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L5_11'] = (['Xmycir.dp/rf/FE_USKC212_CTS_146:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_11:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC132_CTS_250'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L2_3:ZN', 'Xmycir.dp/FE_USKC132_CTS_250:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_7'] = (['Xmycir.dp/FE_USKC159_CTS_237:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_7:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_3'] = (['Xmycir.CTS_ccl_INV_clk_G0_L3_2:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_3:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L4_5'] = (['Xmycir.dp/rf/FE_USKC204_CTS_147:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_5:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC134_CTS_270'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L2_4:ZN', 'Xmycir.dp/FE_USKC134_CTS_270:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_15'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_8:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_15:ZN', -1, -1, 0, 0])
	# matching_dict['cont/CTS_ccl_INV_clk_G0_L6_16'] = (['Xmycir.cont/CTS_ccl_INV_clk_G0_L5_8:ZN', 'Xmycir.cont/CTS_ccl_INV_clk_G0_L6_16:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC171_CTS_231'] = (['Xmycir.dp/FE_USKC289_CTS_231:ZN', 'Xmycir.dp/FE_USKC171_CTS_231:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC199_CTS_147'] = (['Xmycir.dp/rf/FE_USKC154_CTS_147:ZN', 'Xmycir.dp/rf/FE_USKC199_CTS_147:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_48'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_24:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_48:ZN', -1, -1, 0, 0])
	# matching_dict['CTS_ccl_INV_clk_G0_L2_1'] = (['Xmycir.CTS_ccl_INV_clk_G0_L1_1:ZN', 'Xmycir.CTS_ccl_INV_clk_G0_L2_1:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC149_CTS_250'] = (['Xmycir.dp/FE_USKC248_CTS_250:ZN', 'Xmycir.dp/FE_USKC149_CTS_250:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC249_CTS_238'] = (['Xmycir.dp/FE_USKC150_CTS_238:ZN', 'Xmycir.dp/FE_USKC249_CTS_238:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC205_CTS_139'] = (['Xmycir.dp/rf/FE_USKC166_CTS_139:ZN', 'Xmycir.dp/rf/FE_USKC205_CTS_139:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_13'] = (['Xmycir.dp/FE_USKC171_CTS_231:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_13:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_42'] = (['Xmycir.dp/FE_USKC143_CTS_240:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_42:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_44'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_22:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_44:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_45'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_23:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_45:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC209_CTS_146'] = (['Xmycir.dp/rf/FE_USKC164_CTS_146:ZN', 'Xmycir.dp/rf/FE_USKC209_CTS_146:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC203_CTS_147'] = (['Xmycir.dp/rf/FE_USKC155_CTS_147:ZN', 'Xmycir.dp/rf/FE_USKC203_CTS_147:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC141_CTS_259'] = (['Xmycir.dp/FE_USKC140_CTS_259:ZN', 'Xmycir.dp/FE_USKC141_CTS_259:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC194_CTS_270'] = (['Xmycir.dp/FE_USKC246_CTS_270:ZN', 'Xmycir.dp/FE_USKC194_CTS_270:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC133_CTS_250'] = (['Xmycir.dp/FE_USKC132_CTS_250:ZN', 'Xmycir.dp/FE_USKC133_CTS_250:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_11'] = (['Xmycir.dp/FE_USKC157_CTS_249:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_11:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC174_CTS_170'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_25:ZN', 'Xmycir.dp/rf/FE_USKC174_CTS_170:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L5_25'] = (['Xmycir.dp/rf/FE_USKC173_CTS_171:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_25:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_3'] = (['Xmycir.dp/FE_USKC291_CTS_217:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_3:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC130_CTS_210'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_1:ZN', 'Xmycir.dp/FE_USKC130_CTS_210:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_5'] = (['Xmycir.dp/FE_USKC287_CTS_225:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_5:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC173_CTS_171'] = (['Xmycir.dp/rf/FE_USKC172_CTS_171:ZN', 'Xmycir.dp/rf/FE_USKC173_CTS_171:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC250_CTS_238'] = (['Xmycir.dp/FE_USKC249_CTS_238:ZN', 'Xmycir.dp/FE_USKC250_CTS_238:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_6'] = (['Xmycir.dp/FE_USKC287_CTS_225:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_6:ZN', -1, -1, 0, 0])
	# matching_dict['dp/areg/CTS_ccl_INV_clk_G0_L6_25'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_13:ZN', 'Xmycir.dp/areg/CTS_ccl_INV_clk_G0_L6_25:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_8'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_4:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_8:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_7'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_4:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_7:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_6'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_3:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_6:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_5'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_3:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_5:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_4'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_2:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_4:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_62'] = (['Xmycir.dp/FE_USKC196_CTS_267:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_62:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_29'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_15:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_29:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC164_CTS_146'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_6:ZN', 'Xmycir.dp/rf/FE_USKC164_CTS_146:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC152_CTS_164'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L3_5:ZN', 'Xmycir.dp/rf/FE_USKC152_CTS_164:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_18'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_9:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_18:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC197_CTS_266'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L6_61:ZN', 'Xmycir.dp/FE_USKC197_CTS_266:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC142_CTS_240'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_21:ZN', 'Xmycir.dp/FE_USKC142_CTS_240:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC137_CTS_249'] = (['Xmycir.dp/FE_USKC136_CTS_249:ZN', 'Xmycir.dp/FE_USKC137_CTS_249:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L5_20'] = (['Xmycir.dp/rf/FE_USKC161_CTS_163:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_20:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC252_CTS_156'] = (['Xmycir.dp/rf/FE_USKC251_CTS_156:ZN', 'Xmycir.dp/rf/FE_USKC252_CTS_156:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC200_CTS_147'] = (['Xmycir.dp/rf/FE_USKC199_CTS_147:ZN', 'Xmycir.dp/rf/FE_USKC200_CTS_147:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC138_CTS_243'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_11:ZN', 'Xmycir.dp/FE_USKC138_CTS_243:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC136_CTS_249'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L3_6:ZN', 'Xmycir.dp/FE_USKC136_CTS_249:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC143_CTS_240'] = (['Xmycir.dp/FE_USKC142_CTS_240:ZN', 'Xmycir.dp/FE_USKC143_CTS_240:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC201_CTS_147'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L3_3:ZN', 'Xmycir.dp/rf/FE_USKC201_CTS_147:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC289_CTS_231'] = (['Xmycir.dp/FE_USKC288_CTS_231:ZN', 'Xmycir.dp/FE_USKC289_CTS_231:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_27'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_14:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_27:ZN', -1, -1, 0, 0])
	# matching_dict['dp/pcreg/CTS_ccl_INV_clk_G0_L6_41'] = (['Xmycir.dp/FE_USKC143_CTS_240:ZN', 'Xmycir.dp/pcreg/CTS_ccl_INV_clk_G0_L6_41:ZN', -1, -1, 0, 0])
	# matching_dict['dp/ir3/CTS_ccl_INV_clk_G0_L5_7'] = (['Xmycir.CTS_ccl_INV_clk_G0_L4_4:ZN', 'Xmycir.dp/ir3/CTS_ccl_INV_clk_G0_L5_7:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC135_CTS_270'] = (['Xmycir.dp/FE_USKC194_CTS_270:ZN', 'Xmycir.dp/FE_USKC135_CTS_270:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_16'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_8:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_16:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC195_CTS_267'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_31:ZN', 'Xmycir.dp/FE_USKC195_CTS_267:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC282_CTS_218'] = (['Xmycir.dp/FE_USKC244_CTS_218:ZN', 'Xmycir.dp/FE_USKC282_CTS_218:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC256_CTS_156'] = (['Xmycir.dp/rf/FE_USKC255_CTS_156:ZN', 'Xmycir.dp/rf/FE_USKC256_CTS_156:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC206_CTS_139'] = (['Xmycir.dp/rf/FE_USKC205_CTS_139:ZN', 'Xmycir.dp/rf/FE_USKC206_CTS_139:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC251_CTS_156'] = (['Xmycir.dp/rf/FE_USKC162_CTS_156:ZN', 'Xmycir.dp/rf/FE_USKC251_CTS_156:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_61'] = (['Xmycir.dp/FE_USKC196_CTS_267:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_61:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_14'] = (['Xmycir.dp/FE_USKC171_CTS_231:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_14:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC167_CTS_139'] = (['Xmycir.dp/rf/FE_USKC206_CTS_139:ZN', 'Xmycir.dp/rf/FE_USKC167_CTS_139:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC183_CTS_145'] = (['Xmycir.dp/rf/FE_USKC182_CTS_145:ZN', 'Xmycir.dp/rf/FE_USKC183_CTS_145:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC160_CTS_163'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_10:ZN', 'Xmycir.dp/rf/FE_USKC160_CTS_163:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC287_CTS_225'] = (['Xmycir.dp/FE_USKC286_CTS_225:ZN', 'Xmycir.dp/FE_USKC287_CTS_225:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_43'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_22:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_43:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC214_CTS_139'] = (['Xmycir.dp/rf/FE_USKC213_CTS_139:ZN', 'Xmycir.dp/rf/FE_USKC214_CTS_139:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC165_CTS_146'] = (['Xmycir.dp/rf/FE_USKC210_CTS_146:ZN', 'Xmycir.dp/rf/FE_USKC165_CTS_146:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L3_5'] = (['Xmycir.dp/FE_USKC149_CTS_250:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L3_5:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC158_CTS_237'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L3_4:ZN', 'Xmycir.dp/FE_USKC158_CTS_237:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L3_3'] = (['Xmycir.dp/FE_USKC151_CTS_238:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L3_3:ZN', -1, -1, 0, 0])
	# matching_dict['dp/res/CTS_ccl_INV_clk_G0_L6_3'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_2:ZN', 'Xmycir.dp/res/CTS_ccl_INV_clk_G0_L6_3:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC169_CTS_248'] = (['Xmycir.dp/FE_USKC168_CTS_248:ZN', 'Xmycir.dp/FE_USKC169_CTS_248:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC144_CTS_258'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L6_56:ZN', 'Xmycir.dp/FE_USKC144_CTS_258:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_47'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_24:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_47:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC208_CTS_139'] = (['Xmycir.dp/rf/FE_USKC207_CTS_139:ZN', 'Xmycir.dp/rf/FE_USKC208_CTS_139:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_49'] = (['Xmycir.dp/rf/FE_USKC175_CTS_170:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_49:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_12'] = (['Xmycir.dp/FE_USKC157_CTS_249:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_12:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC286_CTS_225'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_3:ZN', 'Xmycir.dp/FE_USKC286_CTS_225:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_40'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_20:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_40:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC180_CTS_152'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_17:ZN', 'Xmycir.dp/rf/FE_USKC180_CTS_152:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC211_CTS_146'] = (['Xmycir.dp/rf/FE_USKC165_CTS_146:ZN', 'Xmycir.dp/rf/FE_USKC211_CTS_146:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_46'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_23:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_46:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC140_CTS_259'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_28:ZN', 'Xmycir.dp/FE_USKC140_CTS_259:ZN', -1, -1, 0, 0])
	# matching_dict['cont/CTS_ccl_INV_clk_G0_L5_8'] = (['Xmycir.CTS_ccl_INV_clk_G0_L4_4:ZN', 'Xmycir.cont/CTS_ccl_INV_clk_G0_L5_8:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_12'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_6:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_12:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_11'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_6:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_11:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_30'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_15:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_30:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L3_4'] = (['Xmycir.dp/FE_USKC151_CTS_238:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L3_4:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_1'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_1:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_1:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_31'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_16:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_31:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC150_CTS_238'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L2_2:ZN', 'Xmycir.dp/FE_USKC150_CTS_238:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC244_CTS_218'] = (['Xmycir.dp/FE_USKC243_CTS_218:ZN', 'Xmycir.dp/FE_USKC244_CTS_218:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC154_CTS_147'] = (['Xmycir.dp/rf/FE_USKC202_CTS_147:ZN', 'Xmycir.dp/rf/FE_USKC154_CTS_147:ZN', -1, -1, 0, 0])
	# matching_dict['dp/ir3/CTS_ccl_INV_clk_G0_L6_14'] = (['Xmycir.dp/ir3/CTS_ccl_INV_clk_G0_L5_7:ZN', 'Xmycir.dp/ir3/CTS_ccl_INV_clk_G0_L6_14:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC247_CTS_250'] = (['Xmycir.dp/FE_USKC148_CTS_250:ZN', 'Xmycir.dp/FE_USKC247_CTS_250:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L4_6'] = (['Xmycir.dp/rf/FE_USKC204_CTS_147:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_6:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC155_CTS_147'] = (['Xmycir.dp/rf/FE_USKC200_CTS_147:ZN', 'Xmycir.dp/rf/FE_USKC155_CTS_147:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_17'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_9:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_17:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC243_CTS_218'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L3_1:ZN', 'Xmycir.dp/FE_USKC243_CTS_218:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_52'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_26:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_52:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC255_CTS_156'] = (['Xmycir.dp/rf/FE_USKC163_CTS_156:ZN', 'Xmycir.dp/rf/FE_USKC255_CTS_156:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_50'] = (['Xmycir.dp/rf/FE_USKC175_CTS_170:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_50:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_15'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L3_8:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_15:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_14'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L3_7:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_14:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L4_16'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L3_8:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L4_16:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC202_CTS_147'] = (['Xmycir.dp/rf/FE_USKC201_CTS_147:ZN', 'Xmycir.dp/rf/FE_USKC202_CTS_147:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC148_CTS_250'] = (['Xmycir.dp/FE_USKC133_CTS_250:ZN', 'Xmycir.dp/FE_USKC148_CTS_250:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_56'] = (['Xmycir.dp/FE_USKC141_CTS_259:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_56:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L5_9'] = (['Xmycir.dp/rf/FE_USKC214_CTS_139:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_9:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L5_18'] = (['Xmycir.dp/rf/FE_USKC256_CTS_156:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_18:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC161_CTS_163'] = (['Xmycir.dp/rf/FE_USKC216_CTS_163:ZN', 'Xmycir.dp/rf/FE_USKC161_CTS_163:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC182_CTS_145'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_12:ZN', 'Xmycir.dp/rf/FE_USKC182_CTS_145:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC172_CTS_171'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_13:ZN', 'Xmycir.dp/rf/FE_USKC172_CTS_171:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC147_CTS_239'] = (['Xmycir.dp/FE_USKC146_CTS_239:ZN', 'Xmycir.dp/FE_USKC147_CTS_239:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_32'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_16:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_32:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC212_CTS_146'] = (['Xmycir.dp/rf/FE_USKC211_CTS_146:ZN', 'Xmycir.dp/rf/FE_USKC212_CTS_146:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC139_CTS_243'] = (['Xmycir.dp/FE_USKC138_CTS_243:ZN', 'Xmycir.dp/FE_USKC139_CTS_243:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC288_CTS_231'] = (['Xmycir.dp/FE_USKC170_CTS_231:ZN', 'Xmycir.dp/FE_USKC288_CTS_231:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC145_CTS_258'] = (['Xmycir.dp/FE_USKC144_CTS_258:ZN', 'Xmycir.dp/FE_USKC145_CTS_258:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC193_CTS_270'] = (['Xmycir.dp/FE_USKC134_CTS_270:ZN', 'Xmycir.dp/FE_USKC193_CTS_270:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC156_CTS_249'] = (['Xmycir.dp/FE_USKC137_CTS_249:ZN', 'Xmycir.dp/FE_USKC156_CTS_249:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_20'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_10:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_20:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_23'] = (['Xmycir.dp/FE_USKC169_CTS_248:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_23:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_22'] = (['Xmycir.dp/FE_USKC139_CTS_243:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_22:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_21'] = (['Xmycir.dp/FE_USKC139_CTS_243:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_21:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_21'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_11:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_21:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_27'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_14:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_27:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_26'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_14:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_26:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_24'] = (['Xmycir.dp/rf/FE_USKC183_CTS_145:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_24:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_24'] = (['Xmycir.dp/FE_USKC169_CTS_248:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_24:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC291_CTS_217'] = (['Xmycir.dp/FE_USKC290_CTS_217:ZN', 'Xmycir.dp/FE_USKC291_CTS_217:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_29'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_15:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_29:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_28'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_15:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_28:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC157_CTS_249'] = (['Xmycir.dp/FE_USKC156_CTS_249:ZN', 'Xmycir.dp/FE_USKC157_CTS_249:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC163_CTS_156'] = (['Xmycir.dp/rf/FE_USKC252_CTS_156:ZN', 'Xmycir.dp/rf/FE_USKC163_CTS_156:ZN', -1, -1, 0, 0])
	# matching_dict['dp/areg/CTS_ccl_INV_clk_G0_L6_60'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_30:ZN', 'Xmycir.dp/areg/CTS_ccl_INV_clk_G0_L6_60:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC253_CTS_156'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_9:ZN', 'Xmycir.dp/rf/FE_USKC253_CTS_156:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC245_CTS_270'] = (['Xmycir.dp/FE_USKC193_CTS_270:ZN', 'Xmycir.dp/FE_USKC245_CTS_270:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_22'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_11:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_22:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_9'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_5:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_9:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC146_CTS_239'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L6_42:ZN', 'Xmycir.dp/FE_USKC146_CTS_239:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_4'] = (['Xmycir.dp/FE_USKC291_CTS_217:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_4:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC213_CTS_139'] = (['Xmycir.dp/rf/FE_USKC167_CTS_139:ZN', 'Xmycir.dp/rf/FE_USKC213_CTS_139:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_28'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_14:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_28:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_23'] = (['Xmycir.dp/rf/FE_USKC183_CTS_145:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_23:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_26'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_13:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_26:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC216_CTS_163'] = (['Xmycir.dp/rf/FE_USKC215_CTS_163:ZN', 'Xmycir.dp/rf/FE_USKC216_CTS_163:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC198_CTS_266'] = (['Xmycir.dp/FE_USKC197_CTS_266:ZN', 'Xmycir.dp/FE_USKC198_CTS_266:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC175_CTS_170'] = (['Xmycir.dp/rf/FE_USKC174_CTS_170:ZN', 'Xmycir.dp/rf/FE_USKC175_CTS_170:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC170_CTS_231'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_7:ZN', 'Xmycir.dp/FE_USKC170_CTS_231:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC196_CTS_267'] = (['Xmycir.dp/FE_USKC195_CTS_267:ZN', 'Xmycir.dp/FE_USKC196_CTS_267:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC210_CTS_146'] = (['Xmycir.dp/rf/FE_USKC209_CTS_146:ZN', 'Xmycir.dp/rf/FE_USKC210_CTS_146:ZN', -1, -1, 0, 0])
	# matching_dict['dp/res/CTS_ccl_INV_clk_G0_L6_51'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_26:ZN', 'Xmycir.dp/res/CTS_ccl_INV_clk_G0_L6_51:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC284_CTS_270'] = (['Xmycir.dp/FE_USKC245_CTS_270:ZN', 'Xmycir.dp/FE_USKC284_CTS_270:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_2'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_1:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_2:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L3_8'] = (['Xmycir.dp/FE_USKC135_CTS_270:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L3_8:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_30'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_16:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_30:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L5_31'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L4_16:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L5_31:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_33'] = (['Xmycir.dp/rf/FE_USKC181_CTS_152:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_33:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC176_CTS_159'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_19:ZN', 'Xmycir.dp/rf/FE_USKC176_CTS_159:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_35'] = (['Xmycir.dp/rf/FE_USKC179_CTS_155:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_35:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_34'] = (['Xmycir.dp/rf/FE_USKC181_CTS_152:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_34:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_37'] = (['Xmycir.dp/rf/FE_USKC177_CTS_159:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_37:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_36'] = (['Xmycir.dp/rf/FE_USKC179_CTS_155:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_36:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_39'] = (['Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L5_20:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_39:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L6_38'] = (['Xmycir.dp/rf/FE_USKC177_CTS_159:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L6_38:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/CTS_ccl_INV_clk_G0_L4_9'] = (['Xmycir.dp/rf/FE_USKC153_CTS_164:ZN', 'Xmycir.dp/rf/CTS_ccl_INV_clk_G0_L4_9:ZN', -1, -1, 0, 0])
	# matching_dict['CTS_ccl_INV_clk_G0_L1_1'] = (['clk', 'Xmycir.CTS_ccl_INV_clk_G0_L1_1:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L1_2'] = (['clk', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L1_2:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L6_10'] = (['Xmycir.dp/CTS_ccl_INV_clk_G0_L5_5:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L6_10:ZN', -1, -1, 0, 0])
	# matching_dict['cont/CTS_ccl_INV_clk_G0_L6_15'] = (['Xmycir.cont/CTS_ccl_INV_clk_G0_L5_8:ZN', 'Xmycir.cont/CTS_ccl_INV_clk_G0_L6_15:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L3_1'] = (['Xmycir.CTS_ccl_INV_clk_G0_L2_1:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L3_1:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L3_6'] = (['Xmycir.dp/FE_USKC149_CTS_250:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L3_6:ZN', -1, -1, 0, 0])
	# matching_dict['dp/CTS_ccl_INV_clk_G0_L3_7'] = (['Xmycir.dp/FE_USKC135_CTS_270:ZN', 'Xmycir.dp/CTS_ccl_INV_clk_G0_L3_7:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC215_CTS_163'] = (['Xmycir.dp/rf/FE_USKC160_CTS_163:ZN', 'Xmycir.dp/rf/FE_USKC215_CTS_163:ZN', -1, -1, 0, 0])
	# matching_dict['CTS_ccl_INV_clk_G0_L3_2'] = (['Xmycir.CTS_ccl_INV_clk_G0_L2_1:ZN', 'Xmycir.CTS_ccl_INV_clk_G0_L3_2:ZN', -1, -1, 0, 0])
	# matching_dict['dp/rf/FE_USKC166_CTS_139'] = (['Xmycir.dp/rf/FE_USKC208_CTS_139:ZN', 'Xmycir.dp/rf/FE_USKC166_CTS_139:ZN', -1, -1, 0, 0])
	# matching_dict['dp/FE_USKC131_CTS_210'] = (['Xmycir.dp/FE_USKC192_CTS_210:ZN', 'Xmycir.dp/FE_USKC131_CTS_210:ZN', -1, -1, 0, 0])


			
	
	# iterate over all data we have (normally at least two, one for rising transition at the input, the other one for falling transition):
	file_list = list()
	file_list.append(sys.argv[1]) # "./main_new_exp.vcd0"
	
	for file in file_list:		
		data = read_modelsim(file, 1.0, 0.50, 0) # vdd / vth / vss not relevant here * (returns the time values / 1e6)
		
		print(data)
				
		# order the data by transition time, list (time, value, port)	
		transition_times = list()
		
		for key in sorted(data.keys()):
			prev_value = -1
			for i in range(len(data[key][0])):				
				time = data[key][0][i] * 1e6 / vcd_timescale # to get time in femto seconds
				value = data[key][1][i]
				if time == 0:
					# ignore initial values
					continue
				
				if time == prev_value:
					# only take the first value (we have for each transition tw0 values)
					continue
				
				prev_value = time
				transition_times.append((time, value, key))
		
		transition_times = sorted(transition_times)
		
		print(transition_times)
		
		# Definitely not the most performant implementation, but working ...
		for idx, (time, value, port) in enumerate(transition_times):
			for key, entry in matching_dict.iteritems():
				if entry[0] == port:
					#print("Port: {0}".format(port))
					# we found the "starting port"
					# look into the future for x ns
					future = subsequent_transition_range
					temp_idx = idx
					found_transition = False
					while len(transition_times) > temp_idx and transition_times[temp_idx][0] < time + future:						
						if transition_times[temp_idx][2] == entry[1]:
							#print("{0} < {1} + {2}".format(transition_times[temp_idx][0], time, future))
							# we found a transition in the specified time range, on the "end" port
							# now add the information to the matching_dict
							delay = transition_times[temp_idx][0] - time
							type = value # 0 = rising; 1 = falling					
						
							if type== 0: # rising transition
								#if entry[2] != -1.0 and abs(entry[3] - delay) > warning_delay_change:
								#	print("Change rising delay from {0} to {1}".format(entry[2], delay))
								entry[2] += delay
								entry[4] += 1
							elif type == 1:
								#if entry[3] != -1.0 and abs(entry[3] - delay) > warning_delay_change:
								#	print("Change falling delay from {0} to {1}".format(entry[3], delay))
								entry[3] += delay
								entry[5] += 1
							else:
								print('This should not happen')
							
							found_transition = True
							
							# No break, because we can also find other transitions that have been caused by this transition
							#break							
						
						temp_idx = temp_idx + 1		
					
					#if not found_transition:
					#	print('Did not find a matching transition for {0} at {1}'.format(entry[0], time))
	
	
	for key in sorted(matching_dict.keys()):
		# time values are in femto seconds, multiply with the multiplicator for sdf files
		rising_time = -1
		falling_time = -1
		if matching_dict[key][4] > 0:
			rising_time = matching_dict[key][2] / matching_dict[key][4]
			matching_dict[key][2] = rising_time
		if matching_dict[key][5] > 0:
			falling_time = matching_dict[key][3] / matching_dict[key][5]
			matching_dict[key][3] = falling_time
		print('Instance: {0}, rise: {1:.6f}, fall: {2:.6f}'.format(key, rising_time / sdf_output_scale, falling_time / sdf_output_scale))
		
	# now go and set each interconnect to 0 (the following code is taken from Juergens customSDF.py script)
	f = open(sys.argv[2])
	fout = open(sys.argv[3],'w')

	lines = f.readlines()
	modified_lines = list()
	for line in lines:
		if line.count('INTERCONNECT') > 0:       
			parts = line.split(' ')
			parts[4] = '(0.000::0.000)'
			parts[5] = '(0.000::0.000))\n'
			modified_lines.append(' '.join(parts))
		else:
			modified_lines.append(line)
			
	# now find for each key in the matching dict the corresponding entry and modify the rise and fall time
	for key in matching_dict.keys():
		found_key = False
		for line_idx, line in enumerate(modified_lines):
			if line.find("(INSTANCE  {0})".format(key)) >= 0:		
				# find the next line withing the next few lines which contains IOPATH, and replace...
				start_idx = line_idx
				while line_idx < start_idx + 5:
					# TODO: Generalize this...
					#if modified_lines[line_idx].find("IOPATH A Z") >= 0:
					if modified_lines[line_idx].find("IOPATH I ZN") >= 0:						
						found_key = True	

						parts = modified_lines[line_idx].split(' ')
						parts[4] = "({0:.6f}::{0:.6f})".format(matching_dict[key][2] / sdf_output_scale)
						parts[5] = "({0:.6f}::{0:.6f}))\n".format(matching_dict[key][3] / sdf_output_scale)
							
						modified_lines[line_idx] = ' '.join(parts)
						
						break;
					line_idx += 1
				break
				
		if not found_key:
			print("There was a problem for key: {0}".format(key))
			
	for line in modified_lines:
		fout.write(line)
				
		
if __name__ == "__main__":
	main()