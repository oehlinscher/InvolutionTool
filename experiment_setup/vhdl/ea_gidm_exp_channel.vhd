-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: ea_gidm_exp_channel.vhd
--	
--  Copyright (C) 2018-2020  Daniel OEHLINGER <d.oehlinger@outlook.com>
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

ENTITY gidm_exp_channel IS
	GENERIC (
        D_INF_UP : time;	
        D_INF_DO : time;	
        V_DD : real := 1.0;
        V_TH : real := 0.5;
        
		D_MIN : time;
		DELTA_PLUS : time;
		DELTA_MINUS : time;
		
		TRANSITION_TIME_FILE_PATH : string
	);
	PORT ( 
		input : IN std_logic;
		output : OUT std_logic := '0'-- For GIDM, this is the transition indicator, and therefore we initialize it to 0
	);

END gidm_exp_channel;

-----------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.math_real.ALL;
USE work.channel_base_pkg.ALL;

ARCHITECTURE beh OF gidm_exp_channel IS
	CONSTANT tau_up: time := integer ( real ( (D_INF_UP-D_MIN-DELTA_PLUS) / 1 fs ) / (- LOG(1.0 - V_TH / V_DD)) ) * 1 fs;
	CONSTANT tau_do: time := integer ( real ( (D_INF_DO-D_MIN-DELTA_MINUS) / 1 fs ) / (- LOG(V_TH / V_DD)) ) * 1 fs;

  	CONSTANT relTime: time := 1 fs;

BEGIN

  --########################################################  

  exp_channel_involution: PROCESS (input)
    VARIABLE last_output_time : time;
	VARIABLE T, delay : time;
	
    FILE tt_file : text;
    VARIABLE tt_line : line;
	VARIABLE tt_level : std_logic;

	VARIABLE first_transition : bit := '1';
  BEGIN
  	-- report "input transition at " & time'IMAGE(now);	
 	-- report "last output at " & time'IMAGE(last_output_time);
	T := now - last_output_time;
	-- report "T = " & time'IMAGE(T);
	
	IF input'EVENT and (input = '1' or input = '0')  THEN
		IF input = '1' THEN			
			-- report "got rising edge";
			if first_transition = '1' then
				-- This is how the "infinite" T is modelled for the first transition
				delay := D_INF_UP - DELTA_PLUS;
				first_transition := '0';
			else			
				delay := D_INF_UP - DELTA_PLUS + integer (
					real (tau_up / relTime) * LOG(
						1.0- EXP(
						-real( (T+D_INF_DO - DELTA_MINUS)/relTime ) / real(tau_do/ relTime ) 
						)
					)
				) * relTime;
			end if;
			
			tt_level := '1';

		ELSIF input = '0' THEN
			-- report "got falling edge";

			if first_transition = '1' then
				-- This is how the "infinite" T is modelled for the first transition
				delay := D_INF_DO - DELTA_MINUS;
				first_transition := '0';
			else		
				delay := D_INF_DO - DELTA_MINUS + integer (
					real (tau_do / relTime) * LOG(
						1.0- EXP( 
						- real( (T+D_INF_UP - DELTA_PLUS)/relTime ) / real(tau_up/ relTime ) 
						)
					)
				) * relTime;
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

		-- Now write the new transition time and the transition level into the file
		
		-- report "CHANNEL: TT_LEVEL: " &  std_logic'image(tt_level) & ", NOW: " & time'image(now) & ", TT_TIME: " & time'image(now + delay);
		
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
