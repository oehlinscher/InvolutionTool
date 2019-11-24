* circuit: mips_clock
.LIB <SPICE_LIB>
* .INCLUDE <SPICE_CIR>

.INCLUDE /home/s01525898/req_files/15/backend/spice/cell/INV_X1.sp
.INCLUDE /home/s01525898/req_files/15/backend/spice/cell/INV_X2.sp
.INCLUDE /home/s01525898/req_files/15/backend/spice/cell/INV_X4.sp
.INCLUDE /home/s01525898/req_files/15/backend/spice/cell/INV_X8.sp
.INCLUDE /home/s01525898/req_files/15/backend/spice/cell/DFFRNQ_X1.sp

* main circuit
.INCLUDE ../clk.spf

* Circuit for shaping the input
.INCLUDE ../../../experiment_setup/spice/shaping_15nm.sp

.TEMP <TEMP>
.OPTION
+ INGOLD=2
+ PARHIER=LOCAL
+ POST=CSDF
+ ABSVAR=0.05
*+ DELMAX=100fs * use automatic DELMAX

* vdd
vdd mvdd 0 <VDD>V

* shaping
vddshape shapevdd 0 <VDD>v
Xmyshape1 clkshape clk shapevdd shaping 

* circuit under test
Xmycir clk 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 mvdd 0 mips 

* input
* use if no shaping should be at the input
*Vgpwl clk 0 PWL(<clk>)
* use if shaping should be at the input
Vgpwl clkshape 0 PWL(<clk>)


.PROBE TRAN v(clk) v(xmycir.*:ZN)

.TRAN 1PS <STOPTIME>NS

* Average Power calculation via average current
.MEAS TRAN avg_cur avg i(vdd) from=0ns to=<STOPTIME>NS 
.MEAS TRAN avg_mvdd avg V(mvdd) from=0ns to=<STOPTIME>NS 
.MEAS TRAN pwr_avg PARAM='abs(avg_cur*avg_mvdd)'

* Maximum Power calculation via maximum current
.MEAS TRAN max_cur max 'abs(i(vdd))' from=0ns to=<STOPTIME>NS 
.MEAS TRAN max_mvdd max V(mvdd) from=0ns to=<STOPTIME>NS 
.MEAS TRAN pwr_max PARAM='abs(max_cur*max_mvdd)'

.END
