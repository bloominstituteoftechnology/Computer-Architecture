"""CPU functionality."""

import sys


LDI = 0b10000010
PRN =  0b01000111
HLT = 0b00000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # creationg of the register
        self.reg = [0] * 8 # the register is 8 bits long
        self.ram = [0] * 256 # this the memory or the ram
        self.pc = 0 # this the program counter

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
                        value = value & maskType
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


    def run(self):
        """Run the CPU."""

        # here is where we will store the 
        # name with the number of each action
        # to perform
        
        

        running = True
        
        # Loop for the program to run
        while running:

            ir = self.ram_read(self.pc)
           

            # This means HALT -- will stop the program from running
            if ir == HLT:
                break

            # LDI -- setting the value of the a register to an integer
            elif ir == LDI:
                # will increment the PC (program counter by 3) 
                # because has 2 parameters
                self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
                #self.pc +=3

            # PRN --- print register number.
            # will print what is found int he register number passed in
            elif ir == PRN:
                print(self.reg[self.ram_read(self.pc+1)])
                #self.pc +=2

            # This line is to increment the pc counter
            self.pc += self.instruction_size(ir)



