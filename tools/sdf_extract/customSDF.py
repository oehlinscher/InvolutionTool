"""
    
	Involution Tool
	File: customSDF.py
	
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

import sys
import json
sys.path.append('../../experiment_setup/python')

if len(sys.argv) < 4:
    print("provide json and sdf input and output file")
    sys.exit(1)

with open(sys.argv[2]) as f:
    crossings = json.load(f)

f = open(sys.argv[1])
fout = open(sys.argv[3],'w')

matchings={}
crossingsName = {"clk":"clk", "din":"din"}

lines = f.readlines()
instName = ""
for line in lines:
    if line.count('TIMESCALE') > 0:
        parts = line.split(' ')
        parts[4] ="ps)\n"
        fout.write(' '.join(parts))
    elif line.count('INTERCONNECT') > 0:       
        parts = line.split(' ')
        parts[4] = '(0.000::0.000)'
        parts[5] = '(0.000::0.000))\n'
        fout.write(' '.join(parts))

        if parts[2].count('/') > 0:
            dest = parts[2][:parts[2].rfind('/')]
            out = "Xmycir."+ dest
        else:
            dest = parts[2]
            if dest== "clk":
                out = dest
            else:
                out = "Xmycir." + dest
            
        if parts[1].count('/') > 0:
            src = parts[1][:parts[1].rfind('/')]
        else:
            src = parts[1]


        if src.startswith("memdata"):
            continue
            
        matchings[dest] = src
        crossingsName[dest] = out
        
    elif line.count('INSTANCE ') > 0:
        instName = line.split(' ')[-1][:-2]
        fout.write(line)
    elif line.count('IOPATH ') > 0:

        if not instName in matchings.keys():
            fout.write(line)
            continue
        
        for name in crossings['crossing_times'].keys():
            if name.startswith(crossingsName[instName]):
                outTrans=crossings['crossing_times'][name]

            if name.startswith(crossingsName[matchings[instName]]):
                inTrans=crossings['crossing_times'][name]

        firstVal = (outTrans[0]- inTrans[0])*1e12
        secondVal = (outTrans[1]- inTrans[1])*1e12

        parts = line.split(' ')

        for name in crossings['crossing_times'].keys():
            if name.startswith(crossingsName[instName]):
        
                if crossings['initial_values'][name] == 0:
                    parts[4] = "(%.6f::%.6f)"%(firstVal, firstVal)
                    parts[5] = "(%.6f::%.6f))\n"%(secondVal,secondVal)
                else:
                    parts[4] = "(%.6f::%.6f)"%(secondVal,secondVal)
                    parts[5] = "(%.6f::%.6f))\n"%(firstVal, firstVal)
                break
            
        fout.write(' '.join(parts))
    else:
        fout.write(line)

#print(matchings)
#print(crossingsName)
