library ieee;
use ieee.std_logic_1164.all;
use ieee.math_real.all;
use work.python_channel_pkg.all;
USE std.textio.ALL;

entity circuit_TB is
	generic(
		VectorsDir :string := ""
	);
  end circuit_TB; 

-----------------------------------------------------------------

architecture TB of circuit_TB is

  signal nx1, nx7, nx3, nx2, nx6 : std_logic;
  signal nx23, nx22 : std_logic;

  signal initialized : std_logic := '0';
  
  signal nx1_done : std_logic := '0'; 
  signal nx7_done : std_logic := '0'; 
  signal nx3_done : std_logic := '0'; 
  signal nx2_done : std_logic := '0'; 
  signal nx6_done : std_logic := '0'; 

  component c17_slack is
    port ( nx1, nx7, nx3, nx2, nx6: in std_logic;
           nx23, nx22: out std_logic
	 );
    end component;

begin

  --########################################################  

	##INPUT_PROCESS##



  
  --########################################################

  uut : c17_slack
  port map(nx1 => nx1,
           nx7 => nx7,
           nx3 => nx3,
           nx2 => nx2,
           nx6 => nx6,
           nx23 => nx23,
           nx22 => nx22
	);

end architecture;