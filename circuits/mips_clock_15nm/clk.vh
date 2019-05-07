module mips (
	clk, 
	reset, 
	memdata, 
	memread, 
	memwrite, 
	adr, 
	writedata);
   input clk;
   input reset;
   input [7:0] memdata;
   output memread;
   output memwrite;
   output [7:0] adr;
   output [7:0] writedata;

   // Internal wires
   wire FE_OCPN130_n;
   wire FE_OCPN304_irwrite_0;
   wire FE_OCPN108_instr_2;
   wire FE_OCPN217_instr_1;
   wire CTS_16;
   wire CTS_15;
   wire CTS_14;
   wire CTS_13;
   wire [1:0] aluop;
   wire [1:0] pcsource;
   wire [31:0] instr;
   wire [2:0] alucont;
   wire [1:0] alusrcb;
   wire [3:0] irwrite;
   wire UNCONNECTED8;
   wire UNCONNECTED9;
   wire UNCONNECTED10;
   wire UNCONNECTED11;
   wire UNCONNECTED12;
   wire UNCONNECTED13;
   wire UNCONNECTED14;
   wire UNCONNECTED15;
   wire UNCONNECTED16;
   wire UNCONNECTED17;
   wire UNCONNECTED18;
   wire UNCONNECTED19;
   wire UNCONNECTED20;
   wire UNCONNECTED21;
   wire UNCONNECTED22;
   wire UNCONNECTED23;
   wire UNCONNECTED24;
   wire UNCONNECTED25;
   wire UNCONNECTED26;
   wire UNCONNECTED27;
   wire UNCONNECTED28;
   wire alusrca;
   wire iord;
   wire memtoreg;
   wire pcen;
   wire regdst;
   wire regwrite;
   wire zero;

   INV_X1 CTS_ccl_INV_clk_G0_L4_4 (.I(CTS_14),
	.ZN(CTS_13));
   INV_X2 CTS_ccl_INV_clk_G0_L3_2 (.I(CTS_15),
	.ZN(CTS_14));
   INV_X4 CTS_ccl_INV_clk_G0_L2_1 (.I(CTS_16),
	.ZN(CTS_15));
   INV_X8 CTS_ccl_INV_clk_G0_L1_1 (.I(clk),
	.ZN(CTS_16));
   alucontrol ac (.aluop({ aluop[1],
		pcsource[0] }),
	.funct({ instr[5],
		instr[4],
		instr[3],
		instr[2],
		instr[1],
		instr[0] }),
	.alucont(alucont),
	.p1(FE_OCPN217_instr_1),
	.FE_OCPN5_instr_2(FE_OCPN108_instr_2),
	.FE_OCPN14_n(FE_OCPN130_n));
   controller cont (.clk(CTS_13),
	.reset(reset),
	.op({ instr[31],
		instr[30],
		instr[29],
		instr[28],
		instr[27],
		instr[26] }),
	.zero(zero),
	.memread(memread),
	.memwrite(memwrite),
	.alusrca(alusrca),
	.memtoreg(memtoreg),
	.iord(iord),
	.pcen(pcen),
	.regwrite(regwrite),
	.regdst(regdst),
	.pcsource(pcsource),
	.alusrcb(alusrcb),
	.aluop({ aluop[1],
		UNCONNECTED8 }),
	.irwrite(irwrite));
   datapath_WIDTH8_REGBITS3 dp (.reset(reset),
	.memdata(memdata),
	.alusrca(alusrca),
	.memtoreg(memtoreg),
	.iord(iord),
	.pcen(pcen),
	.regwrite(regwrite),
	.regdst(regdst),
	.pcsource(pcsource),
	.alusrcb(alusrcb),
	.irwrite({ irwrite[3],
		irwrite[2],
		irwrite[1],
		FE_OCPN304_irwrite_0 }),
	.alucont(alucont),
	.zero(zero),
	.instr({ instr[31],
		instr[30],
		instr[29],
		instr[28],
		instr[27],
		instr[26],
		UNCONNECTED9,
		UNCONNECTED10,
		UNCONNECTED11,
		UNCONNECTED12,
		UNCONNECTED13,
		UNCONNECTED14,
		UNCONNECTED15,
		UNCONNECTED16,
		UNCONNECTED17,
		UNCONNECTED18,
		UNCONNECTED19,
		UNCONNECTED20,
		UNCONNECTED21,
		UNCONNECTED22,
		UNCONNECTED23,
		UNCONNECTED24,
		UNCONNECTED25,
		UNCONNECTED26,
		UNCONNECTED27,
		UNCONNECTED28,
		instr[5],
		instr[4],
		instr[3],
		instr[2],
		instr[1],
		instr[0] }),
	.adr(adr),
	.writedata(writedata),
	.clk_clone2(CTS_13),
	.clk_clone3(CTS_14),
	.clk_clone4(CTS_15),
	.clk_clone1(CTS_16),
	.clk(clk),
	.p1(FE_OCPN217_instr_1),
	.FE_OCPN4_instr_2(FE_OCPN108_instr_2),
	.FE_OCPN13_n(FE_OCPN130_n));
endmodule

module alucontrol (
	aluop, 
	funct, 
	alucont, 
	p1, 
	FE_OCPN5_instr_2, 
	FE_OCPN14_n);
   input [1:0] aluop;
   input [5:0] funct;
   output [2:0] alucont;
   input p1;
   input FE_OCPN5_instr_2;
   input FE_OCPN14_n;

   // Internal wires
   wire FE_OCPN294_instr_2;
   wire FE_RN_1;
   wire FE_OCPN114_n;
   wire FE_RN_130_0;
   wire FE_RN_129_0;
   wire FE_RN_128_0;
   wire FE_RN_127_0;
   wire FE_RN_126_0;
   wire FE_OCPN100_aluop_1;
   wire n_5;
   wire n_6;
   wire n_7;
   wire n_9;
   wire n_11;
   wire n_13;
   wire n_14;
   wire n_15;
   wire n_17;
endmodule

