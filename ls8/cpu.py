"""
## CPU functionality ##

Day 1: Get print8.ls8 running
 Inventory what is here
 Implement the CPU constructor
 Add RAM functions ram_read() and ram_write()
 Implement the core of run()
 Implement the HLT instruction handler
 Add the LDI instruction
 Add the PRN instruction

Day 2: Add the ability to load files dynamically, get mult.ls8 running
 Un-hardcode the machine code
 Implement the load() function to load an .ls8 file given the filename passed in as an argument
 Implement a Multiply instruction (run mult.ls8)

Day 3: Stack
 Implement the System Stack and be able to run the stack.ls8 program

Day 4: Get call.ls8 running
 Implement the CALL and RET instructions
 Implement Subroutine Calls and be able to run the call.ls8 program
"""

import sys

# Instruction Memory Address
LDI = 0b10000010 # load immediate
PRN = 0b01000111 # print value of integer saved to register address
HLT = 0b00000001 # halt program
MUL = 0b10100010 # multiplication
PUSH = 0b01000101 # 69
POP = 0b01000110 # 70
CALL = 0b01010000 # 80
RET = 0b00010001 # 17 - return
ADD = 0b10100000 # 160

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0]*256
        self.register = [0]*8
        self.pc = 0 # program counter
        self.register[7] = 0b11110100 # 244
        self.run_logic = True

    # # Day 1 Code
    ################################################################
    # def load(self):
    #     """Load a program into memory."""

    #     address = 0

    #     # For now, we've just hardcoded a program:

    #     program = [
    #         # From print8.ls8
    #         0b10000010, # LDI R0,8
    #         0b00000000,
    #         0b00001000,
    #         0b01000111, # PRN R0
    #         0b00000000,
    #         0b00000001, # HLT
    #     ]

    #     for instruction in program:
    #         self.memory[address] = instruction
    #         address += 1
    # def alu(self, op, register_a, register_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.register[register_a] += self.register[register_b]
    #     #elif op == "SUB": etc
    #     else:
    #         raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         #self.fl,
    #         #self.ie,
    #         self.memory_read(self.pc),
    #         self.memory_read(self.pc + 1),
    #         self.memory_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.register[i], end='')

    #     print()

    # def memory_read(self, MAR):
    #     return self.memory[MAR]

    # def memory_write(self, MDR, MAR):
    #     self.memory[MAR] = MDR
    #     return

    # def run(self):
    #     """Run the CPU."""
    #     logic = True

    #     LDI = 0b10000010
    #     PRN = 0b01000111
    #     HLT = 0b00000001

    #     while logic:
    #         IR = self.memory_read(self.pc)
    #         operand_a = self.memory_read(self.pc + 1)
    #         operand_b = self.memory_read(self.pc + 2)
    #         if IR == LDI:
    #             self.register[operand_a] = operand_b
    #             self.pc += 3
    #         elif IR == PRN:
    #             print(self.register[operand_a])
    #             self.pc += 2
    #         elif IR == HLT:
    #             self.pc += 1
    #             break
    #         else:
    #             self.pc += 1
    #             print(f"{IR} - command is not available")
    #             sys.exit()
    #################################################################

    # Day 2 - Code
    ################################################################
    # def load(self):
    #     """Load a program into memory."""
    #     if len(sys.argv) != 2:
    #         print("Example Command: python ls8.py examples/mult.ls8")
    #         sys.exit(1)

    #     try:
    #         address = 0
    #         with open(sys.argv[1]) as f:
    #             for line in f:
    #                 # extract number from file
    #                 comment_split = line.split('#')
    #                 num = comment_split[0].strip()
    #                 print(f'{num} == {int(num, 2):4} (binary to decimal)')
    #                 # save number to memory if exists
    #                 if num != "":
    #                     value = int(num, 2)
    #                     self.memory_write(value, address)
    #                     address += 1

    #     except FileNotFoundError:
    #         print(f"{sys.argv[0]}: {sys.argv[1]} not found")
    #         sys.exit(2)

    # def alu(self, op, register_a, register_b):
    #     """
    #     ALU operations. (arithmetic/logic unit)
    #     """

    #     if op == "ADD":
    #         self.register[register_a] += self.register[register_b]
    #     elif op == "MUL":
    #         self.register[register_a] *= self.register[register_b]
    #     #elif op == "SUB": etc
    #     else:
    #         raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         #self.fl,
    #         #self.ie,
    #         self.memory_read(self.pc),
    #         self.memory_read(self.pc + 1),
    #         self.memory_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.register[i], end='')

    #     print()

    # def memory_read(self, MAR):
    #     return self.memory[MAR]

    # def memory_write(self, MDR, MAR):
    #     self.memory[MAR] = MDR
    #     return

    # def run(self):

    #     logic = True

    #     # ASM instruction
    #     LDI = 0b10000010 # load immediate
    #     PRN = 0b01000111 # print value of integer saved to register address
    #     HLT = 0b00000001 # halt program
    #     MUL = 0b10100010 # multiplication

    #     while logic:
    #         # read in instruction
    #         IR = self.memory_read(self.pc)
    #         # read in integer
    #         operand_a = self.memory_read(self.pc + 1)
    #         operand_b = self.memory_read(self.pc + 2)

    #         if IR == LDI:
    #             self.register[operand_a] = operand_b
    #             self.pc += 3 # increments instruction index to next instruction line
    #         elif IR == PRN:
    #             print(self.register[operand_a])
    #             self.pc += 2
    #         elif IR == MUL:
    #             # call alu to perform multiplication
    #             self.alu("MUL", operand_a, operand_b)
    #             self.pc += 3
    #         elif IR == HLT:
    #             # self.pc += 1
    #             break
    #         else:
    #             # self.pc += 1
    #             print(f"{IR} - command is not available")
    #             sys.exit()
    ################################################################

    # Day 3 & 4 - Code
    ################################################################
    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("Example Command: python ls8.py examples/mult.ls8")
            sys.exit(1)

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    # extract number from file
                    comment_split = line.split('#')
                    num = comment_split[0].strip()

                    if num != "":
                        # print out asm instruction
                        print(f'{num} == {int((num), 2):4} (binary - decimal)')

                        # save number to memory if exists
                        value = int(num, 2)
                        self.memory_write(value, address)
                        address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, register_a, register_b):
        """
        ALU operations. (arithmetic/logic unit)
        """

        if op == "ADD":
            self.register[register_a] += self.register[register_b]
        elif op == "MUL":
            self.register[register_a] *= self.register[register_b]
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
            self.memory_read(self.pc),
            self.memory_read(self.pc + 1),
            self.memory_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

    def memory_read(self, MAR):
        """
        read memory address register
        """
        return self.memory[MAR]

    def memory_write(self, MDR, MAR):
        """
        write memory address register from memory data register
        """
        self.memory[MAR] = MDR
        return

    def instruction_switch_run(self, IR, operand_a, operand_b):
        """
        Read in binary instruction from memory read
        Perform action on memory address operand_a and operand_b
        """
        if IR == LDI:
            self.register[operand_a] = operand_b
            self.pc += 3 # increments instruction index to next instruction line
        elif IR == PRN:
            print(self.register[operand_a])
            self.pc += 2
        elif IR == MUL:
            # call alu to perform multiplication
            self.alu("MUL", operand_a, operand_b)
            self.pc += 3
        elif IR == HLT:
            self.run_logic = False
            # sys.exit()
        elif IR == PUSH:
            value = self.register[operand_a]
            self.register[7] -= 1
            self.memory_write(value, self.register[7])
            self.pc += 2
        elif IR == POP:
            self.register[operand_a] = self.memory_read(self.register[7])
            value = self.register[operand_a]
            self.register[7] += 1
            self.pc += 2
        elif IR == CALL:
            call_address = self.pc + 2
            self.register[7] -= 1
            self.memory_write(call_address, self.register[7])
            self.pc = self.register[operand_a]
        elif IR == RET:
            ret_address = self.register[7]
            self.pc = self.memory_read(ret_address)
            self.register[7] += 1
        elif IR == ADD:
            # call alu to perform addition
            self.alu("ADD", operand_a, operand_b)
            self.pc += 3
        else:
            print(f"{IR} - command is not available")
            sys.exit()

    def run(self):
        """
        run the CPU functions
        """
        while self.run_logic:
            # read in instruction
            IR = self.memory_read(self.pc)
            # read in integer
            operand_a = self.memory_read(self.pc + 1)
            operand_b = self.memory_read(self.pc + 2)
            # receive instruction and perform task
            self.instruction_switch_run(IR, operand_a, operand_b)
