#!/bin/sh

echo ${RESULT_OUTPUT_DIR}
echo ${ME_REPORT_FOLDER}

# variables for the target folder
export TARGET_FOLDER=${RESULT_OUTPUT_DIR}/${ME_REPORT_FOLDER}/multi_report/

# remove "old" multi report folder, if it exists and create new empty folder
rm -rf directoryname ${TARGET_FOLDER}
mkdir ${TARGET_FOLDER}


# prepare variables (copy, min, max, avg)
python3 multiReportVars.py

# Prepare the different parts of the Tex-report
python3 prepareConfiguration.py
python3 prepareWaveformComparison.py waveform_comparison.tex "{%##NAME##%} & \num{%##MSIM_REL##%} & \num{%##MSIM_ABS##%} & \num{%##MSIM_SUM##%} & \num{%##GLITCHES_SPICE_MSIM##%} / \num{%##GLITCHES_MSIM##%} & \num{%##INV_REL##%} & \num{%##INV_ABS##%} & \num{%##INV_SUM##%} & \num{%##GLITCHES_SPICE_INV##%} / \num{%##GLITCHES_INV##%}\\\\"
python3 ${EXPERIMENT_SETUP_DIR}/python/prepareSchematic.py ${TARGET_FOLDER}/schematic.tex ${EXPERIMENT_SETUP_DIR}/tex/schematic.tex ${REPORT_CONFIG}
cp ${EXPERIMENT_SETUP_DIR}/tex/basic.tex ${TARGET_FOLDER}/basic.tex
python3 rankingTables.py ranking.tex "{%##NAME##%} & \num{%##VALUE##%}"

sed 's@%##VARIABLES##%@\\\input{variables.tex}@g' report_multi.tex  | \
sed 's@%##BASIC##%@\\\input{basic.tex}@g' | \
sed 's@%##CONFIGURATION##%@\\\input{configuration.tex}@g' | \
sed 's@%##WAVEFORM##%@\\\input{waveform_comparison.tex}@g' | \
sed 's@%##RANKING##%@\\\input{ranking.tex}@g' | \
sed 's@%##SCHEMATIC##%@\\\input{schematic.tex}@g' > ${TARGET_FOLDER}/report_multi.tex

# finally convert the results.json file to a "Tex-readable" version
python3 ${EXPERIMENT_SETUP_DIR}/python/generateReportVars.py ${TARGET_FOLDER}/results.json ${TARGET_FOLDER}/variables.tex

#pdflatex ${TARGET_FOLDER}/report_multi.tex # Not available on asic - Server

# also export into csv, values in the report can be easily checked, sorted, ...
python3 export.py

# Store multi_exec configuration values (for better traceability)
cp ./multi_exec.cfg ${TARGET_FOLDER}/multi_exec.cfg
cp ./multi_exec.json ${TARGET_FOLDER}/multi_exec.json