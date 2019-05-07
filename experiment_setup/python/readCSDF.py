"""
    
	Involution Tool
	File: readCSDF.py
	
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

# -*- coding: utf-8 -*-
#encoding: utf-8

import sys
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math
from operator import itemgetter
import re
from helper import *

#********************************************************************************

def read_file (filepath):
	# dictionary containing the data in the following format
	# Key = Name of the signal
	# Value = Array containing the data
	data= {}
	
	my_print('Filepath: {0}'.format(filepath))
	
	f=open(filepath, 'r')
	total_line_nr = sum(1 for line in open(filepath))
	current_line_nr = 0
	varCnt = 0
	# find out the number of nodes:
	while True:
		line = f.readline()
		current_line_nr += 1
		if line.startswith('NODES='):
			#pprint(line)
			varcnt = re.search(r'\d+', line).group()
			my_print('Number of signals found (without time): ' + varcnt)
			break;

	# find out the name of the signals, and create dictionary
	foundNames = False
	indexToSignalMapping = [None] * (int(varcnt)+1)
	signalIndex = 1
	while True:
		line = f.readline()		
		current_line_nr += 1
		if line.startswith('#C'):
			if not foundNames:
				my_print('Did not find signal names')
			break;
		if line.startswith('#N'):
			foundNames = True
			my_print('Found the start symbol for the signal names')
		if foundNames: 		
			# add the time column
			data['time'] = []
			indexToSignalMapping[0] = 'time'
		
			# Regex designed with regex101.com
			signalRegex = re.compile(r"\'\w+\(([\w\:\.\)\(\/]+)\)\'")
			matches = re.finditer(signalRegex, line)
			for matchNum, match in enumerate(matches):
				matchNum = matchNum + 1
    
				my_print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
				
				for groupNum in range(0, len(match.groups())):
					groupNum = groupNum + 1
			
					my_print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
					
					signalName = match.group(groupNum)
					data[signalName] = []
					my_print('Adding signal: {0} at index: {1}'.format(signalName, signalIndex))
					indexToSignalMapping[signalIndex] = signalName
										
					signalIndex += 1
					
				
    		
	my_print('We parsed the signal names')		
	#pprint(indexToSignalMapping)
	#pprint(data.keys())
	
	#for x in range(0,19):
	#	pprint(indexToSignalMapping[x])

	# Now iterate over all lines, starting with #C, and add the values to the dictionary
	signalIndex = 0
	dataRegex = r"[\+\-]?\d\.\d+e[\+\-]?\d+"
	while True:
		if line.startswith('#;'):
			break;
		if line.startswith('#C'):
			signalIndex = 0
			
		#if (current_line_nr % 250000) == 0:
		#	print("CROSSINGS: Line number {0} of {1}, percent: {2:.2f}".format(current_line_nr, total_line_nr, float(current_line_nr) / float(total_line_nr) * 100))
			
		matches = re.finditer(dataRegex, line)
		
		for matchNum, match in enumerate(matches):
			matchNum = matchNum + 1		
			
			my_print("SignalIndex: {0}, indexToSignalMapping: {1}".format(signalIndex, indexToSignalMapping[signalIndex]))
			
			data[indexToSignalMapping[signalIndex]].append(float(match.group()))
			
			signalIndex += 1	
		
		line = f.readline()		
		current_line_nr	+= 1	
	return data
