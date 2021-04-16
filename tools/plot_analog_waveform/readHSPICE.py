import sys
import os
import matplotlib
#matplotlib.use('PDF')
matplotlib.use('Agg')
#matplotlib.use('pgf')
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import shutil
import pickle

#********************************************************************************

def split_str(seq, length):
    #return [np.float128(seq[i:i+length]) for i in range(0, len(seq), length)]
    # return [float(seq[i:i+length]) for i in range(0, len(seq), length)]
    elements = list()
    for i in range(0, len(seq), int(length)):
        elements.append(float(seq[i:i+int(length)]))
    return elements
"""
    
	Involution Tool
	File: generateTrace.py
	
    Copyright (C) 2018-2020  
    Daniel OEHLINGER <d.oehlinger@outlook.com>
    Juergen MAIER <juergen.maier@tuwien.ac.at>

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



#********************************************************************************
    
def read_hspice(filename, varCnt):
    
    data=[]

    for i in range(varCnt):
        data.append([])

    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # cut first lines, unfortunately not fixed amount, so try splitting on first,
    # if exception thrown remove line
    i = 0
    while(True):
        try:
            fieldCount = lines[0][:-1].count(".")
            fieldLength=len(lines[0][:-1])/fieldCount
            elements = split_str(lines[0][:-1],fieldLength)
            break
        except:
            lines=lines[1:]
        
        i += 1
        
    index=0

    # seperate values in file and move them to their corresponding arrays
    for i in lines:
        fieldCount = i.count(".")
        fieldLength=len(i[:-1])/fieldCount
        elements = split_str(i[:-1],fieldLength)
    
        for k in elements:
            data[index].append(k)
            index = ((index+1)%varCnt)

    minLen = len(data[0])

    # determine length of shortest array
    for i in range(varCnt):
        if (len(data[i]) < minLen):
            minLen = len(data[i])

    # set each array to same length
    for i in range(varCnt):
        data[i] = data[i][:minLen]

    return data
