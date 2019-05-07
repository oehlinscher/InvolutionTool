* circuit: c17_slack
.LIB <SPICE_LIB>
.INCLUDE <SPICE_CIR>

* main circuit
.INCLUDE ../c17_slack.sp

* Circuit for shaping the input
.INCLUDE ../../../experiment_setup/spice/shaping_65nm.sp

.TEMP <TEMP> * To be adapted?
.OPTION
+ INGOLD=2
+ PARHIER=LOCAL
+ POST=CSDF
+ PROBE
+ BRIEF
+ ACCURATE
+ ABSVAR=0.05
+ DELMAX=100fs

* vdd
vdd mvdd 0 <VDD>v

* shaping
vddshape shapevdd 0 <VDD>v
Xmyshape1 nx1shape nx1 shapevdd shaping 
.PROBE TRAN v(nx1shape)
Xmyshape2 nx7shape nx7 shapevdd shaping 
.PROBE TRAN v(nx7shape)
Xmyshape3 nx3shape nx3 shapevdd shaping 
.PROBE TRAN v(nx3shape)
Xmyshape4 nx2shape nx2 shapevdd shaping 
.PROBE TRAN v(nx2shape)
Xmyshape5 nx6shape nx6 shapevdd shaping 
.PROBE TRAN v(nx6shape)
* end shaping

* circuit under test
Xmycir nx1 nx7 nx3 nx2 nx6 nx23 nx22 mvdd c17_slack

* input
* use if no shaping should be at the input
*Vgpwl1 nx1 0 PWL(<nx1>)
*Vgpwl7 nx7 0 PWL(<nx7>)
*Vgpwl3 nx3 0 PWL(<nx3>)
*Vgpwl2 nx2 0 PWL(<nx2>)
*Vgpwl6 nx6 0 PWL(<nx6>)
* use if shaping should be at the input
Vgpwl1 nx1shape 0 PWL(<nx1>)
Vgpwl7 nx7shape 0 PWL(<nx7>)
Vgpwl3 nx3shape 0 PWL(<nx3>)
Vgpwl2 nx2shape 0 PWL(<nx2>)
Vgpwl6 nx6shape 0 PWL(<nx6>)

.PROBE TRAN v(nx1) v(nx2) v(nx3) v(nx6) v(nx7) v(xmycir.inst_*:z)
.TRAN 0.01PS <STOPTIME>NS

* Average Power calculation via average current
.MEAS TRAN avg_cur avg i(vdd) from=0ns to=<STOPTIME>NS 
.MEAS TRAN avg_mvdd avg V(mvdd) from=0ns to=<STOPTIME>NS 
.MEAS TRAN pwr_avg PARAM='abs(avg_cur*avg_mvdd)'

* Maximum Power calculation via maximum current
.MEAS TRAN max_cur max 'abs(i(vdd))' from=0ns to=<STOPTIME>NS 
.MEAS TRAN max_mvdd max V(mvdd) from=0ns to=<STOPTIME>NS 
.MEAS TRAN pwr_max PARAM='abs(max_cur*max_mvdd)'

* Find out the threshold values which are used by SPICE? -> we decided to use a single threshold, the same that we use for creating the crossings file
* net_0, net_1, net_2, net_3
.LPRINT(<VTH>, <VTH>) v(nx1) v(nx2) v(nx3) v(nx6) v(nx7) v(xmycir.inst_*:z)

.END
