"""
    
	Involution Tool
	File: readGenerateCfg.py
	
    Copyright (C) 2018-2021  Daniel OEHLINGER <d.oehlinger@outlook.com>

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

import json
# from helper import *

def read_generate_cfg(config_file):
	cfg = GenerateCfg()
	
	with open(config_file, "r") as cfg_file:
		jsonobject = json.load(cfg_file)	
		for key, value in jsonobject.items():			
			if key.lower() == "groups".lower():
				# we need to handle the groups seperatly (or use pickle for serialization?)
				for value2 in value:
					g = Group()
					g.__dict__.update(value2)
					cfg.groups.append(g)
			else:
				cfg.__dict__[key] = value;				
	return cfg
				
class GenerateCfg:
	def __init__(self):
		self.N = 100
		self.mue = 0.029
		self.sigma = 0.01
		self.rise_time = 0.001
		self.bound = None # Default: we do not cut samples. A value x means, that only values where "abs(mu - sample_value) < bound * sigma" is satisfied, otherwise we resample (no clipping). Moreover, note that if the bound is too small, it might take a lot of resampling, since a lot of variables are rejected
		self.calc_next_transition_mode = CalcNextTransitionMode.GLOBAL
		self.signals = list()
		self.groups = list()

	def __str__(self):
		return "N: {N}, mue: {mue}, sigma: {sigma}, rise_time: {rise_time}, bound: {bound}, calc_next_transition_mode: {calc_next_transition_mode}, signals: {signals}, groups: {groups}".format(N=self.N, mue=self.mue, sigma=self.sigma, rise_time=self.rise_time, bound=self.bound, calc_next_transition_mode=self.calc_next_transition_mode, signals=self.signals, groups=self.groups)
		
class Group:
	def __init__(self):
		self.signals = list()
		self.mue = 0.010
		self.sigma = 0.03
		self.bound = None # Same behavior as for GenerateCfg
		self.oneway = False
		self.correlation_possibility = 0.5 # value between 0 and 1
		
class CalcNextTransitionMode:
	GLOBAL = "GLOBAL"
	LOCAL = "LOCAL"