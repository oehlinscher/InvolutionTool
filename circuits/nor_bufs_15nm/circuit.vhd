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

  signal A1_wire : std_logic;
  signal A2_wire : std_logic;
  signal Z_wire : std_logic;

  
  signal initialized : std_logic := '0';
  signal A1_wire_done : std_logic;
  signal A2_wire_done : std_logic;

  component nor_bufs is
    port ( 
      A1_wire: in std_logic;
      A2_wire: in std_logic;
      Z_wire: out std_logic
	 );
    end component;

begin

  --########################################################  
  
	##INPUT_PROCESS##
	
  --########################################################

  c1 : nor_bufs
  port map(
    A1_wire => A1_wire,
    A2_wire => A2_wire,
	  Z_wire => Z_wire
	);

end architecture;