"""
    @file generateStimuli.py

	@brief Script for generating the input stimuli for 
    multi input gates. These stimuli can be used to
    determine the MIS effects (delay change over Delta)

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


import random

def main():
    delta_start = -100 # ps
    delta_end = 100 # ps
    step_size = 0.25 # ps 

    wait_time = 4000 # ps
    rise_time = 10 / 2 # ps

    



    # For falling output transitions
    # first_lvl = 0.0
    # snd_lvl = 0.8
    # a_1_input = "0.0ps 0.0"
    # a_2_input = "0.0ps 0.0"
    # current_time = wait_time
    # generate_stimuli(first_lvl, snd_lvl, a_1_input, a_2_input, current_time, delta_start, delta_end, rise_time, wait_time, step_size)

    # For rising output transitions
    first_lvl = 0.8
    snd_lvl = 0.0
    a_1_input = "0.0ps 0.0 995ps 0.0 1005ps 0.8"
    a_2_input = "0.0ps 0.0 995ps 0.0 1005ps 0.8"
    current_time = 1000 + wait_time
    generate_stimuli(first_lvl, snd_lvl, a_1_input, a_2_input, current_time, delta_start, delta_end, rise_time, wait_time, step_size)

def generate_stimuli(first_lvl, snd_lvl, a_1_input, a_2_input, current_time, delta_start, delta_end, rise_time, wait_time, step_size):
    current_delta = delta_start
    while current_delta <= delta_end:
        # print(current_delta)

        first_trans = " {time_1}ps {first_lvl} {time_2}ps {snd_lvl}".format(time_1 = current_time-rise_time, time_2 = current_time+rise_time, first_lvl = first_lvl, snd_lvl = snd_lvl)
        current_time = current_time + abs(current_delta)
        snd_trans = " {time_1}ps {first_lvl} {time_2}ps {snd_lvl}".format(time_1 = current_time-rise_time, time_2 = current_time+rise_time, first_lvl = first_lvl, snd_lvl = snd_lvl)
        current_time = current_time + wait_time
        first_trans = first_trans + " {time_1}ps {snd_lvl} {time_2}ps {first_lvl}".format(time_1 = current_time-rise_time, time_2 = current_time+rise_time, first_lvl = first_lvl, snd_lvl = snd_lvl)
        snd_trans = snd_trans + " {time_1}ps {snd_lvl} {time_2}ps {first_lvl}".format(time_1 = current_time-rise_time, time_2 = current_time+rise_time, first_lvl = first_lvl, snd_lvl = snd_lvl)
        current_time = current_time + wait_time

        if current_delta < 0:
            a_1_input = a_1_input + first_trans
            a_2_input = a_2_input + snd_trans
        else:        
            # Input on A2 first
            a_1_input = a_1_input + snd_trans
            a_2_input = a_2_input + first_trans


        current_delta = current_delta + step_size

    print("VgpwlA1 A1 0 PWL(" + a_1_input + ")")
    print("VgpwlA2 A2 0 PWL(" + a_2_input + ")")


if __name__ == "__main__":
    main()

