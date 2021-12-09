-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: p_python_channel.vhd
--	
--  Copyright (C) 2018-2021  Daniel OEHLINGER <d.oehlinger@outlook.com>
--
--  This source file may be used and distributed without restriction provided
--  that this copyright statement is not removed from the file and that any
--  derivative work contains the original copyright notice and the associated
--  disclaimer.
--
--  This source file is free software: you can redistribute it and/or modify it
--  under the terms of the GNU Lesser General Public License as published by
--  the Free Software Foundation, either version 3 of the License, or (at your
--  option) any later version.
--
--  This source file is distributed in the hope that it will be useful, but
--  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
--  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
--  for more details.
--
--  You should have received a copy of the GNU Lesser General Public License
--  along with the noasic library.  If not, see http://www.gnu.org/licenses
--
-------------------------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE work.channel_base_pkg.ALL;

package python_channel_pkg 
is
  -- This is the calculate delay idm function in the standard version
  procedure calculate_delay_idm(
      channel_type : IN string;
      input : IN std_logic;
      d_up : IN time;
      d_do : IN time;
      t_p : IN time;
      t_p_percent : IN real;
      t_p_mode : IN parameter_mode;
      v_dd : IN real;
      v_th : IN real;
      now : IN time;
      last_output_time : INOUT time;
      first_transition : INOUT bit;
      delay : OUT time;
      param_count : IN integer
  );

  -- Since VHDL allows overloading, we can add a procedure with the same name for the sumexp channel with the same name, which requires additional parameters
  procedure calculate_delay_idm(
      channel_type : IN string;
      input : IN std_logic;
      d_up : IN time;
      d_do : IN time;
      t_p : IN time;
      t_p_percent : IN real;
      t_p_mode : IN parameter_mode;
      v_dd : IN real;
      v_th : IN real;
      now : IN time;
      last_output_time : INOUT time;
      first_transition : INOUT bit;
      delay : OUT time;
      param_count : IN integer;

      -- Additional parameters (need to be in alphabetical order)
      TAU_1_DO 	: IN time;
      TAU_1_UP 	: IN time;
      TAU_2_DO 	: IN time;
      TAU_2_UP 	: IN time;
      X_1_DO 		: IN real;
      X_1_UP 		: IN real
  );
    
  attribute foreign of calculate_delay_idm : procedure is "calculate_delay_idm ./vhdl/python_channel/python_channel.so";

  -- This is the calculate delay gidm function in the standard version
  procedure calculate_delay_gidm(
      channel_type : IN string;
      input : IN std_logic;
      d_inf_up : IN time;
      d_inf_do : IN time;
      v_dd : IN real;
      v_th : IN real;
      d_min : IN time;
      delta_plus : IN time;
      delta_minus : IN time;
      now : IN time;
      last_output_time : INOUT time;
      first_transition : INOUT bit;
      delay : OUT time;
      param_count : IN integer
  );

  -- Since VHDL allows overloading, we can add a procedure with the same name for the sumexp channel with the same name, which requires additional parameters
  procedure calculate_delay_gidm(
      channel_type : IN string;
      input : IN std_logic;
      d_inf_up : IN time;
      d_inf_do : IN time;
      v_dd : IN real;
      v_th : IN real;
      d_min : IN time;
      delta_plus : IN time;
      delta_minus : IN time;
      now : IN time;
      last_output_time : INOUT time;
      first_transition : INOUT bit;
      delay : OUT time;
      param_count : IN integer;

      -- Additional parameters (need to be in alphabetical order)
      TAU_1_DO 	: IN time;
      TAU_1_UP 	: IN time;
      TAU_2_DO 	: IN time;
      TAU_2_UP 	: IN time;
      X_1_DO 		: IN real;
      X_1_UP 		: IN real
  );
    
  attribute foreign of calculate_delay_gidm : procedure is "calculate_delay_gidm ./vhdl/python_channel/python_channel.so";

  procedure calculate_delay_hybrid_2in(
    gate_function : IN string; -- "e.g NOR, NAND, ..."
    
    input_1_old : IN std_logic;
    input_2_old : IN std_logic;

    input_1 : IN std_logic;
    input_2 : IN std_logic;

    -- Probably not required, can be set via v_int and v_out parameter initially
    -- v_int_init : IN real;
    -- v_out_init : IN real;

    r_1 : IN real;
    r_2 : IN real;
    r_3 : IN real;
    r_4 : IN real;

    c_int : IN real;
    c_out : IN real;
    
    scale_1 : IN real;

    pure_delay : IN time;

    v_dd : IN real;
    v_th : IN real;

    now : IN time;

    -- State
    first_transition : INOUT bit;
    last_input_switch_time : INOUT time;
    v_int : INOUT real;
    v_out : INOUT real;

    -- Output
    delay : OUT time; -- This is the time we calculated that it takes for V_out to perform a threshold crossing
    delay_valid : OUT bit -- It might happen that there is no threshold crossing, so we can set this here
  );
  
  attribute foreign of calculate_delay_hybrid_2in : procedure is "calculate_delay_hybrid_2in ./vhdl/python_channel/python_channel.so";

  procedure init_wrapper;
  attribute foreign of init_wrapper : procedure is "init_wrapper ./vhdl/python_channel/python_channel.so";

  
  procedure clean_wrapper;
  attribute foreign of clean_wrapper : procedure is "clean_wrapper ./vhdl/python_channel/python_channel.so";
