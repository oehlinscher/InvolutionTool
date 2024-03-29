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

.PHONY: all generate spice crossings read sim power report involution gates sim_involution sim_modelsim power_dc power_pt power_spice power_pt_modelsim power_pt_involution power_dc_modelsim power_dc_involution clean

all: 
	$(eval TIME_ALL := $(shell date +%s%3N))
	$(MAKE) generate
	$(MAKE) spice
	$(MAKE) crossings
	$(MAKE) read
	$(MAKE) sim
	$(MAKE) power	
	# not ideal to directly call reporting, but otherwise performance meassurement does not work properly
	./scripts/reporting.sh ${TIME_ALL}

# Targets which are used from the multi_exec tool, in order to keep certain parts of the simulation.
# do not call manually, unless you know what you are doing!
me_involution:
	$(eval TIME_INVOLUTION := $(shell date +%s%3N))
	$(MAKE) sim_involution	
ifeq ($(ENABLE_DC),True)
	$(MAKE) power_dc_involution	
else
	echo "DesignCompiler disabled"
endif	
ifeq ($(ENABLE_PRIMETIME),True)
	$(MAKE) power_pt_involution	
else
	echo "PrimeTime disabled"
endif
	# not ideal to directly call reporting, but otherwise performance meassurement does not work properly
	./scripts/reporting.sh ${TIME_INVOLUTION}
	
me_digsim:
	$(eval TIME_DIGSIM := $(shell date +%s%3N))
	$(MAKE) sim
	$(MAKE) power	
	# not ideal to directly call reporting, but otherwise performance meassurement does not work properly
	./scripts/reporting.sh ${TIME_DIGSIM}

me_crossings:
	$(eval TIME_ME_CROSSINGS:= $(shell date +%s%3N))	
	rm -f ${CROSSINGS_OUTPUT_DIR}/crossings.json	
	$(MAKE) crossings
	$(MAKE) sim
	$(MAKE) power	
	# not ideal to directly call reporting, but otherwise performance meassurement does not work properly
	./scripts/reporting.sh ${TIME_ME_CROSSINGS}

	


#### SETUP   ##############################################################

generate: 
	$(eval TIME_GENERATE := $(shell date +%s%3N))
	$(MAKE) -B ${GEN_OUTPUT_DIR}/main_new_exp.sp # we always want to generate a new Input Waveform, therefore -B
	./scripts/timing.sh $@ ${TIME_GENERATE} 

${GEN_OUTPUT_DIR}/main_new_exp.sp: ./python/generateWaveform.py 
	mkdir -p ${GEN_INPUT_DIR}
	mkdir -p ${GEN_OUTPUT_DIR}
	$(MAKE) -B clean # we always want to clean before a new waveform is generated (to make sure no old files are "flying" around), also required because we copy the generated waveform into the report folder afterwards and we have to be sure to take the "correct" one
	python3 ./python/generateWaveform.py ${GEN_INPUT_DIR} ${GEN_OUTPUT_DIR} ${WAVEFORM_GENERATION_CONFIG_DIR} ${VDD} ${VTH} ${TEMPERATURE} ${SPICE_LIB} ${SPICE_CIR} ${INPUT_WAVEFORM}
                                                                                         
spice: 
	$(eval TIME_SPICE := $(shell date +%s%3N))
	mkdir -p ${SPICE_OUTPUT_DIR}
ifeq ($(ANALOG_SIMULATION_TOOL),HSPICE)
	$(MAKE) ${SPICE_OUTPUT_DIR}/main_new_exp.tr0
else
	$(MAKE) ${SPICE_OUTPUT_DIR}/main_new_exp.raw
endif
	./scripts/timing.sh $@ ${TIME_SPICE} 


${SPICE_OUTPUT_DIR}/main_new_exp.tr0: ${GEN_OUTPUT_DIR}/main_new_exp.sp 
# 	Enable HSPICE for 65nm
#	hspice -i ${SPICE_INPUT_DIR}/main_new_exp -o ${SPICE_OUTPUT_DIR}/main_new_exp -mt 8 -hpp
	hspice -i ${SPICE_INPUT_DIR}/main_new_exp -o ${SPICE_OUTPUT_DIR}/main_new_exp

