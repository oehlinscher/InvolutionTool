module c17_slack (
nx1,
nx7,
nx3,
nx2,
nx6,
nx23,
nx22);

// Start PIs
input nx1;
input nx7;
input nx3;
input nx2;
input nx6;

// Start POs
output nx23;
output nx22;

// Start wires
wire net_1;
wire nx23;
wire nx1;
wire nx7;
wire nx3;
wire net_2;
wire nx22;
wire nx6;
wire net_0;
wire net_3;
wire nx2;

// Start cells
ND2M1N inst_5 ( .B(net_3), .A(net_0), .Z(nx22) );
ND2M1N inst_2 ( .Z(net_2), .B(net_1), .A(nx7) );
ND2M1N inst_1 ( .Z(net_0), .B(nx3), .A(nx1) );
ND2M1N inst_4 ( .A(net_3), .B(net_2), .Z(nx23) );
ND2M1N inst_3 ( .Z(net_3), .B(net_1), .A(nx2) );
ND2M1N inst_0 ( .Z(net_1), .B(nx6), .A(nx3) );

endmodule

