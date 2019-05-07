.PHONY: all sim report clean

MAKEFLAGS += ${MAKEFILE_ARGS}

include ./multi_exec.cfg
include ${ME_CIRCUIT_UNDER_TEST}/config.cfg
include ./multi_exec.cfg # override settings from circuit if necessary (PRINT_LEVEL, ...)

all:
	$(MAKE) sim
	$(MAKE) report
	
sim: 
	python multiExec.py ${ME_CONFIG_FILE}
	
report: 
	./multi_reporting.sh
	
clean:
	rm -rf temp/*