${SPICE_OUTPUT_DIR}/main_new_exp.raw: ${GEN_OUTPUT_DIR}/main_new_exp.sp python/digitizeRaw.py 
	spectre +spp -format nutbin -outdir ${SPICE_OUTPUT_DIR} ${SPICE_INPUT_DIR}/main_new_exp.sp

    
crossings: 
	$(eval TIME_CROSSINGS := $(shell date +%s%3N))
	mkdir -p ${CROSSINGS_OUTPUT_DIR}
	$(MAKE) ${CROSSINGS_OUTPUT_DIR}/crossings.json	
	./scripts/timing.sh $@ ${TIME_CROSSINGS} 

ifeq ($(ANALOG_SIMULATION_TOOL),HSPICE)	
${CROSSINGS_OUTPUT_DIR}/crossings.json: ${SPICE_OUTPUT_DIR}/main_new_exp.tr0 ./python/digitizeTr0.py
	python3 ./python/digitizeTr0.py ${SPICE_OUTPUT_DIR}/main_new_exp.tr0 ${SPICE_OUTPUT_DIR}/main_new_exp.vcd0 ${CROSSINGS_OUTPUT_DIR}/crossings.json ${VTH} ${TOP_DIR}/${MATCHING_FILE} ${TOP_DIR}/${DISCRETIZATION_THRESHOLDS_FILE}
else
${CROSSINGS_OUTPUT_DIR}/crossings.json: ${SPICE_OUTPUT_DIR}/main_new_exp.raw ./python/digitizeRaw.py
	python3 ./python/digitizeRaw.py ${SPICE_OUTPUT_DIR}/main_new_exp.raw ${SPICE_OUTPUT_DIR}/main_new_exp.vcd0 ${CROSSINGS_OUTPUT_DIR}/crossings.json ${VTH} ${TOP_DIR}/${MATCHING_FILE} ${TOP_DIR}/${DISCRETIZATION_THRESHOLDS_FILE}
endif
	
#### READ   ###############################################################
	
read: 
	$(eval TIME_READ := $(shell date +%s%3N))
	$(MAKE) ${VECTOR_NAMES}
	./scripts/timing.sh $@ ${TIME_READ} 

# DO NOT SWAP the following two rules, otherwise we have an endless recursion	
${VECTOR_OUTPUT_DIR}/vectors_%: ${CROSSINGS_OUTPUT_DIR}/crossings.json ./python/readCrossings.py
	mkdir -p ${VECTOR_OUTPUT_DIR}
	python3 ./python/readCrossings.py ${VECTOR_INPUT_DIR} ${VECTOR_OUTPUT_DIR} ${TOP_DIR}/${MATCHING_FILE} $*

vectors_%: 
	$(MAKE) ${VECTOR_OUTPUT_DIR}/$@ 
	
#### GATES   ##############################################################
gates: 
	$(eval TIME_GATES := $(shell date +%s%3N))
	mkdir -p ${GATES_DIR}
	$(MAKE) $(patsubst %, ${GATES_DIR}/%.vhd, ${REQUIRED_GATES})
	./scripts/timing.sh $@ ${TIME_GATES} 
	
$(patsubst %, ${GATES_DIR}/%.vhd, ${REQUIRED_GATES}): ${VECTOR_NAMES} ./python/generateGates.py ${GENERAL_GATE_CONFIG} ${CIRCUIT_GATE_CONFIG} ${GATES_DIR} ./vhdl/gate_template.vhd ./vhdl/gate_input_process_template.vhd
	#python $^ "${REQUIRED_GATES}"
	mkdir -p ${GATES_DIR}
	cd ./vhdl/python_channel/ && $(MAKE) all 
	# cp ./vhdl/python_channel/python_channel.so ${GATES_DIR}
	# cp ./vhdl/python_channel/python_channel.so .
	python3 ./python/generateGates.py ${GENERAL_GATE_CONFIG} ${CIRCUIT_GATE_CONFIG} ${GATES_DIR} ./vhdl/gate_template.vhd ./vhdl/gate_input_process_template.vhd  $(USE_GIDM) ${TOP_DIR}/${STRUCTURE_FILE} ${TT_OUTPUT_DIR} ${GENERATE_GATE_PER_INSTANCE} ${VECTOR_OUTPUT_DIR} "${REQUIRED_GATES}"
	
