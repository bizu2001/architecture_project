module ALUcontrol(funct,ALUop,ALUctr,ALUsrc,signextend);
input [5:0]funct;
input [5:0]ALUop;
output reg ALUsrc;
output reg signextend;
output reg [3:0] ALUctr;
    always@(*)
    begin
        case(ALUop)
        6'b000000:
        begin
		    signextend = 1'b0;
            ALUsrc = 1'b0;
            case(funct)
                6'b100000://add
                begin
                    ALUctr=4'b0010;
                end
                6'b100001://addu
                begin
                    ALUctr=4'b1011;
                end
                6'b100100://and
                begin
                    ALUctr=4'b0000;
                end
                6'b100010://sub
                begin
                    ALUctr=4'b0110;
                end
                6'b100011://subu
                begin
                    ALUctr=4'b1100;
                end
                6'b100101://or
                begin
                    ALUctr=4'b0001;
                end
                6'b100111://nor
                begin
                    ALUctr=4'b0011;
                end
                6'b100110://xor
                begin
                    ALUctr=4'b0100;
                end
                6'b000000://sll
                begin
                    ALUctr=4'b0101;
                end
                6'b000100://sllv
                begin
                    ALUctr=4'b1101;
                end
                6'b000010://srl
                begin
                    ALUctr=4'b0111;
                end
                6'b000110://srlv
                begin
                    ALUctr=4'b1110;
                end
                6'b000011://sra
                begin
                    ALUctr=4'b1000;
                end
                6'b000111://srav
                begin
                    ALUctr=4'b1111;
                end
                6'b101010://slt
                begin
                    ALUctr=4'b1001;
                end
                6'b101011://sltu
                begin
                    ALUctr=4'b1010;
                end
            endcase
        end
        6'b001010://slti
        begin
		    signextend = 1'b0;
            ALUsrc=1'b1;
            ALUctr=4'b1001;//same as slt
        end
        6'b001011://sltiu
        begin
		    signextend = 1'b0;
            ALUsrc=1'b1;
            ALUctr=4'b1010;//same as sltu
        end
        6'b100011://lw
        begin
		    signextend = 1'b0;
            ALUsrc=1'b1;
            ALUctr=4'b1011;//same as addu
        end
        6'b101011://sw
        begin
		    signextend = 1'b0;
            ALUsrc=1'b1;
            ALUctr=4'b1011;//same as addu
        end
        6'b000100://beq
        begin
		    signextend = 1'b0;
            ALUsrc=1'b0;
            ALUctr=4'b1100;//same as subu
        end
        6'b000101://bne
        begin
		    signextend = 1'b0;
            ALUsrc=1'b0;
            ALUctr=4'b1100;//same as subu
        end
        6'b001101://ori
        begin
		    signextend = 1'b1;
            ALUsrc=1'b1;
            ALUctr=4'b0001;
        end
        6'b001100://andi
        begin
		    signextend =1'b1;
            ALUsrc=1'b1;
            ALUctr=4'b0000;
        end
        6'b001110://xori
        begin
		    signextend = 1'b1;
            ALUsrc=1'b1;
            ALUctr=4'b0100;
        end
        6'b001000://addi
        begin
		    signextend = 1'b0;
            ALUsrc=1'b1;
            ALUctr=4'b0010;//same as add
        end
        6'b001001://addiu
        begin
		    signextend =1'b1;
            ALUsrc=1'b1;
            ALUctr=4'b1011;//same as addu
        end
        endcase
    end
endmodule

//realize the core function of the alu
module ALUcom(aluctr,A,B,shamt,result,zero,negative,overflow);
input[31:0] A;
input[31:0] B;
input [3:0] aluctr;
input [31:0] shamt;
output reg[31:0] result;
output  reg zero;
output  reg negative;
output  reg overflow;
reg [32:0]sum_temp;
reg [32:0]sub_temp;


