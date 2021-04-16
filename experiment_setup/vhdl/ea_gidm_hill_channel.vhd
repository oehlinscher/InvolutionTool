-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: ea_gidm_hill_channel.vhd
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
USE std.textio.ALL;

ENTITY gidm_hill_channel IS
	GENERIC (
		D_INF_UP : time; 
		D_INF_DO : time; 
		
		V_DD : real;
		V_TH : real;

		N_UP : real;
		N_DO : real;
			
		D_MIN : time;
		DELTA_PLUS : time;
		DELTA_MINUS : time;
		
		TRANSITION_TIME_FILE_PATH : string
	);
	PORT ( 
		input : IN std_logic;
		output : OUT std_logic := '0'-- For GIDM, this is the transition indicator, and therefore we initialize it to 0
	);

END gidm_hill_channel;

-----------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.math_real.ALL;
USE work.channel_base_pkg.ALL;

ARCHITECTURE beh OF gidm_hill_channel IS
  CONSTANT relTime : time := 1 fs;
  
  -- calculate the n-th root by using the power function with (1/N)   
  
  -- We decided to disable the "inverse" ansatz, since we get into trouble when we have T_P_PERCENT = 100
  -- It was never really used anyway, and has no benefits over the "correct" ansatz (since they both yield the same results)
  -- "Inverse ansatz"
  -- CONSTANT k_up_inv : real := ((1.0/(V_DD / V_TH - 1.0))**(1.0/(real(N_UP)))) / (real((D_UP - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_UP)) / relTime)); 
  -- CONSTANT k_do_inv : real := ((V_DD / V_TH - 1.0)**(1.0/(real(N_DO)))) / (real((D_DO - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_DO)) / relTime)); 
  
  -- "Correct ansatz"
  CONSTANT k_up_std : real := real(((D_INF_UP-D_MIN-DELTA_PLUS ) / relTime)) * ((V_TH / (V_DD-V_TH))**(1.0/N_UP)); 
  CONSTANT k_do_std : real := real(((D_INF_DO-D_MIN-DELTA_MINUS) / relTime)) * ((V_DD-V_TH) / V_TH)**(1.0/N_DO);
BEGIN

  --########################################################  

  hill_channel_involution: PROCESS (input)
    VARIABLE last_output_time : time;
    VARIABLE T, delay : time;
	
    FILE tt_file : text;
    VARIABLE tt_line : line;
	VARIABLE tt_level : std_logic;
	
	VARIABLE first_transition : bit := '1';
  BEGIN

    T := now - last_output_time;
	IF input'EVENT and (input = '1' or input = '0')  THEN
		IF input = '1' THEN
			if first_transition = '1' then
				first_transition := '0';
				delay := D_INF_UP - DELTA_PLUS;
			else	
				delay := - k_up_std * (k_do_std / real((T + D_INF_DO-DELTA_MINUS) / relTime))**(N_DO/N_UP) * relTime + D_INF_UP - DELTA_PLUS;
			end if;
			tt_level := '1';

		ELSIF input = '0' THEN
			if first_transition = '1' then
				first_transition := '0';
				delay := D_INF_DO - DELTA_MINUS;
			else
				delay := - k_do_std * (k_up_std / real((T + D_INF_UP-DELTA_PLUS) / relTime))**(N_UP/N_DO) * relTime + D_INF_DO - DELTA_MINUS;
			end if;
			tt_level := '0';
		END IF;		
		
		IF now + delay < last_output_time THEN
			-- REPORT "Cancelling transition!";
			IF last_output_time < now THEN
				REPORT "Problem: Output that should be cancelled is in the past";
			END IF;
		END IF;

		last_output_time := now + delay;

		write(tt_line, integer'image(integer((now + delay) / 1 fs)));
		write(tt_line, string'(" "));
		write(tt_line, std_logic'image(tt_level));
		file_open(tt_file, TRANSITION_TIME_FILE_PATH, WRITE_MODE);
		writeline(tt_file, tt_line);
		file_close(tt_file);	

		write(tt_line, integer'image(integer((now + delay) / 1 fs)));
		write(tt_line, string'(" "));
		write(tt_line, std_logic'image(tt_level));
		file_open(tt_file, TRANSITION_TIME_FILE_PATH & ".complete", APPEND_MODE);
		writeline(tt_file, tt_line);
		file_close(tt_file);	
		
		output <= not output; 
	END IF;

  END PROCESS;

  --########################################################

END ARCHITECTURE;
