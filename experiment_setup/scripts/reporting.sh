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
python2.6 ./python/parseMeasureFile.py ${REPORT_CONFIG} ${SPICE_OUTPUT_DIR} ${TARGET_FOLDER}/results.json SPICE
python2.6 ./python/parsePowerFile.py 0 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_spice_dc.power ${TARGET_FOLDER}/results.json SPICE_DC
python2.6 ./python/parsePowerFile.py 0 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_modelsim_dc.power ${TARGET_FOLDER}/results.json MODELSIM_DC
python2.6 ./python/parsePowerFile.py 0 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_involution_dc.power ${TARGET_FOLDER}/results.json INVOLUTION_DC
python2.6 ./python/parsePowerFile.py 1 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_spice_pt.avg.power ${TARGET_FOLDER}/results.json SPICE_PT_AVG
python2.6 ./python/parsePowerFile.py 1 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_modelsim_pt.avg.power ${TARGET_FOLDER}/results.json MODELSIM_PT_AVG
python2.6 ./python/parsePowerFile.py 1 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_involution_pt.avg.power ${TARGET_FOLDER}/results.json INVOLUTION_PT_AVG
python2.6 ./python/parsePowerFile.py 2 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_spice_pt.tim.power ${TARGET_FOLDER}/results.json SPICE_PT_TIM
python2.6 ./python/parsePowerFile.py 2 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_modelsim_pt.tim.power ${TARGET_FOLDER}/results.json MODELSIM_PT_TIM
python2.6 ./python/parsePowerFile.py 2 ${REPORT_CONFIG} ${POWER_OUTPUT_DIR}/sim_involution_pt.tim.power ${TARGET_FOLDER}/results.json INVOLUTION_PT_TIM
./scripts/timing.sh "report_PARSE" ${TIME_REPORT_SUB} 

# Calculate deviations from reference value (SPICE)
TIME_REPORT_SUB=$(date +%s%3N)
python2.6 ./python/prepareDeviation.py ${TARGET_FOLDER}/results.json
./scripts/timing.sh "report_PREPARE_DEVIATION" ${TIME_REPORT_SUB} 

# Add configuration to results.json and store configuration in output folder
TIME_REPORT_SUB=$(date +%s%3N)
python2.6 ./python/printEnvironmentVars.py ${REPORT_CONFIG} ${TARGET_FOLDER}/results.json ENV
python2.6 ./python/printCWG.py ${WAVEFORM_GENERATION_CONFIG_DIR}/generate.json ${TARGET_FOLDER}/results.json CWG
cp ${WAVEFORM_GENERATION_CONFIG_DIR}/generate.json ${TARGET_FOLDER}/generate.json
python2.6 ./python/combineGateGeneration.py ${GENERAL_GATE_CONFIG_DIR}/gate_config.json ${CIRCUIT_GATE_CONFIG_DIR}/gate_config.json ${TARGET_FOLDER}/gate_config.json
cp ${GEN_OUTPUT_DIR}/waveform.json ${TARGET_FOLDER}/waveform.json
./scripts/timing.sh "report_CONFIGURATION" ${TIME_REPORT_SUB} 

# Prepare figures, parse data and store to results.json
TIME_REPORT_SUB=$(date +%s%3N)
cp ./tex/waveform.tex ${TARGET_FOLDER}/waveform.tex	
python2.6 ./python/prepareFigureData.py ${START_OUT_NAME} ${CROSSINGS_OUTPUT_DIR}/crossings.json ${MODELSIM_OUTPUT_DIR}/involution.vcd ${MODELSIM_OUTPUT_DIR}/modelsim.vcd ${TOP_DIR}/${MATCHING_FILE} ${TARGET_FOLDER}/fig/ ${TARGET_FOLDER}/waveform.tex	${TARGET_FOLDER}/results.json "{%##NAME##%} & \num{%##TC_SPICE##%} & \num{%##TC_INVOLUTION##%} & \num{%##TC_MSIM##%} & \num{%##TOTAL_AREA_UNDER_DEV_TRACE_INV##%} & \num{%##TOTAL_AREA_UNDER_DEV_TRACE_MSIM##%} & \num{%##GLITCHES_SPICE_INV##%} / \num{%##GLITCHES_INV##%} & \num{%##GLITCHES_SPICE_MSIM##%} / \num{%##GLITCHES_MSIM##%} \\\\"
./scripts/timing.sh "report_WAVEFORM" ${TIME_REPORT_SUB} 

# Prepare the different parts of the Tex-report
TIME_REPORT_SUB=$(date +%s%3N)
python2.6 ./python/prepareFigure.py ${TARGET_FOLDER}/plot.tex ./tex/figure_group_template.tex ./tex/figure_template.tex ${REPORT_CONFIG}
python2.6 ./python/prepareSchematic.py ${TARGET_FOLDER}/schematic.tex ./tex/schematic.tex ${REPORT_CONFIG}
cp ./tex/cwg.tex ${TARGET_FOLDER}/cwg.tex
cp ./tex/basic.tex ${TARGET_FOLDER}/basic.tex
python2.6 ./python/prepareCWG.py ${WAVEFORM_GENERATION_CONFIG_DIR}/generate.json ${TARGET_FOLDER}/cwg.tex ./tex/cwg_group.tex 
python2.6 ./python/prepareGates.py ${GENERAL_GATE_CONFIG_DIR}/gate_config.json ${CIRCUIT_GATE_CONFIG_DIR}/gate_config.json ./tex/gate_config.tex ${TARGET_FOLDER}/gate_config.tex "${REQUIRED_GATES}"
sed 's@%##VARIABLES##%@\\\input{variables.tex}@g' ./tex/report_single.tex  | \
sed 's@%##WAVEFORM##%@\\\input{waveform.tex}@g' | \
sed 's@%##SCHEMATIC##%@\\\input{schematic.tex}@g' | \
sed 's@%##CWG##%@\\\input{cwg.tex}@g' | \
sed 's@%##GATE_CONFIGURATION##%@\\\input{gate_config.tex}@g' | \
sed 's@%##BASIC##%@\\\input{basic.tex}@g' | \
sed 's@%##PLOT##%@\\\input{plot.tex}@g' > ${TARGET_FOLDER}/report_single.tex


# finally convert the results.json file to a "Tex-readable" version
python2.6 ./python/generateReportVars.py ${TARGET_FOLDER}/results.json ${TARGET_FOLDER}/variables.tex
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

#pdflatex ${TARGET_FOLDER}/report_single.tex # Not available on asic - Server