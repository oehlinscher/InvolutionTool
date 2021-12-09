#!/bin/bash
###############################################################################
#
#	Involution Tool
#	File: reporting.sh
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

TIME_REPORT=$(date +%s%3N)

# variables for the target folder (only required when not called from multi_exec tool, otherwise the multi_exec tool already sets the folder name)
if [ -z "${TARGET_FOLDER}" ]
then
	FOLDER=$(date +%y%m%d_%H%M%S)
    TARGET_FOLDER=${RESULT_OUTPUT_DIR}/${ME_REPORT_FOLDER}/${FOLDER}/
fi

 # required for multi_exec tool, because we need to add more file to the report folder
mkdir -p ${TARGET_FOLDER} 

# Parse the data from the different files and store into results.json
TIME_REPORT_SUB=$(date +%s%3N)
python3 ./python/parseMeasureFile.py ${REPORT_CONFIG} ${SPICE_OUTPUT_DIR} ${TARGET_FOLDER}/results.json SPICE
if [ "$ENABLE_DC" = True ] ; then
	python3 ./python/parsePowerFile.py 0 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_spice_dc.power ${TARGET_FOLDER}/results.json SPICE_DC
	python3 ./python/parsePowerFile.py 0 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_modelsim_dc.power ${TARGET_FOLDER}/results.json MODELSIM_DC
	python3 ./python/parsePowerFile.py 0 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_involution_dc.power ${TARGET_FOLDER}/results.json INVOLUTION_DC
else
	echo "DesignCompiler disabled"
fi

if [ "$ENABLE_PRIMETIME" = True ] ; then
	python3 ./python/parsePowerFile.py 1 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_spice_pt.avg.power ${TARGET_FOLDER}/results.json SPICE_PT_AVG
	python3 ./python/parsePowerFile.py 1 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_modelsim_pt.avg.power ${TARGET_FOLDER}/results.json MODELSIM_PT_AVG
	python3 ./python/parsePowerFile.py 1 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_involution_pt.avg.power ${TARGET_FOLDER}/results.json INVOLUTION_PT_AVG
	python3 ./python/parsePowerFile.py 2 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_spice_pt.tim.power ${TARGET_FOLDER}/results.json SPICE_PT_TIM
	python3 ./python/parsePowerFile.py 2 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_modelsim_pt.tim.power ${TARGET_FOLDER}/results.json MODELSIM_PT_TIM
	python3 ./python/parsePowerFile.py 2 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_involution_pt.tim.power ${TARGET_FOLDER}/results.json INVOLUTION_PT_TIM
else
	echo "PrimeTime disabled"
fi

./scripts/timing.sh "report_PARSE" ${TIME_REPORT_SUB} 

# Calculate deviations from reference value (SPICE)
TIME_REPORT_SUB=$(date +%s%3N)
python3 ./python/prepareDeviation.py ${TARGET_FOLDER}/results.json
./scripts/timing.sh "report_PREPARE_DEVIATION" ${TIME_REPORT_SUB} 

# Add configuration to results.json and store configuration in output folder
TIME_REPORT_SUB=$(date +%s%3N)
python3 ./python/printEnvironmentVars.py ${REPORT_CONFIG} ${TARGET_FOLDER}/results.json ENV
python3 ./python/printCWG.py ${WAVEFORM_GENERATION_CONFIG_DIR}/generate.json ${TARGET_FOLDER}/results.json CWG
cp ${WAVEFORM_GENERATION_CONFIG_DIR}/generate.json ${TARGET_FOLDER}/generate.json
python3 ./python/combineGateGeneration.py ${GENERAL_GATE_CONFIG} ${CIRCUIT_GATE_CONFIG} ${TARGET_FOLDER}/gate_config.json
cp ${GEN_OUTPUT_DIR}/waveform.json ${TARGET_FOLDER}/waveform.json
cp ${WAVEFORM_GENERATION_CONFIG_DIR}/generate.json ${TARGET_FOLDER}/generate.json
python3 ./python/gateGenerationToResults.py ${TARGET_FOLDER}/gate_config.json "${REQUIRED_GATES}" ${TARGET_FOLDER}/results.json GATES
cp ${TOP_DIR}/${STRUCTURE_FILE} ${TARGET_FOLDER}/${STRUCTURE_FILE}
cp ${TOP_DIR}/${SDF_FILE} ${TARGET_FOLDER}/${SDF_FILE}
cp ${TOP_DIR}/${SDF_FILE_GIDM} ${TARGET_FOLDER}/${SDF_FILE_GIDM}
cp ${MODELSIM_OUTPUT_DIR}/involution.vcd ${TARGET_FOLDER}/involution.vcd
if test -f "${MODELSIM_OUTPUT_DIR}/involution_indicators.vcd"; then 
	cp ${MODELSIM_OUTPUT_DIR}/involution_indicators.vcd ${TARGET_FOLDER}/involution_indicators.vcd
