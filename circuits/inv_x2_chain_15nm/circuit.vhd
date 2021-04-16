library ieee;
use ieee.std_logic_1164.all;
use ieee.math_real.all;
use work.exp_channel_pkg.all;
USE std.textio.ALL;

entity circuit_TB is
	generic(
		VectorsDir :string := ""
	);
end circuit_TB; 

-----------------------------------------------------------------

architecture TB of circuit_TB is

  signal I : std_logic;
  signal Z : std_logic;

  component inv_x2_chain is
    port ( I: in std_logic;
           Z: out std_logic
	 );
    end component;

begin

  --########################################################  
  
	##INPUT_PROCESS##
	
  --########################################################

  c1 : inv_x2_chain
  port map(I => I,
	Z => Z
	);

end architecture;