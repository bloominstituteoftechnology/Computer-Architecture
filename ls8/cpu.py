"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    ops = {
        0x00: "NOP",   # no-op
        0x01: "HLT",   # halt; exit
        0x50: "CALL",  # call subroutine at register address
        0x11: "RET",   # return from subroutine
        0x52: "INT",   # interrupt
        0x13: "IRET",  # return from interrupt
        0x54: "JMP",   # jump to address in given reg
        0x55: "JEQ",   # if == flag true, jump to address in given reg
        0x56: "JNE",   # if E flag is clear, jump to address in given reg
        0x57: "JGT",   # if >, jump to address in given reg
        0x58: "JLT",   # if <
        0x59: "JLE",   # if < or ==
        0x5A: "JGE",   # if > or ==
        0x82: "LDI",   # set value of register to integer
        0x83: "LD",    # loads regA w/ value at mem address stored in regB
        0x84: "ST",    # store value in regB at address in regA
        0x45: "PUSH",  # push value in given reg onto stack
        0x46: "POP",   # pop value at top of stack into given reg
        0x47: "PRN",   # print numeric value stored in given reg
        0x48: "PRA",   # print alpha char value stored in given reg
        0xA0: "ADD",   # addition (ALU)
        0xA1: "SUB",   # subtract (ALU)
        0xA2: "MUL",   # multiply (ALU)
        0xA3: "DIV",   # division (ALU)
        0xA4: "MOD",   # modulo (ALU)
        0x65: "INC",   # increment (ALU)
        0x66: "DEC",   # decrement (ALU)
        0xA7: "CMP",   # comparison (ALU)
        0xA8: "AND",   # bitwise-and (ALU)
        0x69: "NOT",   # bitwise-not (ALU)
        0xAA: "OR",    # bitwise-or (ALU)
        0xAB: "XOR",   # XOR (ALU)
        0xAC: "SHL",   # bitshift left (ALU)
        0xAD: "SHR",   # bitshift right (ALU)
    }

    def __init__(self):
        """Construct a new CPU."""
        # pass
        self.ram = [0] * 256
        # self.cpu_reg = [0] * 8
        self.reg = [0] * 8
        self.pc = 0
        self.dispatch = {
            0x82: self._ldi,
            0x47: self._prn
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

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

    def run(self):
        """Run the CPU."""
        # pass
        # ir = self.pc
        ir = self.ram_read(self.pc)  # instruction register

        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        # operation = CPU.ops.get(ir)
        operation = self.dispatch.get(ir)
        args = ir >> 6

        # if operation is None:
        if operation is None or ir == 1:
            return
        elif args == 1:
            operation(operand_a)
        elif args == 2:
            operation(operand_a, operand_b)
        else:
            operation()        
        # elif operation == "HLT":
        #     return
        # elif operation == "LDI":
        #     self.reg[operand_a] = operand_b
        # elif operation == "PRN":
        #     print(self.reg[operand_a])

        # self.pc += (ir >> 6) + 1
        self.pc += args + 1
        self.run()
    def _ldi(self, reg_address, value):
        self.reg[reg_address] = value

    def _prn(self, reg_address):
        print(self.reg[reg_address])



        # (operand_a, operand_b) = (self.ram_read(ir+1), self.ram_read(ir+2))
        
     
