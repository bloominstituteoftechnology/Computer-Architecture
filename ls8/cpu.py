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
    #    self.fl = 0     # flags
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

# beautifuly the run function:

    # def run(self):
    #     ir = HLT
    #     self.branchtable[ir]
    #
    #     ir = LDI
    #     self.branchtable[ir]
    def run(self):
        """Run the CPU."""

        Running=True

        LDI=0b10000010
        HLT=0b00000001
        PRN=0b01000111
        MUL=0b10100010
        ADD=0b10100000
        PUSH=0b01000101
        POP=0b01000110
        CALL=0b01010000
        RET=0b00010001
        ADD=0b10100000
        while Running:
            # read the memory address sotred in pc and store it in Instruction Register
            Command=self.ram_read(self.pc)
            # print(self.reg)
            #print("------")
            # load immediate, store avalue in a register
            if Command == LDI:
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)
                # registers
                # sets a specific register to a specified value
                self.reg[operand_a]=operand_b
                #print("LDI", self.reg)
                self.pc+=3
                # print(operand_a)

            # halt the CPU and exit the emulator
            elif Command==PRN:
                # PRN: adding
                reg = self.ram[self.pc+1]
                # print(self.reg[reg])  # prints 8 to the console.
                self.pc+=2
            elif Command==HLT:
                Running=False
                self.pc+=1

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

            # System stack ..
            elif Command==PUSH:
                #print("PUSH")
                reg=self.ram[self.pc+1]
                #print(reg)
                val=self.reg[reg]
                self.sp-=1
                self.ram[self.reg[self.sp]]= val
                self.pc+=2

            elif Command==POP:
                #print("POP")
                reg=self.ram[self.pc+1]
                #print(reg)
                val=self.ram[self.reg[self.sp]]
                self.reg[reg]=val
                self.reg[self.sp] += 1
                self.pc+=2
                print(val)

            # elif Command == PUSH:
            #     # look at the opcode argument
            #     # a number from 0 to 7
            #     reg = self.ram[self.pc+1]
            #     # look in the identified register and find the value
            #     val = self.reg[reg]
            #     # self.reg[self.sp]
            #     # decriment the value i.e. memory address by 1
            #     self.sp -=1
            #     # copy the value from the register into the memory
            #     self.ram[self.reg[self.sp]] = val
            #     self.pc += 2 # because we had one argument
            #
            # elif Command == POP:
            #     # pop works the same way but in reverse
            #     # look at the memory
            #     #print("POP")
            #     reg = self.ram[self.pc+1]
            #     # memory of the register holding our SP
            #     val = self.ram[self.reg[self.sp]]    # register number 7
            #     #print(val)
            #     # copy that value into register that we are pointing at
            #     self.reg[reg] = val
            #
            #     # incrememnt the stock pointer:
            #     self.reg[self.sp] += 1
            #     # print(val)
            #     self.pc += 2
            #     print(self.reg[reg])
                #print(val)

            # elif Command == CALL:
            #     # the address of the instruction directly after CALL is pushed into the stack.
            #     # decrement the stack pointer
            #     # self.reg[self.sp] -=1 # storing address on the stack.
            #     # # memory from register is self.pc +2 because we are at the pointer
            #     # # we need to move the counter to 0 and then to HALT
            #     # self.ram[self.rag[self.sp]] = self.pc+2
            #     # # the PC is set to the address
            #     # reg = self.ram[self.pc+1]
            #     # self.pc = self.ram[reg]
            #     # this allows us to return to where we left off when the subroutine finishes executing
            #     # The PC is set to the address stored in the given register.
            #     # We jump to that location in ram and execute the first instruction in the subroutine.
            #     # the PC can move forward and abckwards from its current location.
            #     val = self.pc+2
            #     reg = self.ram[self.pc+1]
            #     sub_address = self.reg[reg]
            #     # decriment the stack pointer
            #     self.reg[self.sp]-=1
            #     self.ram[self.reg[self.pc]]=val
                # # update the address
                # self.pc=sub_address
            # elif Command == ADD:
            #     self.alu("ADD", self.ram_read(self.pc+1), self.ram_read(self.pc+2))
            #     self.pc+=3
            #
            # elif Command == RET:
            #     return_add = self.reg[self.sp]
            #     self.pc = self.ram[return_add]
            #     # increment the sp
            #     self.reg[self.sp] +=1


        else:
            print(f"Unknown Instruction: {Command}")
            sys.exit(1)
