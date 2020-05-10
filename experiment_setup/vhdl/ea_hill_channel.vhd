-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: ea_hill_channel.vhd
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

ENTITY hill_channel IS
	GENERIC (
		D_UP : time; 
		D_DO : time; 
		T_P  : time;
		T_P_PERCENT : real				:= 0.0;	
		T_P_MODE	: PARAMETER_MODE 	:= ABSOLUTE;
		V_DD : real;
		V_TH : real;
		N_UP : real;
		N_DO : real
		--USE_INVERSE : bit
	);
	PORT ( 
		input : IN std_logic;
		output : OUT std_logic
	);

END hill_channel;

-----------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.math_real.ALL;
USE work.channel_base_pkg.ALL;

ARCHITECTURE beh OF hill_channel IS
  CONSTANT relTime : time := 1 fs;
  
  -- calculate the n-th root by using the power function with (1/N)   
  
  -- We decided to disable the "inverse" ansatz, since we get into trouble when we have T_P_PERCENT = 100
  -- It was never really used anyway, and has no benefits over the "correct" ansatz (since they both yield the same results)
  -- "Inverse ansatz"
  -- CONSTANT k_up_inv : real := ((1.0/(V_DD / V_TH - 1.0))**(1.0/(real(N_UP)))) / (real((D_UP - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_UP)) / relTime)); 
  -- CONSTANT k_do_inv : real := ((V_DD / V_TH - 1.0)**(1.0/(real(N_DO)))) / (real((D_DO - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_DO)) / relTime)); 
  
  -- "Correct ansatz"
  CONSTANT k_up_std : real := real(((D_UP - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_UP)) / relTime)) * ((V_TH / (V_DD-V_TH))**(1.0/N_UP)); 
  CONSTANT k_do_std : real := real(((D_DO - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_DO)) / relTime)) * ((V_DD-V_TH) / V_TH)**(1.0/N_DO);
BEGIN

  --########################################################  

  hill_channel_involution: PROCESS (input)
    VARIABLE last_output_time : time := -1 sec;
    VARIABLE T, delay : time;
  BEGIN

    T := now - last_output_time;
	IF rising_edge(input) THEN
		-- IF USE_INVERSE = '1' THEN	
			-- delay := - (1.0 / k_up_inv) * (1.0 / (k_do_inv * real((T + D_DO) / relTime)))**(N_DO/N_UP) * relTime + D_UP;
		-- ELSE
			-- delay := - k_up_std * (k_do_std / real((T + D_DO) / relTime))**(N_DO/N_UP) * relTime + D_UP;
		-- END IF;
		
		delay := - k_up_std * (k_do_std / real((T + D_DO) / relTime))**(N_DO/N_UP) * relTime + D_UP;

		last_output_time := now + delay;

		IF (delay < 0 fs) THEN
			delay := 0 fs;
		END IF;	
		output <= TRANSPORT '1' AFTER delay;

    ELSIF falling_edge(input) THEN
		-- IF USE_INVERSE = '1' THEN	
			-- delay := - (1.0 / k_do_inv) * (1.0 / (k_up_inv * real((T + D_UP) / relTime)))**(N_UP/N_DO) * relTime + D_DO;
		-- ELSE
			-- delay := - k_do_std * (k_up_std / real((T + D_UP) / relTime))**(N_UP/N_DO) * relTime + D_DO;
		-- END IF;
		
		delay := - k_do_std * (k_up_std / real((T + D_UP) / relTime))**(N_UP/N_DO) * relTime + D_DO;
		

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
