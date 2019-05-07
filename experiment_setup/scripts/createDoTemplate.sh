#!/bin/bash
###############################################################################
#
#	Involution Tool
#	File: createDoTemplate.sh
#	
#   Copyright (C) 2018-2019  Daniel OEHLINGER <d.oehlinger@outlook.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################

TEXT=""
for i in $5
do
	TEXT+="vcd add ${3}/${4}/${i}\n"
done

GATE_DIRS=""

for i in ./vhdl/gates/*.vhd 
do
	if [ -f "$i" ]; then printf echo "Found"; GATE_DIRS+=" ./vhdl/gates/*.vhd "; fi
	break;
done

for i in  ${9}/*.vhd
do
	if [ -f "$i" ]; then printf echo "Found 2"; GATE_DIRS+="${9}*.vhd"; fi
	break;
done

	
sed "s%##vcdAdd##%${TEXT}%g" ./scripts/templateDo | \
sed "s/##sdfFile##/${1}/g" | \
sed "s/##circuitFile##/${2}/g" | \
sed "s/##unitName##/${4}/g" | \
sed "s@##topDir##@${6}@g" | \
sed "s@##circuitDir##@${7}@g" | \
sed "s@##vectorsDir##@${8}@g" | \
sed "s@##gateDirs##@${GATE_DIRS}@g" | \
sed "s@##simLibraryVerilog##@${10}@g" | \
sed "s@##channelVDD##@${11}@g" | \
sed "s@##channelVTH##@${12}@g" | \
sed "s@##circuitFileType##@${13}@g" > localDoTemplate