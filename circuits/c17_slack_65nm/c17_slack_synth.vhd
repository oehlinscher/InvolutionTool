library ieee;
use ieee.std_logic_1164.all;
use IEEE.VITAL_Timing.all;
use IEEE.VITAL_Primitives.all;

ENTITY c17_slack IS
	GENERIC (
		tipd_nx22 : VitalDelayType01 := (0.0 ns, 0.0 ns);
		tipd_nx23 : VitalDelayType01 := (0.0 ns, 0.0 ns);
		

		MsgOn : Boolean := TRUE;
		TimingChecksOn : Boolean := TRUE;
		XOn : Boolean := TRUE;
		InstancePath : String := "*"
	);
	PORT (
		nx1 : IN std_logic;
		nx2 : IN std_logic;
		nx3 : IN std_logic;
		nx6 : IN std_logic;
		nx7 : IN std_logic;
		nx22 : OUT std_logic;
		nx23 : OUT std_logic
	);
END c17_slack;

ARCHITECTURE arch OF c17_slack IS
	SIGNAL net_0, net_1, net_2, net_3 : std_logic; 
	
	COMPONENT ND2M1N IS
		PORT ( A: IN std_logic;
			   B: IN std_logic;	
			   Z: OUT std_logic
		);
	END COMPONENT;

BEGIN
	inst_5 : ND2M1N
		PORT MAP(
			A => net_0,
			B => net_3,
			Z => nx22);
			
	inst_2 : ND2M1N
		PORT MAP(
			A => nx7,
			B => net_1,
			Z => net_2);
			
	inst_1 : ND2M1N
		PORT MAP(
			A => nx1,
			B => nx3,
			Z => net_0);
			
	inst_4 : ND2M1N
		PORT MAP(
			A => net_3,
			B => net_2,
			Z => nx23);
			
	inst_3 : ND2M1N
		PORT MAP(
			A => nx2,
			B => net_1,
			Z => net_3);
			
	inst_0 : ND2M1N
		PORT MAP(
			A => nx3,
			B => nx6,
			Z => net_1);
	
END arch;