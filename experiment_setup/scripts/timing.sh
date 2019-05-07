#!/bin/bash
###############################################################################
#
#	Involution Tool
#	File: timing.sh
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


if [ -n "${PERF}" ]
then	
	# required for multi_exec tool, because we need to add more file to the report folder	 
	mkdir -p ${TOP_DIR}/perf/ 
	
	ELAPSED=$(($(date +%s%3N)-${2}))
	echo ${1} ${ELAPSED} >> ${TOP_DIR}/perf/performance_meassure.txt

fi

