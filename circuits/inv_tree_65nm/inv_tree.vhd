library ieee;
use ieee.std_logic_1164.all;
use IEEE.VITAL_Timing.all;
use IEEE.VITAL_Primitives.all;

ENTITY inv_tree IS
	GENERIC (
		tipd_dout1 : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tipd_dout2 : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tipd_dout3 : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tipd_dout4 : VitalDelayType01 := (0.0 ns, 0.0 ns);
		

	   MsgOn : Boolean := TRUE;
	   TimingChecksOn : Boolean := TRUE;
	   XOn : Boolean := TRUE;
	   InstancePath : String := "*"
	);
	PORT (
		din : IN std_logic;
		dout1 : OUT std_logic;
		dout2 : OUT std_logic;
		dout3 : OUT std_logic;
		dout4 : OUT std_logic
	);
END inv_tree;

ARCHITECTURE arch OF inv_tree IS
	SIGNAL temp1, temp2, temp3, temp4, temp5, temp51, temp52 : std_logic;
	
	
	  COMPONENT CKINVM1N IS
		PORT ( A: in std_logic;
			   Z: out std_logic
		 );
		END COMPONENT;
BEGIN				

	g10: CKINVM1N
		PORT MAP(
			A => din,
			Z => temp1);
			
	g11: CKINVM1N
		PORT MAP(
			A => temp1,
			Z => temp2);
			
	g12: CKINVM1N
		PORT MAP(
			A => temp2,
			Z => temp3);
			
	g13: CKINVM1N
		PORT MAP(
			A => temp3,
			Z => temp4);
			
	g14: CKINVM1N
		PORT MAP(
			A => temp4,
			Z => temp5);
			
	g15: CKINVM1N
		PORT MAP(
			A => temp5,
			Z => temp51);
			
	g16: CKINVM1N
		PORT MAP(
			A => temp5,
			Z => temp52);	
	
	g17: CKINVM1N
		PORT MAP(
			A => temp51,
			Z => dout1);
			
	g18: CKINVM1N
		PORT MAP(
			A => temp51,
			Z => dout2);
			
	g19: CKINVM1N
		PORT MAP(
			A => temp52,
			Z => dout3);
			
	g20: CKINVM1N
		PORT MAP(
			A => temp52,
			Z => dout4);
			
END arch;