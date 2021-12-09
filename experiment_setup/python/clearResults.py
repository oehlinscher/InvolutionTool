"""
    @file clearResults.py

	@brief Script for removeing all result files in all circuit folders

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

import sys
import os
from os import path
import shutil

def main():
    clear_results(sys.argv[1])
    
def clear_results(circuit_top_folder_path):
    for circuit_folder in os.listdir(circuit_top_folder_path):
        circuit_folder = os.path.join(circuit_top_folder_path, circuit_folder)
        print(circuit_folder)
        if path.isdir(circuit_folder):
            for folder in os.listdir(circuit_folder):
                if folder == "results":
                    print(folder)
                    shutil.rmtree(os.path.join(circuit_folder, folder))

if __name__ == "__main__":
    main()