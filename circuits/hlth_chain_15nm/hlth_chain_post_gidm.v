/*
###############################################################
#  Generated by:      Cadence Innovus 19.11-s128_1
#  OS:                Linux x86_64(Host ID asic.ecs.tuwien.ac.at)
#  Generated on:      Tue Nov 17 19:33:38 2020
#  Design:            hlth_chain
#  Command:           write_netlist hlth_chain_post.v
###############################################################
*/
// Generated by Cadence Genus(TM) Synthesis Solution 19.11-s087_1
// Generated on: Nov 17 2020 19:32:21 CET (Nov 17 2020 18:32:21 UTC)
// Verification Directory fv/hlth_chain 
module hlth_chain (
	I, 
	Z);
   input I;
   output Z;

   // Internal wires
   wire [14:0] B;

   INV_X12_genblk10IX12 \genblk1[0].IX12  (.I(I),
	.ZN(B[1]));
   INV_X16_genblk10IX16 \genblk1[0].IX16  (.I(B[1]),
	.ZN(B[2]));
   INV_X12_genblk12IX12 \genblk1[2].IX12  (.I(B[2]),
	.ZN(B[3]));
   INV_X16_genblk12IX16 \genblk1[2].IX16  (.I(B[3]),
	.ZN(B[4]));
   INV_X12_genblk14IX12 \genblk1[4].IX12  (.I(B[4]),
	.ZN(B[5]));
   INV_X16_genblk14IX16 \genblk1[4].IX16  (.I(B[5]),
	.ZN(B[6]));
   INV_X12_genblk16IX12 \genblk1[6].IX12  (.I(B[6]),
	.ZN(B[7]));
   INV_X16_genblk16IX16 \genblk1[6].IX16  (.I(B[7]),
	.ZN(B[8]));
   INV_X12_genblk18IX12 \genblk1[8].IX12  (.I(B[8]),
	.ZN(B[9]));
   INV_X16_genblk18IX16 \genblk1[8].IX16  (.I(B[9]),
	.ZN(B[10]));
   INV_X12_genblk110IX12 \genblk1[10].IX12  (.I(B[10]),
	.ZN(B[11]));
   INV_X16_genblk110IX16 \genblk1[10].IX16  (.I(B[11]),
	.ZN(B[12]));
   INV_X12_genblk112IX12 \genblk1[12].IX12  (.I(B[12]),
	.ZN(B[13]));
   INV_X16_genblk112IX16 \genblk1[12].IX16  (.I(B[13]),
	.ZN(Z));
endmodule
