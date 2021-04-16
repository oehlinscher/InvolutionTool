-------------------------------------------------------------------------------
--
--	Involution Tool
--	File: ea_exp_channel.vhd
--	
--  Copyright (C) 2018-2019  Daniel OEHLINGER <d.oehlinger@outlook.com>
--
--  This source file may be used and distributed without restriction provided
--  that this copyright statement is not removed from the file and that any
--  derivative work contains the original copyright notice and the associated
--  disclaimer.
--
--  This source file is free software: you can redistribute it and/or modify it
--  under the terms of the GNU Lesser General Public License as published by
--  the Free Software Foundation, either version 3 of the License, or (at your
--  option) any later version.
--
--  This source file is distributed in the hope that it will be useful, but
--  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
--  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
--  for more details.
--
--  You should have received a copy of the GNU Lesser General Public License
--  along with the noasic library.  If not, see http://www.gnu.org/licenses
--
-------------------------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE work.sumexp_channel_pkg.ALL;
USE work.channel_base_pkg.ALL;

ENTITY sumexp_channel IS
	GENERIC (
		D_UP 		: time; 
		D_DO 		: time; 
		T_P  		: time;
		T_P_PERCENT : real;	
		T_P_MODE	: PARAMETER_MODE := ABSOLUTE;
		V_DD 		: real;
		V_TH 		: real;
		TAU_1_UP 	: time;
		TAU_2_UP 	: time;
		X_1_UP 		: real;
		TAU_1_DO 	: time;
		TAU_2_DO 	: time;
		X_1_DO 		: real;
		INIT_VALUE : std_logic := '0'
	);
	PORT ( 
		input : IN std_logic;
		output : OUT std_logic := INIT_VALUE
	);

END sumexp_channel;



-----------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.math_real.ALL;

