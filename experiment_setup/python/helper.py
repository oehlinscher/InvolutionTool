"""
    
	Involution Tool
	File: helper.py
	
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

import os
import json
import inspect
import re

# Maybe later required, if we want to color a certain amount of subsequent messages
#def my_print_start_esc(esc_sequences, override_print_env_flag = False):
#	if check_print(override_print_env_flag, ): 
#		print print_esc_sequences(esc_sequences)
#		
#def my_print_end_esc(override_print_env_flag = False):
#	if check_print(override_print_env_flag): 
#		print EscCodes.ENDC
#	
def my_print(string, esc_sequences = None, override_print_env_flag = False):	
	if check_print(override_print_env_flag, esc_sequences):
		total_string = print_esc_sequences(esc_sequences)
		total_string += str(string)
		total_string += EscCodes.ENDC
		print(total_string)

def print_esc_sequences(esc_sequences):
		string = ""
		if esc_sequences is not None:		
			if type(esc_sequences) is str:
				string += esc_sequences
			else:
				for esc_code in esc_sequences:
					string += esc_code
		return string 
		
def check_print(override_print_env_flag, esc_codes = None):
	msg_print_level = esc_code_to_print_level(esc_codes)
	global_print_level = get_print_level()	
	
	#print EscCodes.FAIL + str(msg_print_level) + " / " + str(global_print_level) + EscCodes.ENDC
	
	return override_print_env_flag or msg_print_level >= global_print_level

def esc_code_to_print_level(esc_codes):
	mapping = dict()
	mapping[EscCodes.OKBLUE] = PrintLevel.INFORMATION
	mapping[EscCodes.OKGREEN] = PrintLevel.INFORMATION
	mapping[EscCodes.WARNING] = PrintLevel.WARNING
	mapping[EscCodes.FAIL] = PrintLevel.FAIL
	
	
	level = PrintLevel.INFORMATION
	if esc_codes is not None:
		# only one escape code, get the level
		if type(esc_codes) is str:
			return mapping[esc_codes]
		
		# get the maximum level from all esc_codes, if we have a list of esc_codes
		for code in esc_codes:
			if code in mapping and level < mappping[code]:
				level = mapping[code]
	return level
	
def get_print_level():
	if "PRINT_LEVEL" in os.environ:
		print_level = os.environ["PRINT_LEVEL"].strip(' \t\r\n')	
		#print "Print level: " + print_level
		if print_level.lower() == "information":
			return PrintLevel.INFORMATION
		if print_level.lower() == "warning":
			return PrintLevel.WARNING
		if print_level.lower() == "fail":
			return PrintLevel.FAIL
		if print_level.lower() == "none":
			return PrintLevel.NONE
		
	return PrintLevel.INFORMATION
	
def parse_csv_string(string):
	if string is None:
		return list()
	if not string.strip():
		return list()
	result = re.split(";|,", string)
	result = [x.strip() for x in result if x.strip()] # filter possible empty / None strings
	return result
	
def apply_regex_to_list(list, regex_string):
	regex = re.compile(regex_string, re.IGNORECASE)
	return [x for x in list if  regex.match(x)]
	
def to_bool(bool_str):
	my_print("Parse the string and return the boolean value encoded or raise an exception")
	if isinstance(bool_str, basestring) and bool_str: 
		if bool_str.lower() in ['true', 't', '1']: return True
		elif bool_str.lower() in ['false', 'f', '0']: return False

	#if here we couldn't parse it
	raise ValueError("%s is no recognized as a boolean value" % bool_str)
	
def replace_ci(str,old,new,count=0):
		# Behaves like S.replace(), but does so in a case-insensitive fashion.
		# taken from http://code.activestate.com/recipes/552726-case-insensitive-string-replacement/
		pattern = re.compile(re.escape(old),re.I)
		return re.sub(pattern,new,str,count)
		
def dict_key_to_lower_case(dictionary):
	temp_dict = dict()
	for key, value in dictionary.iteritems():
		temp_dict[key.lower()] = value
	dictionary = temp_dict
	return dictionary
	
def convert_string_to_filename(str):
	return str.replace("/", "_")
	
def matching_file_to_list(matching_file):
	matching_dict = matching_file_to_dict(matching_file)
	matching_list = list()
	for key, value in matching_dict.items():
		matching_list.append((key, value))
	return matching_list

# Some functions need the value with its case preserved. 
# Call with value_as_is set to True if the value should not be converted to lower case
def matching_file_to_dict(matching_file, value_as_is=False):
	matching = dict()
	with open(matching_file, 'r') as f:
		matching = json.load(f)

	# complete dict to lower case
	if value_as_is:		
		return dict((k.lower(), v) for k,v in matching.items())
	else:
		return dict((k.lower(), v.lower()) for k,v in matching.items())

def convert_instance_name(instance, replace_square_brackets_with_space=False):
	square_brackets_repl = ""
	if replace_square_brackets_with_space:
		square_brackets_repl = " "
	return instance.replace("/", "").replace("_", "").replace("[", square_brackets_repl).replace("]", square_brackets_repl).replace("\\", "").replace(".", "").strip()

def convert_port_name(port):
	return port.replace("/", "").replace("_", "")		

	
class PrintLevel:
	INFORMATION = 1
	WARNING = 2
	FAIL = 3
	NONE = 4
	
	
class EscCodes:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
	
class ObjectEncoder(json.JSONEncoder):
	def default(self, obj):
		if hasattr(obj, "to_json"):
			return self.default(obj.to_json())
		elif hasattr(obj, "__dict__"):
			d = dict(
				(key, value)
				for key, value in inspect.getmembers(obj)
				if not key.startswith("__")
				and not inspect.isabstract(value)
				and not inspect.isbuiltin(value)
				and not inspect.isfunction(value)
				and not inspect.isgenerator(value)
				and not inspect.isgeneratorfunction(value)
				and not inspect.ismethod(value)
				and not inspect.ismethoddescriptor(value)
				and not inspect.isroutine(value)
			)
			return self.default(d)
		return obj