fi
cp ${MODELSIM_OUTPUT_DIR}/involution_sim.log ${TARGET_FOLDER}/involution_sim.log
cp ${MODELSIM_OUTPUT_DIR}/modelsim.vcd ${TARGET_FOLDER}/modelsim.vcd
cp ${MODELSIM_OUTPUT_DIR}/modelsim_sim.log ${TARGET_FOLDER}/modelsim_sim.log
cp ${SPICE_OUTPUT_DIR}/main_new_exp.vcd0 ${TARGET_FOLDER}/main_new_exp.vcd0
cp ${CROSSINGS_OUTPUT_DIR}/crossings.json ${TARGET_FOLDER}/crossings.json
if test -f "${TOP_DIR}/${DISCRETIZATION_THRESHOLDS_FILE}"; then 
	cp ${TOP_DIR}/${DISCRETIZATION_THRESHOLDS_FILE} ${TARGET_FOLDER}/${DISCRETIZATION_THRESHOLDS_FILE}
fi
./scripts/timing.sh "report_CONFIGURATION" ${TIME_REPORT_SUB} 

# Prepare figures, parse data and store to results.json
TIME_REPORT_SUB=$(date +%s%3N)
cp ./tex/waveform.tex ${TARGET_FOLDER}/waveform.tex	
python3 ./python/prepareFigureData.py ${START_OUT_NAME} ${CROSSINGS_OUTPUT_DIR}/crossings.json ${MODELSIM_OUTPUT_DIR}/involution.vcd ${MODELSIM_OUTPUT_DIR}/modelsim.vcd ${TOP_DIR}/${MATCHING_FILE} ${TARGET_FOLDER}/fig/ ${TARGET_FOLDER}/waveform.tex	${TARGET_FOLDER}/results.json "{%##NAME##%} & \num{%##TC_SPICE##%} & \num{%##TC_INVOLUTION##%} & \num{%##TC_MSIM##%} & \num{%##TOTAL_AREA_UNDER_DEV_TRACE_INV##%} & \num{%##TOTAL_AREA_UNDER_DEV_TRACE_MSIM##%} & \num{%##GLITCHES_SPICE_INV##%} / \num{%##GLITCHES_INV##%} & \num{%##GLITCHES_SPICE_MSIM##%} / \num{%##GLITCHES_MSIM##%} \\\\"
./scripts/timing.sh "report_WAVEFORM" ${TIME_REPORT_SUB} 

# Prepare the different parts of the Tex-report
TIME_REPORT_SUB=$(date +%s%3N)
python3 ./python/prepareFigure.py ${TARGET_FOLDER}/plot.tex ./tex/figure_group_template.tex ./tex/figure_template.tex ${REPORT_CONFIG}
python3 ./python/prepareSchematic.py ${TARGET_FOLDER}/schematic.tex ./tex/schematic.tex ${REPORT_CONFIG}
cp ./tex/cwg.tex ${TARGET_FOLDER}/cwg.tex
cp ./tex/basic.tex ${TARGET_FOLDER}/basic.tex
python3 ./python/prepareCWG.py ${WAVEFORM_GENERATION_CONFIG_DIR}/generate.json ${TARGET_FOLDER}/cwg.tex ./tex/cwg_group.tex 
python3 ./python/prepareGates.py ${GENERAL_GATE_CONFIG} ${CIRCUIT_GATE_CONFIG} ./tex/gate_config.tex ${TARGET_FOLDER}/gate_config.tex "${REQUIRED_GATES}"
sed 's@%##VARIABLES##%@\\\input{variables.tex}@g' ./tex/report_single.tex  | \
sed 's@%##WAVEFORM##%@\\\input{waveform.tex}@g' | \
sed 's@%##SCHEMATIC##%@\\\input{schematic.tex}@g' | \
sed 's@%##CWG##%@\\\input{cwg.tex}@g' | \
sed 's@%##GATE_CONFIGURATION##%@\\\input{gate_config.tex}@g' | \
sed 's@%##BASIC##%@\\\input{basic.tex}@g' | \
sed 's@%##PLOT##%@\\\input{plot.tex}@g' > ${TARGET_FOLDER}/report_single.tex


# finally convert the results.json file to a "Tex-readable" version
python3 ./python/generateReportVars.py ${TARGET_FOLDER}/results.json ${TARGET_FOLDER}/variables.tex
./scripts/timing.sh "report_MERGE" ${TIME_REPORT_SUB} 

# finalize (possibly) open timers

./scripts/timing.sh "report" ${TIME_REPORT} 
if [ -n "${1}" ]
then
	./scripts/timing.sh "total" ${1} 
fi

# now move the performance report to the report folder
if [ -f ${TOP_DIR}/perf/performance_meassure.txt ]; then
	mv ${TOP_DIR}/perf/performance_meassure.txt ${TARGET_FOLDER}/performance_meassure.txt
fi

if [ -f ${TOP_DIR}/perf/perf.json ]; then
	python ./python/extendResults.py ${TARGET_FOLDER}/results.json ${TOP_DIR}/perf/perf.json 
fi

#pdflatex ${TARGET_FOLDER}/report_single.tex # Not available on asic - Server