#### SIM    ###############################################################

sim: 
	$(eval TIME_SIM := $(shell date +%s%3N))
	mkdir -p ${MODELSIM_OUTPUT_DIR}
	mkdir -p ${GATES_DIR}
	rm -rf ${TT_OUTPUT_DIR}/*
	rm -rf ${GATES_DIR}/*
	$(MAKE) sim_involution 
	$(MAKE) sim_modelsim
	./scripts/timing.sh $@ ${TIME_SIM} 

sim_involution: 
	$(eval TIME_SIM_INVOLUTION := $(shell date +%s%3N))
	mkdir -p ${TT_OUTPUT_DIR}
	rm -rf ${TT_OUTPUT_DIR}/*
	mkdir -p ${MODELSIM_OUTPUT_DIR}
	mkdir -p ${GATES_DIR}
	rm -rf ${GATES_DIR}/*
	rm -rf ${CIRCUIT_DIR}/circuit_involution.vhd
	$(MAKE) ${MODELSIM_OUTPUT_DIR}/involution.vcd 	
	./scripts/timing.sh $@ ${TIME_SIM_INVOLUTION} 
	
sim_modelsim: 
	$(eval TIME_SIM_MODELSIM := $(shell date +%s%3N))
	mkdir -p ${MODELSIM_OUTPUT_DIR}
	mkdir -p ${GATES_DIR}
	rm -rf ${GATES_DIR}/*
	$(MAKE) ${MODELSIM_OUTPUT_DIR}/modelsim.vcd
	./scripts/timing.sh $@ ${TIME_SIM_MODELSIM} 

${CIRCUIT_DIR}/circuit_involution.vhd: ${TOP_DIR}/circuit.vhd ./vhdl/input_process.vhd ./vhdl/input_process_gidm.vhd ./python/prepareTestbench.py
ifeq ($(USE_GIDM),True)
	python3 ./python/prepareTestbenchGIDM.py ${TOP_DIR}/circuit.vhd $@ ./vhdl/input_process_gidm.vhd "${INPUT_NAMES}" ${TOP_DIR}/${STRUCTURE_FILE} ${TT_OUTPUT_DIR}
else
	python3 ./python/prepareTestbench.py ${TOP_DIR}/circuit.vhd $@ ./vhdl/input_process.vhd "${INPUT_NAMES}" "${VECTOR_NAMES}" ${GENERAL_GATE_CONFIG} ${CIRCUIT_GATE_CONFIG} ${TOP_DIR}/circuit_configuration.vhd
endif	

${CIRCUIT_DIR}/circuit_modelsim.vhd: ${TOP_DIR}/circuit.vhd ./vhdl/input_process.vhd ./python/prepareTestbench.py
	python3 ./python/prepareTestbench.py ${TOP_DIR}/circuit.vhd $@ ./vhdl/input_process.vhd "${INPUT_NAMES}" "${VECTOR_NAMES}" ${GENERAL_GATE_CONFIG} ${CIRCUIT_GATE_CONFIG}

${MODELSIM_OUTPUT_DIR}/involution.vcd: ${MODELSIM_OUTPUT_DIR}/involution.do ${VECTOR_NAMES}
	rm -rf ${TT_OUTPUT_DIR}/*
	vsim -c -do $< > ${MODELSIM_OUTPUT_DIR}/involution_sim.log
ifeq ($(USE_GIDM),True)
	mv -f involution.vcd ${MODELSIM_OUTPUT_DIR}/involution_indicators.vcd
	python3 ./python/fixGIDMVCD.py ${MODELSIM_OUTPUT_DIR}/involution_indicators.vcd ${MODELSIM_OUTPUT_DIR}/involution.vcd ${TT_OUTPUT_DIR} ${TOP_DIR}/port_to_signal_matching.json ${TOP_DIR}/${STRUCTURE_FILE}
else
	mv -f involution.vcd ${MODELSIM_OUTPUT_DIR}/
endif	
	mv -f transcript ${MODELSIM_OUTPUT_DIR}/transcript
	rm -rf ${MODELSIM_OUTPUT_DIR}/work
	mv -f work ${MODELSIM_OUTPUT_DIR}/work

${MODELSIM_OUTPUT_DIR}/%.vcd: ${MODELSIM_OUTPUT_DIR}/%.do ${VECTOR_NAMES}
	vsim -c -do $< > ${MODELSIM_OUTPUT_DIR}/$(basename $*)_sim.log
	mv -f $*.vcd ${MODELSIM_OUTPUT_DIR}/
	mv -f transcript ${MODELSIM_OUTPUT_DIR}/transcript
	rm -rf ${MODELSIM_OUTPUT_DIR}/work
	mv -f work ${MODELSIM_OUTPUT_DIR}/work
	
${MODELSIM_OUTPUT_DIR}/%.do: ${MODELSIM_OUTPUT_DIR}/localDoTemplate
	sed 's@##name##@$(basename $*)@g' ${MODELSIM_OUTPUT_DIR}/localDoTemplate > $@

${MODELSIM_OUTPUT_DIR}/localDoTemplate: $(patsubst %, ${GATES_DIR}/%.vhd, ${REQUIRED_GATES}) ./scripts/templateDo ${CIRCUIT_DIR}/circuit_involution.vhd ${CIRCUIT_DIR}/circuit_modelsim.vhd
	mkdir -p ${MODELSIM_OUTPUT_DIR}
	./scripts/createDoTemplate.sh ${SDF_FILE} ${CIRCUIT_FILE} ${CIRCUIT_NAME} ${UNIT_NAME} "${VCD_SIGNALS}" ${TOP_DIR} ${CIRCUIT_DIR} ${VECTOR_OUTPUT_DIR} ${GATES_DIR} ${SIM_LIBRARY_VERILOG} ${VDD} ${VTH} ${CIRCUIT_FILE_TYPE} ${SIM_LIBRARY_COMPILER} ${VSIM_OPTIONS} ${USE_GIDM} ${CIRCUIT_FILE_GIDM} ${SDF_FILE_GIDM} ${GENERATE_GATE_PER_INSTANCE}
	mv -f localDoTemplate ${MODELSIM_OUTPUT_DIR}/localDoTemplate
	
#### POWER  ###############################################################

power: 
	$(eval TIME_POWER := $(shell date +%s%3N))
	mkdir -p ${POWER_OUTPUT_DIR}
ifeq ($(ENABLE_DC),True)
	$(MAKE) power_dc
else
	echo "DesignCompiler disabled"
endif	
ifeq ($(ENABLE_PRIMETIME),True)
	$(MAKE) power_pt 
else
	echo "PrimeTime disabled"
endif
	$(MAKE) power_spice
	./scripts/timing.sh $@ ${TIME_POWER} 

#Design Compiler Power
power_dc: power_dc_modelsim power_dc_involution

power_dc_modelsim: 
	$(eval TIME_POWER_DC_MODELSIM := $(shell date +%s%3N))
	$(MAKE) ${POWER_OUTPUT_DIR}/sim_modelsim_dc.power
	./scripts/timing.sh $@ ${TIME_POWER_DC_MODELSIM} 
	
power_dc_involution: 
	$(eval TIME_POWER_DC_INVOLUTION := $(shell date +%s%3N))
	$(MAKE) ${POWER_OUTPUT_DIR}/sim_involution_dc.power
	./scripts/timing.sh $@ ${TIME_POWER_DC_INVOLUTION} 

${POWER_OUTPUT_DIR}/sim_%_dc.power: ${POWER_OUTPUT_DIR}/sim_%_dc.scr
	dc_shell -f $< > $@
ifneq ($(MAKEFILE_PRINT_INFO),False) 
	tail -n 16 $@ | head -n 13 
endif
	mv -f command.log ${POWER_OUTPUT_DIR}/command_$*_dc.log
	mv -f default.svf ${POWER_OUTPUT_DIR}/default_$*_dc.svf

${POWER_OUTPUT_DIR}/sim_%_dc.scr: ${POWER_OUTPUT_DIR}/sim_%.saif ./scripts/templateDesignCompilerScr
	sed 's/##verilogFileName##/${VERILOG_FILE}/g' ./scripts/templateDesignCompilerScr | \
	sed 's@##inputFileName##@$<@g' | \
	sed "s@##topDir##@${TOP_DIR}@g" | \
	sed "s@##simLinkLibrary##@${SIM_LINK_LIBRARY}@g" | \
	sed "s@##simTargetLibrary##@${SIM_TARGET_LIBRARY}@g" | \
	sed "s@##simSearchPath##@${SIM_SEARCH_PATH}@g" | \
	sed "s@##simLinkPath##@${SIM_LINK_PATH}@g" | \
	sed "s@##simDBName##@${SIM_DB_NAME}@g" | \
	sed "s@##spefFileName##@${SPEF_FILE_NAME}@g" | \
	sed 's%##circuitName##%${CIRCUIT_NAME}/${UNIT_NAME}%g' > $@

#PrimeTime Power
power_pt: power_pt_modelsim power_pt_involution

power_pt_modelsim: 
	$(eval TIME_POWER_PT_MODELSIM := $(shell date +%s%3N))
	$(MAKE) power_pt_modelsim_avg
	$(MAKE) power_pt_modelsim_tim
	./scripts/timing.sh $@ ${TIME_POWER_PT_MODELSIM} 	

power_pt_modelsim_avg: 
	$(eval TIME_POWER_PT_MODELSIM_AVG := $(shell date +%s%3N))
	$(MAKE) ${POWER_OUTPUT_DIR}/sim_modelsim_pt.avg.power 
	./scripts/timing.sh "$@_AVG" ${TIME_POWER_PT_MODELSIM_AVG}  
	
power_pt_modelsim_tim: 
	$(eval TIME_POWER_PT_MODELSIM_TIM := $(shell date +%s%3N))
	$(MAKE) ${POWER_OUTPUT_DIR}/sim_modelsim_pt.tim.power 
	./scripts/timing.sh "$@_TIM" ${TIME_POWER_PT_MODELSIM_TIM}  

power_pt_involution: 
	$(eval TIME_POWER_PT_INVOLUTION := $(shell date +%s%3N))
	$(MAKE) power_pt_involution_avg
	$(MAKE) power_pt_involution_tim
	./scripts/timing.sh $@ ${TIME_POWER_PT_INVOLUTION} 
	
power_pt_involution_avg:
	$(eval TIME_POWER_PT_INVOLUTION_AVG := $(shell date +%s%3N))
	$(MAKE) ${POWER_OUTPUT_DIR}/sim_involution_pt.avg.power 
	./scripts/timing.sh "$@_AVG" ${TIME_POWER_PT_INVOLUTION_AVG}  
	
power_pt_involution_tim:
	$(eval TIME_POWER_PT_INVOLUTION_TIM := $(shell date +%s%3N))
	$(MAKE) ${POWER_OUTPUT_DIR}/sim_involution_pt.tim.power
	./scripts/timing.sh "$@_TIM" ${TIME_POWER_PT_INVOLUTION_TIM} 

${POWER_OUTPUT_DIR}/sim_%_pt.avg.power: ${POWER_OUTPUT_DIR}/sim_%_pt.avg.scr
	pt_shell -file $< > $@
	mv -f pt_shell_command.log ${POWER_OUTPUT_DIR}/pt_shell_command_$*.avg.log
	[ ! -f parasitics_command.log ] || mv -f parasitics_command.log ${POWER_OUTPUT_DIR}/parasitics_command_$*.avg.log
	
${POWER_OUTPUT_DIR}/sim_%_pt.tim.power: ${POWER_OUTPUT_DIR}/sim_%_pt.tim.scr
	pt_shell -file $< > $@
	mv -f pt_shell_command.log ${POWER_OUTPUT_DIR}/pt_shell_command_$*.tim.log
	[ ! -f primetime_px.fsdb ] || mv -f primetime_px.fsdb ${POWER_OUTPUT_DIR}/primetime_px_$*.tim.fsdb	
	[ ! -f parasitics_command.log ] || mv -f parasitics_command.log ${POWER_OUTPUT_DIR}/parasitics_command_$*.tim.log	
	
${POWER_OUTPUT_DIR}/sim_%_pt.avg.scr: ${POWER_OUTPUT_DIR}/sim_%.saif ${MODELSIM_OUTPUT_DIR}/%.vcd ./scripts/templatePrimetimeavgScr
	sed 's/##verilogFileName##/${VERILOG_FILE}/g' ./scripts/templatePrimetimeavgScr | \
	sed 's@##inputFileName##@$<@g' | \
	sed 's@##vcdFileName##@$(word 2,$^)@g' | \
	sed "s@##topDir##@${TOP_DIR}@g" | \
	sed "s@##simLinkLibrary##@${SIM_LINK_LIBRARY}@g" | \
	sed "s@##simTargetLibrary##@${SIM_TARGET_LIBRARY}@g" | \
	sed "s@##simSearchPath##@${SIM_SEARCH_PATH}@g" | \
	sed "s@##simLinkPath##@${SIM_LINK_PATH}@g" | \
	sed "s@##simDBName##@${SIM_DB_NAME}@g" | \
	sed "s@##spefFileName##@${SPEF_FILE_NAME}@g" | \
	sed 's%##circuitName##%${CIRCUIT_NAME}/${UNIT_NAME}%g' > $@
		
${POWER_OUTPUT_DIR}/sim_%_pt.tim.scr: ${POWER_OUTPUT_DIR}/sim_%.saif ${MODELSIM_OUTPUT_DIR}/%.vcd ./scripts/templatePrimetimetimScr
	sed 's/##verilogFileName##/${VERILOG_FILE}/g' ./scripts/templatePrimetimetimScr | \
	sed 's@##inputFileName##@$<@g' | \
	sed 's@##vcdFileName##@$(word 2,$^)@g' | \
	sed "s@##topDir##@${TOP_DIR}@g" | \
	sed "s@##simLinkLibrary##@${SIM_LINK_LIBRARY}@g" | \
	sed "s@##simTargetLibrary##@${SIM_TARGET_LIBRARY}@g" | \
	sed "s@##simSearchPath##@${SIM_SEARCH_PATH}@g" | \
	sed "s@##simLinkPath##@${SIM_LINK_PATH}@g" | \
	sed "s@##simDBName##@${SIM_DB_NAME}@g" | \
	sed "s@##spefFileName##@${SPEF_FILE_NAME}@g" | \
	sed 's%##circuitName##%${CIRCUIT_NAME}/${UNIT_NAME}%g' > $@

# General SIM Power	
${POWER_OUTPUT_DIR}/sim_%.saif: ${MODELSIM_OUTPUT_DIR}/%.vcd	
	mkdir -p ${POWER_OUTPUT_DIR}
	vcd2saif -input $< -output $@ -32 -format VHDL

#SPICE Power
power_spice: 
	$(eval TIME_POWER_SPICE := $(shell date +%s%3N))
ifeq ($(ENABLE_DC),True)
	$(MAKE) power_spice_dc
else
	echo "DesignCompiler disabled"
endif	
ifeq ($(ENABLE_PRIMETIME),True)
	$(MAKE) power_spice_pt_avg
	$(MAKE) power_spice_pt_tim
else
	echo "PrimeTime disabled"
endif
	./scripts/timing.sh $@ ${TIME_POWER_SPICE} 
	
power_spice_dc:
	$(eval TIME_POWER_SPICE_DC := $(shell date +%s%3N))
	$(MAKE) ${POWER_OUTPUT_DIR}/sim_spice_dc.power
	./scripts/timing.sh $@ ${TIME_POWER_SPICE_DC} 

power_spice_pt_avg:
	$(eval TIME_POWER_SPICE_PT_AVG := $(shell date +%s%3N))
	$(MAKE) ${POWER_OUTPUT_DIR}/sim_spice_pt.avg.power 
	./scripts/timing.sh $@ ${TIME_POWER_SPICE_PT_AVG} 

power_spice_pt_tim:
	$(eval TIME_POWER_SPICE_PT_TIM := $(shell date +%s%3N))
	$(MAKE) ${POWER_OUTPUT_DIR}/sim_spice_pt.tim.power 
	./scripts/timing.sh $@ ${TIME_POWER_SPICE_PT_TIM} 


#SPICE Design Compiler Power
${POWER_OUTPUT_DIR}/sim_spice_dc.power: ${POWER_OUTPUT_DIR}/spice_dc.scr
	dc_shell -f $< > $@	
ifneq ($(MAKEFILE_PRINT_INFO),False) 
	tail -n 16 $@ | head -n 13
endif
	mv -f command.log ${POWER_OUTPUT_DIR}/command_spice_dc.log
	mv -f default.svf ${POWER_OUTPUT_DIR}/default_spice_dc.svf

${POWER_OUTPUT_DIR}/spice_dc.scr: ${POWER_OUTPUT_DIR}/spice.saif ./scripts/templateDesignCompilerScr
	sed 's/##verilogFileName##/${VERILOG_FILE}/g' ./scripts/templateDesignCompilerScr | \
	sed 's@##inputFileName##@$<@g' | \
	sed "s@##topDir##@${TOP_DIR}@g" | \
	sed "s@##simLinkLibrary##@${SIM_LINK_LIBRARY}@g" | \
	sed "s@##simTargetLibrary##@${SIM_TARGET_LIBRARY}@g" | \
	sed "s@##simSearchPath##@${SIM_SEARCH_PATH}@g" | \
	sed "s@##simLinkPath##@${SIM_LINK_PATH}@g" | \
	sed "s@##simDBName##@${SIM_DB_NAME}@g" | \
	sed "s@##spefFileName##@${SPEF_FILE_NAME}@g" | \
	sed 's%##circuitName##%toplevel%g' > $@


#SPICE PrimeTime Power
${POWER_OUTPUT_DIR}/sim_spice_pt.avg.power: ${POWER_OUTPUT_DIR}/spice_pt.avg.scr
	pt_shell -file $< > $@
	mv -f pt_shell_command.log ${POWER_OUTPUT_DIR}/pt_shell_command_spice_pt.avg.log
	[ ! -f parasitics_command.log ] || mv -f parasitics_command.log ${POWER_OUTPUT_DIR}/parasitics_command_spice_pt.avg.log
	
${POWER_OUTPUT_DIR}/sim_spice_pt.tim.power: ${POWER_OUTPUT_DIR}/spice_pt.tim.scr
	pt_shell -file $< > $@
	mv -f pt_shell_command.log ${POWER_OUTPUT_DIR}/pt_shell_command_spice_pt.tim.log
	[ ! -f primetime_px.fsdb ] || mv -f primetime_px.fsdb ${POWER_OUTPUT_DIR}/primetime_px_spice_pt.tim.fsdb	
	[ ! -f parasitics_command.log ] || mv -f parasitics_command.log ${POWER_OUTPUT_DIR}/parasitics_command_spice_pt.tim.log
	
${POWER_OUTPUT_DIR}/spice_pt.%.scr: ${POWER_OUTPUT_DIR}/spice.saif ${POWER_OUTPUT_DIR}/main_new_exp.vcd0 ./scripts/templatePrimetime%Scr
	sed 's/##verilogFileName##/${VERILOG_FILE}/g' ./scripts/templatePrimetime$*Scr | \
	sed 's@##inputFileName##@$<@g' | \
	sed 's@##vcdFileName##@$(word 2,$^)@g' | \
	sed "s@##topDir##@${TOP_DIR}@g" | \
	sed "s@##simLinkLibrary##@${SIM_LINK_LIBRARY}@g" | \
	sed "s@##simTargetLibrary##@${SIM_TARGET_LIBRARY}@g" | \
	sed "s@##simSearchPath##@${SIM_SEARCH_PATH}@g" | \
	sed "s@##simLinkPath##@${SIM_LINK_PATH}@g" | \
	sed "s@##simDBName##@${SIM_DB_NAME}@g" | \
	sed "s@##spefFileName##@${SPEF_FILE_NAME}@g" | \
	sed 's%##circuitName##%toplevel%g' > $@
		
# General SPICE Power
${POWER_OUTPUT_DIR}/spice.saif: ${POWER_OUTPUT_DIR}/main_new_exp.vcd0	
	vcd2saif -input $< -output $@ -32 -format VHDL	
	
${POWER_OUTPUT_DIR}/main_new_exp.vcd0: ${SPICE_OUTPUT_DIR}/main_new_exp.vcd0
	mkdir -p ${POWER_OUTPUT_DIR}
	python3 ./python/convertVCD.py ${SPICE_OUTPUT_DIR}/main_new_exp.vcd0 $@ ${TOP_DIR}/${MATCHING_FILE}
	
#### REPORT  #############################################################
report: 
	./scripts/reporting.sh

#### PREPARE GIDM  #######################################################
prepare_gidm: 
	python3 ./python/extractCircuitStructure.py ${TOP_DIR}/${SDF_FILE} ${TOP_DIR}/${STRUCTURE_FILE}
	# TOOD: We need to run extendVerilogCircuit (only rename the gates)
	# TODO: We need to generate a matching between instance name and signal name for the post processing
ifeq ($(CIRCUIT_FILE_TYPE),verilog)
	python3 ./python/extendCircuitVerilog.py ${TOP_DIR}/${CIRCUIT_FILE} ${TOP_DIR}/${CIRCUIT_FILE_GIDM} "${REQUIRED_GATES}" "${INPUT_NAMES}" ${TOP_DIR}/${STRUCTURE_FILE} ${TOP_DIR}/port_to_signal_matching.json
else
	echo "Automatic extension of the circuit for VHDL not supported yet"
endif
	python3 ./python/convertSDFFileGIDM.py  ${TOP_DIR}/${SDF_FILE} ${TOP_DIR}/${SDF_FILE_GIDM} "${REQUIRED_GATES}"

clear_results:
	python3 ./python/clearResults.py ../circuits

  
#### CLEAN  ###############################################################  
clean: 
	rm -rf ${GEN_OUTPUT_DIR}/main_new_exp.sp ${GEN_OUTPUT_DIR}/waveform.json
	rm -rf ${SPICE_OUTPUT_DIR}/*.tr0 ${SPICE_OUTPUT_DIR}/*.st0 ${SPICE_OUTPUT_DIR}/*.mt0 ${SPICE_OUTPUT_DIR}/*.lis ${SPICE_OUTPUT_DIR}/*.ic0 ${SPICE_OUTPUT_DIR}/*.vcd* ${SPICE_OUTPUT_DIR}/*.printtr0 ${SPICE_OUTPUT_DIR}/*.json SPICE_OUTPUT_DIR}/*.srf ${SPICE_OUTPUT_DIR}/*.raw ${SPICE_OUTPUT_DIR}/*.measure ${SPICE_OUTPUT_DIR}/*.log
	rm -rf ${CROSSINGS_OUTPUT_DIR}/crossings.json
	rm -rf ${VECTOR_OUTPUT_DIR}/vectors_*
	rm -rf ${TT_OUTPUT_DIR}/*
	rm -rf ${MODELSIM_OUTPUT_DIR}/work ${MODELSIM_OUTPUT_DIR}/transcript ${MODELSIM_OUTPUT_DIR}/*.log ${MODELSIM_OUTPUT_DIR}/*.do ${MODELSIM_OUTPUT_DIR}/localDoTemplate ${MODELSIM_OUTPUT_DIR}/*.vcd ${MODELSIM_OUTPUT_DIR}/circuit_involution.vhd ${MODELSIM_OUTPUT_DIR}/circuit_modelsim.vhd
	rm -rf ${POWER_OUTPUT_DIR}/*.saif ${POWER_OUTPUT_DIR}/*.scr ${POWER_OUTPUT_DIR}/*.power ${POWER_OUTPUT_DIR}/*.svf ${POWER_OUTPUT_DIR}/*.log ${POWER_OUTPUT_DIR}/*.vcd0 ${POWER_OUTPUT_DIR}/*.fsdb
	rm -rf ${FIGURE_OUTPUT_DIR}/*.png
	rm -rf ${GATES_DIR}/*.vhd
	rm -rf ${TOP_DIR}/perf/*
	rm -rf ${RESULT_OUTPUT_DIR}/variables.tex ${RESULT_OUTPUT_DIR}/results.json ${RESULT_OUTPUT_DIR}/waveform_table.temp
