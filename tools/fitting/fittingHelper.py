"""
    @file fittingHelper.py

	@brief Helper methods for fitting scripts

	@author Daniel OEHLINGER <d.oehlinger@outlook.com>
	@date 2021

	@copyright
	@parblock
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
	@endparblock	
""" 

import re

def find_cell_in_structure(structure, cellname):
    found_cell = None
    for cell in structure.cells:
        if cell.instance == cellname:
            found_cell = cell
            break

    return found_cell

def get_cellname(char_conf, name):
    matches = re.match(r"cellName\s(.*)", char_conf['simulations'][int(name)]['params']['cellName'])
    return matches[1]
