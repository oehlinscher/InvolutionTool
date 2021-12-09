"""
    @file compareFigs.py

	@brief Compares SPICE with ODE fitting

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

def main():
    fitting_folder = "../../circuits/nor_gate_15nm/hm_fitting/"
    postfix = '_with_dmin'

    # Read the data from all 4 data file
    spice_falling = np.loadtxt(fitting_folder + 'spice_falling_output.data')
    spice_rising = np.loadtxt(fitting_folder + 'spice_rising_output.data')
    ode_falling = np.loadtxt(fitting_folder + 'ode_falling_output' + postfix + '.data')
    ode_fig5 = np.loadtxt(fitting_folder + 'ode_rising_output' + postfix + '.data')


    plt.figure()
    plt.plot(spice_falling[0], spice_falling[1], label='Spice')
    plt.plot(ode_falling[0], ode_falling[1], label='ODE')
    plt.ylabel(r'$t_O - \min(t_A, t_B) [s]$')
    plt.xlabel('$t_B - t_A [s]$')
    plt.legend()
    # plt.xlim((-2.0e-11, 2.0e-11))
    plt.xlim((-1e-10, 1e-10))
    # plt.show()
    plt.savefig(fitting_folder + 'comp_falling_output' + postfix + '.png')
    plt.close()

    plt.figure()
    plt.plot(spice_rising[0], spice_rising[1], label='Spice')
    plt.plot(ode_fig5[0], ode_fig5[1], label='ODE')
    plt.xlabel('$t_B - t_A [s]$')
    # plt.ylabel('$Delay [s]$')
    plt.ylabel(r'$t_O - \max(t_A, t_B) [s]$')
    plt.legend()
    # plt.xlim((-2e-10, 2e-10))
    plt.xlim((-1e-10, 1e-10))
    # plt.show()
    plt.savefig(fitting_folder + 'comp_rising_output' + postfix + '.png')
    plt.close()


if __name__ == "__main__":
    main()