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

  signal clk : std_logic;

  component mips is
    port ( clk: 		in std_logic;
           reset: 		in std_logic;
           memdata: 	in std_logic_vector(7 downto 0);
           memread: 	out std_logic;
           memwrite: 	out std_logic;
		   adr: 		out std_logic_vector(7 downto 0);
		   writedata:	out std_logic_vector(7 downto 0)
	 );
    end component;

begin

  --########################################################  
  
	##INPUT_PROCESS##
	
  --########################################################

  c1 : mips
  port map(clk => clk,
	reset => '0',
	memdata => (others => '0'),
	memread => open,
	memwrite => open,
	adr => open,
	writedata => open
	);

end architecture;
