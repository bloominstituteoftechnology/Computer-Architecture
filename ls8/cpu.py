"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0  # program counter 
        self.ram = [0] * 256
        self.reg = [0] * 8
        SP = 7
        self.reg[SP] = 0xf4



        def LDI(a, b): self.reg[a] = b
        def PRN(a, b): print(self.reg[a])
        def ADD(a, b): self.reg[a] += self.reg[b]
        def MUL(a, b): self.reg[a] *= self.reg[b]
        def PUSH(a, b=None):
            self.reg[SP] -= 1
            self.ram[self.reg[SP]] = self.reg[a]
        def POP(a, b=None):
            self.reg[a] = self.ram[self.reg[SP]]
            self.reg[SP] += 1
        def CALL(a, b):
            self.reg[SP] -= 1
            self.ram[self.reg[SP]] = self.pc + 2
            self.pc = self.reg[a]
        def RET(a, b):
            self.pc = self.ram[self.reg[SP]]
            self.reg[SP] += 1

        self.opcodes = {
            0b00000000: 'NOP',
            0b00000001: 'HLT',
            0b10000010: LDI,
            0b01000111: PRN,
            0b10100000: ADD,
            0b10100010: MUL,
            0b01000101: PUSH,
            0b01000110: POP,
            0b01010000: CALL,
            0b00010001: RET
        }
    
        

    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(filename) as fp:
            for line in fp:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == '':  # ignore blanks
                    continue
                val = int(num, 2)

                self.ram[address] = val
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

         """ALU operations."""
        if op in self.opcodes:
            self.opcodes[op](reg_a, reg_b)
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

    def run(self):
        """Run the CPU."""
        
        def LDI(a, b): self.reg[a] = b
        def PRN(a, b): print(self.reg[a])
        opcodes = {
          0b00000000: 'NOP',
          0b00000001: 'HLT',
          0b10000010: LDI,
          0b01000111: PRN
        }

        ir = self.ram[self.pc]
        op_fn = self.opcodes[ir]

        while (op_fn) != 'HLT':
            num_operands = ir >> 6 # Grab two highest bits
            operand_a = self.ram_read(self.pc + 1) if num_operands > 0 else None
            operand_b = self.ram_read(self.pc + 2) if num_operands > 1 else None
            if op_fn != 'NOP':
                op_fn(operand_a, operand_b)
            self.pc += (num_operands + 1)