-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: ea_exp_channel.vhd
--	
--  Copyright (C) 2018-2019  Daniel OEHLINGER <d.oehlinger@outlook.com>
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

ENTITY exp_channel IS
	GENERIC (
		D_UP : time; 
		D_DO : time; 
		T_P  : time;
		T_P_PERCENT : real				:= 0.0;	
		T_P_MODE	: PARAMETER_MODE 	:= ABSOLUTE;
		V_DD : real;
		V_TH : real
	);
	PORT ( 
		input : IN std_logic;
		output : OUT std_logic
	);

END exp_channel;

-----------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.math_real.ALL;
USE work.channel_base_pkg.ALL;

ARCHITECTURE beh OF exp_channel IS
  CONSTANT tau_up: time := integer ( real ( (D_UP - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_UP)) / 1 fs ) / (- LOG(1.0 - V_TH / V_DD)) ) * 1 fs;
  CONSTANT tau_do: time := integer ( real ( (D_DO - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_DO)) / 1 fs ) / (- LOG(V_TH / V_DD)) ) * 1 fs;

  CONSTANT relTime: time := 1 fs;

BEGIN

  --########################################################  

  exp_channel_involution: PROCESS (input)
    VARIABLE last_output_time : time := -1 sec;
    VARIABLE T, delay : time;
  BEGIN
	-- report "input transition at " & time'IMAGE(now);	
	-- report "last output at " & time'IMAGE(last_output_time);
    T := now - last_output_time;
	-- report "T = " & time'IMAGE(T);

	-- in VITAL they check for A'LAST_VALUE
	-- but there also 'L' and 'H' of importance
	IF rising_edge(input) THEN

		-- report "got rising edge";

		delay := D_UP + integer (
			real (tau_up / relTime) * LOG(
				1.0- EXP(
				-real( (T+D_DO)/relTime ) / real(tau_do/ relTime ) 
				)
			)
		) * relTime;
		-- report "delay: " & time'IMAGE(delay);

		last_output_time := now + delay;

		IF (delay < 0 fs) THEN
			delay := 0 fs;
		END IF;	
		output <= TRANSPORT '1' AFTER delay;

    ELSIF falling_edge(input) THEN
		-- report "got falling edge";

		delay := D_DO + integer (
			real (tau_do / relTime) * LOG(
				1.0- EXP( 
				- real( (T+D_UP)/relTime ) / real(tau_up/ relTime ) 
				)
			)
		) * relTime;
		-- report "delay: " & time'IMAGE(delay);

		last_output_time := now + delay;

		IF (delay < 0 fs) THEN
			delay := 0 fs;
		END IF;	
		output <= TRANSPORT '0' AFTER delay;

    ELSIF (now = 0 fs) THEN
		output <= input;
    END IF;

  END PROCESS;

  --########################################################

END ARCHITECTURE;
