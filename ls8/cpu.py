"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg= [0] * 8
        self.ram= [0] * 256
        self.bootUp()
        # Program Counter, address of the currently executing instruction
        self.pc= 0
        self.fl= 0

    def bootUp(self):
        # reset registers
        for r in range(len(self.reg)-1):
            if r < 7:
                self.reg[r]= 0
            elif r == 7:
                self.reg[r]= 0xF4
        self.isRunning= True


    # MAR contains the address that is being read or written to. The MDR contains the data that was read or the data to write.
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        self.ram[MAR]= MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # print('numOps: ', numOps)
        # print('isALU: ', isALU)
        # print('setsPc: ', setsPc)
        # print('isntID: ', isntID)

        while self.isRunning:
            # Instruction Register
            IR_bin= self.ram_read(self.pc)
            IR= bin(self.ram_read(self.pc))

            # `AABCDDDD`
            #  `AA` Number of operands for this opcode, 0-2
            numOps= IR[2:4]
            # * `B` 1 if this is an ALU operation
            isALU= IR[4:5]
            # * `C` 1 if this instruction sets the PC
            setsPc= IR[5:6]
            # * `DDDD` Instruction identifier
            isntID= IR[6:]

            if 

            # HTL 00000001 
            if IR_bin == 0b00000001:
                self.isRunning= False
                self.pc+= 1
                # print('HLT')

            # LDI 10000010 00000rrr iiiiiiii
            elif IR_bin == 0b10000010:
                mar= self.pc+ 1
                mdr= self.pc+ 2
                self.ram_write(mdr, mar)
                self.pc+= 3
                # print('LDI')

            # PRN 01000111 00000rrr
            elif IR_bin == 0b01000111:
                val= self.pc+1
                print(val)
                self.pc+= 2
                # print('PRN')
