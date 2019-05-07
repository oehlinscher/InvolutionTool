-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: DFFRNQ_X1.vhd
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


library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.VITAL_Timing.all;
use IEEE.VITAL_Primitives.all;
use work.exp_channel_pkg.all;
use work.hill_channel_pkg.all;

ENTITY DFFRNQ_X1 IS

	GENERIC (
		tipd_D : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpd_D_Q : VitalDelayType01Z := (OTHERS => 0.0 ns);
		tipd_RN : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpd_RN_Q : VitalDelayType01Z := (OTHERS => 0.0 ns);
		tipd_CLK : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpd_CLK_Q : VitalDelayType01Z := (OTHERS => 0.0 ns);
		
		tpd_rn_q_op_clk_eq_1_cp_an_op_d_eq_1_cp : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpd_rn_q_op_clk_eq_1_cp_an_op_d_eq_0_cp : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpd_rn_q_op_clk_eq_0_cp_an_op_d_eq_1_cp : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpd_rn_q_op_clk_eq_0_cp_an_op_d_eq_0_cp : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpd_clk_q_posedge 						: VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpw_rn_negedge 							: VitalDelayType := 0.0 ns;
		tpw_clk_posedge 						: VitalDelayType := 0.0 ns;
		tpw_clk_negedge 						: VitalDelayType := 0.0 ns;
		trecovery_rn_clk_posedge_posedge 		: VitalDelayType := 0.0 ns;
		tremoval_rn_clk_posedge_posedge 		: VitalDelayType := 0.0 ns;
		tsetup_d_clk_posedge_posedge 			: VitalDelayType := 0.0 ns;
		thold_d_clk_posedge_posedge 			: VitalDelayType := 0.0 ns;
		tsetup_d_clk_negedge_posedge 			: VitalDelayType := 0.0 ns;
		thold_d_clk_negedge_posedge 			: VitalDelayType := 0.0 ns;

	   MsgOn : Boolean := TRUE;
	   TimingChecksOn : Boolean := TRUE;
	   XOn : Boolean := TRUE;
	   InstancePath : String := "*";
	   
	   -- Parameters required to parametrize the channel itself
	   V_DD : real := 1.0;
	   V_TH : real := 0.5;
	   T_P : time := 1 ps;
	   
	   -- Channel specific parameters Hill Channel
	   N_UP : real := 1.0;
	   N_DO : real := 1.0
	   
	);

	PORT (	
		D : 	IN STD_ULOGIC := 'X';
		RN : 	IN STD_ULOGIC := 'X';
		CLK : 	IN STD_ULOGIC := 'X';
		Q : 	OUT STD_ULOGIC := 'U'
	);

	ATTRIBUTE VITAL_LEVEL0 OF DFFRNQ_X1 : ENTITY IS TRUE;

END DFFRNQ_X1;

--BEGIN_ARCH
ARCHITECTURE EXP_CHANNEL_INPUT OF DFFRNQ_X1 IS
BEGIN
  
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE EXP_CHANNEL_OUTPUT OF DFFRNQ_X1 IS
BEGIN  
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE EXP_CHANNEL_OUTPUT_SWAPPED OF DFFRNQ_X1 IS
BEGIN
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE HILL_CHANNEL_INPUT OF DFFRNQ_X1 IS	
BEGIN  
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE HILL_CHANNEL_OUTPUT OF DFFRNQ_X1 IS
BEGIN  
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE HILL_CHANNEL_OUTPUT_SWAPPED OF DFFRNQ_X1 IS
BEGIN  
END;
--END_ARCH