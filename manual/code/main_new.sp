* circuit: inv tree
.LIB <SPICE_LIB>
.INCLUDE <SPICE_CIR>

* main circuit
.INCLUDE ../inv_tree.sp

* Circuit for shaping the input
.INCLUDE ../../../experiment_setup/spice/shaping.sp

.TEMP <TEMP>
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
Xmyshape1 dinshape din shapevdd shaping 
.PROBE TRAN v(dinshape)

* circuit under test
Xmycir din dout1 dout2 dout3 dout4 mvdd inv_tree 

* input
* use if no shaping should be at the input
*Vgpwl din 0 PWL(<din>)
* use if shaping should be at the input
Vgpwl dinshape 0 PWL(<din>)



.PROBE TRAN v(din) v(dout*) v(xmycir.g*:a) v(dinshape)
.TRAN 0.01PS <STOPTIME>NS

* Average Power calculation via average current
.MEAS TRAN avg_cur avg i(vdd) from=0ns to=<STOPTIME>NS 
.MEAS TRAN pwr_avg PARAM='abs(avg_cur*V(mvdd))'
.print par('pwr_avg')

* Maximum Power calculation via maximum current
.MEAS TRAN max_cur max 'abs(i(vdd))' from=0ns to=<STOPTIME>NS 
.MEAS TRAN pwr_max PARAM='abs(max_cur*V(mvdd))'
.print par('pwr_max')

* Find out the threshold values which are used by SPICE? -> we decided to use a single threshold, the same that we use for creating the crossings file
* temp1, temp2, temp3, temp4, temp5, temp51, temp52
.LPRINT(<VTH>, <VTH>) v(din) v(dout*) v(xmycir.g11:a) v(xmycir.g12:a) v(xmycir.g13:a) v(xmycir.g14:a) v(xmycir.g15:a) v(xmycir.g17:a) v(xmycir.g19:a)

.END