CONFIGURATION circuit_config OF c17_slack IS
  FOR arch
	-- FOR ALL : ND2M1N
		-- USE ENTITY work.ND2M1N(##GATE_ARCHITECTURE_ND2M1N##)
		-- generic map (
			-- T_P => ##T_P_ND2M1N####CHANNEL_SPECIFIC_GENERICS_ND2M1N##
		-- );
    -- END FOR;	
  END FOR;
END circuit_config;