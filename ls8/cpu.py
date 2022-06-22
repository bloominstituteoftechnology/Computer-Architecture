 # Inventory what is here ^
 # Implement the CPU constructor ^
 # Add RAM functions ram_read() and ram_write()
 # Implement the core of run()
 # Implement the HLT instruction handler
 # Add the LDI instruction
 # Add the PRN instruction
 #
"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0    # program counter: address of the currently executing instruction
        self.ir = 0     # flags
        self.sp = 7     # represents the 8th register
        self.Flags = [0]*8

    def load(self):
        """Load a program into memory."""
        try:
            address = 0
            # sys.argv[0] is the name of the running program itself
            filename = sys.argv[1]
            with open(filename) as f:
                for line in f:
                    # ignore comments
                    comment_split = line.split('#')
                    # strip out whitespace
                    num = comment_split[0].strip()
                    # ignore blank lines
                    if num == "":
                        continue
                    # convert the binary string to integers.
                    # built-in integer function dose it for us.
                    value = int(num,2)

                    self.ram[address] = value
                    address+=1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)
        #
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        if op == "AND":
            if reg_a == 1 and reg_b == 1:
                return True
            else:
                return False
        if op =="OR":
            if reg_a == 1 and reg_b ==0:
                return True
            elif reg_a == 0 and reg_b == 1:
                return True
            elif reg_a == 1 and reg_b == 1:
                return True
            else:
                return False
        if op =="XOR":
            if reg_a==1 and reg_b ==0:
                return True
            if reg_a==0 and reg_b ==1:
                return True
            else:
                return False

        if op =="NOR":
            if reg_a==0 and reg_b==0:
                return True
            else:
                return False 

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

    def ram_read(self, MAR):
        """Accepts the address to read and return the value stored there"""
        return self.ram[MAR]
        # MAR contains the address that is being read or written to.
        # MDR contains the data that was read

    def ram_write(self, MAR, MDR):
        """Should accept a value to write and the address to write it to"""
        self.ram[MAR]=MDR
        # so we will move the stuff from MAR TO MDR


    def run(self):
        """Run the CPU."""

        Running=True

        LDI=0b10000010
        HLT=0b00000001
        PRN=0b01000111
        MUL=0b10100010
        PUSH=0b01000101
        POP=0b01000110
        CALL=0b01010000
        RET=0b00010001
        ADD=0b10100000
        CMP=0b10100111
        JMP=0b01010100
        JEQ=0b01010101
        JNE=0b01010110
        L= 0
        E= 0
        G= 0


        while Running:
            # read the memory address sotred in pc and store it in Instruction Register
            Command=self.ram_read(self.pc)
            # print(self.reg)
            #print("------")
            # load immediate, store avalue in a register
            if Command == LDI:
                # self.trace()
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)
                self.reg[operand_a]=operand_b   # sets a specific register to a specified value
                self.pc+=3
                # print(operand_a)
            elif Command==HLT:
                Running=False
                self.pc+=1
            # halt the CPU and exit the emulator
            elif Command==PRN:
                # PRN: adding
                reg = self.ram[self.pc+1]
                #print(num)
                # print(self.reg[reg])  # prints 8 to the console.
                print(self.reg[reg])
                self.pc+=2
            # prints the numeric
            elif Command==MUL:
                register_a = self.ram_read(self.pc+1)
                register_b = self.ram_read(self.pc+2)
                # now save the multiplication of these two in register_a
                self.reg[register_a] = self.reg[register_a]*self.reg[register_b]
                #print(self.reg[register_a])
                self.pc+=3

            # elif Command == SAVE:
            #     num = self.ram[self.pc+1]
            #     reg = self.ram[self.pc+2]
            #     self.reg[reg] = num
            #     self.pc+=3

            # elif Command == ADD:
            #     register_a = self.ram[self.pc+1]
            #     register_b = self.ram[self.pc+2]
            #     self.reg[register_a] += self.reg[register_b]
            #     self.pc += 3

            elif Command == PUSH:
                # a number from 0 to 7
                #self.trace()
                reg = self.ram[self.pc+1]
                # look in the identified register and find the value
                val = self.reg[reg]
                # decriment the value i.e. memory address by 1
                self.reg[self.sp] -=1
                # copy the value from the register into the memory
                self.ram[self.reg[self.sp]] = val
                self.pc += 2 # because we had one argument

            elif Command == POP:
                reg = self.ram[self.pc+1]     # memory of the register holding our SP
                val = self.ram[self.reg[self.sp]]    # register number 7
                self.reg[reg] = val    # copy that value into register that we are pointing at
                self.reg[self.sp] += 1    # incrememnt the stock pointer:
                # print(val)
                self.pc += 2

            elif Command == CALL:
                val = self.pc+2
                reg = self.ram[self.pc+1]
                sub_address = self.reg[reg]
                # decriment the stack pointer
                self.reg[self.sp]-=1
                self.ram[self.reg[self.sp]]=val
                # update the address
                self.pc=sub_address
            elif Command == ADD:
                self.alu("ADD", self.ram_read(self.pc+1), self.ram_read(self.pc+2))
                self.pc+=3

            elif Command == RET:
                return_add = self.reg[self.sp]
                self.pc = self.ram[return_add]
                # increment the sp
                self.reg[self.sp] +=1

                # get the values froms the ram and read it into register
                # registerA = self.reg[self.ram_read(self.pc+1)]
                # registerB = self.reg[self.ram_read(self.pc+2)]
                # if A is less than B, set L flag to 1
            elif Command==CMP:
                self.Flags = CMP
                if self.reg[self.ram_read(self.pc+1)] < self.reg[self.ram_read(self.pc+2)]:
                    L=1
                    G=0
                    E=0
                    self.Flags=CMP-0b00000100
                elif self.reg[self.ram_read(self.pc+1)] > self.reg[self.ram_read(self.pc+2)]:
                    G=1
                    L=0
                    E=0
                    self.Flags=CMP-0b00000010
                elif self.reg[self.ram_read(self.pc+1)] ==self.reg[self.ram_read(self.pc+2)]:
                    E=1
                    L=0
                    G=0
                    self.Flags=CMP-0b00000001
                self.pc+=3
#                self.trace()
                # takes in the register
                # jumps to the address stored in the given register
                # set the PC to the address stored in the given register.
            elif Command==JMP:
                self.pc = self.reg[self.ram_read(self.pc+1)]

            elif Command==JEQ:
                if E==1:
                    self.pc = self.reg[self.ram_read(self.pc+1)]
                else:
                    self.pc+=2

            elif Command==JNE:
                if E==0:
                    self.pc = self.reg[self.ram_read(self.pc+1)]
                else:
                    self.pc+=2

            # else:
            #     print(f"Unknown Instruction: {Command}")
            #     sys.exit(1)
