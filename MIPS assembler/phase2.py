import phase1
#"D:/Python/python code/mips assembler/CSC3050_P1/testfile3.asm"
with open("tem_file.txt","r") as tempfile:
    filename = tempfile.readlines()
    file_list = filename[0].split()
    test_name = file_list[0]
    output_name = file_list[1]

try:
    with open(test_name,"r") as input_file:
        lines = input_file.readlines()
        input_file.close()
        source = phase1.first_scan(lines)
        asm_list = source[1]
        label_dic = source[0]
except:
    print("input file not found!")

#mips instruction formats
#r type
#op(6 bits)|rs(5 bits)|rt(5 bits)|rd(5 bits)|shamt(5 bits)|funct(6 bits)
#i type
#op(6 bits)|rs(5 bits)|rt(5 bits)|immediate number (16 bits)
#j type
#op(6 bits)|jump target(26 bits)
#Use a dictionary to store all the r code of the operations
#list of registers
Register_list = ["$zero","$at", "$v0", "$v1","$a0","$a1","$a2","$a3",
                 "$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7",
                 "$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7",
                 "$t8","$t9","$k0","$k1","$gp","$sp","$fp","$ra"]

#the opcods for r type instructions are all 000000
#a dictionary for r instructions(without shift) and their funct
R_noshift_funct_dic={"add":"100000","addu":"100001","sub":"100010",
"subu":"100011","and":"100100","or":"100101","xor":"100110",
"nor":"100111","slt":"101010","sltu":"101011"}
# dictionaries for r instructions(with shift) and their funct
# dictionary for shifting instructions without utilizing shamt
R_shift_funct_dic_ns={
    "sllv":"000100","srlv":"000110","srav":"000111"}
# dictionary for shifting instructions which needs shamt
R_shift_funct_dic_s={"sll":"000000","srl":"000010","sra":"000011"}
# for jump to instructions
R_jumpto_funct_dic={"jr":"001000","mthi":"010001","mtlo":"010011"}
# for jump from instructions
R_jumpfr_funct_dic={"mfhi":"010000","mflo":"010010"}
#for signed or unsigned mult instructions
R_mult_funct_dic = {"div":"011010","divu":"011011","mult":"011000",
"multu":"011001"}
#jalr(rd,rs)
jalr = {"jalr":"001001"}

#dictionaries for i instructions 
#i instructions concerning arithmetic operations
i_opcode_dic_nb={ "addi":"001000","addiu":"001001","andi":"001100",
"ori":"001101","xori":"001110","slti":"001010","sltiu":"001011",}
#i instructions with branch and their opcodes
i_opcode_dic_b={"beq":"000100","bne":"000101"}
#i instructions with branch(also rt value a constant)
i_opcode_dic_cons_b={"bgez":"000001","bgtz":"000111",
"blez":"000110","bltz":"000001"}
#i instructions with loading and saving operations
i_opcode_dic_load={"lb":"100000","lbu":"100100","lh":"100001",
"lhu":"100101","lw":"100011","sb":"101000","sh":"101001","sw":"101011",
"lwl":"100010","lwr":"100110","swl":"101010","swr":"101110"}
#lui
lui={"lui":"001111"}

#j form
j_opcode_dic={"j":"000010","jal":"000011"}

