`timescale 100fs/100fs
`include "CPU.v"
module cpu_test;
reg clk;
CPU testcpu();
initial begin
	#20 clk = 1'b1;
	forever begin
		#20 clk = ~clk;
//		$monitor("%b",testcpu.pc);
		if(testcpu.MEM_instruction==32'b11111111111111111111111111111111)
	    $finish;
	end
end


endmodule