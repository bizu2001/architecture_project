import sys
import os
file_names = sys.argv
test_asm = file_names[1]
test_txt = file_names[2]
checkpoint_txt= file_names[3]
test_in = file_names[4]
test_out = file_names[5]
one_extend ="00000000000000000000000000000001"
zero_extend ="00000000000000000000000000000000"
four_extend ="00000000000000000000000000000100"
def unbinary2int(binary):
    count = 0
    number_str=str(binary)[::-1]
    for i in range(0,len(number_str)):
         count+=int(number_str[i])*2**i
    return count
#convert signed binary number to decimal
#caution:return an int
def binary2int(binary):
    count = 0
    number_str=str(binary)[::-1]
    for i in range(0,len(number_str)-1):
         count+=int(number_str[i])*2**i
    count-=int(number_str[-1])*2**(len(number_str)-1)
    return count
#extend the binary code to one word length(32 bits)
def extend2word(code):
    count = len(code)
    while count<32:
        code=code[0]+code
        count+=1
    return code
#extend the binary code with only “0”
def zero2word(output):
    count = len(output)
    while count<32:
        output="0"+output
        count+=1
    return output
#convert positive number to binary number
#as the function is only used in mult(do not require negative number)
#the function only suppport
def decimal2binary(dec):
    binary_digit="01"
    dec = int(dec)
    if dec<2 and dec >= 0:
        return binary_digit[dec]
    elif dec>=2:
        return decimal2binary(dec//2)+binary_digit[dec%2]
#convert a binary code to its 2's component's form
def twocomp(bin):
    temp1 = bin
    temp2= ""
    for tem_index in range(len(temp1)):
        if temp1[tem_index] == "1":
            temp2+="0"
        else:
            temp2+="1"
    output = add(temp2,one_extend)
    return output
def load(input):
    if isinstance(input,str) and len(input)==8:
        return input
    if isinstance(input,str) and len(input)==1:
        asc = decimal2binary(ord(input))
        input = zero2word(asc)[24:32]
        return input
    if isinstance(input,int):
        if input>=0:
            code = zero2word(decimal2binary(input))[24:32]
        else:
            code = zero2word(decimal2binary(input))
            code = twocomp(code)[24:32]
        return code
#the phase1 is modified from the pro1 as their functions are similar
def phase1(lines):
    for tem in range(len(lines)):
        lines[tem] = lines[tem].replace("\t","").replace("\n","").rstrip()
        # delete all the comments
        if "#" in lines[tem]:
            comment = lines[tem].index("#")
            lines[tem] = lines[tem][:comment]
    while "" in lines:
        lines.remove("")
    #".data" may locate at bottom of the asm file
    for item in lines:
        if '.data' in item:
            q = lines.index(item)
            del lines[:q+1]
            break
    #delete the ".text" part
    for item in lines:
        if '.text' in item:
            q = lines.index(item)
            del lines[q:]
            break
    for tem in range(len(lines)):
        lines[tem] = lines[tem].replace("\\n","\n")
        if ":" in lines[tem]:
            colon_index =lines[tem].index(":")
            lines[tem]=lines[tem][colon_index+2:]
    return lines
def type_dic(lines):
    type_dic = dict()
    for line in lines:
        blank_index = line.index(" ")
        type_dic[line[blank_index+1:]]=line[:blank_index]
    return type_dic
def readdata(lines):
    lines = phase1(lines)
    result=type_dic(lines)
    return result
start_address=4194304#the text starts from 0x400000hex
PC_dict=[start_address]
#4 bytes for one block,1 byte for one element
Memory = [0]*6*2**20#The total memory space is 6MB
#list of the value of the registers
Register_list =[zero_extend]*32
#two special registers
Hi_LO=[zero_extend,zero_extend]#["Hi","Lo"]
#convert unsigned binary number to decimal
while True:
    try:
        with open(test_txt,"r") as inputmac:
            lines = inputmac.readlines()
        start=start_address-4194304
        for line in lines:
            #line = line.replace("\n","").replace("\t","").replace(" ","").rstrip("\n")
            for i in range(4):
                # Memory[start+i]=line[i*8:i*8+8]
                Memory[start+i]=line[24-i*8:32-i*8]#store the text in little endian
                #print(line[i*8:i*8+8])
            start = start+4
        #load the static data
        with open(test_asm,"r") as inputass:
            lines = inputass.readlines()
            result = readdata(lines)
            start = 5242880-start_address#the static data starts from 0x500000
            for key in result:
                if result[key]==".ascii":
                    key=key[1:-1]
                    length = len(key)
                    allocate = ((length-1)//4+1)*4
                    for i in range(length):
                        Memory[start+i]=key[i]
                elif result[key]==".asciiz":
                    key=key[1:-1]
                    length = len(key)
                    allocate = ((length)//4+1)*4
                    for i in range(length):
                        Memory[start+i]=key[i]
                    Memory[start+length]="\0"
                elif result[key]==".word":
                    key=key.split(",")
                    count = 0
                    for i in key:
                        if int(i)>=0:
                            i = zero2word(decimal2binary(i))
                            seg1 = i[0:8]
                            seg2 =i[8:16]
                            seg3 = i[16:24]
                            seg4 = i[24:32]
                        else:
                            i = zero2word(decimal2binary(i))
                            neg = twocomp(i)
                            seg1 = neg[0:8]
                            seg2 = neg[8:16]
                            seg3 = neg[16:24]
                            seg4 = neg[24:32]
                        Memory[start+count]=seg1
                        Memory[start+2*count]=seg2
                        Memory[start+3*count]=seg3
                        Memory[start+3*count]=seg4
                        allocate=4*(count+1)
                        count=count+1
                elif result[key]==".byte":
                    key=key.split(",")
                    count = 0
                    for i in key:
                        if int(i)>0:
                            i = zero2word(decimal2binary(i))[24:32]
                        else:
                            i = zero2word(decimal2binary(-i))
                            i = twocomp(i)[24:32]
                        Memory[start+count]=i
                        allocate=count+1
                        count=count+1
                elif result[key]==".half":
                    key=key.split(",")
                    count = 0
                    for i in key:
                        if int(i)>=0:
                            i = zero2word(decimal2binary(i))[16:32]
                            HI = i[0:8]
                            LO = i[8:16]
                        else:
                            i = zero2word(decimal2binary(-i))
                            neg = twocomp(i)[16:32]
                            HI = neg[0:8]
                            LO = neg[8:16]
                        Memory[start+2*count]=LO
                        Memory[start+2*count+1]=HI
                        allocate=2*(count+1)
                        count=count+1
                start = start+allocate
                dynamic_end = start
        break
    except:
        print("wrong input!")
        break
#input:the 5 bits code for the register 
#Output:value stored in the register
def lift_value(binary):
    reg = unbinary2int(binary)
    value = Register_list[reg]
    return value
#add two binary numbers
#check whether overflow occurs in R_add() opertaion
#both binary number should be 32 words
def add(binary1,binary2):
    binary1 = binary1[::-1]
    binary2 = binary2[::-1]
    carry="0"
    output =""
    for bit in range(32):
        if binary1[bit]=="0" and carry=="0":
            output=output+binary2[bit]
            carry = "0"
        elif(binary1[bit] =="0" and carry=="1") or\
        (binary1[bit] =="1" and carry=="0"):
            if binary2[bit] == "0":
                output=output+"1"
                carry = "0"
            else:
                output=output+"0"
                carry="1"
        else:
            output =output+ binary2[bit]
            carry="1"
    return output[::-1]
def logicand(binary1,binary2):
    output = ""
    for bit in range(32):
        if((binary1[bit]=="1") and (binary2[bit]=="1")):
            output=output+"1"
        else:
            output=output+"0"
    return output
def logicor(binary1,binary2):
    output =""
    for bit in range(32):
        if ((binary1[bit]=="0") and(binary2[bit]=="0")):
            output=output+"0"
        else:
            output = output+"1"
    return output
def logicxor(binary1,binary2):
    output=""
    for bit in range(32):
        if (binary1[bit]==binary2[bit]):
            output=output+"1"
        else:
            output=output+"0"
    return output
#compare the value of two signed binary codes
#if binary1 is smalller than binary2,then return one
def compare(binary1,binary2):
    if ((binary1[0]=="1") and (binary2[0]=="0")):
        return one_extend
    elif((binary1[0]=="0") and (binary2[0]=="1")):
        return zero_extend
    else:
        for bit in range(1,32):
            if ((binary1[bit]=="1") and (binary2[bit]=="0")):
                return zero_extend
            elif((binary1[bit]=="0") and (binary2[bit]=="1")):
                return one_extend
            else:pass
    return zero_extend
#compare the value of two unsigned codes
def unsigned_compare(binary1,binary2):
    for bit in range(0,32):
        if ((binary1[bit]=="1") and (binary2[bit]=="0")):
            return zero_extend
        elif((binary1[bit]=="0") and (binary2[bit]=="1")):
            return one_extend
    return zero_extend
#$sp stores the address of the top of the memory
#$fp initialized the same as $sp
top = 10485760
glo = 5275648#0x508000
top = zero2word(decimal2binary(top))
glo = zero2word(decimal2binary(glo))
Register_list[29]=top
Register_list[30]=top
Register_list[28]=glo
#functions of all the instructions
def R_add(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    result = add(binary1,binary2)
    Register_list[int(unbinary2int(rd))]=extend2word(result)
#only difference between add and addu: no overflow check  
def R_addu(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    result = add(binary1,binary2)
    Register_list[int(unbinary2int(rd))]=extend2word(result)
def R_sub(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = twocomp(extend2word(lift_value(rt)))
    result = add(binary1,binary2)
    Register_list[int(unbinary2int(rd))]=extend2word(result)
def R_subu(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = twocomp(extend2word(lift_value(rt)))
    result = add(binary1,binary2)
    Register_list[int(unbinary2int(rd))]=extend2word(result)
def R_and(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    Register_list[int(unbinary2int(rd))]=logicand(binary1,binary2)
def R_or(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    Register_list[int(unbinary2int(rd))]=logicor(binary1,binary2)
def R_xor(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    Register_list[int(unbinary2int(rd))]=logicxor(binary1,binary2)
def R_nor(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    output=""
    for bit in range(32):
        if ((binary1[bit]=="0") and (binary2[bit]=="0")):
            output=output+"1"
        else:
            output =output+"0"
    Register_list[int(unbinary2int(rd))]=output
def R_slt(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    output = compare(binary1,binary2)
    Register_list[int(unbinary2int(rd))]=output
def R_sltu(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    output = unsigned_compare(binary1,binary2)
    Register_list[int(unbinary2int(rd))]=output
#rs determines the offset amount of the shift
def R_sllv(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    shift =unbinary2int(binary1[28:])
    sh=1
    output=binary2
    while sh<=shift:
        output=output[1:]+"0"
        sh+=1
    Register_list[int(unbinary2int(rd))]=output

def R_srlv(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    shift =unbinary2int(binary1[28:])
    sh=1
    output=binary2
    while sh<=shift:
        output="0"+output[:31]
        sh+=1
    Register_list[int(unbinary2int(rd))]=output

def R_srav(rs,rt,rd):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    shift =unbinary2int(binary1[28:])
    sh=1
    output = binary2
    while sh<=shift:
        output=output[0]+output[0:31]
        sh+=1
    Register_list[int(unbinary2int(rd))]=output
def R_sll(rt,rd,shamt):
    binary = extend2word(lift_value(rt))
    shift = unbinary2int(shamt)
    sh =1
    output = binary
    while sh<=shift:
        output = output[1:]+"0"
        sh+=1
    Register_list[int(unbinary2int(rd))]=output
def R_srl(rt,rd,shamt):
    binary = extend2word(lift_value(rt))
    shift = unbinary2int(shamt)
    sh =1
    output = binary
    while sh<=shift:
        output = "0"+output[0:31]
        sh+=1
    Register_list[int(unbinary2int(rd))]=output
def R_sra(rt,rd,shamt):
    binary = extend2word(lift_value(rt))
    shift = unbinary2int(shamt)
    sh = 1
    output = binary 
    while sh<=shift:
        output = output[0]+output[0:31]
        sh+=1
    Register_list[int(unbinary2int(rd))]=output
def R_jr(rs):
    PC_dict[0]=unbinary2int(lift_value(rs))-4#as all the PC will plus 4 after every execution,
     #for every jump instruction, the PC has to delete 4 inside the function
def R_mthi(rs):
    Hi_LO[0]=lift_value(rs)
def R_mtlo(rs):
    Hi_LO[1]=lift_value(rs)
def R_mfhi(rd):
    Register_list[int(unbinary2int(rd))]=Hi_LO[0]
def R_mflo(rd):
    Register_list[int(unbinary2int(rd))]=Hi_LO[1]
def R_div(rs,rt):
    divident = binary2int(extend2word(lift_value(rs)))
    divisor = binary2int(extend2word(lift_value(rt)))
    quotient = decimal2binary(divident//divisor)
    remain =decimal2binary(divident%divisor) 
    quotient_word=extend2word(quotient)
    remain_word=extend2word(remain)
    Hi_LO[0]=remain_word
    Hi_LO[1]=quotient_word
def R_divu(rs,rt):
    divident = unbinary2int(extend2word(lift_value(rs)))
    divisor = unbinary2int(extend2word(lift_value(rt)))
    quotient = decimal2binary(divident//divisor)
    remain =decimal2binary(divident%divisor) 
    quotient_word=extend2word(quotient)
    remain_word=extend2word(remain)
    Hi_LO[0]=remain_word
    Hi_LO[1]=quotient_word
def R_mult(rs,rt):
    mult1 = binary2int(extend2word(lift_value(rs)))
    mult2 = binary2int(extend2word(lift_value(rt)))
    result = decimal2binary(mult1*mult2)
    count = len(result)
    while count<64:
        result=result[0]+result
        count+=1
    Hi_LO[0]=count[0:32]
    Hi_LO[1]=count[32:64]
def R_multu(rs,rt):
    mult1 = unbinary2int(extend2word(lift_value(rs)))
    mult2 = unbinary2int(extend2word(lift_value(rt)))
    result = decimal2binary(mult1*mult2)
    count = len(result)
    while count<64:
        result=result[0]+result
        count+=1
    Hi_LO[0]=count[0:32]
    Hi_LO[1]=count[32:64]
def R_jalr(rs,rd):
    binary = zero2word(lift_value(rs))
    Next=add(binary,four_extend)
    PC_dict[0]=unbinary2int(binary)-4
    Register_list[int(unbinary2int(rd))]=Next
def addi(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    result= add(imm,binary)
    Register_list[int(unbinary2int(rt))]=extend2word(result)
def addiu(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    result= add(imm,binary)
    Register_list[int(unbinary2int(rt))]=extend2word(result)
def andi(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    output = logicand(imm,binary)
    Register_list[int(unbinary2int(rt))]=output
#the imm number is extended with "0" only
def ori(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    count = len(imm)
    while count<32:
        imm="0"+imm
        count+=1
    output = logicor(imm,binary)
    Register_list[int(unbinary2int(rt))]=output
#the imm number is extended with "0" only
def xori(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    count = len(imm)
    while count<32:
        imm="0"+imm
        count+=1
    output= logicxor(imm,binary)
    Register_list[int(unbinary2int(rt))]=output
def slti(rs,rt,imm):
    binary1 = extend2word(lift_value(rs))
    imm = extend2word(imm)
    output = compare(binary1,imm)
    Register_list[int(unbinary2int(rt))]=output
def sltiu(rs,rt,imm):
    binary1 = extend2word(lift_value(rs))
    imm = extend2word(imm)
    output = unsigned_compare(binary1,imm)
    Register_list[int(unbinary2int(rt))]=output
def beq(rs,rt,imm):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    imm = imm+"00"
    imm =extend2word(imm)
    if binary1==binary2:
        address =zero2word(decimal2binary(PC_dict[0]))
        next = add(address,four_extend)
        final = add(next,imm)
        PC_dict[0] = unbinary2int(final)-4
def bne(rs,rt,imm):
    binary1 = extend2word(lift_value(rs))
    binary2 = extend2word(lift_value(rt))
    imm = imm+"00"
    imm =extend2word(imm)
    if binary1!=binary2:
        address =zero2word(decimal2binary(PC_dict[0]))
        next = add(address,four_extend)
        final = add(next,imm)
        PC_dict[0] = unbinary2int(final)-4
#positive or zero
def bgez(rs,imm):
    binary = extend2word(lift_value(rs))
    signal = compare(zero_extend,binary)
    imm = imm+"00"
    imm =extend2word(imm)
    if (signal == one_extend) or (binary==zero_extend):
        address =zero2word(decimal2binary(PC_dict[0]))
        next = add(address,four_extend)
        final = add(next,imm)[1]
        PC_dict[0] = unbinary2int(final)-4
#positive
def bgtz(rs,imm):
    binary = extend2word(lift_value(rs))
    signal = compare(zero_extend,binary)
    imm = imm+"00"
    imm =extend2word(imm)
    if (signal == one_extend):
        address =zero2word(decimal2binary(PC_dict[0]))
        next = add(address,four_extend)
        final = add(next,imm)
        PC_dict[0] = unbinary2int(final)-4
#negative or zero
def blez(rs,imm):
    binary = extend2word(lift_value(rs))
    signal = compare(binary,zero_extend)
    imm = imm+"00"
    imm =extend2word(imm)
    if (signal == one_extend) or (binary==zero_extend):
        address =zero2word(decimal2binary(PC_dict[0]))
        next = add(address,four_extend)
        final = add(next,imm)
        PC_dict[0] = unbinary2int(final)-4
#negative
def bltz(rs,imm):
    binary = extend2word(lift_value(rs))
    signal = compare(binary,zero_extend)
    imm = imm+"00"
    imm =extend2word(imm)
    if (signal == one_extend):
        address =zero2word(decimal2binary(PC_dict[0]))
        next = add(address,four_extend)
        final = add(next,imm)
        PC_dict[0] =unbinary2int(final)-4
#for store and load operation, the program uses big endian
def lb(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))-start_address
    if isinstance(Memory[address],str) and (len(Memory[address])==1):
        char = Memory[address]
        unicode = ord(char)
        result = zero2word(decimal2binary(unicode))
        Register_list[int(unbinary2int(rt))]=result
    else:
        output = extend2word(Memory[address])#the output should be 8 bits
        Register_list[int(unbinary2int(rt))]=output
def lbu(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))-start_address
    output = load(Memory[address])#the output should be 8 bits
    count = len(output)
    while count<32:
        output="0"+output
        count+=1
    Register_list[int(unbinary2int(rt))]=output
def lh(rs,rt,imm):#take half word
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))-start_address
    output = load(Memory[address])+load(Memory[address+1])#the output should be 16 bits
    count = len(output)
    while count<32:
        output=output[0]+output
        count+=1
    Register_list[int(unbinary2int(rt))]=output
#difference between lh:extend with "0"
def lhu(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))-start_address
    output = load(Memory[address])+load(Memory[address+1])#the output should be 16 bits
    count = len(output)
    while count<32:
        output="0"+output
        count+=1
    Register_list[int(unbinary2int(rt))]=output
#load word
def lw(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))-start_address
    output = load(Memory[address])+load(Memory[address+1])
    output+=load(Memory[address+2])+load(Memory[address+3])
    Register_list[int(unbinary2int(rt))]=output
#save one byte    
def sb(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    savevalue = extend2word(lift_value(rt))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))-start_address
    Memory[address]=savevalue[24:]
#store half word; big endian
def sh(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    savevalue = extend2word(lift_value(rt))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))-start_address
    Memory[address]=savevalue[16:24]
    Memory[address+1]=savevalue[24:32]
def sw(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    savevalue = extend2word(lift_value(rt))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))-start_address
    for i in range(4):
        Memory[address+i]=savevalue[i*8:i*8+8]
def lwl(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))
    mount = 4-address%4
    output = ""
    for i in range(mount):
        output+=Memory[address+i]
    right = extend2word(lift_value(rt))[8*mount:]
    Register_list[int(unbinary2int(rt))]=output+right
def lwr(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))
    mount = address%4+1
    output = ""
    for i in range(mount):
        output+=Memory[address-mount+i+1]
    left = extend2word(lift_value(rt))[:8*(4-mount)]
    Register_list[int(unbinary2int(rt))]=left+output
def swl(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    savevalue = extend2word(lift_value(rt))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))
    mount = 4-address%4
    for i in range(mount):
        Memory[address+i]=savevalue[:mount*8]
def swr(rs,rt,imm):
    binary = extend2word(lift_value(rs))
    savevalue = extend2word(lift_value(rt))
    imm = extend2word(imm)
    address = unbinary2int(add(binary,imm))
    mount = address%4+1
    for i in range(mount):
        Memory[address-mount+i+1]=savevalue[(4-mount+i)*8:(4-mount+i+1)]
def lui(rt,imm):
    imm = extend2word(imm)
    output = imm[16:32]+zero_extend[16:32]
    Register_list[int(unbinary2int(rt))]=output
def j(label):
    current = zero2word(decimal2binary(PC_dict[0]))
    target = current[0:4]+label+"00"
    dec_target = unbinary2int(target)
    PC_dict[0]=dec_target-4
def jal(label):
    next = PC_dict[0]+4
    output= decimal2binary(PC_dict[0])
    current = zero2word(output)
    target = current[0:4]+label+"00"
    dec_target = unbinary2int(target)
    PC_dict[0]=dec_target-4
    Register_list[31]=zero2word(decimal2binary(next))
#del with the input operation
with open(test_in,"r") as data:
    data = data.readlines()
    for i in range(len(data)):
        data[i]=data[i].replace("\n","")#the input information stored in the data list
def syscall(i):#i means the (i+1)th line of the .in  file will be the input
    global dynamic_end
    v0 = unbinary2int(lift_value("00010"))
    #a0 stores the int value
    if v0==1:
        a0 = binary2int(lift_value("00100"))
        with open(test_out,"a") as output_file:
            output_file.write(str(a0))
    #for print_string, a0 stores the address
    elif v0==4:
        a0 =lift_value("00100")
        address = unbinary2int(a0)
        i=address-start_address
        output = ""
        while(Memory[i]!="\x00"):
            output=output+Memory[i]
            i+=1
        output=output+"\0"
        with open(test_out,"a") as output_file:
            output_file.write(output)
    #read in data   
    elif v0==5: 
        readinteger = data[i]
        a0 = int(readinteger)
        if a0>=0:
            a0_code=zero2word(decimal2binary(a0))
        else:
            a0_code=zero2word(decimal2binary(-a0))
            a0_code=twocomp(a0_code)
        Register_list[int(unbinary2int("00010"))]=a0_code
    #a0 stores address of the string; 
    #a1 stores the number of characters +1
    elif v0==8:
        string = data[i]
        a0 = unbinary2int(lift_value("00100"))
        a1 = unbinary2int(lift_value("00101"))
        address=a0-start_address
        try:
            for i in range(a1-1):
                Memory[address+i]=string[i]
            Memory[address+a1-1]="\0"
        except:
            for i in range(len(string)):
                Memory[address+i]=string[i]
            Memory[address+len(string)]="\0"
    #a0 stores the number of bytes of storage desired
    #
    elif v0==9:
        a0 = binary2int(lift_value("00100"))
        output = dynamic_end+a0
        v0_code = zero2word(decimal2binary(output))
        Register_list[int(unbinary2int("00010"))]=v0_code
    #exit
    elif v0==10:
        sys.exit()
    elif v0==11:
        a0 = unbinary2int(lift_value("00100"))
        char = chr(a0)
        with open(test_out,"a") as output_file:
            output_file.write(char)
    elif v0==12:
        while True:
            char=data[i]
            if len(char)==1:
                break
        num=ord(char)
        Register_list[int(unbinary2int("00010"))]=zero2word(decimal2binary(num))
    elif v0==13:
        a0 = unbinary2int(lift_value("00100"))
        address=a0-start_address
        output = ""
        while(Memory[address]!="\x00"):
            output=output+Memory[address]
            address+=1
        # output=output+"\0"
        a2 = unbinary2int(lift_value("00110"))
        file_discriptor = os.open(output,flags=os.O_RDWR|os.O_CREAT,mode=a2)
        file_discriptor = zero2word(decimal2binary(file_discriptor))
        Register_list[int(unbinary2int("00010"))]=file_discriptor
    elif v0==14:
        a0 = unbinary2int(lift_value("00100"))#file discriptor
        a1 = unbinary2int(lift_value("00101"))#address
        a2 = unbinary2int(lift_value("00110"))
        content = os.read(a0,a2)
        content=content.decode()
        address=a1-start_address
        i=0
        for char in content:
            Memory[address+i]=char
            i+=1
        code=decimal2binary(len(content))
        Register_list[int(unbinary2int("00100"))]=zero2word(code)
    elif v0==15:
        a0 = unbinary2int(lift_value("00100"))#file discriptor
        a1 = unbinary2int(lift_value("00101"))#address
        a2 = unbinary2int(lift_value("00110"))
        output=""
        address = a1-start_address
        while Memory[address]!=0:
            if len(output)<=a2:
                output = output +Memory[address] 
                address+=1
            else:
                break
        os.write(a0,output.encode())
        code=decimal2binary(len(output))
        Register_list[int(unbinary2int("00100"))]=zero2word(code)
    elif v0==16:
        a0 = unbinary2int(lift_value("00100"))#file discriptor
        os.close(a0)
    elif v0==17:
        a0 = unbinary2int(lift_value("00100"))
        sys.exit(a0)
    return v0
#the opcods for r type instructions are all 000000
#a dictionary for r instructions(without shift) and their funct
R_noshift_funct_dic={"100000":R_add,"100001":R_addu,"100010":R_sub,
"100011":R_subu,"100100":R_and,"100101":R_or,"100110":R_xor,
"100111":R_nor,"101010":R_slt,"101011":R_sltu,"000100":R_sllv,"000110":R_srlv,"000111":R_srav}
# dictionary for shifting instructions which needs shamt
R_shift_funct_dic_s={"000000":R_sll,"000010":R_srl,"000011":R_sra}
# for jump to instructions
R_jumpto_funct_dic={"001000":R_jr,"010001":R_mthi,"010011":R_mtlo}
# for jump from instructions
R_jumpfr_funct_dic={"010000":R_mfhi,"010010":R_mflo}
#for signed or unsigned mult instructions
R_mult_funct_dic = {"011010":R_div,"011011":R_divu,"011000":R_mult,
"011001":R_multu}
#jalr(rd,rs)
jalr = {"001001":R_jalr}
#dictionaries for i instructions 
#i instructions whose input format is rs,rt,imm
i_opcode_dic_nb={ "001000":addi,"001001":addiu,
"001100":andi,"001101":ori,"001110":xori,"001010":slti,
"001011":sltiu,"100000":lb,"100100":lbu,"100001":lh,"100101":lhu,
"100011":lw,"101000":sb,"101001":sh,"101011":sw,"100010":lwl,
"100110":lwr,"101010":swl,"101110":swr,"000100":beq,"000101":bne}
#i instructions with branch(also rt value a constant)
i_opcode_dic_cons_b={"000001":bgez,"000111":bgtz,
"000110":blez,"000001":bltz}
#lui
lui_dic={"001111":lui}
#j form
j_opcode_dic={"000010":j,"000011":jal}
#mips instruction formats
#r type
#op(6 bits)|rs(5 bits)|rt(5 bits)|rd(5 bits)|shamt(5 bits)|funct(6 bits)
#i type
#op(6 bits)|rs(5 bits)|rt(5 bits)|immediate number (16 bits)
#j type
#op(6 bits)|jump target(16 bits)
#output the dump file for the program
with open(checkpoint_txt) as checkpoint:
    check = checkpoint.readlines()
    for i in range(len(check)):
        check[i]=check[i].replace("\n","")#list check points
def write_bin(fd,value,order,len):
    bin_data = int(value).to_bytes(length=len,byteorder=order,signed=True)
    fd.write(bin_data)
def dump(x):
    memory_file = open(f'memory_{x}.bin',"wb")
    reg_file = open(f'register_{x}.bin',"wb")
    for value in Register_list:
        value = unbinary2int(value)
        write_bin(reg_file,value,"little",4)
    write_bin(reg_file,PC_dict[0],"little",4)
    write_bin(reg_file,Hi_LO[0],"little",4)
    write_bin(reg_file,Hi_LO[0],"little",4)
    for value in Memory:
        if isinstance(value,int):
            # print(value)
            write_bin(memory_file,value,"little",1)
        elif len(value)==8:
            value = binary2int(value)
            write_bin(memory_file,value,"little",1)
        else:
            value = ord(value)
            write_bin(memory_file,value,"big",1)
#start fetching the instructions
count=0
readinorder = 0
while True:
    if str(count) in check:
        dump(count)
    line=""
    start=PC_dict[0]-4194304
    # for i in range(4):
    #     line=line+Memory[start+i]
    line = Memory[start+3]+Memory[start+2]+Memory[start+1]+Memory[start]
    # print(line)
    if line=="":
        break
    elif line=="00000000000000000000000000001100":
        v0=syscall(readinorder)
        if (v0==5 or v0==8 or v0==12):
            readinorder+=1

    elif line[0:6]=="000000":
        rs = line[6:11]
        rt = line[11:16]
        rd = line[16:21]
        shamt = line[21:26]
        funct = line[26:]
        if funct in R_noshift_funct_dic.keys():
            R_noshift_funct_dic[funct](rs,rt,rd)
        elif funct in R_shift_funct_dic_s.keys():
            R_shift_funct_dic_s[funct](rt,rd,shamt)
        elif funct in R_jumpto_funct_dic.keys():
            R_jumpto_funct_dic[funct](rs)
        elif funct in R_jumpfr_funct_dic.keys():
            R_jumpfr_funct_dic[funct](rd)
        elif funct in R_mult_funct_dic.keys():
            R_mult_funct_dic[funct](rs,rt)
        elif funct in jalr.keys():
            jalr[funct](rs,rd)
    elif (line[0:6]=="000010" )or (line[0:6]=="000011"):
        imm=line[6:32]
        j_opcode_dic[line[0:6]](imm)
    else:
        op = line[0:6]
        rs=line[6:11]
        rt=line[11:16]
        imm =line[16:32]
        if op in i_opcode_dic_nb.keys():
            i_opcode_dic_nb[op](rs,rt,imm)
        elif op in i_opcode_dic_cons_b.keys():
            i_opcode_dic_cons_b[op](rs,imm)
        elif op =="001111":
            lui_dic[op](rt,imm)
    PC_dict[0]=PC_dict[0]+4
    count=count+1
    # print(Register_list)
    # print(PC_dict[0])


    

