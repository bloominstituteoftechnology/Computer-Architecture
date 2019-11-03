"""CPU functionality."""

import sys
import os

class CPU:
    """Main CPU class."""

    OPCODES = {
    "ADD":  {"type": 2, "code": "10100000"},
    "AND":  {"type": 2, "code": "10101000"},
    "CALL": {"type": 1, "code": "01010000"},
    "CMP":  {"type": 2, "code": "10100111"},
    "DEC":  {"type": 1, "code": "01100110"},
    "DIV":  {"type": 2, "code": "10100011"},
    "HLT":  {"type": 0, "code": "00000001"},
    "INC":  {"type": 1, "code": "01100101"},
    "INT":  {"type": 1, "code": "01010010"},
    "IRET": {"type": 0, "code": "00010011"},
    "JEQ":  {"type": 1, "code": "01010101"},
    "JGE":  {"type": 1, "code": "01011010"},
    "JGT":  {"type": 1, "code": "01010111"},
    "JLE":  {"type": 1, "code": "01011001"},
    "JLT":  {"type": 1, "code": "01011000"},
    "JMP":  {"type": 1, "code": "01010100"},
    "JNE":  {"type": 1, "code": "01010110"},
    "LD":   {"type": 2, "code": "10000011"},
    "LDI":  {"type": 8, "code": "10000010"},
    "MOD":  {"type": 2, "code": "10100100"},
    "MUL":  {"type": 2, "code": "10100010"},
    "NOP":  {"type": 0, "code": "00000000"},
    "NOT":  {"type": 1, "code": "01101001"},
    "OR":   {"type": 2, "code": "10101010"},
    "POP":  {"type": 1, "code": "01000110"},
    "PRA":  {"type": 1, "code": "01001000"},
    "PRN":  {"type": 1, "code": "01000111"},
    "PUSH": {"type": 1, "code": "01000101"},
    "RET":  {"type": 0, "code": "00010001"},
    "SHL":  {"type": 2, "code": "10101100"},
    "SHR":  {"type": 2, "code": "10101101"},
    "ST":   {"type": 2, "code": "10000100"},
    "SUB":  {"type": 2, "code": "10100001"},
    "XOR":  {"type": 2, "code": "10101011"},
    }
    opCodeMap = {}
    for op, x in OPCODES.items():
        opCodeMap[x["code"]] = op

    def getOperation(self, opcode):
        if opcode in self.opCodeMap:
            return self.opCodeMap[opcode]


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg =[0]*8
        self.pc=0


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

    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self,address, value):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.#ram_read() should accept the address to read and return the value stored there.ram_write() should accept a value to write, and the address to write it to.
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

    def run(self):
        """Run the CPU."""
        IR = self.ram_read(self.PC)

        op = self.getOperation(IR)
        if op == "ADD":
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            self.alu(op, operand_a, operand_b)
            self.PC += 3
        elif op == "HLT":
            os.exit()
        elif op == "LDI":
            operand_a = self.ram_read(self.PC + 1) #Register where to write
            operand_b = self.ram_read(self.PC + 2) #Value to write
            self.reg[operand_a] = operand_b
            self.PC += 3

        elif op == "PRN":
            operand_a = self.ram_read(self.PC + 1)  # Value to write
            print(self.reg[operand_a])
            self.PC += 2