always@(*)begin
    case(aluctr)
    4'b0010://add
    begin
        result = A+B;
        // sum_temp = A+B;
        // case(sum_temp[32:31])
        // 2'b01:overflow = 1'b1;
        // 2'b10:overflow = 1'b1;
        // default: overflow = 1'b0;
        // endcase
        overflow = (A[31]^B[31]) ? 0: (result[31]^A[31]);
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b1011://addu
    begin
        result = A+B;
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b0000://and
    begin
        result = A&B;
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b0110://sub
    begin
        result = $signed(A)-$signed(B);
        // sub_temp = A-B;
        // case(sub_temp[32:31])
        // 2'b01:overflow = 1'b1;
        // 2'b10:overflow = 1'b1;
        // default: overflow = 1'b0;
        // endcase
        overflow = (A[31]^B[31]) ? (result[31]^A[31]):0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b1100://subu
    begin
        result=$signed(A)-$signed(B);
        overflow =1'b0;
        negative = 1'b0;
        zero = result?0:1;
    end
    4'b0001://or
    begin
        result = A|B;
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b0011://nor
    begin
        result=~(A|B);
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b0100://xor
    begin
        result = A^B;
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b0101://sll
    begin
        result=B<<shamt[4:0];
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b1101://sllv
    begin
        result=B<<A[4:0];
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b0111://srl
    begin
        result=B>>shamt[4:0];
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b1110://srlv
    begin
        result=B>>A[4:0];
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b1000://sra
    begin
        result = $signed($signed(B) >>> shamt[4:0]);
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b1111://srav
    begin
        result = $signed($signed(B) >>> A[4:0]);
        overflow =1'b0;
        negative = 1'b0;
        zero = 1'b0;
    end
    4'b1001://slt
    begin
        result=($signed(A)<$signed(B))?32'b1:32'b0;
        overflow =1'b0;
        negative = result[0];
        zero = 1'b0;
    end
    4'b1010://sltu
    begin
        result = (A<B) ? 32'b1 : 32'b0;
        overflow =1'b0;
        negative = result[0];
        zero = 1'b0;
    end
    endcase
end
endmodule

module ALU(instruction, regA, regB, result, zero,negative,overflow);
input [31:0] instruction, regA, regB; // the address of regA is 00000, the address of regB is 00001
output signed[31:0] result;
output [2:0]flags;// the first bit is zero flag, the second bit is negative flag, the third bit is overflow flag.
output zero,negative,overflow;
// Step 1: You should parsing the instruction;
wire [5:0] funct;
wire [5:0] ALUop;
wire [4:0]rs;
wire [4:0]rt;
wire [31:0]shamt;
wire [31:0]imm1;
wire [31:0]imm2;
wire [3:0] ALUctr;
wire ALUsrc;
wire signextend;
wire [31:0]result;
reg [31:0]inputA;//the sane as rs
reg [31:0]inputB;//the same as rt
assign funct=instruction[5:0];
assign ALUop=instruction[31:26];
assign rs=instruction[25:21];
assign rt=instruction[20:16];
assign shamt={{27{1'b0}},instruction[10:6]};
assign imm1={{16{instruction[15]}},instruction[15:0]};//sign extended
assign imm2={{16{1'b0}},instruction[15:0]};//zero extended
ALUcontrol module1(funct,ALUop,ALUctr,ALUsrc,signextend);
//Step 2: You may fetch values in mem
always@(*)
begin
    if (ALUsrc==1'b0)
    begin
        if(rs==5'b00000&&rt==5'b00001)
        begin
            inputA = regA;
            inputB = regB;
        end
        if(rs==5'b00001&&rt==5'b00000)
        begin
            inputB = regA;
            inputA = regB;
        end
        if(rs==5'b00000&&rt==5'b00000)
        begin
            inputB = regA;
            inputA = regA;
        end
        if(rs==5'b00001&&rt==5'b00001)
        begin
            inputB = regB;
            inputA = regB;
        end
    end
    else
    begin
        if(rs==5'b00000)
        begin
            inputA = regA;
			if(signextend==1'b0)
			begin
			    inputB = imm1;
			end
			else
			begin
				inputB = imm2;
			end
        end
        if (rs==5'b00001)
        begin
            inputA = regB;
            if(signextend==1'b0)
			begin
			    inputB = imm1;
			end
			else
			begin
				inputB = imm2;
			end
        end

    end
end
// wire [31:0]A;
// wire [31:0]B;
// assign A=inputA;
// assign B=inputB;
//You should output the correct value of result and correct status of flags
ALUcom module2(ALUctr,inputA,inputB,shamt,result,zero,negative,overflow);
assign flags[0] = overflow;
assign flags[1] = negative;
assign flags[2] = zero;
endmodule