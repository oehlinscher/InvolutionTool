-------------------------------------------------------------------------------
--! @file ea_exp_channel.vhd
--!
--! @brief Entity and architecture of the IDM Exp-Channel
--!
--! @author Daniel OEHLINGER <d.oehlinger@outlook.com>
--!
--! @date 2018-2021
--!
--! @copyright
--! @parblock
--! This source file may be used and distributed without restriction provided
--! that this copyright statement is not removed from the file and that any
--! derivative work contains the original copyright notice and the associated
--! disclaimer.
--!
--! This source file is free software: you can redistribute it and/or modify it
--! under the terms of the GNU Lesser General Public License as published by
--! the Free Software Foundation, either version 3 of the License, or (at your
--! option) any later version.
--!
--! This source file is distributed in the hope that it will be useful, but
--! WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
--! or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
--! for more details.
--!
--! You should have received a copy of the GNU Lesser General Public License
--! along with the noasic library.  If not, see http://www.gnu.org/licenses
--! @endparblock
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
		V_TH : real;
		INIT_VALUE : std_logic := '0'
	);
	PORT ( 
		input : IN std_logic;
		output : OUT std_logic := INIT_VALUE
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
    VARIABLE last_output_time : time;
    VARIABLE T, delay : time;
	VARIABLE first_transition : bit := '1';
  BEGIN
	-- report "input transition at " & time'IMAGE(now);	
	-- report "last output at " & time'IMAGE(last_output_time);
    T := now - last_output_time;
	-- report "T = " & time'IMAGE(T);

	-- in VITAL they check for A'LAST_VALUE
	-- but there also 'L' and 'H' of importance
	IF input'EVENT and input = '1'  THEN

		-- report "got rising edge";
		if first_transition = '1' then
			delay := D_UP;
			first_transition := '0';
		else
			delay := D_UP + integer (
				real (tau_up / relTime) * LOG(
					1.0- EXP(
					-real( (T+D_DO)/relTime ) / real(tau_do/ relTime ) 
					)
				)
			) * relTime;		
		end if;
		-- report "delay: " & time'IMAGE(delay);

		last_output_time := now + delay;

		IF (delay < 0 fs) THEN
			delay := 0 fs;
		END IF;	
		output <= TRANSPORT '1' AFTER delay;

    ELSIF input'EVENT and input = '0' THEN
		-- report "got falling edge";
		if first_transition = '1' then
			delay := D_DO;
			first_transition := '0';
		else
			delay := D_DO + integer (
				real (tau_do / relTime) * LOG(
					1.0- EXP( 
					- real( (T+D_UP)/relTime ) / real(tau_up/ relTime ) 
					)
				)
			) * relTime;	
		end if;

		-- report "delay: " & time'IMAGE(delay);

		last_output_time := now + delay;

		IF (delay < 0 fs) THEN
			delay := 0 fs;
		END IF;	
		output <= TRANSPORT '0' AFTER delay;
    END IF;

  END PROCESS;

  --########################################################

END ARCHITECTURE;
