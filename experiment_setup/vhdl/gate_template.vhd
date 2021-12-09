-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: gate_template.vhd
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

library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.VITAL_Timing.all;
use IEEE.VITAL_Primitives.all;
USE work.channel_base_pkg.ALL;
use work.exp_channel_pkg.all;
use work.hill_channel_pkg.all;
use work.sumexp_channel_pkg.all;
use work.puredelay_channel_pkg.all;
use work.gidm_exp_channel_pkg.all;
use work.gidm_hill_channel_pkg.all;
use work.gidm_sumexp_channel_pkg.all;
use work.python_channel_pkg.all;
USE std.textio.all;

ENTITY ##ENTITY_NAME## IS

	GENERIC (
		##ENTITY_GENERIC##

	   MsgOn : Boolean := TRUE;
	   TimingChecksOn : Boolean := TRUE;
	   XOn : Boolean := TRUE;
	   InstancePath : String := "*"
	);

	PORT (
		-- GIDM: We need to initialize in- and outputs with 0, since they are our transition indicator
		-- IDM: We need to initialize the input signals with the value of the predecessor
		##PORTS##
	);

	ATTRIBUTE VITAL_LEVEL0 OF ##ENTITY_NAME## : ENTITY IS TRUE;

END ##ENTITY_NAME##;


--BEGIN_ARCH
ARCHITECTURE ##ARCH_NAME## OF ##ENTITY_NAME## IS
	-- GIDM: Here we need to initialize the GIs with the value of its predecessor and the GO with the value of the channel itself
	-- IDM: Currently only channel location output supported: We need to initialize the GO with the value of the channel itself 
	##ARCH_SIGNALS##
BEGIN

	##ARCH_INPUT_PROCESSES##

	##ARCH_DELAY_CHANNEL##
	
	##ARCH_FUNCTION##
  
END;
--END_ARCH