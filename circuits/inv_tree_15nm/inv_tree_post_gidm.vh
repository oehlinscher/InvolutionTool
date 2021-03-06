module inv_tree (
	din, 
	dout1, 
	dout2, 
	dout3, 
	dout4);
   input din;
   output dout1;
   output dout2;
   output dout3;
   output dout4;

   // Internal wires
   wire temp1;
   wire temp2;
   wire temp3;
   wire temp4;
   wire temp5;
   wire temp51;
   wire temp52;

   INV_X1_g10 g10 (.I(din),
	.ZN(temp1));
   INV_X1_g11 g11 (.I(temp1),
	.ZN(temp2));
   INV_X1_g12 g12 (.I(temp2),
	.ZN(temp3));
   INV_X1_g13 g13 (.I(temp3),
	.ZN(temp4));
   INV_X1_g14 g14 (.I(temp4),
	.ZN(temp5));
   INV_X1_g15 g15 (.I(temp5),
	.ZN(temp51));
   INV_X1_g16 g16 (.I(temp5),
	.ZN(temp52));
   INV_X1_g17 g17 (.I(temp51),
	.ZN(dout1));
   INV_X1_g18 g18 (.I(temp51),
	.ZN(dout2));
   INV_X1_g19 g19 (.I(temp52),
	.ZN(dout3));
   INV_X1_g20 g20 (.I(temp52),
	.ZN(dout4));
endmodule
