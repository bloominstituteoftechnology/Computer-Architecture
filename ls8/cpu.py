"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256        # Memory
        self.reg = [0] * 8          # General-purpose numeric registers R0-R7
        self.pc = 0                 # Program Counter
        self.ir = 0                 # Instruction Register
        self.mar = 0                # Memory Address Register
        self.mdr = 0                # Memory Data Register
        self.fl = [0] * 8           # 8-bit Flags Register


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, val, addr):
        self.ram[addr] = val

    def run(self):
        """Run the CPU."""
        for i in range(256):
            to_bin = lambda x: format(x, 'b').zfill(8)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.ir = to_bin(self.pc)
            instruction = {
                "10100000" : ["pass"],   #ADD
                "10101000" : ["pass"],   #AND
                "01010000" : ["pass"],   #CALL register
                "01100110" : ["pass"],   #DEC
                "10100011" : ["pass"],   #DIV
                "00000001" : ["exit()"],   #HLT
                "01100101" : ["pass"],   #INC
                "01010010" : ["pass"],   #INT
                "00010011" : ["pass"],   #IRET
                "01010101" : ["pass"],   #JEQ
                "01011010" : ["pass"],   #JGE
                "01010111" : ["pass"],   #JGT
                "01011001" : ["pass"],   #JLE
                "01011000" : ["pass"],   #JLT
                "01010100" : ["pass"],   #JMP
                "01010110" : ["pass"],   #JNE
                "10000011" : ["pass"],   #LD
                "10000010" : ["self.reg[{0}] = {1}"],   #LDI
                "10100100" : ["pass"],   #MOD
                "10100010" : ["pass"],   #MUL
                "00000000" : ["pass"],   #NOP
                "01101001" : ["pass"],   #NOT
                "10101010" : ["pass"],   #OR
                "01000110" : ["pass"],   #POP
                "01001000" : ["pass"],   #PRA
                "01000111" : ["print(self.reg[{0}])"],   #PRN
                "01000101" : ["pass"],   #PUSH
                "00010001" : ["pass"],   #RET
                "10101100" : ["pass"],   #SHL
                "10101101" : ["pass"],   #SHR
                "10000100" : ["pass"],   #ST
                "10100001" : ["pass"],   #SUB
                "10101011" : ["pass"],   #XOR
            }
            byte = to_bin(self.ram[int(self.ir, 2)])
            if byte[:2] == "00":
                # execute all operations in an instruction
                for op in instruction[byte]:
                    exec(op)
                self.pc += 1
            elif byte[:2] == "01":
                for op in instruction[byte]:
                    exec(op.format(operand_a))
                self.pc += 2
            elif byte[:2] == "10":
                for op in instruction[byte]:
                    exec(op.format(operand_a, operand_b))
                self.pc += 3