module controller (
	clk, 
	reset, 
	op, 
	zero, 
	memread, 
	memwrite, 
	alusrca, 
	memtoreg, 
	iord, 
	pcen, 
	regwrite, 
	regdst, 
	pcsource, 
	alusrcb, 
	aluop, 
	irwrite);
   input clk;
   input reset;
   input [5:0] op;
   input zero;
   output memread;
   output memwrite;
   output alusrca;
   output memtoreg;
   output iord;
   output pcen;
   output regwrite;
   output regdst;
   output [1:0] pcsource;
   output [1:0] alusrcb;
   output [1:0] aluop;
   output [3:0] irwrite;

   // Internal wires
   wire FE_OCPN317_state_1;
   wire FE_OCPN311_state_3;
   wire FE_RN_15;
   wire FE_RN_246_0;
   wire FE_RN_242_0;
   wire FE_RN_13;
   wire FE_RN_217_0;
   wire FE_RN_216_0;
   wire FE_RN_215_0;
   wire FE_RN_210_0;
   wire FE_RN_204_0;
   wire FE_RN_201_0;
   wire FE_OCPN297_n_60;
   wire FE_RN_194_0;
   wire FE_RN_12;
   wire FE_RN_186_0;
   wire FE_RN_183_0;
   wire FE_OCPN281_FE_RN_6;
   wire FE_OCPN276_n_65;
   wire FE_OCPN273_pcsource_0;
   wire FE_OCPN267_n_60;
   wire FE_OCPN265_n_106;
   wire FE_RN_10;
   wire FE_RN_157_0;
   wire FE_RN_141_0;
   wire FE_OCPN232_n_76;
   wire FE_RN_136_0;
   wire FE_OCPN189_state_3;
   wire FE_RN_124_0;
   wire FE_RN_123_0;
   wire FE_OCPN125_aluop_1;
   wire FE_OCPN118_state_1;
   wire FE_OCPN117_n_105;
   wire FE_OCPN108_n_61;
   wire FE_OCPN107_n_90;
   wire FE_RN_87_0;
   wire FE_OCPN99_n_12;
   wire FE_OCPN96_FE_RN_2;
   wire FE_RN_6;
   wire FE_RN_74_0;
   wire FE_RN_70_0;
   wire FE_RN_67_0;
   wire FE_OCPN102_n_62;
   wire FE_RN_65_0;
   wire FE_RN_3;
   wire FE_RN_2;
   wire FE_OCPN101_state_0;
   wire FE_RN_60_0;
   wire FE_OCPN98_pcsource_0;
   wire FE_RN_34_0;
   wire FE_RN_33_0;
   wire FE_OCPN61_n;
   wire FE_OCPN13_n_67;
   wire FE_OCPN10_state_1;
   wire FE_OCPN9_state_1;
   wire FE_OCPN2_state_2;
   wire CTS_15;
   wire CTS_14;
   wire CTS_13;
   wire [3:0] state;
   wire n_7;
   wire n_8;
   wire n_10;
   wire n_12;
   wire n_15;
   wire n_16;
   wire n_17;
   wire n_18;
   wire n_19;
   wire n_20;
   wire n_21;
   wire n_23;
   wire n_24;
   wire n_28;
   wire n_29;
   wire n_30;
   wire n_31;
   wire n_32;
   wire n_33;
   wire n_34;
   wire n_35;
   wire n_36;
   wire n_37;
   wire n_38;
   wire n_40;
   wire n_41;
   wire n_42;
   wire n_43;
   wire n_45;
   wire n_46;
   wire n_48;
   wire n_49;
   wire n_50;
   wire n_51;
   wire n_52;
   wire n_53;
   wire n_60;
   wire n_61;
   wire n_62;
   wire n_64;
   wire n_65;
   wire n_66;
   wire n_67;
   wire n_68;
   wire n_69;
   wire n_70;
   wire n_71;
   wire n_73;
   wire n_76;
   wire n_77;
   wire n_78;
   wire n_80;
   wire n_81;
   wire n_89;
   wire n_90;
   wire n_92;
   wire n_104;
   wire n_105;
   wire n_106;

   assign aluop[0] = 1'b0 ;

   INV_X1 CTS_ccl_INV_clk_G0_L6_16 (.I(CTS_15),
	.ZN(CTS_14));
   INV_X1 CTS_ccl_INV_clk_G0_L6_15 (.I(CTS_15),
	.ZN(CTS_13));
   INV_X1 CTS_ccl_INV_clk_G0_L5_8 (.I(clk),
	.ZN(CTS_15));
   DFFRNQ_X1 \state_reg[2]  (.D(n_53),
	.RN(1'b1),
	.CLK(CTS_13),
	.Q(state[2]));
   DFFRNQ_X1 \state_reg[3]  (.D(n_52),
	.RN(1'b1),
	.CLK(CTS_13),
	.Q(state[3]));
   DFFRNQ_X1 \state_reg[0]  (.D(n_50),
	.RN(1'b1),
	.CLK(CTS_14),
	.Q(state[0]));
   DFFRNQ_X1 \state_reg[1]  (.D(n_51),
	.RN(1'b1),
	.CLK(CTS_14),
	.Q(state[1]));
endmodule

module mux2_WIDTH8 (
	d0, 
	d1, 
	s, 
	y);
   input [7:0] d0;
   input [7:0] d1;
   input s;
   output [7:0] y;

   // Internal wires
   wire FE_RN_185_0;
   wire FE_RN_176_0;
   wire FE_OCPN106_FE_RN_159_0;
   wire FE_OCPN105_FE_RN_159_0;
   wire FE_OCPN104_FE_RN_159_0;
   wire FE_RN_155_0;
   wire FE_RN_154_0;
   wire FE_RN_153_0;
   wire FE_RN_152_0;
   wire FE_RN_151_0;
   wire FE_RN_147_0;
   wire FE_RN_146_0;
   wire FE_RN_145_0;
   wire FE_RN_144_0;
   wire FE_RN_143_0;
   wire FE_RN_142_0;
   wire FE_RN_140_0;
   wire FE_RN_139_0;
   wire n_12;
endmodule

module alu_WIDTH8 (
	a, 
	b, 
	alucont, 
	result);
   input [7:0] a;
   input [7:0] b;
   input [2:0] alucont;
   output [7:0] result;

   // Internal wires
   wire FE_OCPN312_src2_3;
   wire FE_RN_184_0;
   wire FE_RN_19;
   wire FE_RN_18;
   wire FE_RN_17;
   wire FE_RN_179_0;
   wire FE_RN_178_0;
   wire FE_RN_177_0;
   wire FE_RN_175_0;
   wire FE_RN_174_0;
   wire FE_OCPN292_n_27;
   wire FE_RN_16;
   wire FE_OCPN270_src2_5;
   wire FE_OCPN266_n_89;
   wire FE_OCPN264_n_38;
   wire FE_OCPN259_n_44;
   wire FE_OCPN258_src1_1;
   wire FE_OCPN257_src2_2;
   wire FE_RN_14;
   wire FE_RN_13;
   wire FE_RN_12;
   wire FE_RN_11;
   wire FE_OCPN111_src1_2;
   wire FE_RN_10;
   wire FE_OCPN241_src2_3;
   wire FE_RN_9;
   wire FE_RN_161_0;
   wire FE_OCPN226_src2_4;
   wire FE_RN_133_0;
   wire FE_RN_132_0;
   wire FE_OCPN222_n_8;
   wire FE_OCPN221_n_111;
   wire FE_RN_131_0;
   wire FE_RN_125_0;
   wire FE_OCPN188_n_1;
   wire FE_RN_121_0;
   wire FE_RN_120_0;
   wire FE_RN_119_0;
   wire FE_OCPN122_n_92;
   wire FE_OCPN119_n_85;
   wire FE_RN_8;
   wire FE_OCPN112_src2_3;
   wire FE_RN_100_0;
   wire FE_RN_97_0;
   wire FE_OCPN109_alucont_2;
   wire FE_OCPN102_n_25;
   wire FE_OCPN100_src2_0;
   wire FE_OCPN95_n_51;
   wire FE_RN_78_0;
   wire FE_RN_77_0;
   wire FE_RN_73_0;
   wire FE_RN_72_0;
   wire FE_RN_71_0;
   wire FE_OCPN92_FE_RN_1;
   wire FE_RN_6;
   wire FE_RN_66_0;
   wire FE_RN_5;
   wire FE_RN_63_0;
   wire FE_RN_2;
   wire FE_RN_59_0;
   wire FE_RN_1;
   wire FE_RN_56_0;
   wire FE_OCPN95_n_173;
   wire FE_OCPN19_n_25;
   wire FE_RN_14_0;
   wire FE_RN_8_0;
   wire FE_RN_7_0;
   wire FE_RN_4_0;
   wire FE_RN_3_0;
   wire FE_OCPN12_n_8;
   wire FE_RN_0_0;
   wire n_0;
   wire n_1;
   wire n_11;
   wire n_12;
   wire n_27;
   wire n_31;
   wire n_32;
   wire n_33;
   wire n_35;
   wire n_37;
   wire n_38;
   wire n_39;
   wire n_40;
   wire n_41;
   wire n_43;
   wire n_44;
   wire n_45;
   wire n_46;
   wire n_47;
   wire n_48;
   wire n_49;
   wire n_50;
   wire n_51;
   wire n_52;
   wire n_53;
   wire n_54;
   wire n_55;
   wire n_56;
   wire n_57;
   wire n_58;
   wire n_59;
   wire n_60;
   wire n_61;
   wire n_64;
   wire n_65;
   wire n_66;
   wire n_67;
   wire n_68;
   wire n_69;
   wire n_71;
   wire n_72;
   wire n_75;
   wire n_76;
   wire n_77;
   wire n_82;
   wire n_83;
   wire n_84;
   wire n_85;
   wire n_86;
   wire n_88;
   wire n_89;
   wire n_90;
   wire n_91;
   wire n_92;
   wire n_93;
   wire n_94;
   wire n_95;
   wire n_96;
   wire n_97;
   wire n_98;
   wire n_99;
   wire n_102;
   wire n_103;
   wire n_104;
   wire n_105;
   wire n_106;
   wire n_107;
   wire n_109;
   wire n_110;
   wire n_111;
   wire n_112;
   wire n_113;
   wire n_114;
   wire n_117;
   wire n_118;
   wire n_119;
   wire n_120;
   wire n_121;
   wire n_124;
   wire n_126;
   wire n_127;
   wire n_128;
   wire n_130;
   wire n_132;
   wire n_133;
   wire n_136;
   wire n_137;
   wire n_139;
   wire n_140;
   wire n_141;
   wire n_142;
   wire n_143;
   wire n_171;
   wire n_172;
   wire n_173;
   wire n_174;
   wire n_204;
endmodule

module flop_WIDTH8_36 (
	d, 
	q, 
	clk_clone6, 
	clk_clone5, 
	clk_clone4, 
	clk_clone3, 
	clk_clone2, 
	clk_clone1, 
	clk);
   input [7:0] d;
   output [7:0] q;
   input clk_clone6;
   input clk_clone5;
   input clk_clone4;
   input clk_clone3;
   input clk_clone2;
   input clk_clone1;
   input clk;

   // Internal wires
   wire CTS_11;
   wire CTS_10;

   INV_X1 CTS_ccl_INV_clk_G0_L6_60 (.I(clk),
	.ZN(CTS_11));
   INV_X1 CTS_ccl_INV_clk_G0_L6_25 (.I(clk_clone4),
	.ZN(CTS_10));
   DFFRNQ_X1 \q_reg[7]  (.D(d[7]),
	.RN(1'b1),
	.CLK(clk_clone6),
	.Q(q[7]));
   DFFRNQ_X1 \q_reg[6]  (.D(d[6]),
	.RN(1'b1),
	.CLK(clk_clone5),
	.Q(q[6]));
   DFFRNQ_X1 \q_reg[4]  (.D(d[4]),
	.RN(1'b1),
	.CLK(CTS_10),
	.Q(q[4]));
   DFFRNQ_X1 \q_reg[3]  (.D(d[3]),
	.RN(1'b1),
	.CLK(CTS_11),
	.Q(q[3]));
   DFFRNQ_X1 \q_reg[5]  (.D(d[5]),
	.RN(1'b1),
	.CLK(clk_clone3),
	.Q(q[5]));
   DFFRNQ_X1 \q_reg[2]  (.D(d[2]),
	.RN(1'b1),
	.CLK(CTS_11),
	.Q(q[2]));
   DFFRNQ_X1 \q_reg[1]  (.D(d[1]),
	.RN(1'b1),
	.CLK(clk_clone2),
	.Q(q[1]));
   DFFRNQ_X1 \q_reg[0]  (.D(d[0]),
	.RN(1'b1),
	.CLK(clk_clone1),
	.Q(q[0]));
endmodule

module flopen_WIDTH8 (
	clk, 
	en, 
	d, 
	q, 
	clk_clone7, 
	clk_clone6, 
	clk_clone5, 
	clk_clone4, 
	clk_clone3, 
	clk_clone2, 
	clk_clone1, 
	p1, 
	FE_OCPN6_instr_4, 
	FE_OCPN9_instr_3, 
	p2, 
	FE_OCPN11_instr_2, 
	FE_OCPN116_instr_5);
   input clk;
   input en;
   input [7:0] d;
   output [7:0] q;
   input clk_clone7;
   input clk_clone6;
   input clk_clone5;
   input clk_clone4;
   input clk_clone3;
   input clk_clone2;
   input clk_clone1;
   output p1;
   output FE_OCPN6_instr_4;
   output FE_OCPN9_instr_3;
   output p2;
   output FE_OCPN11_instr_2;
   input FE_OCPN116_instr_5;

   // Internal wires
   wire FE_OCPN320_FE_RN_45_0;
   wire FE_OCPN318_FE_RN_46_0;
   wire FE_OCPN278_instr_3;
   wire FE_RN_48_0;
   wire FE_RN_47_0;
   wire FE_RN_46_0;
   wire FE_RN_45_0;
   wire FE_RN_44_0;
   wire FE_OCPN67_irwrite_0;
   wire n_12;
   wire n_13;
   wire n_14;
   wire n_15;
   wire n_16;
   wire n_17;
   wire n_18;
   wire n_19;
   wire n_20;
   wire n_21;
   wire n_22;
   wire n_23;
   wire n_24;
   wire n_25;
   wire n_26;
   wire n_27;

   DFFRNQ_X1 \q_reg[0]  (.D(n_25),
	.RN(1'b1),
	.CLK(clk_clone3),
	.Q(q[0]));
   DFFRNQ_X1 \q_reg[3]  (.D(n_27),
	.RN(1'b1),
	.CLK(clk),
	.Q(q[3]));
   DFFRNQ_X1 \q_reg[4]  (.D(n_23),
	.RN(1'b1),
	.CLK(clk_clone7),
	.Q(q[4]));
   DFFRNQ_X1 \q_reg[5]  (.D(n_21),
	.RN(1'b1),
	.CLK(clk_clone6),
	.Q(p2));
   DFFRNQ_X1 \q_reg[6]  (.D(n_19),
	.RN(1'b1),
	.CLK(clk_clone5),
	.Q(q[6]));
   DFFRNQ_X1 \q_reg[1]  (.D(n_17),
	.RN(1'b1),
	.CLK(clk_clone1),
	.Q(p1));
   DFFRNQ_X1 \q_reg[7]  (.D(n_15),
	.RN(1'b1),
	.CLK(clk_clone4),
	.Q(q[7]));
   DFFRNQ_X1 \q_reg[2]  (.D(n_13),
	.RN(1'b1),
	.CLK(clk_clone2),
	.Q(FE_OCPN11_instr_2));
endmodule

module flopen_WIDTH8_39 (
	clk, 
	en, 
	d, 
	q, 
	clk_clone2, 
	clk_clone1);
   input clk;
   input en;
   input [7:0] d;
   output [7:0] q;
   input clk_clone2;
   input clk_clone1;

   // Internal wires
   wire FE_RN_260_0;
   wire FE_RN_259_0;
   wire n_0;
   wire n_1;
   wire n_2;
   wire n_3;
   wire n_5;

   assign q[0] = 1'b0 ;
   assign q[1] = 1'b0 ;
   assign q[2] = 1'b0 ;
   assign q[6] = 1'b0 ;
   assign q[7] = 1'b0 ;

   DFFRNQ_X1 \q_reg[3]  (.D(n_3),
	.RN(1'b1),
	.CLK(clk_clone1),
	.Q(q[3]));
   DFFRNQ_X1 \q_reg[4]  (.D(n_1),
	.RN(1'b1),
	.CLK(clk_clone2),
	.Q(q[4]));
   DFFRNQ_X1 \q_reg[5]  (.D(n_5),
	.RN(1'b1),
	.CLK(clk),
	.Q(q[5]));
endmodule

module flopen_WIDTH8_38 (
	clk, 
	en, 
	d, 
	q, 
	clk_clone5, 
	clk_clone4, 
	clk_clone3, 
	clk_clone2, 
	clk_clone1, 
	FE_OCPN0_ra2_1, 
	FE_OCPN1_ra2_0, 
	FE_OCPN2_n);
   input clk;
   input en;
   input [7:0] d;
   output [7:0] q;
   input clk_clone5;
   input clk_clone4;
   input clk_clone3;
   input clk_clone2;
   input clk_clone1;
   output FE_OCPN0_ra2_1;
   output FE_OCPN1_ra2_0;
   output FE_OCPN2_n;

   // Internal wires
   wire FE_RN_233_0;
   wire FE_RN_232_0;
   wire FE_RN_230_0;
   wire FE_RN_229_0;
   wire FE_RN_206_0;
   wire FE_RN_205_0;
   wire FE_OCPN76_ra1_0;
   wire FE_OCPN72_ra1_2;
   wire FE_OCPN69_irwrite_2;
   wire FE_RN_40_0;
   wire FE_RN_39_0;
   wire n_0;
   wire n_1;
   wire n_3;
   wire n_4;
   wire n_5;
   wire n_6;
   wire n_7;
   wire n_9;
   wire n_10;
   wire n_11;

   assign q[3] = 1'b0 ;
   assign q[4] = 1'b0 ;

   DFFRNQ_X1 \q_reg[0]  (.D(n_7),
	.RN(1'b1),
	.CLK(clk_clone5),
	.Q(q[0]));
   DFFRNQ_X1 \q_reg[1]  (.D(n_5),
	.RN(1'b1),
	.CLK(clk_clone4),
	.Q(q[1]));
   DFFRNQ_X1 \q_reg[6]  (.D(n_11),
	.RN(1'b1),
	.CLK(clk_clone2),
	.Q(q[6]));
   DFFRNQ_X1 \q_reg[7]  (.D(n_9),
	.RN(1'b1),
	.CLK(clk),
	.Q(FE_OCPN72_ra1_2));
   DFFRNQ_X1 \q_reg[2]  (.D(n_3),
	.RN(1'b1),
	.CLK(clk_clone1),
	.Q(q[2]));
   DFFRNQ_X1 \q_reg[5]  (.D(n_1),
	.RN(1'b1),
	.CLK(clk_clone3),
	.Q(FE_OCPN76_ra1_0));
endmodule

module flopen_WIDTH8_37 (
	en, 
	d, 
	q, 
	clk_clone2, 
	clk_clone1, 
	clk);
   input en;
   input [7:0] d;
   output [7:0] q;
   input clk_clone2;
   input clk_clone1;
   input clk;

   // Internal wires
   wire FE_RN_245_0;
   wire FE_RN_244_0;
   wire FE_RN_237_0;
   wire FE_RN_236_0;
   wire FE_RN_226_0;
   wire FE_RN_225_0;
   wire FE_RN_222_0;
   wire FE_RN_221_0;
   wire FE_RN_220_0;
   wire FE_RN_219_0;
   wire CTS_12;
   wire CTS_11;
   wire CTS_10;
   wire n_1;
   wire n_3;
   wire n_5;
   wire n_7;
   wire n_9;
   wire n_10;
   wire n_11;

   assign q[0] = 1'b0 ;
   assign q[1] = 1'b0 ;

   INV_X1 CTS_ccl_INV_clk_G0_L6_14 (.I(CTS_12),
	.ZN(CTS_11));
   INV_X1 CTS_ccl_INV_clk_G0_L6_13 (.I(CTS_12),
	.ZN(CTS_10));
   INV_X1 CTS_ccl_INV_clk_G0_L5_7 (.I(clk),
	.ZN(CTS_12));
   DFFRNQ_X1 \q_reg[2]  (.D(n_7),
	.RN(1'b1),
	.CLK(clk_clone1),
	.Q(q[2]));
   DFFRNQ_X1 \q_reg[3]  (.D(n_5),
	.RN(1'b1),
	.CLK(CTS_11),
	.Q(q[3]));
   DFFRNQ_X1 \q_reg[6]  (.D(n_11),
	.RN(1'b1),
	.CLK(clk_clone2),
	.Q(q[6]));
   DFFRNQ_X1 \q_reg[7]  (.D(n_9),
	.RN(1'b1),
	.CLK(CTS_10),
	.Q(q[7]));
   DFFRNQ_X1 \q_reg[4]  (.D(n_3),
	.RN(1'b1),
	.CLK(CTS_11),
	.Q(q[4]));
   DFFRNQ_X1 \q_reg[5]  (.D(n_1),
	.RN(1'b1),
	.CLK(CTS_10),
	.Q(q[5]));
endmodule

module flop_WIDTH8 (
	clk, 
	d, 
	q, 
	clk_clone7, 
	clk_clone6, 
	clk_clone5, 
	clk_clone4, 
	clk_clone3, 
	clk_clone2, 
	clk_clone1);
   input clk;
   input [7:0] d;
   output [7:0] q;
   input clk_clone7;
   input clk_clone6;
   input clk_clone5;
   input clk_clone4;
   input clk_clone3;
   input clk_clone2;
   input clk_clone1;

   DFFRNQ_X1 \q_reg[7]  (.D(d[7]),
	.RN(1'b1),
	.CLK(clk_clone6),
	.Q(q[7]));
   DFFRNQ_X1 \q_reg[6]  (.D(d[6]),
	.RN(1'b1),
	.CLK(clk_clone5),
	.Q(q[6]));
   DFFRNQ_X1 \q_reg[4]  (.D(d[4]),
	.RN(1'b1),
	.CLK(clk_clone7),
	.Q(q[4]));
   DFFRNQ_X1 \q_reg[3]  (.D(d[3]),
	.RN(1'b1),
	.CLK(clk),
	.Q(q[3]));
   DFFRNQ_X1 \q_reg[5]  (.D(d[5]),
	.RN(1'b1),
	.CLK(clk_clone4),
	.Q(q[5]));
   DFFRNQ_X1 \q_reg[2]  (.D(d[2]),
	.RN(1'b1),
	.CLK(clk_clone1),
	.Q(q[2]));
   DFFRNQ_X1 \q_reg[1]  (.D(d[1]),
	.RN(1'b1),
	.CLK(clk_clone3),
	.Q(q[1]));
   DFFRNQ_X1 \q_reg[0]  (.D(d[0]),
	.RN(1'b1),
	.CLK(clk_clone2),
	.Q(q[0]));
endmodule

module mux4_WIDTH8_42 (
	d0, 
	d1, 
	d2, 
	d3, 
	s, 
	y);
   input [7:0] d0;
   input [7:0] d1;
   input [7:0] d2;
   input [7:0] d3;
   input [1:0] s;
   output [7:0] y;

   // Internal wires
   wire n_8;
   wire n_9;
   wire n_10;
   wire n_11;
   wire n_12;
   wire n_13;
   wire n_14;
   wire n_15;
   wire n_16;
   wire n_17;
   wire n_18;
   wire n_19;
   wire n_20;
   wire n_21;
   wire n_23;
   wire n_25;
   wire n_26;
   wire n_27;
   wire n_28;
   wire n_29;
endmodule

module flopenr_WIDTH8 (
	clk, 
	reset, 
	en, 
	d, 
	q, 
	clk_clone6, 
	clk_clone4, 
	clk_clone5, 
	clk_clone3, 
	clk_clone2, 
	clk_clone1, 
	FE_OCPN10_pc_3, 
	p1, 
	FE_OCPN12_pc_1);
   input clk;
   input reset;
   input en;
   input [7:0] d;
   output [7:0] q;
   input clk_clone6;
   input clk_clone4;
   input clk_clone5;
   input clk_clone3;
   input clk_clone2;
   input clk_clone1;
   output FE_OCPN10_pc_3;
   output p1;
   output FE_OCPN12_pc_1;

   // Internal wires
   wire FE_OCPN319_n_8;
   wire FE_RN_5;
   wire FE_OCPN310_n_11;
   wire FE_OCPN129_pcen;
   wire FE_OCPN119_pc_3;
   wire FE_OCPN107_n_10;
   wire FE_RN_160_0;
   wire FE_OCPN239_pc_3;
   wire FE_OCPN186_n_10;
   wire FE_RN_118_0;
   wire FE_RN_117_0;
   wire FE_RN_103_0;
   wire FE_RN_102_0;
   wire FE_RN_99_0;
   wire FE_RN_98_0;
   wire FE_RN_94_0;
   wire FE_RN_93_0;
   wire FE_RN_92_0;
   wire FE_RN_91_0;
   wire FE_RN_90_0;
   wire FE_RN_89_0;
   wire FE_RN_85_0;
   wire FE_RN_84_0;
   wire FE_RN_83_0;
   wire FE_RN_82_0;
   wire FE_RN_81_0;
   wire FE_OCPN103_n_85;
   wire FE_OCPN1_n_11;
   wire CTS_4;
   wire n_8;
   wire n_10;
   wire n_11;
   wire n_13;
   wire n_15;
   wire n_17;
   wire n_19;
   wire n_21;
   wire n_23;
   wire n_25;
   wire n_27;

   INV_X1 CTS_ccl_INV_clk_G0_L6_41 (.I(clk_clone5),
	.ZN(CTS_4));
   DFFRNQ_X1 \q_reg[0]  (.D(n_15),
	.RN(1'b1),
	.CLK(clk_clone2),
	.Q(FE_RN_5));
   DFFRNQ_X1 \q_reg[2]  (.D(n_13),
	.RN(1'b1),
	.CLK(clk_clone4),
	.Q(q[2]));
   DFFRNQ_X1 \q_reg[3]  (.D(n_27),
	.RN(1'b1),
	.CLK(CTS_4),
	.Q(FE_OCPN119_pc_3));
   DFFRNQ_X1 \q_reg[4]  (.D(n_25),
	.RN(1'b1),
	.CLK(clk),
	.Q(q[4]));
   DFFRNQ_X1 \q_reg[5]  (.D(n_23),
	.RN(1'b1),
	.CLK(clk_clone1),
	.Q(q[5]));
   DFFRNQ_X1 \q_reg[1]  (.D(n_19),
	.RN(1'b1),
	.CLK(CTS_4),
	.Q(q[1]));
   DFFRNQ_X1 \q_reg[6]  (.D(n_21),
	.RN(1'b1),
	.CLK(clk_clone3),
	.Q(q[6]));
   DFFRNQ_X1 \q_reg[7]  (.D(n_17),
	.RN(1'b1),
	.CLK(clk_clone6),
	.Q(q[7]));
endmodule

module mux2_WIDTH3 (
	d0, 
	d1, 
	s, 
	y);
   input [2:0] d0;
   input [2:0] d1;
   input s;
   output [2:0] y;

   // Internal wires
   wire FE_RN_191_0;
   wire FE_RN_190_0;
   wire FE_OCPN125_n_75;
   wire FE_RN_13_0;
   wire FE_RN_12_0;
endmodule

module flop_WIDTH8_34 (
	clk, 
	d, 
	q, 
	clk_clone5, 
	clk_clone4, 
	clk_clone3, 
	clk_clone2, 
	clk_clone1);
   input clk;
   input [7:0] d;
   output [7:0] q;
   input clk_clone5;
   input clk_clone4;
   input clk_clone3;
   input clk_clone2;
   input clk_clone1;

   // Internal wires
   wire CTS_8;
   wire CTS_7;

   INV_X1 CTS_ccl_INV_clk_G0_L6_51 (.I(clk_clone4),
	.ZN(CTS_8));
   INV_X1 CTS_ccl_INV_clk_G0_L6_3 (.I(clk_clone5),
	.ZN(CTS_7));
   DFFRNQ_X1 \q_reg[7]  (.D(d[7]),
	.RN(1'b1),
	.CLK(clk_clone3),
	.Q(q[7]));
   DFFRNQ_X1 \q_reg[6]  (.D(d[6]),
	.RN(1'b1),
	.CLK(CTS_7),
	.Q(q[6]));
   DFFRNQ_X1 \q_reg[4]  (.D(d[4]),
	.RN(1'b1),
	.CLK(clk_clone1),
	.Q(q[4]));
   DFFRNQ_X1 \q_reg[3]  (.D(d[3]),
	.RN(1'b1),
	.CLK(clk),
	.Q(q[3]));
   DFFRNQ_X1 \q_reg[5]  (.D(d[5]),
	.RN(1'b1),
	.CLK(CTS_7),
	.Q(q[5]));
   DFFRNQ_X1 \q_reg[2]  (.D(d[2]),
	.RN(1'b1),
	.CLK(CTS_8),
	.Q(q[2]));
   DFFRNQ_X1 \q_reg[1]  (.D(d[1]),
	.RN(1'b1),
	.CLK(CTS_8),
	.Q(q[1]));
   DFFRNQ_X1 \q_reg[0]  (.D(d[0]),
	.RN(1'b1),
	.CLK(clk_clone2),
	.Q(q[0]));
endmodule

module regfile_WIDTH8_REGBITS3 (
	regwrite, 
	ra1, 
	ra2, 
	wa, 
	wd, 
	rd1, 
	rd2, 
	clk_clone15, 
	clk_clone13, 
	clk_clone12, 
	clk_clone10, 
	clk_clone11, 
	clk_clone9, 
	clk_clone14, 
	clk_clone7, 
	clk_clone6, 
	clk_clone5, 
	clk_clone3, 
	clk_clone4, 
	clk_clone8, 
	clk_clone1, 
	clk_clone2, 
	clk, 
	FE_OCPN3_n);
   input regwrite;
   input [2:0] ra1;
   input [2:0] ra2;
   input [2:0] wa;
   input [7:0] wd;
   output [7:0] rd1;
   output [7:0] rd2;
   input clk_clone15;
   input clk_clone13;
   input clk_clone12;
   input clk_clone10;
   input clk_clone11;
   input clk_clone9;
   input clk_clone14;
   input clk_clone7;
   input clk_clone6;
   input clk_clone5;
   input clk_clone3;
   input clk_clone4;
   input clk_clone8;
   input clk_clone1;
   input clk_clone2;
   input clk;
   input FE_OCPN3_n;

   // Internal wires
   wire FE_OCPN315_n_140;
   wire FE_RN_267_0;
   wire FE_RN_266_0;
   wire FE_RN_265_0;
   wire FE_OCPN302_n_13;
   wire FE_OCPN301_n_182;
   wire FE_OCPN300_n_174;
   wire FE_RN_264_0;
   wire FE_RN_263_0;
   wire FE_RN_262_0;
   wire FE_RN_261_0;
   wire FE_RN_258_0;
   wire FE_RN_257_0;
   wire FE_RN_256_0;
   wire FE_RN_255_0;
   wire FE_RN_254_0;
   wire FE_RN_253_0;
   wire FE_RN_252_0;
   wire FE_RN_250_0;
   wire FE_RN_249_0;
   wire FE_RN_248_0;
   wire FE_RN_247_0;
   wire FE_RN_243_0;
   wire FE_RN_239_0;
   wire FE_RN_238_0;
   wire FE_OCPN298_n_171;
   wire FE_RN_231_0;
   wire FE_RN_228_0;
   wire FE_RN_223_0;
   wire FE_RN_218_0;
   wire FE_RN_214_0;
   wire FE_RN_213_0;
   wire FE_RN_212_0;
   wire FE_RN_209_0;
   wire FE_RN_208_0;
   wire FE_RN_207_0;
   wire FE_RN_2;
   wire FE_RN_203_0;
   wire FE_RN_199_0;
   wire FE_RN_1;
   wire FE_RN_198_0;
   wire FE_RN_197_0;
   wire FE_RN_196_0;
   wire FE_RN_195_0;
   wire FE_RN_193_0;
   wire FE_RN_189_0;
   wire FE_RN_188_0;
   wire FE_RN_187_0;
   wire FE_OCPN123_n_13;
   wire FE_USKN256_CTS_156;
   wire FE_USKN255_CTS_156;
   wire FE_USKN254_CTS_156;
   wire FE_USKN253_CTS_156;
   wire FE_USKN252_CTS_156;
   wire FE_USKN251_CTS_156;
   wire FE_USKN216_CTS_163;
   wire FE_USKN215_CTS_163;
   wire FE_USKN214_CTS_139;
   wire FE_USKN213_CTS_139;
   wire FE_USKN212_CTS_146;
   wire FE_USKN211_CTS_146;
   wire FE_USKN210_CTS_146;
   wire FE_USKN209_CTS_146;
   wire FE_USKN208_CTS_139;
   wire FE_USKN207_CTS_139;
   wire FE_USKN206_CTS_139;
   wire FE_USKN205_CTS_139;
   wire FE_USKN204_CTS_147;
   wire FE_USKN203_CTS_147;
   wire FE_USKN202_CTS_147;
   wire FE_USKN201_CTS_147;
   wire FE_USKN200_CTS_147;
   wire FE_USKN199_CTS_147;
   wire FE_USKN183_CTS_145;
   wire FE_USKN182_CTS_145;
   wire FE_USKN181_CTS_152;
   wire FE_USKN180_CTS_152;
   wire FE_USKN179_CTS_155;
   wire FE_USKN178_CTS_155;
   wire FE_USKN177_CTS_159;
   wire FE_USKN176_CTS_159;
   wire FE_USKN175_CTS_170;
   wire FE_USKN174_CTS_170;
   wire FE_USKN173_CTS_171;
   wire FE_USKN172_CTS_171;
   wire FE_USKN167_CTS_139;
   wire FE_USKN166_CTS_139;
   wire FE_USKN165_CTS_146;
   wire FE_USKN164_CTS_146;
   wire FE_USKN163_CTS_156;
   wire FE_USKN162_CTS_156;
   wire FE_USKN161_CTS_163;
   wire FE_USKN160_CTS_163;
   wire FE_USKN155_CTS_147;
   wire FE_USKN154_CTS_147;
   wire FE_USKN153_CTS_164;
   wire FE_USKN152_CTS_164;
   wire FE_RN_51_0;
   wire FE_OCPN90_n_274;
   wire FE_OCPN89_n_266;
   wire FE_OCPN88_n_276;
   wire FE_OCPN87_n_277;
   wire FE_OCPN86_n_269;
   wire FE_OCPN85_n_275;
   wire FE_RN_50_0;
   wire FE_OCPN84_ra1_1;
   wire FE_OCPN83_n_273;
   wire FE_OCPN82_ra2_2;
   wire FE_OCPN80_n_270;
   wire FE_OCPN79_n_268;
   wire FE_OCPN77_n_271;
   wire FE_OCPN75_n_267;
   wire FE_OCPN74_n_272;
   wire FE_OCPN73_n_272;
   wire FE_RN_49_0;
   wire FE_RN_43_0;
   wire FE_RN_42_0;
   wire FE_RN_41_0;
   wire FE_RN_38_0;
   wire FE_RN_37_0;
   wire FE_RN_36_0;
   wire FE_RN_35_0;
   wire FE_RN_32_0;
   wire FE_RN_31_0;
   wire FE_RN_30_0;
   wire FE_RN_29_0;
   wire FE_RN_28_0;
   wire FE_RN_27_0;
   wire FE_RN_25_0;
   wire FE_RN_24_0;
   wire FE_RN_23_0;
   wire FE_RN_22_0;
   wire FE_RN_21_0;
   wire FE_RN_20_0;
   wire FE_OCPN66_n_16;
   wire FE_RN_17_0;
   wire FE_RN_16_0;
   wire FE_OCPN65_n_18;
   wire FE_OCPN64_n_0;
   wire FE_OCPN63_n_0;
   wire FE_OCPN62_n_15;
   wire FE_OCPN27_n_16;
   wire FE_OCPN18_n_18;
   wire FE_OCPN17_n_17;
   wire FE_RN_11_0;
   wire FE_RN_10_0;
   wire FE_RN_9_0;
   wire FE_RN_6_0;
   wire FE_RN_5_0;
   wire CTS_173;
   wire CTS_172;
   wire CTS_171;
   wire CTS_170;
   wire CTS_169;
   wire CTS_168;
   wire CTS_167;
   wire CTS_166;
   wire CTS_165;
   wire CTS_164;
   wire CTS_163;
   wire CTS_162;
   wire CTS_161;
   wire CTS_160;
   wire CTS_159;
   wire CTS_158;
   wire CTS_157;
   wire CTS_156;
   wire CTS_155;
   wire CTS_154;
   wire CTS_153;
   wire CTS_152;
   wire CTS_151;
   wire CTS_150;
   wire CTS_149;
   wire CTS_148;
   wire CTS_147;
   wire CTS_146;
   wire CTS_145;
   wire CTS_144;
   wire CTS_143;
   wire CTS_142;
   wire CTS_141;
   wire CTS_140;
   wire CTS_139;
   wire CTS_138;
   wire CTS_137;
   wire CTS_136;
   wire CTS_135;
   wire CTS_134;
   wire CTS_133;
   wire [7:0] \RAM[2] ;
   wire [7:0] \RAM[1] ;
   wire [7:0] \RAM[3] ;
   wire [7:0] \RAM[5] ;
   wire [7:0] \RAM[6] ;
   wire [7:0] \RAM[4] ;
   wire [7:0] \RAM[7] ;
   wire n_0;
   wire n_1;
   wire n_2;
   wire n_3;
   wire n_4;
   wire n_6;
   wire n_7;
   wire n_8;
   wire n_9;
   wire n_11;
   wire n_12;
   wire n_13;
   wire n_14;
   wire n_15;
   wire n_16;
   wire n_17;
   wire n_18;
   wire n_19;
   wire n_20;
   wire n_22;
   wire n_23;
   wire n_24;
   wire n_25;
   wire n_26;
   wire n_27;
   wire n_28;
   wire n_29;
   wire n_30;
   wire n_31;
   wire n_32;
   wire n_33;
   wire n_34;
   wire n_35;
   wire n_36;
   wire n_37;
   wire n_38;
   wire n_39;
   wire n_40;
   wire n_41;
   wire n_42;
   wire n_44;
   wire n_45;
   wire n_46;
   wire n_48;
   wire n_50;
   wire n_51;
   wire n_52;
   wire n_53;
   wire n_54;
   wire n_56;
   wire n_58;
   wire n_59;
   wire n_60;
   wire n_61;
   wire n_62;
   wire n_63;
   wire n_64;
   wire n_66;
   wire n_67;
   wire n_68;
   wire n_69;
   wire n_70;
   wire n_71;
   wire n_72;
   wire n_74;
   wire n_75;
   wire n_76;
   wire n_78;
   wire n_79;
   wire n_80;
   wire n_81;
   wire n_82;
   wire n_83;
   wire n_84;
   wire n_86;
   wire n_87;
   wire n_88;
   wire n_89;
   wire n_90;
   wire n_91;
   wire n_92;
   wire n_94;
   wire n_95;
   wire n_96;
   wire n_98;
   wire n_100;
   wire n_101;
   wire n_102;
   wire n_103;
   wire n_104;
   wire n_105;
   wire n_106;
   wire n_107;
   wire n_108;
   wire n_109;
   wire n_110;
   wire n_111;
   wire n_112;
   wire n_113;
   wire n_114;
   wire n_116;
   wire n_118;
   wire n_119;
   wire n_120;
   wire n_121;
   wire n_122;
   wire n_123;
   wire n_124;
   wire n_126;
   wire n_128;
   wire n_129;
   wire n_130;
   wire n_132;
   wire n_133;
   wire n_134;
   wire n_135;
   wire n_136;
   wire n_137;
   wire n_138;
   wire n_139;
   wire n_140;
   wire n_141;
   wire n_142;
   wire n_143;
   wire n_144;
   wire n_145;
   wire n_146;
   wire n_147;
   wire n_148;
   wire n_149;
   wire n_150;
   wire n_151;
   wire n_152;
   wire n_153;
   wire n_154;
   wire n_155;
   wire n_156;
   wire n_157;
   wire n_158;
   wire n_159;
   wire n_160;
   wire n_161;
   wire n_162;
   wire n_163;
   wire n_164;
   wire n_165;
   wire n_166;
   wire n_167;
   wire n_168;
   wire n_169;
   wire n_170;
   wire n_171;
   wire n_172;
   wire n_173;
   wire n_174;
   wire n_175;
   wire n_176;
   wire n_177;
   wire n_178;
   wire n_179;
   wire n_180;
   wire n_181;
   wire n_182;
   wire n_183;
   wire n_184;
   wire n_185;
   wire n_186;
   wire n_187;
   wire n_252;
   wire n_253;
   wire n_254;
   wire n_255;
   wire n_256;
   wire n_257;
   wire n_258;
   wire n_259;
   wire n_260;
   wire n_261;
   wire n_262;
   wire n_263;
   wire n_264;
   wire n_265;
   wire n_266;
   wire n_267;
   wire n_268;
   wire n_269;
   wire n_270;
   wire n_271;
   wire n_272;
   wire n_273;
   wire n_274;
   wire n_275;
   wire n_276;
   wire n_277;
   wire n_278;
   wire n_279;
   wire n_280;
   wire n_281;
   wire n_282;
   wire n_283;
   wire n_284;
   wire n_285;
   wire n_286;
   wire n_287;
   wire n_288;
   wire n_289;
   wire n_290;
   wire n_291;
   wire n_292;
   wire n_293;
   wire n_295;
   wire n_296;
   wire n_298;
   wire n_299;
   wire n_300;
   wire n_301;
   wire n_302;
   wire n_303;
   wire n_304;
   wire n_305;
   wire n_306;
   wire n_307;
   wire n_308;
   wire n_309;
   wire n_310;
   wire n_311;
   wire n_312;
   wire n_313;
   wire n_314;
   wire n_315;
   wire n_316;
   wire n_317;
   wire n_318;
   wire n_319;
   wire n_320;
   wire n_321;
   wire n_322;
   wire n_323;
   wire n_324;
   wire n_325;
   wire n_326;
   wire n_327;
   wire n_329;
   wire n_330;
   wire n_331;
   wire n_332;
   wire n_333;
   wire n_334;
   wire n_335;
   wire n_336;
   wire n_337;
   wire n_338;
   wire n_339;
   wire n_340;
   wire n_341;
   wire n_345;
   wire n_347;
   wire n_349;
   wire n_350;
   wire n_353;
   wire n_354;
   wire n_357;

   INV_X8 FE_USKC256_CTS_156 (.I(FE_USKN256_CTS_156),
	.ZN(CTS_156));
   INV_X8 FE_USKC255_CTS_156 (.I(FE_USKN255_CTS_156),
	.ZN(FE_USKN256_CTS_156));
   INV_X4 FE_USKC254_CTS_156 (.I(FE_USKN254_CTS_156),
	.ZN(FE_USKN162_CTS_156));
   INV_X4 FE_USKC253_CTS_156 (.I(FE_USKN253_CTS_156),
	.ZN(FE_USKN254_CTS_156));
   INV_X4 FE_USKC252_CTS_156 (.I(FE_USKN252_CTS_156),
	.ZN(FE_USKN163_CTS_156));
   INV_X4 FE_USKC251_CTS_156 (.I(FE_USKN251_CTS_156),
	.ZN(FE_USKN252_CTS_156));
   INV_X4 FE_USKC216_CTS_163 (.I(FE_USKN216_CTS_163),
	.ZN(FE_USKN161_CTS_163));
   INV_X4 FE_USKC215_CTS_163 (.I(FE_USKN215_CTS_163),
	.ZN(FE_USKN216_CTS_163));
   INV_X8 FE_USKC214_CTS_139 (.I(FE_USKN214_CTS_139),
	.ZN(CTS_139));
   INV_X8 FE_USKC213_CTS_139 (.I(FE_USKN213_CTS_139),
	.ZN(FE_USKN214_CTS_139));
   INV_X8 FE_USKC212_CTS_146 (.I(FE_USKN212_CTS_146),
	.ZN(CTS_146));
   INV_X8 FE_USKC211_CTS_146 (.I(FE_USKN211_CTS_146),
	.ZN(FE_USKN212_CTS_146));
   INV_X4 FE_USKC210_CTS_146 (.I(FE_USKN210_CTS_146),
	.ZN(FE_USKN165_CTS_146));
   INV_X4 FE_USKC209_CTS_146 (.I(FE_USKN209_CTS_146),
	.ZN(FE_USKN210_CTS_146));
   INV_X4 FE_USKC208_CTS_139 (.I(FE_USKN208_CTS_139),
	.ZN(FE_USKN166_CTS_139));
   INV_X4 FE_USKC207_CTS_139 (.I(FE_USKN207_CTS_139),
	.ZN(FE_USKN208_CTS_139));
   INV_X4 FE_USKC206_CTS_139 (.I(FE_USKN206_CTS_139),
	.ZN(FE_USKN167_CTS_139));
   INV_X4 FE_USKC205_CTS_139 (.I(FE_USKN205_CTS_139),
	.ZN(FE_USKN206_CTS_139));
   INV_X4 FE_USKC204_CTS_147 (.I(FE_USKN204_CTS_147),
	.ZN(CTS_147));
   INV_X4 FE_USKC203_CTS_147 (.I(FE_USKN203_CTS_147),
	.ZN(FE_USKN204_CTS_147));
   INV_X4 FE_USKC202_CTS_147 (.I(FE_USKN202_CTS_147),
	.ZN(FE_USKN154_CTS_147));
   INV_X4 FE_USKC201_CTS_147 (.I(FE_USKN201_CTS_147),
	.ZN(FE_USKN202_CTS_147));
   INV_X4 FE_USKC200_CTS_147 (.I(FE_USKN200_CTS_147),
	.ZN(FE_USKN155_CTS_147));
   INV_X4 FE_USKC199_CTS_147 (.I(FE_USKN199_CTS_147),
	.ZN(FE_USKN200_CTS_147));
   INV_X2 FE_USKC183_CTS_145 (.I(FE_USKN183_CTS_145),
	.ZN(CTS_145));
   INV_X2 FE_USKC182_CTS_145 (.I(FE_USKN182_CTS_145),
	.ZN(FE_USKN183_CTS_145));
   INV_X2 FE_USKC181_CTS_152 (.I(FE_USKN181_CTS_152),
	.ZN(CTS_152));
   INV_X2 FE_USKC180_CTS_152 (.I(FE_USKN180_CTS_152),
	.ZN(FE_USKN181_CTS_152));
   INV_X2 FE_USKC179_CTS_155 (.I(FE_USKN179_CTS_155),
	.ZN(CTS_155));
   INV_X2 FE_USKC178_CTS_155 (.I(FE_USKN178_CTS_155),
	.ZN(FE_USKN179_CTS_155));
   INV_X2 FE_USKC177_CTS_159 (.I(FE_USKN177_CTS_159),
	.ZN(CTS_159));
   INV_X2 FE_USKC176_CTS_159 (.I(FE_USKN176_CTS_159),
	.ZN(FE_USKN177_CTS_159));
   INV_X4 FE_USKC175_CTS_170 (.I(FE_USKN175_CTS_170),
	.ZN(CTS_170));
   INV_X4 FE_USKC174_CTS_170 (.I(FE_USKN174_CTS_170),
	.ZN(FE_USKN175_CTS_170));
   INV_X4 FE_USKC173_CTS_171 (.I(FE_USKN173_CTS_171),
	.ZN(CTS_171));
   INV_X4 FE_USKC172_CTS_171 (.I(FE_USKN172_CTS_171),
	.ZN(FE_USKN173_CTS_171));
   INV_X4 FE_USKC167_CTS_139 (.I(FE_USKN167_CTS_139),
	.ZN(FE_USKN213_CTS_139));
   INV_X4 FE_USKC166_CTS_139 (.I(FE_USKN166_CTS_139),
	.ZN(FE_USKN205_CTS_139));
   INV_X4 FE_USKC165_CTS_146 (.I(FE_USKN165_CTS_146),
	.ZN(FE_USKN211_CTS_146));
   INV_X4 FE_USKC164_CTS_146 (.I(FE_USKN164_CTS_146),
	.ZN(FE_USKN209_CTS_146));
   INV_X4 FE_USKC163_CTS_156 (.I(FE_USKN163_CTS_156),
	.ZN(FE_USKN255_CTS_156));
   INV_X4 FE_USKC162_CTS_156 (.I(FE_USKN162_CTS_156),
	.ZN(FE_USKN251_CTS_156));
   INV_X4 FE_USKC161_CTS_163 (.I(FE_USKN161_CTS_163),
	.ZN(CTS_163));
   INV_X4 FE_USKC160_CTS_163 (.I(FE_USKN160_CTS_163),
	.ZN(FE_USKN215_CTS_163));
   INV_X4 FE_USKC155_CTS_147 (.I(FE_USKN155_CTS_147),
	.ZN(FE_USKN203_CTS_147));
   INV_X4 FE_USKC154_CTS_147 (.I(FE_USKN154_CTS_147),
	.ZN(FE_USKN199_CTS_147));
   INV_X4 FE_USKC153_CTS_164 (.I(FE_USKN153_CTS_164),
	.ZN(CTS_164));
   INV_X4 FE_USKC152_CTS_164 (.I(FE_USKN152_CTS_164),
	.ZN(FE_USKN153_CTS_164));
   INV_X1 CTS_ccl_INV_clk_G0_L6_62 (.I(clk),
	.ZN(CTS_173));
   INV_X1 CTS_ccl_INV_clk_G0_L6_52 (.I(clk_clone1),
	.ZN(CTS_172));
   INV_X2 CTS_ccl_INV_clk_G0_L6_50 (.I(CTS_170),
	.ZN(CTS_169));
   INV_X1 CTS_ccl_INV_clk_G0_L6_49 (.I(CTS_170),
	.ZN(CTS_168));
   INV_X4 CTS_ccl_INV_clk_G0_L5_25 (.I(CTS_171),
	.ZN(FE_USKN174_CTS_170));
   INV_X4 CTS_ccl_INV_clk_G0_L4_13 (.I(clk_clone2),
	.ZN(FE_USKN172_CTS_171));
   INV_X2 CTS_ccl_INV_clk_G0_L6_47 (.I(clk_clone4),
	.ZN(CTS_167));
   INV_X2 CTS_ccl_INV_clk_G0_L6_46 (.I(clk_clone5),
	.ZN(CTS_166));
   INV_X1 CTS_ccl_INV_clk_G0_L6_43 (.I(clk_clone7),
	.ZN(CTS_165));
   INV_X1 CTS_ccl_INV_clk_G0_L6_40 (.I(CTS_162),
	.ZN(CTS_161));
   INV_X1 CTS_ccl_INV_clk_G0_L6_39 (.I(CTS_162),
	.ZN(CTS_160));
   INV_X2 CTS_ccl_INV_clk_G0_L5_20 (.I(CTS_163),
	.ZN(CTS_162));
   INV_X1 CTS_ccl_INV_clk_G0_L6_38 (.I(CTS_159),
	.ZN(CTS_158));
   INV_X1 CTS_ccl_INV_clk_G0_L6_37 (.I(CTS_159),
	.ZN(CTS_157));
   INV_X1 CTS_ccl_INV_clk_G0_L5_19 (.I(CTS_163),
	.ZN(FE_USKN176_CTS_159));
   INV_X2 CTS_ccl_INV_clk_G0_L4_10 (.I(CTS_164),
	.ZN(FE_USKN160_CTS_163));
   INV_X1 CTS_ccl_INV_clk_G0_L6_36 (.I(CTS_155),
	.ZN(CTS_154));
   INV_X1 CTS_ccl_INV_clk_G0_L6_35 (.I(CTS_155),
	.ZN(CTS_153));
   INV_X1 CTS_ccl_INV_clk_G0_L5_18 (.I(CTS_156),
	.ZN(FE_USKN178_CTS_155));
   INV_X1 CTS_ccl_INV_clk_G0_L6_34 (.I(CTS_152),
	.ZN(CTS_151));
   INV_X1 CTS_ccl_INV_clk_G0_L6_33 (.I(CTS_152),
	.ZN(CTS_150));
   INV_X1 CTS_ccl_INV_clk_G0_L5_17 (.I(CTS_156),
	.ZN(FE_USKN180_CTS_152));
   INV_X2 CTS_ccl_INV_clk_G0_L4_9 (.I(CTS_164),
	.ZN(FE_USKN253_CTS_156));
   INV_X8 CTS_ccl_INV_clk_G0_L3_5 (.I(clk_clone8),
	.ZN(FE_USKN152_CTS_164));
   INV_X2 CTS_ccl_INV_clk_G0_L6_31 (.I(clk_clone9),
	.ZN(CTS_149));
   INV_X1 CTS_ccl_INV_clk_G0_L6_29 (.I(clk_clone11),
	.ZN(CTS_148));
   INV_X1 CTS_ccl_INV_clk_G0_L6_24 (.I(CTS_145),
	.ZN(CTS_144));
   INV_X1 CTS_ccl_INV_clk_G0_L6_23 (.I(CTS_145),
	.ZN(CTS_143));
   INV_X1 CTS_ccl_INV_clk_G0_L5_12 (.I(CTS_146),
	.ZN(FE_USKN182_CTS_145));
   INV_X1 CTS_ccl_INV_clk_G0_L6_22 (.I(CTS_142),
	.ZN(CTS_141));
   INV_X1 CTS_ccl_INV_clk_G0_L6_21 (.I(CTS_142),
	.ZN(CTS_140));
   INV_X1 CTS_ccl_INV_clk_G0_L5_11 (.I(CTS_146),
	.ZN(CTS_142));
   INV_X2 CTS_ccl_INV_clk_G0_L4_6 (.I(CTS_147),
	.ZN(FE_USKN164_CTS_146));
   INV_X1 CTS_ccl_INV_clk_G0_L6_20 (.I(CTS_138),
	.ZN(CTS_137));
   INV_X1 CTS_ccl_INV_clk_G0_L6_19 (.I(CTS_138),
	.ZN(CTS_136));
   INV_X1 CTS_ccl_INV_clk_G0_L5_10 (.I(CTS_139),
	.ZN(CTS_138));
   INV_X1 CTS_ccl_INV_clk_G0_L6_18 (.I(CTS_135),
	.ZN(CTS_134));
   INV_X1 CTS_ccl_INV_clk_G0_L6_17 (.I(CTS_135),
	.ZN(CTS_133));
   INV_X1 CTS_ccl_INV_clk_G0_L5_9 (.I(CTS_139),
	.ZN(CTS_135));
   INV_X4 CTS_ccl_INV_clk_G0_L4_5 (.I(CTS_147),
	.ZN(FE_USKN207_CTS_139));
   INV_X8 CTS_ccl_INV_clk_G0_L3_3 (.I(clk_clone14),
	.ZN(FE_USKN201_CTS_147));
   DFFRNQ_X1 \RAM_reg[1][0]  (.D(n_92),
	.RN(1'b1),
	.CLK(CTS_149),
	.Q(n_187));
   DFFRNQ_X1 \RAM_reg[1][1]  (.D(n_128),
	.RN(1'b1),
	.CLK(CTS_173),
	.Q(n_186));
   DFFRNQ_X1 \RAM_reg[2][4]  (.D(n_20),
	.RN(1'b1),
	.CLK(CTS_160),
	.Q(n_175));
   DFFRNQ_X1 \RAM_reg[2][5]  (.D(n_34),
	.RN(1'b1),
	.CLK(clk_clone6),
	.Q(n_174));
   DFFRNQ_X1 \RAM_reg[6][3]  (.D(n_36),
	.RN(1'b1),
	.CLK(clk_clone3),
	.Q(n_144));
   DFFRNQ_X1 \RAM_reg[6][4]  (.D(n_130),
	.RN(1'b1),
	.CLK(CTS_169),
	.Q(n_143));
   DFFRNQ_X1 \RAM_reg[6][5]  (.D(n_126),
	.RN(1'b1),
	.CLK(clk_clone13),
	.Q(n_142));
   DFFRNQ_X1 \RAM_reg[6][6]  (.D(n_124),
	.RN(1'b1),
	.CLK(CTS_143),
	.Q(n_141));
   DFFRNQ_X1 \RAM_reg[2][6]  (.D(n_32),
	.RN(1'b1),
	.CLK(CTS_133),
	.Q(n_173));
   DFFRNQ_X1 \RAM_reg[6][7]  (.D(n_122),
	.RN(1'b1),
	.CLK(CTS_144),
	.Q(n_140));
   DFFRNQ_X1 \RAM_reg[7][0]  (.D(n_120),
	.RN(1'b1),
	.CLK(CTS_161),
	.Q(n_139));
   DFFRNQ_X1 \RAM_reg[2][7]  (.D(n_30),
	.RN(1'b1),
	.CLK(CTS_140),
	.Q(n_172));
   DFFRNQ_X1 \RAM_reg[7][1]  (.D(n_118),
	.RN(1'b1),
	.CLK(CTS_173),
	.Q(n_138));
   DFFRNQ_X1 \RAM_reg[7][2]  (.D(n_114),
	.RN(1'b1),
	.CLK(CTS_169),
	.Q(n_137));
   DFFRNQ_X1 \RAM_reg[3][0]  (.D(n_116),
	.RN(1'b1),
	.CLK(CTS_137),
	.Q(n_171));
   DFFRNQ_X1 \RAM_reg[3][1]  (.D(n_108),
	.RN(1'b1),
	.CLK(CTS_165),
	.Q(n_170));
   DFFRNQ_X1 \RAM_reg[7][3]  (.D(n_112),
	.RN(1'b1),
	.CLK(CTS_154),
	.Q(n_136));
   DFFRNQ_X1 \RAM_reg[7][4]  (.D(n_110),
	.RN(1'b1),
	.CLK(CTS_158),
	.Q(n_135));
   DFFRNQ_X1 \RAM_reg[7][5]  (.D(n_106),
	.RN(1'b1),
	.CLK(CTS_149),
	.Q(n_134));
   DFFRNQ_X1 \RAM_reg[7][6]  (.D(n_104),
	.RN(1'b1),
	.CLK(CTS_143),
	.Q(n_133));
   DFFRNQ_X1 \RAM_reg[3][2]  (.D(n_102),
	.RN(1'b1),
	.CLK(CTS_158),
	.Q(n_169));
   DFFRNQ_X1 \RAM_reg[7][7]  (.D(n_98),
	.RN(1'b1),
	.CLK(CTS_168),
	.Q(n_132));
   DFFRNQ_X1 \RAM_reg[3][3]  (.D(n_100),
	.RN(1'b1),
	.CLK(CTS_166),
	.Q(n_168));
   DFFRNQ_X1 \RAM_reg[1][2]  (.D(n_88),
	.RN(1'b1),
	.CLK(CTS_154),
	.Q(n_185));
   DFFRNQ_X1 \RAM_reg[3][4]  (.D(n_96),
	.RN(1'b1),
	.CLK(CTS_136),
	.Q(n_167));
   DFFRNQ_X1 \RAM_reg[3][5]  (.D(n_94),
	.RN(1'b1),
	.CLK(clk_clone10),
	.Q(n_166));
   DFFRNQ_X1 \RAM_reg[3][6]  (.D(n_90),
	.RN(1'b1),
	.CLK(CTS_133),
	.Q(n_165));
   DFFRNQ_X1 \RAM_reg[3][7]  (.D(n_86),
	.RN(1'b1),
	.CLK(CTS_144),
	.Q(n_164));
   DFFRNQ_X1 \RAM_reg[1][3]  (.D(n_84),
	.RN(1'b1),
	.CLK(CTS_151),
	.Q(n_184));
   DFFRNQ_X1 \RAM_reg[4][0]  (.D(n_82),
	.RN(1'b1),
	.CLK(CTS_134),
	.Q(n_163));
   DFFRNQ_X1 \RAM_reg[4][1]  (.D(n_78),
	.RN(1'b1),
	.CLK(CTS_165),
	.Q(n_162));
   DFFRNQ_X1 \RAM_reg[1][4]  (.D(n_80),
	.RN(1'b1),
	.CLK(CTS_136),
	.Q(n_183));
   DFFRNQ_X1 \RAM_reg[4][2]  (.D(n_76),
	.RN(1'b1),
	.CLK(CTS_157),
	.Q(n_161));
   DFFRNQ_X1 \RAM_reg[4][3]  (.D(n_74),
	.RN(1'b1),
	.CLK(CTS_166),
	.Q(n_160));
   DFFRNQ_X1 \RAM_reg[1][5]  (.D(n_72),
	.RN(1'b1),
	.CLK(CTS_160),
	.Q(n_182));
   DFFRNQ_X1 \RAM_reg[1][6]  (.D(n_68),
	.RN(1'b1),
	.CLK(CTS_141),
	.Q(n_181));
   DFFRNQ_X1 \RAM_reg[4][4]  (.D(n_70),
	.RN(1'b1),
	.CLK(CTS_157),
	.Q(n_159));
   DFFRNQ_X1 \RAM_reg[4][5]  (.D(n_66),
	.RN(1'b1),
	.CLK(clk_clone12),
	.Q(n_158));
   DFFRNQ_X1 \RAM_reg[4][6]  (.D(n_62),
	.RN(1'b1),
	.CLK(CTS_134),
	.Q(n_157));
   DFFRNQ_X1 \RAM_reg[4][7]  (.D(n_60),
	.RN(1'b1),
	.CLK(CTS_140),
	.Q(n_156));
   DFFRNQ_X1 \RAM_reg[1][7]  (.D(n_64),
	.RN(1'b1),
	.CLK(CTS_168),
	.Q(n_180));
   DFFRNQ_X1 \RAM_reg[5][0]  (.D(n_58),
	.RN(1'b1),
	.CLK(CTS_148),
	.Q(n_155));
   DFFRNQ_X1 \RAM_reg[5][1]  (.D(n_56),
	.RN(1'b1),
	.CLK(CTS_172),
	.Q(n_154));
   DFFRNQ_X1 \RAM_reg[5][2]  (.D(n_54),
	.RN(1'b1),
	.CLK(CTS_151),
	.Q(n_153));
   DFFRNQ_X1 \RAM_reg[2][0]  (.D(n_28),
	.RN(1'b1),
	.CLK(CTS_137),
	.Q(n_179));
   DFFRNQ_X1 \RAM_reg[2][1]  (.D(n_24),
	.RN(1'b1),
	.CLK(CTS_150),
	.Q(n_178));
   DFFRNQ_X1 \RAM_reg[5][3]  (.D(n_52),
	.RN(1'b1),
	.CLK(CTS_167),
	.Q(n_152));
   DFFRNQ_X1 \RAM_reg[5][4]  (.D(n_50),
	.RN(1'b1),
	.CLK(CTS_167),
	.Q(n_151));
   DFFRNQ_X1 \RAM_reg[5][5]  (.D(n_48),
	.RN(1'b1),
	.CLK(CTS_148),
	.Q(n_150));
   DFFRNQ_X1 \RAM_reg[5][6]  (.D(n_46),
	.RN(1'b1),
	.CLK(CTS_141),
	.Q(n_149));
   DFFRNQ_X1 \RAM_reg[2][2]  (.D(n_26),
	.RN(1'b1),
	.CLK(CTS_153),
	.Q(n_177));
   DFFRNQ_X1 \RAM_reg[5][7]  (.D(n_44),
	.RN(1'b1),
	.CLK(clk_clone15),
	.Q(n_148));
   DFFRNQ_X1 \RAM_reg[6][0]  (.D(n_42),
	.RN(1'b1),
	.CLK(CTS_161),
	.Q(n_147));
   DFFRNQ_X1 \RAM_reg[2][3]  (.D(n_22),
	.RN(1'b1),
	.CLK(CTS_150),
	.Q(n_176));
   DFFRNQ_X1 \RAM_reg[6][1]  (.D(n_40),
	.RN(1'b1),
	.CLK(CTS_172),
	.Q(n_146));
   DFFRNQ_X1 \RAM_reg[6][2]  (.D(n_38),
	.RN(1'b1),
	.CLK(CTS_153),
	.Q(n_145));
endmodule

module mux2_WIDTH8_41 (
	d0, 
	d1, 
	s, 
	y);
   input [7:0] d0;
   input [7:0] d1;
   input s;
   output [7:0] y;

   // Internal wires
   wire FE_RN_182_0;
   wire FE_RN_181_0;
   wire FE_RN_180_0;
   wire FE_OCPN280_alusrca;
   wire FE_RN_173_0;
   wire FE_RN_172_0;
   wire FE_RN_167_0;
   wire FE_RN_166_0;
   wire FE_RN_163_0;
   wire FE_RN_162_0;
   wire FE_RN_76_0;
   wire FE_RN_75_0;
   wire FE_OCPN97_alusrca;
   wire FE_OCPN96_alusrca;
   wire FE_OCPN93_alusrca;
   wire n_0;
   wire n_2;
   wire n_4;
   wire n_10;
   wire n_12;
   wire n_14;
endmodule

module mux4_WIDTH8 (
	d0, 
	d1, 
	d2, 
	d3, 
	s, 
	y, 
	p1, 
	p2, 
	p3, 
	FE_OCPN7_instr_4, 
	FE_OCPN8_instr_0);
   input [7:0] d0;
   input [7:0] d1;
   input [7:0] d2;
   input [7:0] d3;
   input [1:0] s;
   output [7:0] y;
   input p1;
   input p2;
   input p3;
   input FE_OCPN7_instr_4;
   input FE_OCPN8_instr_0;

   // Internal wires
   wire FE_OCPN279_n_15;
   wire FE_OCPN261_n_12;
   wire FE_RN_171_0;
   wire FE_RN_170_0;
   wire FE_RN_169_0;
   wire FE_RN_168_0;
   wire FE_RN_3;
   wire FE_RN_2;
   wire FE_RN_134_0;
   wire FE_OCPN225_n_13;
   wire FE_OCPN98_alusrcb_0;
   wire FE_RN_54_0;
   wire FE_RN_53_0;
   wire FE_OCPN23_n_12;
   wire FE_OCPN22_n_12;
   wire FE_RN_2_0;
   wire FE_OCPN7_n_15;
   wire FE_DBTN0_n_15;
   wire n_3;
   wire n_4;
   wire n_5;
   wire n_6;
   wire n_7;
   wire n_9;
   wire n_10;
   wire n_11;
   wire n_12;
   wire n_14;
   wire n_15;
   wire n_22;
   wire n_23;
   wire n_24;
   wire n_28;
   wire n_29;
endmodule

module mux2_WIDTH8_40 (
	d0, 
	d1, 
	s, 
	y);
   input [7:0] d0;
   input [7:0] d1;
   input s;
   output [7:0] y;

   // Internal wires
   wire FE_OCPN24_memtoreg;
   wire n_0;
   wire n_2;
   wire n_4;
   wire n_6;
   wire n_8;
   wire n_10;
   wire n_12;
endmodule

module flop_WIDTH8_35 (
	clk, 
	d, 
	q, 
	clk_clone7, 
	clk_clone6, 
	clk_clone5, 
	clk_clone4, 
	clk_clone3, 
	clk_clone2, 
	clk_clone1);
   input clk;
   input [7:0] d;
   output [7:0] q;
   input clk_clone7;
   input clk_clone6;
   input clk_clone5;
   input clk_clone4;
   input clk_clone3;
   input clk_clone2;
   input clk_clone1;

   DFFRNQ_X1 \q_reg[7]  (.D(d[7]),
	.RN(1'b1),
	.CLK(clk_clone5),
	.Q(q[7]));
   DFFRNQ_X1 \q_reg[6]  (.D(d[6]),
	.RN(1'b1),
	.CLK(clk_clone7),
	.Q(q[6]));
   DFFRNQ_X1 \q_reg[4]  (.D(d[4]),
	.RN(1'b1),
	.CLK(clk),
	.Q(q[4]));
   DFFRNQ_X1 \q_reg[3]  (.D(d[3]),
	.RN(1'b1),
	.CLK(clk_clone2),
	.Q(q[3]));
   DFFRNQ_X1 \q_reg[5]  (.D(d[5]),
	.RN(1'b1),
	.CLK(clk_clone6),
	.Q(q[5]));
   DFFRNQ_X1 \q_reg[2]  (.D(d[2]),
	.RN(1'b1),
	.CLK(clk_clone1),
	.Q(q[2]));
   DFFRNQ_X1 \q_reg[1]  (.D(d[1]),
	.RN(1'b1),
	.CLK(clk_clone3),
	.Q(q[1]));
   DFFRNQ_X1 \q_reg[0]  (.D(d[0]),
	.RN(1'b1),
	.CLK(clk_clone4),
	.Q(q[0]));
endmodule

module zerodetect_WIDTH8 (
	a, 
	y);
   input [7:0] a;
   output y;

   // Internal wires
   wire FE_RN_268_0;
   wire FE_RN_52_0;
   wire n_0;
   wire n_1;
   wire n_2;
   wire n_3;
endmodule

module datapath_WIDTH8_REGBITS3 (
	reset, 
	memdata, 
	alusrca, 
	memtoreg, 
	iord, 
	pcen, 
	regwrite, 
	regdst, 
	pcsource, 
	alusrcb, 
	irwrite, 
	alucont, 
	zero, 
	instr, 
	adr, 
	writedata, 
	clk_clone2, 
	clk_clone3, 
	clk_clone4, 
	clk_clone1, 
	clk, 
	p1, 
	FE_OCPN4_instr_2, 
	FE_OCPN13_n);
   input reset;
   input [7:0] memdata;
   input alusrca;
   input memtoreg;
   input iord;
   input pcen;
   input regwrite;
   input regdst;
   input [1:0] pcsource;
   input [1:0] alusrcb;
   input [3:0] irwrite;
   input [2:0] alucont;
   output zero;
   output [31:0] instr;
   output [7:0] adr;
   output [7:0] writedata;
   input clk_clone2;
   input clk_clone3;
   input clk_clone4;
   input clk_clone1;
   input clk;
   output p1;
   output FE_OCPN4_instr_2;
   output FE_OCPN13_n;

   // Internal wires
   wire FE_OCPN314_aluresult_0;
   wire FE_OCPN131_n;
   wire FE_OCPN309_aluresult_6;
   wire FE_OCPN121_pc_1;
   wire FE_OCPN295_instr_1;
   wire FE_USKN291_CTS_217;
   wire FE_USKN290_CTS_217;
   wire FE_USKN289_CTS_231;
   wire FE_USKN288_CTS_231;
   wire FE_USKN287_CTS_225;
   wire FE_USKN286_CTS_225;
   wire FE_USKN285_CTS_270;
   wire FE_USKN284_CTS_270;
   wire FE_USKN283_CTS_218;
   wire FE_USKN282_CTS_218;
   wire FE_OCPN275_pc_2;
   wire FE_OCPN274_aluresult_3;
   wire FE_OCPN263_instr_0;
   wire FE_OCPN262_aluresult_1;
   wire FE_OCPN260_instr_5;
   wire FE_OCPN120_pc_3;
   wire FE_USKN250_CTS_238;
   wire FE_USKN249_CTS_238;
   wire FE_USKN248_CTS_250;
   wire FE_USKN247_CTS_250;
   wire FE_USKN246_CTS_270;
   wire FE_USKN245_CTS_270;
   wire FE_USKN244_CTS_218;
   wire FE_USKN243_CTS_218;
   wire FE_OCPN112_instr_3;
   wire FE_OCPN109_instr_4;
   wire FE_OCPN227_instr_1;
   wire FE_USKN198_CTS_266;
   wire FE_USKN197_CTS_266;
   wire FE_USKN196_CTS_267;
   wire FE_USKN195_CTS_267;
   wire FE_USKN194_CTS_270;
   wire FE_USKN193_CTS_270;
   wire FE_USKN192_CTS_210;
   wire FE_USKN191_CTS_210;
   wire FE_OCPN187_instr_3;
   wire FE_USKN171_CTS_231;
   wire FE_USKN170_CTS_231;
   wire FE_USKN169_CTS_248;
   wire FE_USKN168_CTS_248;
   wire FE_USKN159_CTS_237;
   wire FE_USKN158_CTS_237;
   wire FE_USKN157_CTS_249;
   wire FE_USKN156_CTS_249;
   wire FE_USKN151_CTS_238;
   wire FE_USKN150_CTS_238;
   wire FE_USKN149_CTS_250;
   wire FE_USKN148_CTS_250;
   wire FE_USKN147_CTS_239;
   wire FE_USKN146_CTS_239;
   wire FE_USKN145_CTS_258;
   wire FE_USKN144_CTS_258;
   wire FE_USKN143_CTS_240;
   wire FE_USKN142_CTS_240;
   wire FE_USKN141_CTS_259;
   wire FE_USKN140_CTS_259;
   wire FE_USKN139_CTS_243;
   wire FE_USKN138_CTS_243;
   wire FE_USKN137_CTS_249;
   wire FE_USKN136_CTS_249;
   wire FE_USKN135_CTS_270;
   wire FE_USKN134_CTS_270;
   wire FE_USKN133_CTS_250;
   wire FE_USKN132_CTS_250;
   wire FE_USKN131_CTS_210;
   wire FE_USKN130_CTS_210;
   wire FE_OCPN116_aluresult_0;
   wire FE_OCPN111_aluresult_4;
   wire FE_OCPN97_aluresult_2;
   wire FE_OCPN93_aluresult_5;
   wire FE_OCPN78_n;
   wire FE_OCPN71_ra2_0;
   wire FE_OCPN70_ra2_1;
   wire CTS_271;
   wire CTS_270;
   wire CTS_269;
   wire CTS_268;
   wire CTS_267;
   wire CTS_266;
   wire CTS_265;
   wire CTS_264;
   wire CTS_263;
   wire CTS_262;
   wire CTS_261;
   wire CTS_260;
   wire CTS_259;
   wire CTS_258;
   wire CTS_257;
   wire CTS_256;
   wire CTS_255;
   wire CTS_254;
   wire CTS_253;
   wire CTS_252;
   wire CTS_251;
   wire CTS_250;
   wire CTS_249;
   wire CTS_248;
   wire CTS_247;
   wire CTS_246;
   wire CTS_245;
   wire CTS_244;
   wire CTS_243;
   wire CTS_242;
   wire CTS_241;
   wire CTS_240;
   wire CTS_239;
   wire CTS_238;
   wire CTS_237;
   wire CTS_236;
   wire CTS_235;
   wire CTS_234;
   wire CTS_233;
   wire CTS_232;
   wire CTS_231;
   wire CTS_230;
   wire CTS_229;
   wire CTS_228;
   wire CTS_227;
   wire CTS_226;
   wire CTS_225;
   wire CTS_224;
   wire CTS_223;
   wire CTS_222;
   wire CTS_221;
   wire CTS_220;
   wire CTS_219;
   wire CTS_218;
   wire CTS_217;
   wire CTS_216;
   wire CTS_215;
   wire CTS_214;
   wire CTS_213;
   wire CTS_212;
   wire CTS_211;
   wire CTS_210;
   wire CTS_209;
   wire CTS_208;
   wire CTS_207;
   wire CTS_206;
   wire CTS_205;
   wire [7:0] pc;
   wire [7:0] aluout;
   wire [7:0] src1;
   wire [7:0] src2;
   wire [7:0] aluresult;
   wire [7:0] rd1;
   wire [7:0] a;
   wire [2:0] ra1;
   wire [2:0] ra2;
   wire [7:0] md;
   wire [7:0] nextpc;
   wire [2:0] wa;
   wire [7:0] wd;
   wire [7:0] rd2;
   wire UNCONNECTED;
   wire UNCONNECTED0;
   wire UNCONNECTED1;
   wire UNCONNECTED2;
   wire UNCONNECTED3;
   wire UNCONNECTED4;
   wire UNCONNECTED5;
   wire UNCONNECTED6;
   wire UNCONNECTED7;
   wire n_17;
   wire n_21;
   wire n_29;
   wire n_30;
   wire n_31;

   assign instr[6] = 1'b0 ;
   assign instr[7] = 1'b0 ;
   assign instr[8] = 1'b0 ;
   assign instr[9] = 1'b0 ;
   assign instr[10] = 1'b0 ;
   assign instr[11] = 1'b0 ;
   assign instr[12] = 1'b0 ;
   assign instr[13] = 1'b0 ;
   assign instr[14] = 1'b0 ;
   assign instr[15] = 1'b0 ;
   assign instr[16] = 1'b0 ;
   assign instr[17] = 1'b0 ;
   assign instr[18] = 1'b0 ;
   assign instr[19] = 1'b0 ;
   assign instr[20] = 1'b0 ;
   assign instr[21] = 1'b0 ;
   assign instr[22] = 1'b0 ;
   assign instr[23] = 1'b0 ;
   assign instr[24] = 1'b0 ;
   assign instr[25] = 1'b0 ;

   INV_X4 FE_USKC291_CTS_217 (.I(FE_USKN291_CTS_217),
	.ZN(CTS_217));
   INV_X4 FE_USKC290_CTS_217 (.I(FE_USKN290_CTS_217),
	.ZN(FE_USKN291_CTS_217));
   INV_X8 FE_USKC289_CTS_231 (.I(FE_USKN289_CTS_231),
	.ZN(FE_USKN171_CTS_231));
   INV_X8 FE_USKC288_CTS_231 (.I(FE_USKN288_CTS_231),
	.ZN(FE_USKN289_CTS_231));
   INV_X2 FE_USKC287_CTS_225 (.I(FE_USKN287_CTS_225),
	.ZN(CTS_225));
   INV_X2 FE_USKC286_CTS_225 (.I(FE_USKN286_CTS_225),
	.ZN(FE_USKN287_CTS_225));
   INV_X8 FE_USKC285_CTS_270 (.I(FE_USKN285_CTS_270),
	.ZN(FE_USKN246_CTS_270));
   INV_X8 FE_USKC284_CTS_270 (.I(FE_USKN284_CTS_270),
	.ZN(FE_USKN285_CTS_270));
   INV_X4 FE_USKC283_CTS_218 (.I(FE_USKN283_CTS_218),
	.ZN(CTS_218));
   INV_X4 FE_USKC282_CTS_218 (.I(FE_USKN282_CTS_218),
	.ZN(FE_USKN283_CTS_218));
   INV_X4 FE_USKC250_CTS_238 (.I(FE_USKN250_CTS_238),
	.ZN(FE_USKN151_CTS_238));
   INV_X4 FE_USKC249_CTS_238 (.I(FE_USKN249_CTS_238),
	.ZN(FE_USKN250_CTS_238));
   INV_X8 FE_USKC248_CTS_250 (.I(FE_USKN248_CTS_250),
	.ZN(FE_USKN149_CTS_250));
   INV_X8 FE_USKC247_CTS_250 (.I(FE_USKN247_CTS_250),
	.ZN(FE_USKN248_CTS_250));
   INV_X8 FE_USKC246_CTS_270 (.I(FE_USKN246_CTS_270),
	.ZN(FE_USKN194_CTS_270));
   INV_X8 FE_USKC245_CTS_270 (.I(FE_USKN245_CTS_270),
	.ZN(FE_USKN284_CTS_270));
   INV_X2 FE_USKC244_CTS_218 (.I(FE_USKN244_CTS_218),
	.ZN(FE_USKN282_CTS_218));
   INV_X2 FE_USKC243_CTS_218 (.I(FE_USKN243_CTS_218),
	.ZN(FE_USKN244_CTS_218));
   INV_X4 FE_USKC198_CTS_266 (.I(FE_USKN198_CTS_266),
	.ZN(CTS_266));
   INV_X4 FE_USKC197_CTS_266 (.I(FE_USKN197_CTS_266),
	.ZN(FE_USKN198_CTS_266));
   INV_X4 FE_USKC196_CTS_267 (.I(FE_USKN196_CTS_267),
	.ZN(CTS_267));
   INV_X4 FE_USKC195_CTS_267 (.I(FE_USKN195_CTS_267),
	.ZN(FE_USKN196_CTS_267));
   INV_X4 FE_USKC194_CTS_270 (.I(FE_USKN194_CTS_270),
	.ZN(FE_USKN135_CTS_270));
   INV_X4 FE_USKC193_CTS_270 (.I(FE_USKN193_CTS_270),
	.ZN(FE_USKN245_CTS_270));
   INV_X4 FE_USKC192_CTS_210 (.I(FE_USKN192_CTS_210),
	.ZN(FE_USKN131_CTS_210));
   INV_X4 FE_USKC191_CTS_210 (.I(FE_USKN191_CTS_210),
	.ZN(FE_USKN192_CTS_210));
   INV_X8 FE_USKC171_CTS_231 (.I(FE_USKN171_CTS_231),
	.ZN(CTS_231));
   INV_X8 FE_USKC170_CTS_231 (.I(FE_USKN170_CTS_231),
	.ZN(FE_USKN288_CTS_231));
   INV_X8 FE_USKC169_CTS_248 (.I(FE_USKN169_CTS_248),
	.ZN(CTS_248));
   INV_X8 FE_USKC168_CTS_248 (.I(FE_USKN168_CTS_248),
	.ZN(FE_USKN169_CTS_248));
   INV_X8 FE_USKC159_CTS_237 (.I(FE_USKN159_CTS_237),
	.ZN(CTS_237));
   INV_X8 FE_USKC158_CTS_237 (.I(FE_USKN158_CTS_237),
	.ZN(FE_USKN159_CTS_237));
   INV_X8 FE_USKC157_CTS_249 (.I(FE_USKN157_CTS_249),
	.ZN(CTS_249));
   INV_X8 FE_USKC156_CTS_249 (.I(FE_USKN156_CTS_249),
	.ZN(FE_USKN157_CTS_249));
   INV_X4 FE_USKC151_CTS_238 (.I(FE_USKN151_CTS_238),
	.ZN(CTS_238));
   INV_X4 FE_USKC150_CTS_238 (.I(FE_USKN150_CTS_238),
	.ZN(FE_USKN249_CTS_238));
   INV_X4 FE_USKC149_CTS_250 (.I(FE_USKN149_CTS_250),
	.ZN(CTS_250));
   INV_X4 FE_USKC148_CTS_250 (.I(FE_USKN148_CTS_250),
	.ZN(FE_USKN247_CTS_250));
   INV_X2 FE_USKC147_CTS_239 (.I(FE_USKN147_CTS_239),
	.ZN(CTS_239));
   INV_X2 FE_USKC146_CTS_239 (.I(FE_USKN146_CTS_239),
	.ZN(FE_USKN147_CTS_239));
   INV_X2 FE_USKC145_CTS_258 (.I(FE_USKN145_CTS_258),
	.ZN(CTS_258));
   INV_X2 FE_USKC144_CTS_258 (.I(FE_USKN144_CTS_258),
	.ZN(FE_USKN145_CTS_258));
   INV_X4 FE_USKC143_CTS_240 (.I(FE_USKN143_CTS_240),
	.ZN(CTS_240));
   INV_X4 FE_USKC142_CTS_240 (.I(FE_USKN142_CTS_240),
	.ZN(FE_USKN143_CTS_240));
   INV_X8 FE_USKC141_CTS_259 (.I(FE_USKN141_CTS_259),
	.ZN(CTS_259));
   INV_X8 FE_USKC140_CTS_259 (.I(FE_USKN140_CTS_259),
	.ZN(FE_USKN141_CTS_259));
   INV_X4 FE_USKC139_CTS_243 (.I(FE_USKN139_CTS_243),
	.ZN(CTS_243));
   INV_X4 FE_USKC138_CTS_243 (.I(FE_USKN138_CTS_243),
	.ZN(FE_USKN139_CTS_243));
   INV_X8 FE_USKC137_CTS_249 (.I(FE_USKN137_CTS_249),
	.ZN(FE_USKN156_CTS_249));
   INV_X8 FE_USKC136_CTS_249 (.I(FE_USKN136_CTS_249),
	.ZN(FE_USKN137_CTS_249));
   INV_X4 FE_USKC135_CTS_270 (.I(FE_USKN135_CTS_270),
	.ZN(CTS_270));
   INV_X4 FE_USKC134_CTS_270 (.I(FE_USKN134_CTS_270),
	.ZN(FE_USKN193_CTS_270));
   INV_X4 FE_USKC133_CTS_250 (.I(FE_USKN133_CTS_250),
	.ZN(FE_USKN148_CTS_250));
   INV_X4 FE_USKC132_CTS_250 (.I(FE_USKN132_CTS_250),
	.ZN(FE_USKN133_CTS_250));
   INV_X2 FE_USKC131_CTS_210 (.I(FE_USKN131_CTS_210),
	.ZN(CTS_210));
   INV_X2 FE_USKC130_CTS_210 (.I(FE_USKN130_CTS_210),
	.ZN(FE_USKN191_CTS_210));
   INV_X2 CTS_ccl_INV_clk_G0_L6_61 (.I(CTS_267),
	.ZN(FE_USKN197_CTS_266));
   INV_X4 CTS_ccl_INV_clk_G0_L5_31 (.I(CTS_268),
	.ZN(FE_USKN195_CTS_267));
   INV_X2 CTS_ccl_INV_clk_G0_L6_59 (.I(CTS_265),
	.ZN(CTS_264));
   INV_X2 CTS_ccl_INV_clk_G0_L5_30 (.I(CTS_268),
	.ZN(CTS_265));
   INV_X8 CTS_ccl_INV_clk_G0_L4_16 (.I(CTS_269),
	.ZN(CTS_268));
   INV_X1 CTS_ccl_INV_clk_G0_L6_58 (.I(CTS_262),
	.ZN(CTS_261));
   INV_X1 CTS_ccl_INV_clk_G0_L6_57 (.I(CTS_262),
	.ZN(CTS_260));
   INV_X4 CTS_ccl_INV_clk_G0_L5_29 (.I(CTS_263),
	.ZN(CTS_262));
   INV_X1 CTS_ccl_INV_clk_G0_L6_56 (.I(CTS_259),
	.ZN(FE_USKN144_CTS_258));
   INV_X1 CTS_ccl_INV_clk_G0_L6_55 (.I(CTS_259),
	.ZN(CTS_257));
   INV_X4 CTS_ccl_INV_clk_G0_L5_28 (.I(CTS_263),
	.ZN(FE_USKN140_CTS_259));
   INV_X8 CTS_ccl_INV_clk_G0_L4_15 (.I(CTS_269),
	.ZN(CTS_263));
   INV_X8 CTS_ccl_INV_clk_G0_L3_8 (.I(CTS_270),
	.ZN(CTS_269));
   INV_X1 CTS_ccl_INV_clk_G0_L6_54 (.I(CTS_254),
	.ZN(CTS_253));
   INV_X1 CTS_ccl_INV_clk_G0_L6_53 (.I(CTS_254),
	.ZN(CTS_252));
   INV_X1 CTS_ccl_INV_clk_G0_L5_27 (.I(CTS_255),
	.ZN(CTS_254));
   INV_X2 CTS_ccl_INV_clk_G0_L5_26 (.I(CTS_255),
	.ZN(CTS_251));
   INV_X4 CTS_ccl_INV_clk_G0_L4_14 (.I(CTS_256),
	.ZN(CTS_255));
   INV_X8 CTS_ccl_INV_clk_G0_L3_7 (.I(CTS_270),
	.ZN(CTS_256));
   INV_X8 CTS_ccl_INV_clk_G0_L2_4 (.I(CTS_271),
	.ZN(FE_USKN134_CTS_270));
   INV_X1 CTS_ccl_INV_clk_G0_L6_48 (.I(CTS_247),
	.ZN(CTS_246));
   INV_X4 CTS_ccl_INV_clk_G0_L5_24 (.I(CTS_248),
	.ZN(CTS_247));
   INV_X1 CTS_ccl_INV_clk_G0_L6_45 (.I(CTS_245),
	.ZN(CTS_244));
   INV_X4 CTS_ccl_INV_clk_G0_L5_23 (.I(CTS_248),
	.ZN(CTS_245));
   INV_X8 CTS_ccl_INV_clk_G0_L4_12 (.I(CTS_249),
	.ZN(FE_USKN168_CTS_248));
   INV_X1 CTS_ccl_INV_clk_G0_L6_44 (.I(CTS_242),
	.ZN(CTS_241));
   INV_X2 CTS_ccl_INV_clk_G0_L5_22 (.I(CTS_243),
	.ZN(CTS_242));
   INV_X2 CTS_ccl_INV_clk_G0_L6_42 (.I(CTS_240),
	.ZN(FE_USKN146_CTS_239));
   INV_X2 CTS_ccl_INV_clk_G0_L5_21 (.I(CTS_243),
	.ZN(FE_USKN142_CTS_240));
   INV_X4 CTS_ccl_INV_clk_G0_L4_11 (.I(CTS_249),
	.ZN(FE_USKN138_CTS_243));
   INV_X8 CTS_ccl_INV_clk_G0_L3_6 (.I(CTS_250),
	.ZN(FE_USKN136_CTS_249));
   INV_X8 CTS_ccl_INV_clk_G0_L2_3 (.I(CTS_271),
	.ZN(FE_USKN132_CTS_250));
   INV_X4 CTS_ccl_INV_clk_G0_L1_2 (.I(clk),
	.ZN(CTS_271));
   INV_X1 CTS_ccl_INV_clk_G0_L6_32 (.I(CTS_235),
	.ZN(CTS_234));
   INV_X4 CTS_ccl_INV_clk_G0_L5_16 (.I(CTS_236),
	.ZN(CTS_235));
   INV_X1 CTS_ccl_INV_clk_G0_L6_30 (.I(CTS_233),
	.ZN(CTS_232));
   INV_X2 CTS_ccl_INV_clk_G0_L5_15 (.I(CTS_236),
	.ZN(CTS_233));
   INV_X4 CTS_ccl_INV_clk_G0_L4_8 (.I(CTS_237),
	.ZN(CTS_236));
   INV_X1 CTS_ccl_INV_clk_G0_L6_28 (.I(CTS_230),
	.ZN(CTS_229));
   INV_X1 CTS_ccl_INV_clk_G0_L6_27 (.I(CTS_230),
	.ZN(CTS_228));
   INV_X2 CTS_ccl_INV_clk_G0_L5_14 (.I(CTS_231),
	.ZN(CTS_230));
   INV_X1 CTS_ccl_INV_clk_G0_L6_26 (.I(CTS_227),
	.ZN(CTS_226));
   INV_X4 CTS_ccl_INV_clk_G0_L5_13 (.I(CTS_231),
	.ZN(CTS_227));
   INV_X8 CTS_ccl_INV_clk_G0_L4_7 (.I(CTS_237),
	.ZN(FE_USKN170_CTS_231));
   INV_X8 CTS_ccl_INV_clk_G0_L3_4 (.I(CTS_238),
	.ZN(FE_USKN158_CTS_237));
   INV_X4 CTS_ccl_INV_clk_G0_L2_2 (.I(clk_clone1),
	.ZN(FE_USKN150_CTS_238));
   INV_X1 CTS_ccl_INV_clk_G0_L6_12 (.I(CTS_224),
	.ZN(CTS_223));
   INV_X1 CTS_ccl_INV_clk_G0_L6_11 (.I(CTS_224),
	.ZN(CTS_222));
   INV_X1 CTS_ccl_INV_clk_G0_L5_6 (.I(CTS_225),
	.ZN(CTS_224));
   INV_X1 CTS_ccl_INV_clk_G0_L6_10 (.I(CTS_221),
	.ZN(CTS_220));
   INV_X1 CTS_ccl_INV_clk_G0_L6_9 (.I(CTS_221),
	.ZN(CTS_219));
   INV_X1 CTS_ccl_INV_clk_G0_L5_5 (.I(CTS_225),
	.ZN(CTS_221));
   INV_X1 CTS_ccl_INV_clk_G0_L4_3 (.I(clk_clone3),
	.ZN(FE_USKN286_CTS_225));
   INV_X1 CTS_ccl_INV_clk_G0_L6_8 (.I(CTS_216),
	.ZN(CTS_215));
   INV_X1 CTS_ccl_INV_clk_G0_L6_7 (.I(CTS_216),
	.ZN(CTS_214));
   INV_X2 CTS_ccl_INV_clk_G0_L5_4 (.I(CTS_217),
	.ZN(CTS_216));
   INV_X1 CTS_ccl_INV_clk_G0_L6_6 (.I(CTS_213),
	.ZN(CTS_212));
   INV_X1 CTS_ccl_INV_clk_G0_L6_5 (.I(CTS_213),
	.ZN(CTS_211));
   INV_X1 CTS_ccl_INV_clk_G0_L5_3 (.I(CTS_217),
	.ZN(CTS_213));
   INV_X2 CTS_ccl_INV_clk_G0_L4_2 (.I(CTS_218),
	.ZN(FE_USKN290_CTS_217));
   INV_X1 CTS_ccl_INV_clk_G0_L6_4 (.I(CTS_209),
	.ZN(CTS_208));
   INV_X1 CTS_ccl_INV_clk_G0_L5_2 (.I(CTS_210),
	.ZN(CTS_209));
   INV_X1 CTS_ccl_INV_clk_G0_L6_2 (.I(CTS_207),
	.ZN(CTS_206));
   INV_X1 CTS_ccl_INV_clk_G0_L6_1 (.I(CTS_207),
	.ZN(CTS_205));
   INV_X1 CTS_ccl_INV_clk_G0_L5_1 (.I(CTS_210),
	.ZN(CTS_207));
   INV_X2 CTS_ccl_INV_clk_G0_L4_1 (.I(CTS_218),
	.ZN(FE_USKN130_CTS_210));
   INV_X2 CTS_ccl_INV_clk_G0_L3_1 (.I(clk_clone4),
	.ZN(FE_USKN243_CTS_218));
   mux2_WIDTH8 adrmux (.d0({ pc[7],
		pc[6],
		pc[5],
		pc[4],
		FE_OCPN120_pc_3,
		FE_OCPN275_pc_2,
		FE_OCPN121_pc_1,
		pc[0] }),
	.d1(aluout),
	.s(iord),
	.y(adr));
   alu_WIDTH8 alunit (.a(src1),
	.b(src2),
	.alucont(alucont),
	.result(aluresult));
   flop_WIDTH8_36 areg (.d(rd1),
	.q(a),
	.clk_clone6(CTS_206),
	.clk_clone5(CTS_208),
	.clk_clone4(CTS_227),
	.clk_clone3(CTS_234),
	.clk_clone2(CTS_239),
	.clk_clone1(CTS_253),
	.clk(CTS_265));
   flopen_WIDTH8 ir0 (.clk(CTS_264),
	.en(irwrite[0]),
	.d(memdata),
	.q({ n_29,
		n_30,
		FE_UNCONNECTEDZ_0,
		instr[4],
		instr[3],
		instr[2],
		instr[1],
		instr[0] }),
	.clk_clone7(CTS_205),
	.clk_clone6(CTS_206),
	.clk_clone5(CTS_212),
	.clk_clone4(CTS_215),
	.clk_clone3(CTS_234),
	.clk_clone2(CTS_252),
	.clk_clone1(CTS_261),
	.p1(p1),
	.FE_OCPN6_instr_4(FE_OCPN109_instr_4),
	.FE_OCPN9_instr_3(FE_OCPN112_instr_3),
	.p2(FE_OCPN260_instr_5),
	.FE_OCPN11_instr_2(FE_OCPN4_instr_2),
	.FE_OCPN116_instr_5(FE_OCPN131_n));
   flopen_WIDTH8_39 ir1 (.clk(CTS_220),
	.en(irwrite[1]),
	.d({ 1'b0,
		1'b0,
		memdata[5],
		memdata[4],
		memdata[3],
		1'b0,
		1'b0,
		1'b0 }),
	.q({ UNCONNECTED,
		UNCONNECTED0,
		n_17,
		n_21,
		n_31,
		UNCONNECTED1,
		UNCONNECTED2,
		UNCONNECTED3 }),
	.clk_clone2(CTS_211),
	.clk_clone1(CTS_212));
   flopen_WIDTH8_38 ir2 (.clk(CTS_223),
	.en(irwrite[2]),
	.d({ memdata[7],
		memdata[6],
		memdata[5],
		1'b0,
		1'b0,
		memdata[2],
		memdata[1],
		memdata[0] }),
	.q({ ra1,
		UNCONNECTED4,
		UNCONNECTED5,
		ra2 }),
	.clk_clone5(CTS_214),
	.clk_clone4(CTS_215),
	.clk_clone3(CTS_219),
	.clk_clone2(CTS_220),
	.clk_clone1(CTS_222),
	.FE_OCPN0_ra2_1(FE_OCPN70_ra2_1),
	.FE_OCPN1_ra2_0(FE_OCPN71_ra2_0),
	.FE_OCPN2_n(FE_OCPN78_n));
   flopen_WIDTH8_37 ir3 (.en(irwrite[3]),
	.d({ memdata[7],
		memdata[6],
		memdata[5],
		memdata[4],
		memdata[3],
		memdata[2],
		1'b0,
		1'b0 }),
	.q({ instr[31],
		instr[30],
		instr[29],
		instr[28],
		instr[27],
		instr[26],
		UNCONNECTED6,
		UNCONNECTED7 }),
	.clk_clone2(CTS_222),
	.clk_clone1(CTS_223),
	.clk(clk_clone2));
   flop_WIDTH8 mdr (.clk(CTS_264),
	.d(memdata),
	.q(md),
	.clk_clone7(CTS_205),
	.clk_clone6(CTS_211),
	.clk_clone5(CTS_214),
	.clk_clone4(CTS_229),
	.clk_clone3(CTS_241),
	.clk_clone2(CTS_252),
	.clk_clone1(CTS_261));
   mux4_WIDTH8_42 pcmux (.d0({ aluresult[7],
		FE_OCPN309_aluresult_6,
		FE_OCPN93_aluresult_5,
		FE_OCPN111_aluresult_4,
		FE_OCPN274_aluresult_3,
		FE_OCPN97_aluresult_2,
		FE_OCPN262_aluresult_1,
		FE_OCPN116_aluresult_0 }),
	.d1(aluout),
	.d2({ FE_OCPN131_n,
		FE_OCPN109_instr_4,
		FE_OCPN187_instr_3,
		instr[2],
		FE_OCPN295_instr_1,
		FE_OCPN263_instr_0,
		1'b0,
		1'b0 }),
	.d3({ 1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b0 }),
	.s(pcsource),
	.y(nextpc));
   flopenr_WIDTH8 pcreg (.clk(CTS_266),
	.reset(reset),
	.en(pcen),
	.d(nextpc),
	.q(pc),
	.clk_clone6(CTS_208),
	.clk_clone4(CTS_239),
	.clk_clone5(CTS_240),
	.clk_clone3(CTS_257),
	.clk_clone2(CTS_258),
	.clk_clone1(CTS_260),
	.FE_OCPN10_pc_3(FE_OCPN120_pc_3),
	.p1(FE_OCPN275_pc_2),
	.FE_OCPN12_pc_1(FE_OCPN121_pc_1));
   mux2_WIDTH3 regmux (.d0(ra2),
	.d1({ n_17,
		n_21,
		n_31 }),
	.s(regdst),
	.y(wa));
   flop_WIDTH8_34 res (.clk(CTS_266),
	.d({ aluresult[7],
		FE_OCPN309_aluresult_6,
		FE_OCPN93_aluresult_5,
		FE_OCPN111_aluresult_4,
		aluresult[3],
		FE_OCPN97_aluresult_2,
		FE_OCPN262_aluresult_1,
		FE_OCPN116_aluresult_0 }),
	.q(aluout),
	.clk_clone5(CTS_209),
	.clk_clone4(CTS_251),
	.clk_clone3(CTS_257),
	.clk_clone2(CTS_258),
	.clk_clone1(CTS_260));
   regfile_WIDTH8_REGBITS3 rf (.regwrite(regwrite),
	.ra1(ra1),
	.ra2({ ra2[2],
		FE_OCPN70_ra2_1,
		FE_OCPN71_ra2_0 }),
	.wa(wa),
	.wd(wd),
	.rd1(rd1),
	.rd2(rd2),
	.clk_clone15(CTS_219),
	.clk_clone13(CTS_226),
	.clk_clone12(CTS_228),
	.clk_clone10(CTS_232),
	.clk_clone11(CTS_233),
	.clk_clone9(CTS_235),
	.clk_clone14(CTS_238),
	.clk_clone7(CTS_242),
	.clk_clone6(CTS_244),
	.clk_clone5(CTS_245),
	.clk_clone3(CTS_246),
	.clk_clone4(CTS_247),
	.clk_clone8(CTS_250),
	.clk_clone1(CTS_251),
	.clk_clone2(CTS_256),
	.clk(CTS_267),
	.FE_OCPN3_n(FE_OCPN78_n));
   mux2_WIDTH8_41 src1mux (.d0(pc),
	.d1(a),
	.s(alusrca),
	.y(src1));
   mux4_WIDTH8 src2mux (.d0(writedata),
	.d1({ 1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b1 }),
	.d2({ n_29,
		n_30,
		1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b0,
		1'b0 }),
	.d3({ FE_OCPN13_n,
		instr[4],
		FE_OCPN112_instr_3,
		instr[2],
		FE_OCPN227_instr_1,
		FE_OCPN263_instr_0,
		1'b0,
		1'b0 }),
	.s(alusrcb),
	.y(src2),
	.p1(FE_OCPN131_n),
	.p2(FE_OCPN187_instr_3),
	.p3(instr[1]),
	.FE_OCPN7_instr_4(FE_OCPN109_instr_4),
	.FE_OCPN8_instr_0(FE_OCPN263_instr_0));
   mux2_WIDTH8_40 wdmux (.d0(aluout),
	.d1(md),
	.s(memtoreg),
	.y(wd));
   flop_WIDTH8_35 wrd (.clk(CTS_253),
	.d(rd2),
	.q(writedata),
	.clk_clone7(CTS_226),
	.clk_clone6(CTS_228),
	.clk_clone5(CTS_229),
	.clk_clone4(CTS_232),
	.clk_clone3(CTS_241),
	.clk_clone2(CTS_244),
	.clk_clone1(CTS_246));
   zerodetect_WIDTH8 zd (.a(aluresult),
	.y(zero));
endmodule

