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

  signal din : std_logic;
  signal din_TransitionIndicator : std_logic := '0';
  signal din_TransitionAck : std_logic;
  signal dout1, dout2, dout3, dout4 : std_logic;

  component inv_tree is
    port ( 
      din: in std_logic;
      din_TransitionIndicator: in std_logic;
      din_TransitionAck: out std_logic;
      dout1: out std_logic;
      dout2: out std_logic;
      dout3: out std_logic;
      dout4: out std_logic
	 );
    end component;

begin

  --########################################################  
  
	generate_din: PROCESS
    FILE vector_file : text;
    VARIABLE l : line;
    VARIABLE vector_time : time;
    VARIABLE vector_value : std_logic;
    VARIABLE r : integer;
    VARIABLE good_number : boolean;

    FILE tt_file : text;
    VARIABLE tt_line : line;
  BEGIN

    file_open(vector_file, VectorsDir & "vectors_din", READ_MODE);
    WHILE NOT endfile(vector_file) LOOP
      readline(vector_file, l);
      
      -- read the time from the beginning of the line
      -- skip the line if it doesn't start with a number
      read(l, r, good => good_number);
      NEXT WHEN NOT good_number;

      vector_time := r * 1 fs;        -- convert real number to time

      -- IF (now < vector_time) THEN     -- wait until the vector time
      --   WAIT FOR vector_time - now;     -- TODO: As soon as we have negative \delta_min^up/downs, we are not allowed to wait so long here, in order to not violate the ModelSim property of causality
      -- END IF;
      
      -- This is the output for comparability with default delay model

      FOR i IN l'RANGE LOOP
        CASE l(i) IS 
          WHEN '0' => -- Drive 0
              vector_value := '0';
              EXIT;
          WHEN '1' => -- Drive 1
              vector_value := '1';
              EXIT;
          WHEN ' ' | ht => -- Skip white space
              NEXT;
          WHEN OTHERS =>
              -- Illegal character
              ASSERT false REPORT "Illegal character in vector file: " & l(i);
              EXIT;
        END CASE;
      END LOOP;
      
      din <= TRANSPORT vector_value AFTER vector_time - now;
      
      -- Write the Transition Time to file 
      file_open(tt_file, "/home/s01525898/ECSLab_InvolutionTool/circuits/inv_tree_15nm/tt/g10_I", WRITE_MODE);
      write(tt_line, integer'image(r));
      write(tt_line, string'(" "));
      write(tt_line, std_logic'image(vector_value));
      writeline(tt_file, tt_line);
      file_close(tt_file);

      din_TransitionIndicator <= not din_TransitionIndicator;

      -- wait for a toggle on the transition ack signal, then we can continue
      WAIT UNTIL (falling_edge(din_TransitionAck) OR rising_edge(din_TransitionAck)); -- and (falling or rising) and ... if we have fan out >= 2

    END LOOP;
    REPORT "Test complete";
    file_close(vector_file);
    WAIT;
  END PROCESS;
	
  --########################################################

  c1 : inv_tree
  port map(din => din,
  din_TransitionIndicator => din_TransitionIndicator,
  din_TransitionAck => din_TransitionAck,
	dout1 => dout1,
	dout2 => dout2,
	dout3 => dout3,
	dout4 => dout4
	);

end architecture;