end;
  
package body python_channel_pkg is
  procedure calculate_delay_idm(
    channel_type : IN string;
    input : IN std_logic;
    d_up : IN time;
    d_do : IN time;
    t_p : IN time;
    t_p_percent : IN real;
    t_p_mode : IN parameter_mode;
    v_dd : IN real;
    v_th : IN real;
    now : IN time;
    last_output_time : INOUT time;
    first_transition : INOUT bit;
    delay : OUT time;
    param_count : IN integer
  ) is
  begin
    report "ERROR: foreign subprogram calculate_delay_idm not called";
  end;

  procedure calculate_delay_idm(
    channel_type : IN string;
    input : IN std_logic;
    d_up : IN time;
    d_do : IN time;
    t_p : IN time;
    t_p_percent : IN real;
    t_p_mode : IN parameter_mode;
    v_dd : IN real;
    v_th : IN real;
    now : IN time;
    last_output_time : INOUT time;
    first_transition : INOUT bit;
    delay : OUT time;
    param_count : IN integer;

      -- Additional parameters (need to be in alphabetical order)
    TAU_1_DO 	: IN time;
    TAU_1_UP 	: IN time;
    TAU_2_DO 	: IN time;
    TAU_2_UP 	: IN time;
    X_1_DO 		: IN real;
    X_1_UP 		: IN real
  ) is
  begin
    report "ERROR: foreign subprogram calculate_delay_idm not called";
  end;

  procedure calculate_delay_gidm(
    channel_type : IN string;
    input : IN std_logic;
    d_inf_up : IN time;
    d_inf_do : IN time;
    v_dd : IN real;
    v_th : IN real;
    d_min : IN time;
    delta_plus : IN time;
    delta_minus : IN time;
    now : IN time;
    last_output_time : INOUT time;
    first_transition : INOUT bit;
    delay : OUT time;
    param_count : IN integer
  ) is
  begin
    report "ERROR: foreign subprogram calculate_delay_gidm not called";
  end;

-- Since VHDL allows overloading, we can add a procedure with the same name for the sumexp channel with the same name, which requires additional parameters
procedure calculate_delay_gidm(
    channel_type : IN string;
    input : IN std_logic;
    d_inf_up : IN time;
    d_inf_do : IN time;
    v_dd : IN real;
    v_th : IN real;
    d_min : IN time;
    delta_plus : IN time;
    delta_minus : IN time;
    now : IN time;
    last_output_time : INOUT time;
    first_transition : INOUT bit;
    delay : OUT time;
    param_count : IN integer;

    -- Additional parameters (need to be in alphabetical order)
    TAU_1_DO 	: IN time;
    TAU_1_UP 	: IN time;
    TAU_2_DO 	: IN time;
    TAU_2_UP 	: IN time;
    X_1_DO 		: IN real;
    X_1_UP 		: IN real
  ) is
  begin
    report "ERROR: foreign subprogram calculate_delay_gidm not called";
  end;

  procedure calculate_delay_hybrid_2in(
    gate_function : IN string; -- "e.g NOR, NAND, ..."
    
    input_1_old : IN std_logic;
    input_2_old : IN std_logic;

    input_1 : IN std_logic;
    input_2 : IN std_logic;

    -- Probably not required, can be set via v_int and v_out parameter initially
    -- v_int_init : IN real;
    -- v_out_init : IN real;

    r_1 : IN real;
    r_2 : IN real;
    r_3 : IN real;
    r_4 : IN real;

    c_int : IN real;
    c_out : IN real;
    
    scale_1 : IN real;

    pure_delay : IN time;

    v_dd : IN real;
    v_th : IN real;

    now : IN time;

    -- State
    first_transition : INOUT bit;
    last_input_switch_time : INOUT time;
    v_int : INOUT real;
    v_out : INOUT real;

    -- Output
    delay : OUT time; -- This is the time we calculated that it takes for V_out to perform a threshold crossing
    delay_valid : OUT bit -- It might happen that there is no threshold crossing, so we can set this here
  ) is
  begin
    report "ERROR: foreign subprogram calculate_delay_hybrid_2in not called";
  end;

  
  procedure init_wrapper is
  begin
    report "ERROR: foreign subprogram init_wrapper not called";
  end;
  
  procedure clean_wrapper is
  begin
    report "ERROR: foreign subprogram clean_wrapper not called";
  end;       

end;