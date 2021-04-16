##INPUT##_delta_proc : PROCESS(##INPUT##)		
		FILE tt_file : TEXT;
		VARIABLE l : LINE;
		VARIABLE r : INTEGER;
		VARIABLE good_number : BOOLEAN;

		VARIABLE tt_time : TIME;
		VARIABLE tt_level : STD_ULOGIC;

		VARIABLE last_transition : time := -1 sec;
		VARIABLE delay : time := -1 sec;
		VARIABLE pure_delay : time;
	BEGIN	
		IF rising_edge(##INPUT##) or falling_edge(##INPUT##) THEN
			-- We read from the file corresponding to the outut of the predecessor
			file_open(tt_file, "##TT_FILE##", READ_MODE);
			readline(tt_file, l);			
			read(l, r, good => good_number);
			tt_time := r * 1 fs;
			FOR i IN l'RANGE LOOP
				CASE l(i) IS  
					WHEN '0' => -- Drive 0
						tt_level := '0';
					WHEN '1' => -- Drive 1
						tt_level := '1';
					WHEN ' ' | ht | ''' => -- Skip white space / tab and '
						NEXT;
					WHEN OTHERS => -- Drive 1
						-- Illegal character
						ASSERT false REPORT "Illegal character in vector file: " & l(i);
						EXIT;
				END CASE;
			END LOOP;

			file_close(tt_file);


			##PURE_DELAY_CALC##

			if tt_time + pure_delay < now then
				-- In this case we possibly need to cap the delay.
				-- However, we first check if there is no acausal behaviour happening
				if last_transition < now then
					REPORT "Acausal behaviour. This should never happen!" severity failure;
				end if;				
				##INPUT##AfterDelta <= tt_level; -- Cap the delay
				last_transition := now; -- Update the time of the last transition
			else
				##INPUT##AfterDelta <= TRANSPORT tt_level AFTER tt_time + pure_delay - now;	
				last_transition := tt_time + pure_delay; -- Update the time of the last transition			
			end if;

		END IF;
    END PROCESS;