ARCHITECTURE beh OF sumexp_channel IS
	CONSTANT relTime : time := 1 fs;  
	
	-- TODO: Pass from outside?
	-- C should be around 1 (at least if TAU_1 and TAU_2 are specified propperly)
	CONSTANT EPSILON_C : real := 1.0e-10; -- TODO: Discuss termination criteria
	-- The delay is probably around 
	CONSTANT EPSILON_T : real := 1.0e-7; -- TODO: Discuss termination criteria
		
	FUNCTION newton_raphson_func
	  GENERIC (
		FUNCTION FUNC (x: real) RETURN real;	
		FUNCTION FUNC_PRIME (x: real) RETURN real;
		EPSILON : real;	-- Termination criteria
		X_MIN_VALUE : in real; -- Required that we do not run into numerical issues
		ATTENUATION_BELOW_VALUE : in real -- If the value for X is below this value, we apply attenuation (useful to find the "correct" root), set to min value if damping feature is not required
	  )
	  PARAMETER
	  (
	    X_IN  : in  real; -- Initial Value
		TARGET_VALUE : in real; -- f(x) = TARGET_VALUE
		ENABLE : in boolean -- Especially required when called before timing data is loaded (function call in architecture section)
	  )   
	  RETURN real 
	  IS
		VARIABLE FUNC_X : real := 0.0;
		VARIABLE FUNC_PRIME_X : real := 0.0;
		VARIABLE H : real := 0.0;	
		VARIABLE X : real := 0.0;
	  BEGIN  		
		X := X_IN;		
		H := EPSILON;	
		if ENABLE then
			-- report "Start Iteration with X: " & real'IMAGE(X) & ", TARGET_VALUE: " & real'IMAGE(TARGET_VALUE) & ", EPSILON: " & real'IMAGE(EPSILON) & ", D_UP: " & time'IMAGE(D_UP) & ", X_MIN_VALUE:" & real'IMAGE(X_MIN_VALUE);
			WHILE ABS(H) >= EPSILON AND ABS(X_IN) >= X_MIN_VALUE LOOP
				FUNC_X := FUNC(X);
				FUNC_PRIME_X := FUNC_PRIME(X);
				-- report "FUNC(X): " & real'IMAGE(FUNC_X); 
				-- report "FUNC_PRIME(X): " & real'IMAGE(FUNC_PRIME_X); 
				H := (FUNC_X - TARGET_VALUE) / FUNC_PRIME_X;
				WHILE X - H < ATTENUATION_BELOW_VALUE LOOP
					H := H / 2.0;
				END LOOP;			
				X := X - h;
				-- report "X: " & real'IMAGE(X);
			END LOOP;
			-- report "End Iteration with X: " & real'IMAGE(X);
		END IF;
		RETURN X;
	END;
	
	FUNCTION is_pure_delay
	RETURN boolean
	IS
	BEGIN
		RETURN (T_P_PERCENT = 100.0 and T_P_MODE = PERCENT);
	END;	
	
	FUNCTION set_c 
	GENERIC 
	(	
		FUNCTION FUNC (x_in: real; target_value: real; enable: boolean) RETURN real	
	)
	PARAMETER 
	(
		D : in time
	)
	RETURN real
	IS
	BEGIN
		IF is_pure_delay THEN
			-- We are in the PureDelay Channel case (and we cannot find a c (at least one which is not infinity) which satisfies f(c) = V_TH, and hence we set it to 0)
			-- We will check later anyway that if we are in the pure delay case we do not call newton on f(t)
			RETURN 1.0;
		ELSE
			RETURN FUNC(1.0, V_TH, real(D / relTime) > 0.0);
		END IF;

	END;
	
	-- General f with c and t as variables
	FUNCTION f_up_ct (c : IN real; t : IN real; x1 : IN real; tau1 : IN time; tau2 : in time)
		RETURN real IS
	VARIABLE V : real := 0.0;
	BEGIN
		-- report "f_up_ct: c: " & real'IMAGE(c) & ", t: " & real'IMAGE(t);
		V := V_DD * (1.0 - x1 * EXP(-c * (t / real(tau1 / relTime))) - (1.0 - x1) * EXP(-c * (t / real(tau2 / relTime))));
		-- report "V: " & real'IMAGE(V);
		return V;
	END;
	
	FUNCTION f_do_ct (c : IN real; t : IN real; x1 : IN real; tau1 : IN time; tau2 : in time)
		RETURN real IS
	VARIABLE V : real := 0.0;
	BEGIN
		-- report "f_do_ct: c: " & real'IMAGE(c) & ", t: " & real'IMAGE(t);
		V := V_DD - f_up_ct(c, t, x1, tau1, tau2);
		-- report "V: " & real'IMAGE(V);
		return V;
	END;
	
	-- f(c)'
	FUNCTION f_up_ct_prime_c (c : IN real; t : IN real; x1 : IN real; tau1 : IN time; tau2 : in time)
		RETURN real IS
	VARIABLE V : real := 0.0;
	BEGIN
		-- report "f_up_ct_prime_c: c: " & real'IMAGE(c) & ", t: " & real'IMAGE(t);
		V := V_DD * ((x1 * (t / real(tau1 / relTime))) * EXP(-c * (t / real(tau1 / relTime))) + ((1.0 - x1) * (t / real(tau2 / relTime))) * EXP(-c * (t / real(tau2 / relTime))));
		-- report "V: " & real'IMAGE(V);
		return V;
	END;
	
	FUNCTION f_do_ct_prime_c (c : IN real; t : IN real; x1 : IN real; tau1 : IN time; tau2 : in time)
		RETURN real IS
	VARIABLE V : real := 0.0;
	BEGIN
		-- report "f_do_ct_prime_c: c: " & real'IMAGE(c) & ", t: " & real'IMAGE(t);
		V := -f_up_ct_prime_c(c, t, x1, tau1, tau2);
		-- report "V: " & real'IMAGE(V);
		return V;
	END;
	
	-- Overloads for f(c) and f'(c)
	FUNCTION f_up_c(c : IN real)
		RETURN real IS
	BEGIN
		-- report "D_UP: " & time'IMAGE(D_UP) & ", D_DO: " & time'IMAGE(D_DO) & ", VTH:" & real'IMAGE(V_TH) & ", VDD:" & real'IMAGE(V_DD);
		return f_up_ct(c, real((D_UP - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_UP)) / relTime), X_1_UP, TAU_1_UP, TAU_2_UP);
	END;
	
	FUNCTION f_do_c(c : IN real)
		RETURN real IS
	BEGIN
		return f_do_ct(c, real((D_DO - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_DO)) / relTime), X_1_DO, TAU_1_DO, TAU_2_DO);
	END;
	
	FUNCTION f_up_c_prime_c(c : IN real)
		RETURN real IS
	BEGIN
		return f_up_ct_prime_c(c, real((D_UP - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_UP)) / relTime), X_1_UP, TAU_1_UP, TAU_2_UP);
	END;
	
	FUNCTION f_do_c_prime_c(c : IN real)
		RETURN real IS
	BEGIN
		return f_do_ct_prime_c(c, real((D_DO - calc_tp(T_P, T_P_PERCENT, T_P_MODE, D_DO)) / relTime), X_1_DO, TAU_1_DO, TAU_2_DO);
	END;
	
	-- Instantiations of newton for calculation C_UP / C_DO
	FUNCTION newton_f_up_c IS NEW newton_raphson_func
	GENERIC MAP(FUNC => f_up_c, FUNC_PRIME => f_up_c_prime_c, EPSILON => EPSILON_C, X_MIN_VALUE => 0.0, ATTENUATION_BELOW_VALUE => 0.0);
	
	FUNCTION newton_f_do_c IS NEW newton_raphson_func
	GENERIC MAP(FUNC => f_do_c, FUNC_PRIME => f_do_c_prime_c, EPSILON => EPSILON_C, X_MIN_VALUE => 0.0, ATTENUATION_BELOW_VALUE => 0.0);
	
	-- NOTE: The check if D_DO and D_UP > 0 is required, 
	-- because otherwise the function would be executed before the sdf file has been loaded, 
	-- which causes overflows (since D_UP and D_DO are then assumed to be 0)
	-- This is just a workaround, maybe there is a better solution to specifiy the order of execution
		
	FUNCTION set_c_up_inst IS NEW set_c
	GENERIC MAP(FUNC => newton_f_up_c);
	
	FUNCTION set_c_do_inst IS NEW set_c
	GENERIC MAP(FUNC => newton_f_do_c);
	
	CONSTANT C_UP : real := set_c_up_inst(D_UP);
	CONSTANT C_DO : real := set_c_do_inst(D_DO);
  
	-- f(t)
	FUNCTION f_up_t (t : IN real)
		RETURN real IS
	BEGIN
		RETURN f_up_ct(C_UP, t, X_1_UP, TAU_1_UP, TAU_2_UP);
	END;

	FUNCTION f_do_t (t : IN real)
		RETURN real IS
	BEGIN
		RETURN f_do_ct(C_DO, t, X_1_DO, TAU_1_DO, TAU_2_DO);
	END; 
	
	-- f(t)' (with c as parameter)	
	FUNCTION f_up_ct_prime_t (c : IN real; t : IN real; x1 : IN real; tau1 : IN time; tau2 : in time)
		RETURN real IS
	BEGIN
		RETURN V_DD * ((x1 * (c / real(tau1 / relTime))) * EXP(-c * (t / real(tau1 / relTime))) + ((1.0 - x1) * (c / real(tau2 / relTime))) * EXP(-c * (t / real(tau2 / relTime))));
	END;
	
	FUNCTION f_do_ct_prime_t (c : IN real; t : IN real; x1 : IN real; tau1 : IN time; tau2 : in time)
		RETURN real IS
	BEGIN
		RETURN -f_up_ct_prime_t(C_DO, t, x1, tau1, tau2);
	END;
	
	-- f'(t)
	FUNCTION f_up_t_prime_t (t : IN real)
		RETURN real IS
	BEGIN
		RETURN f_up_ct_prime_t(C_UP, t, X_1_UP, TAU_1_UP, TAU_2_UP);
	END;
	
	FUNCTION f_do_t_prime_t (t : IN real)
		RETURN real IS
	BEGIN
		RETURN f_do_ct_prime_t(C_DO, t, X_1_DO, TAU_1_DO, TAU_2_DO);
	END;

	-- FUNCTION newton_f_up_t IS NEW newton_raphson_func
	-- GENERIC MAP(FUNC => f_up_t, FUNC_PRIME => f_up_t_prime_t, EPSILON => EPSILON_T, X_MIN_VALUE => real(D_UP / relTime)/1.0e9);
	
	-- FUNCTION newton_f_do_t IS NEW newton_raphson_func
	-- GENERIC MAP(FUNC => f_do_t, FUNC_PRIME => f_do_t_prime_t, EPSILON => EPSILON_T, X_MIN_VALUE => real(D_DO / relTime)/1.0e9);
	
	
	FUNCTION newton_f_up_t IS NEW newton_raphson_func
	GENERIC MAP(FUNC => f_up_t, FUNC_PRIME => f_up_t_prime_t, EPSILON => EPSILON_T, X_MIN_VALUE => 1.0e-2, ATTENUATION_BELOW_VALUE => 0.0);
	
	FUNCTION newton_f_do_t IS NEW newton_raphson_func
	GENERIC MAP(FUNC => f_do_t, FUNC_PRIME => f_do_t_prime_t, EPSILON => EPSILON_T, X_MIN_VALUE => 1.0e-2, ATTENUATION_BELOW_VALUE => 0.0);
	
