-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: p_channel_base.vhd
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

PACKAGE channel_base_pkg IS
	CONSTANT REL_TIME : time := 1 fs;  
	TYPE PARAMETER_MODE is (ABSOLUTE, PERCENT);
	
	FUNCTION calc_tp
	PARAMETER
	(
		T_P 		: time;
		T_P_PERCENT : real;		
		T_P_MODE	: PARAMETER_MODE;
		D			: time
	)
	RETURN time;
	
END channel_base_pkg;

PACKAGE BODY channel_base_pkg IS

	FUNCTION calc_tp
	PARAMETER
	(
		T_P 		: time;
		T_P_PERCENT : real;		
		T_P_MODE	: PARAMETER_MODE;
		D			: time
	)
	RETURN time IS
	BEGIN
		-- report "calc_tp";
		CASE T_P_MODE IS
			WHEN ABSOLUTE =>			
				-- report "T_P ABSOLUTE: " & time'IMAGE(T_P);	
				RETURN T_P;
			WHEN PERCENT =>
				ASSERT (T_P_PERCENT >= 0.0 AND T_P_PERCENT <= 100.0) REPORT "The range for the T_P_PERCENT value is [0, 100]" SEVERITY error;
				IF D = 0 fs THEN					
					-- REPORT "T_P PERCENT FIRST: " & time'IMAGE((real(D / REL_TIME) * (T_P_PERCENT / 100.0)) * REL_TIME);
					RETURN T_P; -- This is required since the SDF File is loaded after this function is called, and we would return 0, which would cause some channels (e.g. Hill-Channel to get infinite parameter values). Once the sdf file is loaded, the function is reexecuted, and we go into the else branch and return a proper value
				ELSE				
					-- REPORT "D: " & time'IMAGE(D);
					-- REPORT "T_P PERCENT 1: " & real'IMAGE(real(D / REL_TIME));
					-- REPORT "T_P PERCENT 2: " & real'IMAGE((real(D / REL_TIME) * (T_P_PERCENT / 100.0)));
					-- REPORT "T_P PERCENT: " & time'IMAGE((real(D / REL_TIME) * (T_P_PERCENT / 100.0)) * REL_TIME);	
					RETURN (real(D / REL_TIME) * (T_P_PERCENT / 100.0)) * REL_TIME;
				END IF;
		END CASE;
	END;	
	
END PACKAGE BODY channel_base_pkg;