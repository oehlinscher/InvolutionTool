-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: ea_pure_delay_channel.vhd
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

ENTITY puredelay_channel IS
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

END puredelay_channel;

-----------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ARCHITECTURE beh OF puredelay_channel IS

BEGIN
	pure_delay : PROCESS (input)
	BEGIN
		IF rising_edge(input) THEN
			output <= TRANSPORT input AFTER D_UP;
		ELSIF falling_edge(input) THEN
			output <= TRANSPORT input AFTER D_DO;
		ELSIF (now = 0 fs) THEN
			output <= input;
		END IF;

	END PROCESS;

END ARCHITECTURE;