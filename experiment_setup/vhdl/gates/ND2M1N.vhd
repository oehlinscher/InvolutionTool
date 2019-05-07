-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: ND2M1N.vhd
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

ENTITY ND2M1N IS

	GENERIC (
		tipd_A : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpd_A_Z : VitalDelayType01Z := (OTHERS => 0.0 ns);
		tipd_B : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tpd_B_Z : VitalDelayType01Z := (OTHERS => 0.0 ns);
		

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
		A : IN STD_ULOGIC := 'X';
		B : IN STD_ULOGIC := 'X';
		Z : OUT STD_ULOGIC := 'U'
	);

	ATTRIBUTE VITAL_LEVEL0 OF ND2M1N : ENTITY IS TRUE;

END ND2M1N;

--BEGIN_ARCH
ARCHITECTURE EXP_CHANNEL_INPUT OF ND2M1N IS
	SIGNAL A_del : STD_ULOGIC := 'X';
	SIGNAL B_del : STD_ULOGIC := 'X';
	
BEGIN

	delay_A : exp_channel
	generic map(
		D_UP => tpd_A_Z(tr01),
		D_DO => tpd_A_Z(tr10),
		T_P => T_P,
		V_DD => V_DD,
		V_TH => V_TH)
	port map(
		input => A,
		output => A_del);

	delay_B : exp_channel
	generic map(
		D_UP => tpd_B_Z(tr01),
		D_DO => tpd_B_Z(tr10),
		T_P => T_P,
		V_DD => V_DD,
		V_TH => V_TH)
	port map(
		input => B,
		output => B_del);

	
	
	Z <= A_del nand B_del;
  
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE EXP_CHANNEL_OUTPUT OF ND2M1N IS
	SIGNAL Z_pre : STD_ULOGIC := 'X';
	
BEGIN

	delay_Z_pre : exp_channel
	generic map(
		D_UP => (tpd_A_Z(tr01) + tpd_A_Z(tr01))/2,
		D_DO => (tpd_A_Z(tr10) + tpd_A_Z(tr10))/2,
		T_P => T_P,
		V_DD => V_DD,
		V_TH => V_TH)
	port map(
		input => Z_pre,
		output => Z);

	
	
	Z_pre <= A nand B;
  
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE EXP_CHANNEL_OUTPUT_SWAPPED OF ND2M1N IS
	SIGNAL Z_pre : STD_ULOGIC := 'X';
	
BEGIN

	delay_Z_pre : exp_channel
	generic map(
		D_UP => (tpd_A_Z(tr10) + tpd_A_Z(tr10))/2,
		D_DO => (tpd_A_Z(tr01) + tpd_A_Z(tr01))/2,
		T_P => T_P,
		V_DD => V_DD,
		V_TH => V_TH)
	port map(
		input => Z_pre,
		output => Z);

	
	
	Z_pre <= A nand B;
  
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE HILL_CHANNEL_INPUT OF ND2M1N IS
	SIGNAL A_del : STD_ULOGIC := 'X';
	SIGNAL B_del : STD_ULOGIC := 'X';
	
BEGIN

	delay_A : hill_channel
	generic map(
		D_UP => tpd_A_Z(tr01),
		D_DO => tpd_A_Z(tr10),
		T_P => T_P,
		V_DD => V_DD,
		V_TH => V_TH,
		N_UP => N_UP,
		N_DO => N_DO)
	port map(
		input => A,
		output => A_del);

	delay_B : hill_channel
	generic map(
		D_UP => tpd_B_Z(tr01),
		D_DO => tpd_B_Z(tr10),
		T_P => T_P,
		V_DD => V_DD,
		V_TH => V_TH,
		N_UP => N_UP,
		N_DO => N_DO)
	port map(
		input => B,
		output => B_del);

	
	
	Z <= A_del nand B_del;
  
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE HILL_CHANNEL_OUTPUT OF ND2M1N IS
	SIGNAL Z_pre : STD_ULOGIC := 'X';
	
BEGIN

	delay_Z_pre : hill_channel
	generic map(
		D_UP => (tpd_A_Z(tr01) + tpd_A_Z(tr01))/2,
		D_DO => (tpd_A_Z(tr10) + tpd_A_Z(tr10))/2,
		T_P => T_P,
		V_DD => V_DD,
		V_TH => V_TH,
		N_UP => N_UP,
		N_DO => N_DO)
	port map(
		input => Z_pre,
		output => Z);

	
	
	Z_pre <= A nand B;
  
END;
--END_ARCH

--BEGIN_ARCH
ARCHITECTURE HILL_CHANNEL_OUTPUT_SWAPPED OF ND2M1N IS
	SIGNAL Z_pre : STD_ULOGIC := 'X';
	
BEGIN

	delay_Z_pre : hill_channel
	generic map(
		D_UP => (tpd_A_Z(tr10) + tpd_A_Z(tr10))/2,
		D_DO => (tpd_A_Z(tr01) + tpd_A_Z(tr01))/2,
		T_P => T_P,
		V_DD => V_DD,
		V_TH => V_TH,
		N_UP => N_UP,
		N_DO => N_DO)
	port map(
		input => Z_pre,
		output => Z);

	
	
	Z_pre <= A nand B;
  
END;
--END_ARCH