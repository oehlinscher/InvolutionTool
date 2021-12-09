/*
    
	Involution Tool
	File: python_channel.c
	
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
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include "mti.h"
#include "Python.h"
#include <dlfcn.h>


static char *get_string(mtiVariableIdT id);
PyObject *build_channel_parameter_dict(char* channel_type, va_list args);
PyObject *build_python_function(char* function_name);
void convert_result(PyObject* p_result, mtiTime64T* delay, mtiTime64T* last_output_time, char* first_transition);
void init_wrapper();
void clean_wrapper();


// Not working yet
// int main() {
//     init_wrapper();
//     // calculate_delay_idm();
//     clean_wrapper();
//     return 0;
// }

void init_wrapper() {
    dlopen("libpython3.6m.so", RTLD_LAZY | RTLD_GLOBAL);
    setenv("PYTHONPATH", "./vhdl/python_channel", 1);
    Py_Initialize();    
}

void clean_wrapper() {
    Py_Finalize();    
}

void calculate_delay_idm(
    mtiVariableIdT channel_type,
    int input, // : IN std_logic;
    mtiTime64T* d_up,
    mtiTime64T* d_do,
    mtiTime64T* t_p,
    double* t_p_percent,
    int t_p_mode, // parameter_mode,
    double* v_dd,
    double* v_th,
    mtiTime64T* now,
    mtiTime64T* last_output_time,
    char* first_transition, // bit
    mtiTime64T* delay, 
    int param_count,
    ...
)
{
    PyObject *p_func = build_python_function("calculate_delay_idm");

    PyObject *p_channel_type = Py_BuildValue("(z)", get_string(channel_type));
    PyObject *p_input = Py_BuildValue("(i)", input);
    PyObject *p_d_up = Py_BuildValue("(l)", *d_up);
    PyObject *p_d_do = Py_BuildValue("(l)", *d_do);
    PyObject *p_t_p = Py_BuildValue("(l)", *t_p);
    PyObject *p_t_p_percent = Py_BuildValue("(d)", *t_p_percent);
    PyObject *p_t_p_mode = Py_BuildValue("(i)", t_p_mode);
    PyObject *p_v_dd = Py_BuildValue("(d)", *v_dd);
    PyObject *p_v_th = Py_BuildValue("(d)", *v_th);
    PyObject *p_now = Py_BuildValue("(l)", *now);
    PyObject *p_last_output_time = Py_BuildValue("(l)", *last_output_time);
    PyObject *p_first_transition = Py_BuildValue("(i)", *first_transition);

    // Depending on the channel type, we build a dictionary with addional channel parameters (which might be empty if there are none)    
    va_list args;
    va_start(args, param_count);
    PyObject *p_channel_parameters = build_channel_parameter_dict(get_string(channel_type), args);
    va_end(args);
    
    PyErr_Print();
    
    PyObject* p_result = PyObject_CallFunctionObjArgs(p_func, p_channel_type, p_input, p_d_up, p_d_do, p_t_p, p_t_p_percent, p_t_p_mode, p_v_dd, p_v_th, p_now, p_last_output_time, p_first_transition, p_channel_parameters, NULL);
    convert_result(p_result, delay, last_output_time, first_transition);

    PyErr_Print();
}

void calculate_delay_gidm(
    mtiVariableIdT channel_type,
    int input, // : IN std_logic;
    mtiTime64T* d_inf_up,
    mtiTime64T* d_inf_do,
    double* v_dd,
    double* v_th,
    mtiTime64T* d_min,
    mtiTime64T* delta_plus,
    mtiTime64T* delta_minus,
    mtiTime64T* now,
    mtiTime64T* last_output_time,
    char* first_transition, // bit
    mtiTime64T* delay, 
    int param_count,
    ...
) {
    PyObject *p_func = build_python_function("calculate_delay_gidm");

    PyObject *p_channel_type = Py_BuildValue("(z)", get_string(channel_type));
    PyObject *p_input = Py_BuildValue("(i)", input);
    PyObject *p_d_inf_up = Py_BuildValue("(l)", *d_inf_up);
    PyObject *p_d_inf_do = Py_BuildValue("(l)", *d_inf_do);
    PyObject *p_v_dd = Py_BuildValue("(d)", *v_dd);
    PyObject *p_v_th = Py_BuildValue("(d)", *v_th);
    PyObject *p_d_min = Py_BuildValue("(l)", *d_min);
    PyObject *p_delta_plus = Py_BuildValue("(l)", *delta_plus);
    PyObject *p_delta_minus = Py_BuildValue("(l)", *delta_minus);
    PyObject *p_now = Py_BuildValue("(l)", *now);
    PyObject *p_last_output_time = Py_BuildValue("(l)", *last_output_time);
    PyObject *p_first_transition = Py_BuildValue("(i)", *first_transition);

    // Depending on the channel type, we build a dictionary with additional channel parameters (which might be empty if there are none)    
    va_list args;
    va_start(args, param_count);
    PyObject *p_channel_parameters = build_channel_parameter_dict(get_string(channel_type), args);
    va_end(args);
    
    PyErr_Print();
    
    PyObject* p_result = PyObject_CallFunctionObjArgs(p_func, p_channel_type, p_input, p_d_inf_up, p_d_inf_do, p_v_dd, p_v_th, p_d_min, p_delta_plus, p_delta_minus, p_now, p_last_output_time, p_first_transition, p_channel_parameters, NULL);
    
    convert_result(p_result, delay, last_output_time, first_transition);


    PyErr_Print();
}

void calculate_delay_hybrid_2in(
    mtiVariableIdT gate_function,
    
    int input_1_old,
    int input_2_old,

    int input_1,
    int input_2,
    
    double* r_1,
    double* r_2,
    double* r_3,
    double* r_4,

    double* c_int,
    double* c_out,
    
    double* scale_1,

    mtiTime64T* pure_delay,

    double* v_dd,
    double*v_th,

    mtiTime64T* now,

    char* first_transition,
    mtiTime64T* last_input_switch_time,
    double*  v_int,
    double* v_out,

    mtiTime64T* delay,
    char* delay_valid
) {    
    PyObject *p_func = build_python_function("calculate_delay_hybrid_2in");

    PyObject *p_gate_function = Py_BuildValue("(z)", get_string(gate_function));
    PyObject *p_input_1_old = Py_BuildValue("(i)", input_1_old);
    PyObject *p_input_2_old = Py_BuildValue("(i)", input_2_old);
    PyObject *p_input_1 = Py_BuildValue("(i)", input_1);
    PyObject *p_input_2 = Py_BuildValue("(i)", input_2);
    
    PyObject *p_r_1 = Py_BuildValue("(d)", *r_1);
    PyObject *p_r_2 = Py_BuildValue("(d)", *r_2);
    PyObject *p_r_3 = Py_BuildValue("(d)", *r_3);
    PyObject *p_r_4 = Py_BuildValue("(d)", *r_4);
    PyObject *p_c_int = Py_BuildValue("(d)", *c_int);
    PyObject *p_c_out = Py_BuildValue("(d)", *c_out);
    
    PyObject *p_scale_1 = Py_BuildValue("(d)", *scale_1);

    PyObject *p_pure_delay = Py_BuildValue("(l)", *pure_delay);

    PyObject *p_v_dd = Py_BuildValue("(d)", *v_dd);
    PyObject *p_v_th = Py_BuildValue("(d)", *v_th);

    PyObject *p_now = Py_BuildValue("(l)", *now);
    
    PyObject *p_first_transition = Py_BuildValue("(i)", *first_transition);
    PyObject *p_last_input_switch_time = Py_BuildValue("(l)", *last_input_switch_time);
    PyObject *p_v_int = Py_BuildValue("(d)", *v_int);
    PyObject *p_v_out = Py_BuildValue("(d)", *v_out);
    
    PyObject* p_result = PyObject_CallFunctionObjArgs(p_func, p_gate_function, p_input_1_old, p_input_2_old, p_input_1, p_input_2, p_r_1, p_r_2, p_r_3, p_r_4, p_c_int, p_c_out, p_scale_1, p_pure_delay, p_v_dd, p_v_th, p_now, p_first_transition, p_last_input_switch_time, p_v_int, p_v_out, NULL);

    PyObject* p_result_delay = PyTuple_GetItem(p_result, 0);
    PyObject* p_result_delay_valid = PyTuple_GetItem(p_result, 1);
    PyObject* p_result_first_transition = PyTuple_GetItem(p_result, 2);
    PyObject* p_result_last_input_switch_time = PyTuple_GetItem(p_result, 3);
    PyObject* p_result_v_int = PyTuple_GetItem(p_result, 4);
    PyObject* p_result_v_out = PyTuple_GetItem(p_result, 5);
    PyErr_Print(); 

    
    *delay = PyLong_AsLong(p_result_delay);
    *delay_valid = PyLong_AsSize_t(p_result_delay_valid);
    *first_transition = PyLong_AsSize_t(p_result_first_transition);
    *last_input_switch_time = PyLong_AsLong(p_result_last_input_switch_time);
    *v_int = PyFloat_AsDouble(p_result_v_int);
    *v_out = PyFloat_AsDouble(p_result_v_out);

    // printf("C. Delay: %ld\n", *delay);


    PyErr_Print();
}

PyObject *build_python_function(char* function_name) {
    PyObject* p_name = PyUnicode_FromString((char *)"python_channel_implementation");    
    PyObject* p_module = PyImport_Import(p_name);
    PyObject* p_dict = PyModule_GetDict(p_module);
    PyObject* p_func = PyDict_GetItemString(p_dict, function_name);

    return p_func;
}


PyObject *build_channel_parameter_dict(char* channel_type, va_list args) {
    PyObject *p_channel_parameters = PyDict_New();

    // Comparison needs to be lower case
    if (strcmp(channel_type, "sumexp_channel") == 0 || strcmp(channel_type, "gidm_sumexp_channel") == 0) 
    {
        PyDict_SetItem(p_channel_parameters, Py_BuildValue("(z)", "tau_1_do"), Py_BuildValue("(l)", *va_arg(args, mtiTime64T*)));
        PyDict_SetItem(p_channel_parameters, Py_BuildValue("(z)", "tau_1_up"), Py_BuildValue("(l)", *va_arg(args, mtiTime64T*)));
        PyDict_SetItem(p_channel_parameters, Py_BuildValue("(z)", "tau_2_do"), Py_BuildValue("(l)", *va_arg(args, mtiTime64T*)));
        PyDict_SetItem(p_channel_parameters, Py_BuildValue("(z)", "tau_2_up"), Py_BuildValue("(l)", *va_arg(args, mtiTime64T*)));
        PyDict_SetItem(p_channel_parameters, Py_BuildValue("(z)", "x_1_do"), Py_BuildValue("(d)", *va_arg(args, double*)));
        PyDict_SetItem(p_channel_parameters, Py_BuildValue("(z)", "x_1_up"), Py_BuildValue("(d)", *va_arg(args, double*)));
    }  

    return p_channel_parameters;

}    

void convert_result(PyObject* p_result, mtiTime64T* delay, mtiTime64T* last_output_time, char* first_transition) {
    PyObject* p_result_delay = PyTuple_GetItem(p_result, 0);
    PyObject* p_result_last_output_time = PyTuple_GetItem(p_result, 1);
    PyObject* p_result_first_transition = PyTuple_GetItem(p_result, 2);
    PyErr_Print();

    
    *delay = PyLong_AsLong(p_result_delay);
    *last_output_time = PyLong_AsLong(p_result_last_output_time);
    *first_transition = PyLong_AsSize_t(p_result_first_transition);
}

/* Convert a VHDL String array into a NULL terminated string */
static char *get_string(mtiVariableIdT id)
{
    static char buf[1000];
    mtiTypeIdT type;
    int len;
    mti_GetArrayVarValue(id, buf);
    type = mti_GetVarType(id);
    len = mti_TickLength(type);
    buf[len] = 0;
    return buf;
}