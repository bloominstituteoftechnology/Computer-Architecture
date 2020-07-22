"""CPU functionality."""

import sys

def to_decimal(num_string, base):
    digit_list = list(num_string)
    digit_list.reverse()
    value = 0
    for i in range(len(digit_list)):
        # print(f"+({int(digit_list[i])} * {base ** i})")
        value += int(digit_list[i]) * (base ** i)
    return value

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.isRunning = False

    instructionDefs = {
        'HLT': 0b00000001,
        'LDI': 0b10000010,
        'PRN': 0b01000111,
    }

    def ram_read(self, MAR):
        storedValue = self.ram[MAR]
        return storedValue

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0
        try: 
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        # print('line: ', line.split('#', 1)[0])
                        line = line.split('#', 1)[0]

                        line = int(line, 2)
                        self.ram_write(line, address)
                        address += 1
                    except ValueError:
                        pass

        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")

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
        # self.trace()

        self.isRunning = True

        # IR R0-R8
        IR = self.ram[self.pc]

        # run the operations
        while self.isRunning == True:
            # decode opcode
            opCode = bin(self.ram_read(self.pc))
            opCode = opCode[2:]
            # does inst set pc or do we
            numOps = to_decimal(opCode[:2], 2)
            isALU = opCode[2:3]
            setsPC = opCode[3:4]
            instID = opCode[4:]

            if numOps == 2:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
            elif numOps == 1:
                operand_a = self.ram[self.pc + 1]

            # HLT
            # no operands
            if to_decimal(opCode, 2) == self.instructionDefs['HLT']:
                self.pc += 1
                print('HLT run')

            # LDI
            # takes 2 operands
            elif to_decimal(opCode, 2) == self.instructionDefs['LDI']:
                self.reg[operand_a] = operand_b
                self.pc += 3
                print('LDI run')

            # PRN
            # takes one operand
            elif to_decimal(opCode, 2) == self.instructionDefs['PRN']:
                self.pc += 2
                print('PRN output: ', self.reg[operand_a])
                print('PRN run')

            else:
                self.isRunning = False
