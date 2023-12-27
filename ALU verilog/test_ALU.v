`timescale 1ns/1ps

module alu_test;

reg[31:0] instruction,regA,regB;
wire[31:0]result;
wire[2:0]flags;
ALU testalu(instruction,regA,regB,result,zero,negative,overflow);
initial
begin

$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
$monitor("   %h:%h: %h :  %h   :   %h  : %h: %h:%h:  %h  :  %h  :   %h  :  %h   :   %h      :  %h      :%b",
instruction, testalu.ALUop, testalu.funct, testalu.ALUctr, testalu.ALUsrc, regA , regB, testalu.result, testalu.inputA, testalu.inputB,
testalu.shamt[4:0],testalu.zero, testalu.negative, testalu.overflow, testalu.flags);  

//add
#10 instruction<=32'b000000_00001_00000_00010_00000_100000;
regA<=32'b0000_0000_0000_0000_0010_0000_0000_1111;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_1001;
$display("add");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000000_00001_00000_00010_00000_100000;
regA<=32'b1000_0000_0000_0000_0010_0000_0000_0001;
regB<=32'b1000_0000_0000_0000_0010_0000_0000_0001;
#10 instruction<=32'b000000_00001_00000_00010_00000_100000;
regA<=32'b0100_0000_0000_0000_0011_0000_0000_0001;
regB<=32'b0100_0000_0000_0000_0011_0000_0000_0001;
#10 instruction<=32'b000000_00001_00000_00010_00000_100000;
regA<=32'b0000_0000_0000_0000_0000_0000_1101_1101;
regB<=32'b1111_1111_1111_1111_1111_1111_0010_0011;
#10 instruction<=32'b000000_00001_00000_00010_00000_100000;
regA<=32'b0000_0000_0000_0000_0000_0000_0101_1101;
regB<=32'b1111_1111_1111_1111_1111_1111_0010_0011;
//addu
#10 instruction<=32'b000000_00001_00000_00010_00000_100001;
regA<=32'b1000_0000_0000_1000_1000_0000_0000_0001;
regB<=32'b1000_0000_0000_1000_1000_0000_0000_0001;
$display("addu");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
//and
#10 instruction<=32'b000000_00001_00000_00010_00000_100100;
regA<=32'b1000_0000_0000_0000_0000_0100_0000_0000;
regB<=32'b1111_1111_1111_1111_1111_1011_1111_1111;
$display("and");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
//sub
#10 instruction<=32'b000000_00000_00001_00010_00000_100010;
regA<=32'b1111_0000_0000_0000_0000_0000_0111_1101;
regB<=32'b0000_0000_0000_0000_0000_0000_0010_0001;
$display("sub");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000000_00000_00001_00010_00000_100010;
regA<=32'b1000_0000_0000_0000_0000_0000_0010_0001;
regB<=32'b0111_0000_0000_0000_0000_0000_0111_1101;

#10 instruction<=32'b000000_00000_00001_00010_00000_100010;
regA<=32'b0000_0001_0000_0000_0000_0100_0000_0001;
regB<=32'b1111_0001_0000_0000_0000_0100_0101_1101;

#10 instruction<=32'b000000_00000_00001_00010_00000_100010;
regA<=32'b0000_0001_0000_0000_0000_0000_0000_0000;
regB<=32'b0000_0001_0000_0000_0000_0000_0000_0000;
//subu
#10 instruction<=32'b000000_00000_00001_00010_00000_100011;
regA<=32'b1000_0000_0000_0000_0000_0000_0010_0001;
regB<=32'b0111_0000_0000_0000_0000_0000_0111_1101;
$display("subu");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
//or
#10 instruction<=32'b000000_00000_00001_00010_00000_100101;
regA<=32'b1000_0001_0000_0000_0000_0000_0000_0001;
regB<=32'b0111_0001_0000_0000_0000_0000_0101_1101;
$display("or");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000000_00000_00001_00010_00000_100101;
regA<=32'b1000_0001_0000_0000_0000_0000_0000_0001;
regB<=32'b0111_0001_0000_0010_1000_0000_0101_1101;
//nor
#10 instruction<=32'b000000_00000_00001_00010_00000_100111;
regA<=32'b1000_0000_0000_0100_0000_0100_0000_0001;
regB<=32'b0111_0000_0000_0100_0000_0100_0101_1101;
$display("nor");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000000_00000_00001_00010_00000_100111;
regA<=32'b1000_0001_0010_0100_0000_0100_0000_0001;
regB<=32'b0111_0010_0010_0100_0010_0100_0101_1101;
//xor
#10 instruction<=32'b000000_00000_00001_00010_00000_100110;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b0111_0000_0000_0000_0000_0000_0101_1101;
$display("xor");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000000_00000_00001_00010_00000_100110;
regA<=32'b1000_0000_0000_1000_0000_0100_0000_0001;
regB<=32'b0111_0000_0010_1000_0000_0000_0101_1101;
//sll
#10 instruction<=32'b000000_00000_00001_00010_00100_000000;
//regB will be shifted
regA<=32'b1111_1100_0010_0000_0000_0000_0000_0000;
regB<=32'b0000_0000_0000_0000_0000_0000_0011_0110;
$display("sll");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
//regA will be shifted
#10 instruction<=32'b000000_00000_00000_00010_00010_000000;
regA<=32'b1111_1100_0010_0000_0000_0000_0000_0000;
regB<=32'b0000_0000_0000_0000_0000_0000_0011_0110;
//sllv
#10 instruction<=32'b000000_00000_00001_00010_01000_000100;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0100;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0010;
$display("sllv");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000000_00001_00000_00010_01000_000100;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0100;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0010;
//srl
//regB get shifted
#10 instruction<=32'b000000_00000_00001_00010_00001_000010;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0100;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0010;
$display("srl");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
//regA get shifted
#10 instruction<=32'b000000_00000_00000_00010_00001_000010;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0100;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0010;
//srlv
#10 instruction<=32'b000000_00000_00001_00010_00000_000110;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0100;
$display("srlv");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
//sra
//reg A get shifted
#10 instruction<=32'b000000_00000_00000_00010_10100_000011;
regA<=32'b1111_1100_0010_0000_0000_0000_0000_0000;
regB<=32'b0000_0000_0000_0000_0000_0000_0011_0010;
$display("sra");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
//regB get shifted
#10 instruction<=32'b000000_00000_00001_00010_10000_000011;
regA<=32'b1111_1100_0010_0000_0000_0000_0000_0000;
regB<=32'b0000_0000_0000_0000_0000_0000_0011_0010;
//srav
#10 instruction<=32'b000000_00000_00001_00010_00000_000111;
regA<=32'b1111_1100_0010_0000_0000_0000_0000_0000;
regB<=32'b0000_0000_0000_0000_0000_0000_0011_0010;
$display("srav");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
//slt
#10 instruction<=32'b000000_00000_00001_00010_00000_101010;//if regA<regB,set to be 1
regA<=32'b1111_1100_0010_0000_0000_0000_0000_0000;
regB<=32'b0000_0000_0000_0000_0000_0000_0011_0010;
$display("slt");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000000_00001_00000_00010_00000_101010;//if regA>regB,set to be 1
regA<=32'b1111_1100_0010_0000_0000_0000_0000_0000;
regB<=32'b0000_0000_0000_0000_0000_0000_0011_0010;
//sltu
#10 instruction<=32'b000000_00000_00001_00010_00000_101011;//if regA<regB,set to be 1
regA<=32'b1111_1100_0010_0000_0000_0000_0000_0000;
regB<=32'b0000_0000_0000_0000_0000_0000_0011_0010;
$display("sltu");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(rt) :shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000000_00001_00000_00010_00000_101011;//if regA>regB,set to be 1
regA<=32'b1111_1100_0010_0000_0000_0000_0000_0000;
regB<=32'b0000_0000_0000_0000_0000_0000_0011_0010;
//slti
#10 instruction<=32'b001010_00000_00010_1000000000100000;//compare with the regA;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
$display("slti");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b001010_00001_00010_1000000000100000;//compare with the regA;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
//sltiu
#10 instruction<=32'b001011_00000_00010_1000000000100000;//compare with the regA;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
$display("sltiu");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b001011_00001_00010_1000000000100000;//compare with the regA;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b1111_1111_1111_1111_1111_1111_0000_0001;
//lw
#10 instruction<=32'b100011_00000_00010_1000000000100000;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
$display("lw");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b100011_00000_00010_1000000000100000;
regA<=32'b1000_0000_0000_0000_0000_0000_0010_0000;
regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
#10 instruction<=32'b100011_00000_00010_1000000000100000;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0011;
//sw
#10 instruction<=32'b101011_00000_00010_1111111111100000;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
// regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
$display("sw");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b101011_00000_00010_0000000000100000;
regA<=32'b1000_0000_0000_0000_0000_0000_0010_0000;
// regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
#10 instruction<=32'b101011_00001_00010_0000000000100000;
// regA<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0011;
//beq
#10 instruction<=32'b000100_00001_00000_0000000000000001;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
$display("beq");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000100_00001_00000_0000000000000001;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0000;
regB<=32'b0100_0000_0000_0000_0000_0000_0000_0000;
//bne
#10 instruction<=32'b000101_00001_00000_0000000000000001;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
regB<=32'b0000_0000_0000_0000_0000_0000_0000_0001;
$display("bne");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b000101_00001_00000_0000000000000001;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0000;
regB<=32'b0111_1111_1111_1111_1111_1111_1111_1111;
//ori
#10 instruction<=32'b001101_00001_00010_1000000000100000;
regB<=32'b1000_0000_0000_1111_0000_0000_1111_0001;
$display("ori");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b001101_00001_00010_1000000000100000;
regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
#10 instruction<=32'b001101_00000_00010_0000000000000000;
regA<=32'b0000_0000_0000_0000_0000_0000_1111_0000;
//andi
#10 instruction<=32'b001100_00001_00010_1000000000100000;
regB<=32'b1000_0000_0000_1111_0000_0000_1111_0001;
$display("andi");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b001100_00001_00010_1000000000111111;
regB<=32'b1000_0000_0000_0000_0000_0000_0001_1111;
#10 instruction<=32'b001100_00000_00010_0000000000000000;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0000;
//xori
#10 instruction<=32'b001110_00001_00010_1000000000100000;
regB<=32'b1000_0000_0000_1111_0000_0000_1111_0001;
$display("xori");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b001110_00001_00010_1000000000100000;
regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
#10 instruction<=32'b001110_00000_00010_0000000000000000;
regA<=32'b0000_0000_0000_0000_0000_0000_0000_0000;
//addi
#10 instruction<=32'b001000_00001_00010_1000000000100000;
regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
$display("addi");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b001000_00001_00010_1111111111111111;
regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
#10 instruction<=32'b001000_00000_00010_0000000000100001;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
//addiu
#10 instruction<=32'b001001_00001_00010_1000000000100000;
regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
$display("addiu");
$display("instruction:op:func:ALUctr:ALUsrc:  regA   :  regB   :result  : inputA(rs) : inputB(imm):shamt  : zero : negative : overflow:flags");
#10 instruction<=32'b001001_00001_00010_1111111111111111;
regB<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
#10 instruction<=32'b001001_00000_00010_0000000000100001;
regA<=32'b1000_0000_0000_0000_0000_0000_0000_0001;
#10 $stop;
end


endmodule