#convert deciaml number to binary number
def decimal2binary(dec):
    binary_digit="01"
    dec = int(dec)
    if dec<2 and dec >= 0:
        return binary_digit[dec]
    elif dec>=2:
        return decimal2binary(dec//2)+binary_digit[dec%2]
    elif dec<0 and dec>-2:
        return "-1"
    else:
        dec = -dec
        return "-"+decimal2binary(dec//2)+binary_digit[dec%2]

#extend the binary to n bits. Keep the "-" if the number is negative
def code_extend(bin,n):
    if len(bin)>n:
        return "overflow"
    if bin[0]=="-":
        u_bin = bin[1:]
        while len(u_bin)<n:
            u_bin = "0"+u_bin
        u_bin="-"+u_bin
        return u_bin
    else:
        while len(bin)<n:
            bin = "0"+bin
        return bin

#convert the binary number to signed code or unsigned code
def binary2code(bin):
    if bin[0] == "-":
        temp1 = bin[1:][::-1]
        index = 0
        for tem_index in range(len(temp1)):
            if temp1[tem_index] == "1":
                index = tem_index
                break
        temp2 = temp1[:index+1]
        for char in temp1[index+1:]:
            if char == "0":
                temp2+="1"
            else:
                temp2+="0"
        return temp2[::-1]
    else:
        return bin

#convert the deciaml number to n bits signed code
def decimal2code(dec,n):
    a=decimal2binary(dec)
    b=code_extend(a,n)
    c=binary2code(b)
    return c

#convert the name of register to 6 bits code
def reg2code(reg_name):
    if reg_name in Register_list:
        reg_num = Register_list.index(reg_name)
        return decimal2code(reg_num,5)

#forming the 16 bits immediate code for bne opertions
def i_target_goto(label,pc):
    target=4194304+label_dic[label]*4
    offset=target-pc-4
    Next_pc = decimal2code(offset/4,16)
    return Next_pc

#forming the 26 bits immediate code for j operations
def j_target_goto(label):
    offset = label_dic[label]*4
    target = decimal2code(4194304+offset,32)
    immediate = target[4:30]
    return immediate

machine_code_list=[]
PC=4194304#0x400000 in decimal(the basic address)
for element in asm_list:
    split_line=[]
#coping with ",","$t1,2" may become "$t12" after deleting the ","
#lift out the opertion first
    oper = element.split()[0]
    split_line.append(oper)
#split the left strings by "," and delete all the blanks
    elements = element.replace(oper,"")
    elements = [x.strip() for x in elements.split(",")]
    for element in elements:
        split_line.append(element)
    if split_line[0] in R_noshift_funct_dic.keys():
        opcodes="000000"
        rs =reg2code(split_line[2])
        rt =reg2code(split_line[3])
        rd =reg2code(split_line[1])
        shamt = "00000"
        funct =R_noshift_funct_dic[split_line[0]]
        code = opcodes+rs+rt+rd+shamt+funct
    elif split_line[0] in R_shift_funct_dic_ns.keys():
        opcodes="000000"
        rs = reg2code(split_line[3])
        rt = reg2code(split_line[2])
        rd = reg2code(split_line[1])
        shamt = "00000"
        funct = R_shift_funct_dic_ns[split_line[0]]
        code = opcodes+rs+rt+rd+shamt+funct
    elif split_line[0] in R_shift_funct_dic_s.keys():
        opcodes = "000000"
        rs = "00000"
        rt = reg2code(split_line[2])
        rd = reg2code(split_line[1])
        shamt = decimal2code(split_line[3],5)
        funct = R_shift_funct_dic_s[split_line[0]]
        code = opcodes+rs+rt+rd+shamt+funct
    elif split_line[0] in R_jumpto_funct_dic.keys():
        opcodes="000000"
        rs = reg2code(split_line[1])
        rt = "00000"
        rd = "00000"
        shamt = "00000"
        funct = R_jumpto_funct_dic[split_line[0]]
        code = opcodes+rs+rt+rd+shamt+funct
    elif split_line[0] in R_jumpfr_funct_dic.keys():
        opcodes="000000"
        rs="00000"
        rt="00000"
        rd=reg2code(split_line[1])
        shamt = "00000"
        funct = R_jumpfr_funct_dic[split_line[0]]
        code = opcodes+rs+rt+rd+shamt+funct
    elif split_line[0] in R_mult_funct_dic.keys():
        opcodes="000000"
        rs=reg2code(split_line[1])
        rt=reg2code(split_line[2])
        rd="00000"
        shamt="00000"
        funct = R_mult_funct_dic[split_line[0]]
        code = opcodes+rs+rt+rd+shamt+funct
    elif split_line[0] in jalr.keys():
        opcodes = jalr[split_line[0]]
        rs = reg2code(split_line[2])
        rt = reg2code(split_line[1])
        rd = "00000"
        shamt ="00000"
        funct = jalr[split_line[0]]
        code = opcodes+rs+rt+rd+shamt+funct
    elif split_line[0] == "break":
        opcodes = "001101"
        rs=rt=rd=shamt="00000"
        funct="000000"
        code = opcodes+rs+rt+rd+shamt+funct
    elif split_line[0] in i_opcode_dic_nb.keys():
        opcodes = i_opcode_dic_nb[split_line[0]]
        rs = reg2code(split_line[2])
        rt = reg2code(split_line[1])
        immediate = decimal2code(split_line[3],16)
        code = opcodes+rs+rt+immediate
    elif split_line[0] in i_opcode_dic_b.keys():
        opcodes = i_opcode_dic_b[split_line[0]]
        rs=reg2code(split_line[1])
        rt=reg2code(split_line[2])
        immediate=i_target_goto(split_line[3],PC)
        code = opcodes+rs+rt+immediate
    elif split_line[0] in i_opcode_dic_cons_b.keys():
        opcodes = i_opcode_dic_cons_b[split_line[0]]
        rs=reg2code(split_line[1])
        if split_line =="bgez":
            rt="00001"
        else:
            rt="00000"
        immediate=i_target_goto(split_line[2],PC)
        code = opcodes+rs+rt+immediate
    elif split_line[0] in i_opcode_dic_load.keys():
        opcodes = i_opcode_dic_load[split_line[0]]
        temp = split_line[2]
        right = temp.find("(")
        left = temp.find(")")
        rs = reg2code(temp[right+1:left])
        rt = reg2code(split_line[1])
        immediate = decimal2code(temp[:right],16)
        code = opcodes+rs+rt+immediate
    elif split_line[0] in lui:
        opcodes = lui[split_line[0]]
        rs="00000"
        rt=reg2code(split_line[1])
        immediate = decimal2code(split_line[2],16)
        code = opcodes+rs+rt+immediate
    elif split_line[0] in j_opcode_dic.keys():
        opcodes = j_opcode_dic[split_line[0]]
        label = split_line[1]
        immediate = j_target_goto(label)
        code = opcodes+immediate
    else:
        wrong = (PC-4194304)//4+1
        code = "undefined operation appears in "+str(wrong)+"th line"
    PC+=4
    machine_code_list.append(code)

    with open(output_name,"w") as output_file:
        for i in machine_code_list:
            output_file.write(i)
            output_file.write('\n')

print(machine_code_list)
print("the machine code is now stored in outputfile.txt ")


