###############################################################################
#
#	Involution Tool
#	File: Makefile
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

.PRECIOUS: %.vcd %.saif %.scr %.do
.PHONY: all clean generate spice crossings read gates sim power

MAKEFLAGS += ${MAKEFILE_ARGS}

include ./config.cfg

# We can use the Default Makefile of the experiment_setup, and do not have to override rules
all:
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) all 
	
clean:
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) clean 
	
generate:
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) generate

# We have to specify all targets seperately, and cannot work with %, because otherwise .PHONY does not work, and
# since we have folders called like targets, the rules would never be executed.	
spice:
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) spice
	
crossings:
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) crossings

read:
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) read

gates:	
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) gates
			
sim:
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) sim
	
power:
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) power
		
report:
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) report
	
%:
	echo "Try to find rule in sub-make"
	cd ${EXPERIMENT_SETUP_DIR} && $(MAKE) $@