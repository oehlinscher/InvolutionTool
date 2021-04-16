generate_##SIGNALNAME## : PROCESS
  FILE vector_file : text;
  VARIABLE l : line;
  VARIABLE vector_time : TIME;
  VARIABLE vector_value : std_logic;
  VARIABLE r : INTEGER;
  VARIABLE good_number : BOOLEAN;  
  FILE tt_file : text;
  VARIABLE tt_line : line;
BEGIN
  file_open(vector_file, VectorsDir & "##VECTORNAME##", READ_MODE);
  WHILE NOT endfile(vector_file) LOOP
    readline(vector_file, l);

    -- read the time from the beginning of the line
    -- skip the line if it doesn't start with a number
    read(l, r, good => good_number);
    NEXT WHEN NOT good_number;

    vector_time := r * 1 fs; -- convert real number to time

    FOR idx IN l'RANGE LOOP
      CASE l(idx) IS
        WHEN '0' => -- Drive 0
          vector_value := '0';
        WHEN '1' => -- Drive 0
          vector_value := '1';
        WHEN ' ' | ht => -- Skip white space
          NEXT;
        WHEN OTHERS => -- Drive 1
          -- Illegal character
          ASSERT false REPORT "Illegal character in vector file: " & l(idx);
          EXIT;
      END CASE;
    END LOOP;

    
    ##SIGNALNAME## <= vector_value;

    write(tt_line, integer'image(r));
    write(tt_line, string'(" "));
    write(tt_line, std_logic'image(vector_value));
    file_open(tt_file, "##TT_FILE_PATH##", WRITE_MODE);
    writeline(tt_file, tt_line);
    file_close(tt_file);
    
    write(tt_line, integer'image(r));
    write(tt_line, string'(" "));
    write(tt_line, std_logic'image(vector_value));
    file_open(tt_file, "##TT_FILE_PATH##.complete", APPEND_MODE);
    writeline(tt_file, tt_line);
    file_close(tt_file);    

    -- This is necessary to ensure that the previous transition has been processed by the successors
    -- Waiting 1 fs is no problem, since it is the smallest timestep possible,
    -- and therefore we cannot "miss" the next transition
    WAIT FOR 1 fs;
  END LOOP;
  REPORT "Test complete";
  file_close(vector_file);
  WAIT;
END PROCESS;