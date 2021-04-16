generate_##SIGNALNAME## : PROCESS
  FILE vector_file : text;
  VARIABLE l : line;
  VARIABLE vector_time : TIME;
  VARIABLE r : INTEGER;
  VARIABLE good_number : BOOLEAN;
BEGIN
  file_open(vector_file, VectorsDir & "##VECTORNAME##", READ_MODE);
  WHILE NOT endfile(vector_file) LOOP
    readline(vector_file, l);

    -- read the time from the beginning of the line
    -- skip the line if it doesn't start with a number
    read(l, r, good => good_number);
    NEXT WHEN NOT good_number;

    vector_time := r * 1 fs; -- convert real number to time

    IF (now < vector_time) THEN -- wait until the vector time
      WAIT FOR vector_time - now;
    END IF;

    FOR idx IN l'RANGE LOOP
      CASE l(idx) IS
        WHEN '0' => -- Drive 0
          ##SIGNALNAME## <= '0';
        WHEN '1' => -- Drive 0
          ##SIGNALNAME## <= '1';
        WHEN ' ' | ht => -- Skip white space
          NEXT;
        WHEN OTHERS => -- Drive 1
          -- Illegal character
          ASSERT false REPORT "Illegal character in vector file: " & l(idx);
          EXIT;
      END CASE;
    END LOOP;
  END LOOP;
  REPORT "Test complete";
  file_close(vector_file);
  WAIT;
END PROCESS;