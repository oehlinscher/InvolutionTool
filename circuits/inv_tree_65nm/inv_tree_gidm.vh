module inv_tree(din, dout1, dout2, dout3, dout4);
  input din;
  output dout1, dout2, dout3, dout4;
  
  wire din;
  wire dout1, dout2, dout3, dout4;
  
  wire temp1, temp2, temp3, temp4;
  wire temp5, temp51, temp52;

  CKINVM1N_g10 g10(.A (din), .Z (temp1));
  CKINVM1N_g11 g11(.A (temp1), .Z (temp2));
  CKINVM1N_g12 g12(.A (temp2), .Z (temp3));
  CKINVM1N_g13 g13(.A (temp3), .Z (temp4));
  CKINVM1N_g14 g14(.A (temp4), .Z (temp5));

  CKINVM1N_g15 g15(.A (temp5), .Z (temp51));
  CKINVM1N_g16 g16(.A (temp5), .Z (temp52));

  CKINVM1N_g17 g17(.A (temp51), .Z (dout1));
  CKINVM1N_g18 g18(.A (temp51), .Z (dout2));  
  CKINVM1N_g19 g19(.A (temp52), .Z (dout3));
  CKINVM1N_g20 g20(.A (temp52), .Z (dout4));
  
  // Experiment with sdf_annotate --> did not work!
  //initial
  //$sdf_annotate("/home/s01525898/involution_tool/circuits/inv_tree/inv_tree_30.sdf");

endmodule
