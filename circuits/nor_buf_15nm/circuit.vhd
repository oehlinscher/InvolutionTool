library ieee;
use ieee.std_logic_1164.all;
use ieee.math_real.all;
use work.exp_channel_pkg.all;
use work.python_channel_pkg.all;
USE std.textio.ALL;

entity circuit_TB is
	generic(
		VectorsDir :string := ""
	);
end circuit_TB; 

-----------------------------------------------------------------

architecture TB of circuit_TB is

  signal A1 : std_logic;
  signal A2 : std_logic;
  signal Z : std_logic;

  
  signal initialized : std_logic := '0';
  signal A1_done : std_logic;
  signal A2_done : std_logic;

  component nor_buf is
    port ( 
      A1: in std_logic;
      A2: in std_logic;
      Z: out std_logic
	 );
    end component;

begin

  --########################################################  
  
	##INPUT_PROCESS##
	
  --########################################################

  c1 : nor_buf
  port map(
    A1 => A1,
    A2 => A2,
	  Z => Z
	);

end architecture;