import matplotlib.pyplot as plt
import numpy as np
import json

def main():

    fitting_folder = "../../circuits/nor_gate_15nm/hm_fitting/"
    in1 = 'A1'
    in2 = 'A2'
    out = 'Z'

    # Falling
    file_name = fitting_folder + "crossings_falling_output.json"
    start = 0
    func = min
    sign = -1 # A1 and A2 are swapped in NOR2_X2.sp compared to our assignment
    func_name = "min"
    fig_name = fitting_folder + "spice_falling_output.png"
    data_file = fitting_folder + "spice_falling_output.data"
    xlim = None
    
    plot_fig(in1, in2, out, file_name, start, func, sign, func_name, fig_name, data_file, xlim)

    # Rising
    file_name = fitting_folder + "crossings_rising_output.json"
    start = 1
    func = max
    sign = 1
    func_name = "max"
    fig_name = fitting_folder + "spice_rising_output.png"
    data_file = fitting_folder + "spice_rising_output.data"
    xlim = None
    
    plot_fig(in1, in2, out, file_name, start, func, sign, func_name, fig_name, data_file, xlim)

def plot_fig(in1, in2, out, file_name, start, func, sign, func_name, fig_name, data_file, xlim):

    middle = (None, None)


    with open(file_name) as json_file:
        data = json.load(json_file)

        assert(len(data['crossing_times'][in1]) == len(data['crossing_times'][in2]))
        assert(len(data['crossing_times'][in2]) == len(data['crossing_times'][out]))

        delta = list()
        delay = list()
        
        for i in range(start, len(data['crossing_times'][in1]), 2):
            time_in1 = data['crossing_times'][in1][i]
            time_in2 = data['crossing_times'][in2][i]
            time_out = data['crossing_times'][out][i]

            delta_ = (time_in2 - time_in1) * sign
            delay_ = time_out - func(time_in1, time_in2)

            if (middle[0] == None or abs(middle[0]) > abs(delta_)):
                middle = (delta_, delay_)

            delta.append(delta_)
            delay.append(delay_)


        # print(data)
        # print(delay)

        # plt.plot(delta, delay, marker='X')
        plt.figure()
        plt.plot(delta, delay)
        plt.xlabel('$t_B - t_A [s]$')
        plt.ylabel('$t_O - {func}(t_A, t_B) [s]$'.format(func = func_name))
        plt.xlim(xlim)    
        # plt.show()    
        plt.savefig(fig_name)

        data = np.array([delta, delay])
        np.savetxt(data_file, data)

        if sign == -1:
            left = delta[0], delay[0]
            right = delta[-1], delay[-1]
        elif sign == 1:
            left = delta[-1], delay[-1]
            right = delta[0], delay[0]
        else:
            assert(False)

        print("Delta << 0: ", left)
        print("Delta = 0: ", middle)
        print("Delta >> 0: ", right)
        plt.close()


if __name__ == "__main__":
    main()