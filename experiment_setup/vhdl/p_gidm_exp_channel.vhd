-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: p_gidm_exp_channel.vhd
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

PACKAGE gidm_exp_channel_pkg IS
	COMPONENT gidm_exp_channel IS

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
			output : OUT std_logic
		);

	END COMPONENT gidm_exp_channel;
END gidm_exp_channel_pkg;