BEGIN

  --########################################################  
  
  sumexp_channel_involution: PROCESS (input)
    VARIABLE last_output_time : time;
    VARIABLE T, delay : time;
	VARIABLE sum_exp_del : time;
	VARIABLE first_transition : bit := '1';
  BEGIN
	-- report "D_UP: " & time'IMAGE(D_UP) & ", T_P: " & time'IMAGE(T_P);   
	-- report "C_UP: " & real'IMAGE(C_UP) & ", C_DO: " & real'IMAGE(C_DO);	
	

	-- report "input transition at " & time'IMAGE(now);	
	-- report "last output at " & time'IMAGE(last_output_time);
    T := now - last_output_time;
	-- report "T = " & time'IMAGE(T);

	-- in VITAL they check for A'LAST_VALUE
	-- but there also 'L' and 'H' of importance
	IF input'EVENT and input = '1'  THEN
		-- report "got rising edge";	

		if first_transition = '1' then
			delay := D_UP;
			first_transition := '0';
		else
			sum_exp_del := 0 fs;
			IF NOT is_pure_delay THEN
				sum_exp_del := (newton_f_up_t(1000.0, f_do_t(real((T + D_DO) / relTime)), true) * relTime);
			END IF;		
			delay := D_UP - sum_exp_del;
		end if;
		-- report "SumExpDelay UP: " & time'IMAGE(sum_exp_del) & ", T: " & time'IMAGE(T) & ", D_DO: " & time'IMAGE(D_DO) &  ", Target Value: " & real'IMAGE(f_do_t(real((T + D_DO) / relTime)));
		-- report "delay: " & time'IMAGE(delay);

		last_output_time := now + delay;

		IF (delay < 0 fs) THEN
			delay := 0 fs;
			report "Capped delay";
		END IF;	
		output <= TRANSPORT '1' AFTER delay;

	ELSIF input'EVENT and input = '0' THEN
		-- report "got falling edge";

		if first_transition = '1' then
			delay := D_DO;
			first_transition := '0';
		else	
			sum_exp_del := 0 fs;
			IF NOT is_pure_delay THEN
				sum_exp_del := (newton_f_do_t(1000.0, f_up_t(real((T + D_UP) / relTime)), true) * relTime);
			END IF;

			delay := D_DO - sum_exp_del;	
		end if;

		-- report "SumExpDelay DO: " & time'IMAGE(sum_exp_del) & ", T: " & time'IMAGE(T) & ", D_UP: " & time'IMAGE(D_UP) &  ", Target Value: " & real'IMAGE(f_up_t(real((T + D_UP) / relTime)));
		-- report "delay: " & time'IMAGE(delay);

		last_output_time := now + delay;

		IF (delay < 0 fs) THEN
			delay := 0 fs;
			report "Capped delay";
		END IF;	
		output <= TRANSPORT '0' AFTER delay;
    END IF;

  END PROCESS;

  --########################################################

END ARCHITECTURE;
