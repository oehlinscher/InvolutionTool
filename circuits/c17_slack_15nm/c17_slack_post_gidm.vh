module c17_slack (
	nx1, 
	nx7, 
	nx3, 
	nx2, 
	nx6, 
	nx23, 
	nx22);
   input nx1;
   input nx7;
   input nx3;
   input nx2;
   input nx6;
   output nx23;
   output nx22;

   // Internal wires
   wire net_1;
   wire net_2;
   wire net_0;
   wire net_3;

   NAND2_X2_inst5 inst_5 (.A1(net_0),
	.A2(net_3),
	.ZN(nx22));
   NAND2_X2_inst2 inst_2 (.A1(nx7),
	.A2(net_1),
	.ZN(net_2));
   NAND2_X2_inst1 inst_1 (.A1(nx1),
	.A2(nx3),
	.ZN(net_0));
   NAND2_X2_inst4 inst_4 (.A1(net_3),
	.A2(net_2),
	.ZN(nx23));
   NAND2_X2_inst3 inst_3 (.A1(nx2),
	.A2(net_1),
	.ZN(net_3));
   NAND2_X2_inst0 inst_0 (.A1(nx3),
	.A2(nx6),
	.ZN(net_1));
endmodule
