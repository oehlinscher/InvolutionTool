configuration circuit_config of inv_tree is
  for arch
	-- for all : CKINVM1N
		-- use entity work.CKINVM1N(##GATE_ARCHITECTURE_CKINVM1N##)
		-- generic map (
			-- T_P => ##T_P_ND2M1N####CHANNEL_SPECIFIC_GENERICS_CKINVM1N##
		-- );
    -- end for;	
  end for;
end circuit_config;