"""
    @file simulate.py

	@brief Script for simulating the hybrid delay model and obtaining 
    MIS delay functions

	@author Daniel OEHLINGER <d.oehlinger@outlook.com>
	@date 2021

	@copyright
	@parblock
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
	@endparblock	
""" 

import matplotlib.pyplot as plt
import numpy as np
import json
import sys

sys.path.append('../../experiment_setup/python')
from helper import *

sys.path.append('../../experiment_setup/vhdl/python_channel')
from hybrid_nor2_delay_channel import *
from python_channel_base import *


def main():
    v_dd = 0.8
    v_th = 0.4

    fitting_folder = "../../circuits/nor_gate_15nm/hm_fitting/"
    postfix = "_with_dmin"

    fitting_result_file = fitting_folder + 'fitting_result' + postfix + '.json'

    # For falling output
    lvl_old = std_logic_t.STD_LOGIC_0
    lvl_new = std_logic_t.STD_LOGIC_1
    v_int_init = v_dd
    v_out_init = v_dd
    use_first = True
    fig_name = fitting_folder + 'ode_falling_output' + postfix + '.png'
    data_file = fitting_folder + 'ode_falling_output' + postfix + '.data'
    simulate(v_dd, v_th, lvl_old, lvl_new, v_int_init, v_out_init, use_first, fig_name, data_file, fitting_result_file)

    # For rising output
    lvl_old = std_logic_t.STD_LOGIC_1
    lvl_new = std_logic_t.STD_LOGIC_0
    v_int_init = 0
    v_out_init = 0
    use_first = False
    fig_name = fitting_folder + 'ode_rising_output' + postfix + '.png'
    data_file = fitting_folder + 'ode_rising_output' + postfix + '.data'
    simulate(v_dd, v_th, lvl_old, lvl_new, v_int_init, v_out_init, use_first, fig_name, data_file, fitting_result_file)

def simulate(v_dd, v_th, lvl_old, lvl_new, v_int_init, v_out_init, use_first, fig_name, data_file, fitting_result_file):   

    with open(fitting_result_file) as json_file:
        r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay = json.load(json_file)

    print(r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay)

    delta_start = -200000 # fs
    delta_end = 200000 # fs
    step_size = 500 # fs

    pure_delay = pure_delay * 1e15

    current_delta = delta_start

    deltas = list()
    delays = list()

    while current_delta <= delta_end:
        print("----------------------------------")
        # print("Current delta: ", current_delta)
        
        now = step_size
        v_int = v_int_init
        v_out = v_out_init
        delay = 0
        
        if current_delta > 0:         
            # if delta is positive, A goes first, than B
            (delay_first, delay_first_valid, _, _, v_int, v_out) = calculate_delay_hybrid_nor2(lvl_old, lvl_old, lvl_new, lvl_old, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay, v_dd, v_th, now, True, 0, v_int, v_out)
            print("A, B, First trans: ", delay_first, delay_first_valid, v_int, v_out, now)
            
            # now, we increase the time with delta
            last_input_switch_time = now
            now = now + abs(current_delta)
            (delay_snd, delay_snd_valid, _, _, v_int, v_out) = calculate_delay_hybrid_nor2(lvl_new, lvl_old, lvl_new, lvl_new, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay, v_dd, v_th, now, False, last_input_switch_time, v_int, v_out)
            # print("Snd trans: ", delay_snd, delay_snd_valid, v_int, v_out, now)

            print("A, B, Delays: ", delay_first, delay_first_valid, delay_snd, delay_snd_valid)

            if delay_snd_valid:
                if use_first:
                    delay = abs(current_delta) + delay_snd
                else:
                    delay = delay_snd
            elif delay_first_valid:
                assert(use_first)
                delay = delay_first
            else:
                assert(False)    

        elif current_delta == 0:
            # both go at the same time
            (delay, _, _, _, _, _) = calculate_delay_hybrid_nor2(lvl_old, lvl_old, lvl_new, lvl_new, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay, v_dd, v_th, now, True, 0, v_int, v_out)

        else:
            # B goes first, than A
            (delay_first, delay_first_valid, _, _, v_int, v_out) = calculate_delay_hybrid_nor2(lvl_old, lvl_old, lvl_old, lvl_new, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay, v_dd, v_th, now, True, 0, v_int, v_out)
            print("B, A, First trans: ", delay_first, delay_first_valid, v_int, v_out, now)
            
            # now, we increase the time with delta
            last_input_switch_time = now
            now = now + abs(current_delta)
            (delay_snd, delay_snd_valid, _, _, v_int, v_out) = calculate_delay_hybrid_nor2(lvl_old, lvl_new, lvl_new, lvl_new, r_1, r_2, r_3, r_4, c_int, c_out, scale_1, pure_delay, v_dd, v_th, now, False, last_input_switch_time, v_int, v_out)
            # print("Snd trans: ", delay_snd, delay_snd_valid, v_int, v_out, now)

            print("B, A, Delays: ", delay_first, delay_first_valid, delay_snd, delay_snd_valid)

            if delay_snd_valid:
                if use_first:
                    delay = abs(current_delta) + delay_snd
                else:
                    delay = delay_snd
            elif delay_first_valid:
                assert(use_first)
                delay = delay_first
            else:
                assert(False)  

        print("Current delta: {current_delta}, Delay: {delay}".format(current_delta = current_delta, delay = delay))


        deltas.append(current_delta)
        delays.append(delay)

        
        current_delta = current_delta + step_size

    # print(deltas)
    # print(delays)

    deltas = np.array(deltas) * 1e-15
    delays = np.array(delays) * 1e-15

    plt.figure()
    plt.plot(deltas, delays, marker='X')
    plt.xlabel('$t_B - t_A [s]$')
    plt.ylabel('$Delay [s]$')
    # plt.show()


    plt.savefig(fig_name)

    data = np.array([deltas, delays])
    np.savetxt(data_file, data)


if __name__ == "__main__":
    main()