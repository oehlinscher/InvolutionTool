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

  signal din : std_logic;
  signal dout1, dout2, dout3, dout4 : std_logic;

  signal initialized : std_logic := '0';
  signal din_done : std_logic;

  component inv_tree is
    port ( din: in std_logic;
           dout1: out std_logic;
           dout2: out std_logic;
           dout3: out std_logic;
           dout4: out std_logic
	 );
    end component;

begin

  --########################################################  
  
	##INPUT_PROCESS##
	
  --########################################################

  c1 : inv_tree
  port map(din => din,
	dout1 => dout1,
	dout2 => dout2,
	dout3 => dout3,
	dout4 => dout4
	);

end architecture;