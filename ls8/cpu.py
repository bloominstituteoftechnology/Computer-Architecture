"""CPU functionality."""

import sys

SP = 7

LDI =  0b10000010
PRN =  0b01000111
HLT =  0b00000001
MUL =  0b10100010
PUSH = 0b01000101
POP =  0b01000110
CALL = 0b01010000
RET =  0b00010001
ADD =  0b10100000

class CPU:
    """Main CPU class."""
    
    
    def __init__(self):
        """Construct a new CPU."""
        # creationg of the register
        self.codes = {}
        self.reg = [0] * 8 # the register is 8 bits long
        self.ram = [0] * 256 # this the memory or the ram
        self.pc = 0 # this the program counter
        # putting in the opcodes
        self.build_codes_dict()
        # initializing the register 7 to the address 0xf4 in ram
        self.reg[7] = 0xf4
        # address for the end of the program -- will let us know if we can do a push
        self.end_program_addr = None


    # Function to add the values of two different registers
    def op_ADD(self):
        
        # send the next two values in the registers to the alu
        reg1 = self.ram[self.pc + 1]
        reg2 = self.ram[self.pc + 2]
        self.alu("ADD", reg1, reg2)


    # This function will move the pc counter to the address that is 
    # found in the register after the opCode.  Will push the current pc point + 1 on the stack
    def op_CALL(self):
        
        where_to_return_to = self.pc + self.instruction_size(CALL)
        reg_num = self.ram[self.pc + 1]
        self.pc = self.reg[reg_num]
        self.op_PUSH(where_to_return_to) 


    # This function will return from the subroutine and will pop off the stack 
    # where to set the pc counter to
    def op_RET(self):
        # Return from subroutine.
        # Pop the value from the top of the stack and store it in the `PC`.
        # using my own version of the POP so that it doesn't try to set to just any 
        # register
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] +=1


    # This means HALT -- will stop the program from running
    def op_HLT(self):
        sys.exit()

    # POP -- used to pop off of the stack
    def op_POP(self):
        # 1. Copy the value from the address pointed to by `SP` to the given register.
        # 2. Increment `SP`.
        if self.reg[SP] == 0xf4:
            raise("Unable to pop becuase the stack is empty")
        self.reg[self.ram[self.pc+1]] = self.ram[self.reg[SP]]
        self.reg[SP] += 1


    # PUSH -- push on to the stack
    def op_PUSH(self, val=None):
        #1. Decrement the `SP`.
        #2. Copy the value in the given register to the address pointed to by  `SP`.

        # This means that we will use the value in the next register to put on the stack
        # using val so that we can put in our own value or just use pc + 1 to get the value
        if val == None:
            register_num = self.ram[self.pc + 1 ]
            val =  self.reg[register_num]
        #decrementing the register 7
        if self.reg[SP] - 1 == self.end_program_addr:
            raise ("Stack overflow:  unable to do this as this will overwrite the program")
        self.reg[SP] -= 1
        # using the address in the stack pointer to point to the location in ram (top of the stack)
        # where we will put the value that was in the register
        self.ram[self.reg[SP]]  = val
        
  

    # PRN --- print register number.
    def op_PRN(self):
        print(self.reg[self.ram_read(self.pc+1)])


    # LDI -- setting the value of the a register to an integer
    def op_LDI(self):
        self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]

    def op_MUL(self):
        # get the value from the first register
        #fval = self.reg[self.ram[self.pc + 1]]
        sVal = self.reg[self.ram[self.pc + 2]]
        # will set the reg where the second val was
        # to the the same as firstVal
        self.reg[self.ram[self.pc + 2]] = self.reg[self.ram[self.pc + 1]]
        # calling the alu for addition and will do it 
        # for the number of sval and then will put the 
        # amounts into the register of the fval -- self.pc + 1
        # def alu(self, op, reg_a, reg_b):
        #if op == "ADD":
            #self.reg[reg_a] += self.reg[reg_b]
        # this amount for the range is because 
        # any number times 1 is itself
        if sVal > 1:
            for _ in range(1, sVal): 
                
                self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2])
        if sVal == 0:
            # setting the register
            self.reg[self.ram[self.pc + 1]] = 0
         
        

    def build_codes_dict(self):
        """
        This is the function that will build 
        the dictionary that contains the opcodes 
        as the key and the value is the function that the opcode will need 
        to call
        """
        self.codes[HLT] = self.op_HLT
        self.codes[PRN] = self.op_PRN
        self.codes[LDI] = self.op_LDI
        self.codes[MUL] = self.op_MUL
        self.codes[PUSH] = self.op_PUSH
        self.codes[POP] = self.op_POP
        self.codes[RET] = self.op_RET
        self.codes[CALL] = self.op_CALL
        self.codes[ADD] = self.op_ADD

    def run(self):
        """Run the CPU."""

        # here is where we will store the 
        # name with the number of each action
        # to perform
        
        

        running = True

        
        # Loop for the program to run
        while running:
            
            ir = self.ram_read(self.pc)
            # calling the function 
            self.codes[ir]()
            
            # This is to check if the function itself will move the PC if if does
            # then this is skipped
            
            if self.sets_PC(ir) == False:
                # This line is to increment the pc counter
                self.pc += self.instruction_size(ir)

    def load(self):
        """Load a program into memory."""

        #address = 0

        # For now, we've just hardcoded a program:
        if len(sys.argv) != 2:
            print("You need to specify what program you want the LS8 to run")
            print("Such as, ls8.py \"name of file to run on\" ")
            exit(2)
        file_to_open = sys.argv[1]
        self.read_file_to_mem(file_to_open)


        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def read_file_to_mem(self, fileName):
        """
        This will read the file into memory so that we can then run the code.
        This program will remove all the comments and will put the binary into the memory.
        """
        memCount = 0
        
        with open(fileName, mode="r") as program:
            # looping through each line of the program
            for line in program:
                binaryNum = ""
                # will put each binary into the memory 
                # will then increment the binary.
                # ignore any comments
                for char in line:
                    # This will make it to skip all the rest after a comment
                    if char == "#":
                        break
                    elif char == "\n":
                        continue
                    if char.isdigit():
                        binaryNum += char
                # checking to see if binaryNum is empty or not 
                # if empty will not put it into memory
                if binaryNum:
                    try:
                        # add to the memory and increment the memCounter
                        self.ram[memCount] = int(binaryNum, base=2)
                        memCount +=1
                    except:
                        print(f"Improper number:  a number was not in binary form.  {binaryNum} is not proper code")
                        sys.exit(1)
                # storing the end of the program to not allow stack overflow        
                self.end_program_addr = memCount


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


    def ram_read(self, mem_add_reg):
        return self.ram[mem_add_reg]


    def ram_write(self, mem_dat_reg, mem_add_reg):
        self.ram[mem_add_reg] = mem_dat_reg

    
    def bitwise_opp(self, value, maskFirst=True, mask=None, maskType=1,  bitShiftVal=None, bitShiftDir="r", useNot=False):
        """
        Value starts with holding the opcode and then will at the end hold the value asked for.
        This function can be used to get the values or info from 
        a byte. A mask can be passed in, the the mask parameter and the type of mask
        in the maskType.  The mask type can be 1 for ANDING, 2 for ORing and 3 for XORing.
        After the mask has been applied, a bitwise shift can then also be applied which is 
        applied after the mask.  The value of this is then returned.

        If only a bitwise shift is wanted then can put maskFirst as False and don't pass a mask, 
        and put in a bitshift value. Default is to shift to the right

        Before returning will check to see if the useNot is True.  If it is then will use this and then return the value
        """
        
        working = True
        firstDone = False

        while working:

            if maskFirst or firstDone:
                if mask != None:
                    
                    # applying the mask
                    # XOR --- to toggle the bits on or off
                    if maskType == 3:
                        value = value ^ mask
                    # ORing  -- to set some of the values to 1 or to 
                    # make sure some of the bits are turned on.
                    elif maskType == 2:
                        value = value | mask
                    # ANDing  -- to extract some of the bits out of the 
                    # byte 
                    elif maskType == 1:
                        value = value & mask
                    else:
                        raise Exception("Wrong value for mask type used")
                if firstDone == False:
                    # saying that the first is done
                    firstDone = True
                else:
                    if useNot:
                        return ~(value)
                    
                    return value

            # now doing the bitwise operation
            if not maskFirst or firstDone:
                if bitShiftVal != None:
                    if bitShiftDir == "r":
                        value = value >>  bitShiftVal
                    else:
                        value = value << bitShiftVal
                if not firstDone:
                    firstDone = True
                else:
                    if useNot:
                        return ~(value)

                    return value



    def get_num_operands(self, opcode):
        return self.bitwise_opp(opcode, maskFirst=False,  mask=None, bitShiftVal=6)


    def get_instruction_code(self, opcode):
        return self.bitwise_opp(opcode, mask=0b00001111)


    def used_by_ALU(self, opcode):
        """
        This will return the boolean if this opcode will be used by the 
        ALU or not. True == Yes, False == No
        """
        return 0b00100000 == self.bitwise_opp(opcode, mask=0b00100000)    


    def sets_PC(self, opcode):
        """
        Will return True if the opcode is used to set the program counter, and
        False otherwise
        """
        
        return 0b00010000 == self.bitwise_opp(opcode, mask=0b00010000)


    def instruction_size(self, opcode):
        """
        This funtion will tell how much to increment the 
        PC counter after an instruction.
        """
        return self.get_num_operands(opcode) + 1


    


