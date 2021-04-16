"""
    
	Involution Tool
	File: generateTrace.py
	
    Copyright (C) 2018-2020  Daniel OEHLINGER <d.oehlinger@outlook.com>

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
import os
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import operator
sys.path.append('../../experiment_setup/python')
from helper import *
from fixGIDMVCD import read_signal_transitions

V_DD = 1.0
V_TH = 0.5
V_SS = 0.0

def main():
    if len(sys.argv) == 3:
        generate_trace(sys.argv[1], sys.argv[2], None)
    elif len(sys.argv) == 4:
        generate_trace(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        # python generateTrace.py g10ZN.complete '[["f_sumexp_up.dat","f_sumexp_down.dat", "sumexp"], ["f_exp_up.dat", "f_exp_down.dat", "exp"]]' temp.png
        # python generateTrace.py g10ZN.complete '[["f_sumexp_up.dat","f_sumexp_down.dat", "sumexp"], ["f_exp_up.dat", "f_exp_down.dat", "exp"], ["f_real_up.dat","f_real_down.dat","real"]]' temp.png
        my_print("usage: python generateTrace.py tt_file_path frsws plot_file_path", EscCodes.FAIL)
        sys.exit(1)



def generate_trace(tt_file_path, frsws, plot_file_path):
    # frsw_up = np.fromfile(f_up_filepath)
    # frsw_down = np.fromfile(f_down_filepath)
    
    frsws = json.loads(frsws)

    signal_transitions = read_signal_transitions(tt_file_path) # The time is here in fs

    plt.axhline(y=V_TH, color='black', linestyle=":")
    for trans in signal_transitions:
        color = None
        if trans[1] == 1:
            color = 'red'
        else:
            color = 'blue'
        plt.axvline(x=trans[0] * 1e-15 , ymin=V_SS, ymax=V_DD, color=color, linestyle="--", alpha=0.4)

    for frsw in frsws:
        f_up_filepath = frsw[0]
        f_down_filepath = frsw[1]
        label = frsw[2]
        waveform = generate_waveform(f_up_filepath, f_down_filepath, signal_transitions)
        plt.plot(waveform[:,0], waveform[:,1], label=label)

    plt.legend(loc='upper right')
    plt.show()
    if plot_file_path is not None:        
        plt.savefig(plot_file_path)

def generate_waveform(f_up_filepath, f_down_filepath, signal_transitions):

    frsw_up = np.loadtxt(f_up_filepath, comments="#")
    frsw_down = np.loadtxt(f_down_filepath, comments="#")
    
    # waveform = np.array(frsw_up)
    # plt.plot(waveform[:,0], waveform[:,1])    
    # waveform = np.array(frsw_down)
    # plt.plot(waveform[:,0], waveform[:,1])
    # plt.show()

    start_idx = 0
    end_idx = None
    waveform = []

    # Calculate the middle_idx and the middle_time for both FRSW
    (up_middle_idx, up_middle_time) = calc_middle(frsw_up, 0, 1)
    (down_middle_idx, down_middle_time) = calc_middle(frsw_down, len(frsw_down)-1, -1)

    for idx in range(len(signal_transitions)):
        first_trans = signal_transitions[idx]
        snd_trans = None
        if idx+1 >= len(signal_transitions):
            # Edge case for last transition with no predecessor
            # inverse value and far away...
            snd_trans = [first_trans[0]*10, 1-first_trans[1]] 
        else:
            snd_trans = signal_transitions[idx+1]

        # need some preprocssing, so that we have the data in s and not in fs
        first_trans_time = first_trans[0] * 1e-15
        snd_trans_time = snd_trans[0] * 1e-15


        assert first_trans[1] != snd_trans[1] # they must have different levels
        op = None
        if first_trans[1] == 0:
            # we have a falling followed by rising
            first_frsw = frsw_down
            snd_frsw = frsw_up
            first_middle_idx = down_middle_idx
            snd_middle_idx = up_middle_idx
            first_middle_time = down_middle_time
            op = operator.gt
        else:
            # we have a rising followed by falling
            first_frsw = frsw_up
            snd_frsw = frsw_down
            first_middle_idx = up_middle_idx
            snd_middle_idx = down_middle_idx
            first_middle_time = up_middle_time
            op = operator.lt

        (end_idx, new_start_idx) = calc_crossing_idx(first_frsw, snd_frsw, first_trans_time, snd_trans_time, first_middle_idx, snd_middle_idx, op)
        
        # start_time = first_trans_time - first_middle_time + first_frsw[start_idx][0]
        # end_time = first_trans_time - first_middle_time + first_frsw[end_idx][0]
        # print(start_time, end_time)

        for idx in range(start_idx, end_idx):
            waveform.append([first_trans_time - first_middle_time + first_frsw[idx][0], first_frsw[idx][1]])

        start_idx = new_start_idx

    waveform = np.array(waveform)
    return waveform

def calc_middle(frsw, start, inc):
    idx = start
    while frsw[idx][1] < V_TH:
        idx = idx + inc
    # We assume that the precision is high enough, so we do not make any special kind of round.
    # I think this is a reasonable assumption, since we only plot the data, and therefore the precision should be sufficient
    return (idx, frsw[idx][0])

def calc_crossing_idx(first_frsw, snd_frsw, first_time, snd_time, first_middle_idx, snd_middle_idx, op):    
    cur_first_time = 0
    cur_snd_time = 0
    first_idx = first_middle_idx
    snd_idx = snd_middle_idx

    if first_time < snd_time:
        # Non cancelling transitions
        # first goes fwd in time, snd goes back in time
        while cur_first_time + cur_snd_time < snd_time - first_time:
            if op(first_frsw[first_idx][1], snd_frsw[snd_idx][1]):
                if (first_idx + 1 >= len(first_frsw)):
                    break
                first_idx += 1
                cur_first_time += first_frsw[first_idx][0] - first_frsw[first_idx-1][0]
            else:
                if (snd_idx == 0):
                    break
                snd_idx -= 1
                cur_snd_time += snd_frsw[snd_idx+1][0] - snd_frsw[snd_idx][0]
    else:     
        # Cancelling transition   
        # first goes back in time, snd goes fwd in time
        while cur_first_time + cur_snd_time < first_time - snd_time:
            if op(snd_frsw[snd_idx][1], first_frsw[first_idx][1]):
                if (first_idx == 0):
                    break
                first_idx -= 1
                cur_first_time += first_frsw[first_idx+1][0] - first_frsw[first_idx][0]
            else:
                if (snd_idx + 1 == len(snd_frsw)):
                    break
                snd_idx += 1
                cur_snd_time += snd_frsw[snd_idx][0] - snd_frsw[snd_idx-1][0]

    return first_idx, snd_idx


if __name__ == "__main__":
    main()