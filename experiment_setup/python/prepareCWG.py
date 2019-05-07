"""
    
	Involution Tool
	File: prepareCWG.py
	
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
from readGenerateCfg import *
import helper

def main():
	if len(sys.argv) != 4:
		my_print("usage: python prepareCWG.py report_cfg_file template_cwg_file template_group_file", EscCodes.FAIL)
		sys.exit(1)
	prepare_cwg(sys.argv[1], sys.argv[2], sys.argv[3])

def prepare_cwg(report_cfg_file, template_cwg_file, template_group_file):		
	report_cfg = read_generate_cfg(report_cfg_file)
	
	
	cwg_template = ""
	with open(template_cwg_file, 'r') as tempfile:
		cwg_template = tempfile.read()
	
	cwg_template = cwg_template.replace("%##N##%", str(report_cfg.N)).replace("%##SIGMA##%", str(report_cfg.sigma)).replace("%##MUE##%", str(report_cfg.mue)).replace("%##NEXT_TRANSITION_MODE##%", report_cfg.calc_next_transition_mode)
	
	group_template = ""
	with open(template_group_file, 'r') as tempfile:
		group_template = tempfile.read()
	
	groups_content = ""
	# iterate over the groups ...
	for g in report_cfg.groups:
		group_content = group_template.replace("%##SIGMA##%", str(g.sigma)).replace("%##MUE##%", str(g.mue)).replace("%##SIGNALS##%", ", ".join(g.signals)).replace("%##ONEWAY##%", str(g.oneway)).replace("%##CORRELATION_POSSIBILITY##%", str(g.correlation_possibility * 100))
		if g.oneway:
			group_content = group_content.replace("%##ONEWAYCHECKBOX##%", "$\\boxtimes$")	
		else:
			group_content = group_content.replace("%##ONEWAYCHECKBOX##%", "$\\square$")

		groups_content += group_content
		
	content = cwg_template.replace("%##GROUPS##%", groups_content)
	
	with open(template_cwg_file, 'w') as outfile:
		outfile.write(content)
	
if __name__ == "__main__":
    main()