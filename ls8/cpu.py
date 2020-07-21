"""CPU functionality."""

import sys

def to_decimal(num_string, base):
    digit_list = list(num_string)
    digit_list.reverse()
    value = 0
    for i in range(len(digit_list)):
        print(f"+({int(digit_list[i])} * {base ** i})")
        value += int(digit_list[i]) * (base ** i)
    return value


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg= [0] * 8
        self.ram= [0] * 256
        self.pc= 0
        self.isRunning= False

    instructionDefs= {
        'HLT': 0b00000001,
        'LDI': 0b10000010,
    }

    def ram_read(self, MAR):
        storedValue= self.ram[MAR]
        return storedValue

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
        self.isRunning= True
        # OP-CODE

        # Meanings of the bits in the first byte of each instruction: `AABCDDDD`
        # * `AA` Number of operands for this opcode, 0-2
        # * `B` 1 if this is an ALU operation
        # * `C` 1 if this instruction sets the PC
        # * `DDDD` Instruction identifier

        # The number of operands `AA` is useful to know because the total number of bytes in any
        # instruction is the number of operands + 1 (for the opcode). This
        # allows you to know how far to advance the `PC` with each instruction.

        # It might also be useful to check the other bits in an emulator implementation, but
        # there are other ways to code it that don't do these checks.
        
        # IR R0-R8
        IR= self.ram[self.pc]

        # decode opcode
        opCode= bin(self.ram_read(0))
        opCode= opCode[2:]
        numOps= opCode[:2]
        isALU= opCode[2:3]
        setsPC= opCode[3:4]
        instID= opCode[4:]

        # grab operands as specified
        if numOps == 2:
            operand_a= self.ram[self.pc + 1]
            operand_b= self.ram[self.pc + 2]
            self.pc+= 3
        elif numOps == 1:
            operand_a= self.ram[self.pc + 1]
            self.pc+= 3
        print('inst defs hlt: ', self.instructionDefs['HLT'])

        # run the operations
        while self.isRunning == True:
            # get current instruction from ram
            instruction= self.ram_read(self.pc)

            print('instruction: ', instruction)
            print('hlt:', self.instructionDefs['HLT'])
            print('pc: ', self.pc)

            # if HLT instruction
            if instruction == self.instructionDefs['HLT']:
                self.isRunning= False
                print('run HLT')

                # set pc bit in opCode
                if setsPC == 0:
                    self.pc+= 1
            elif instruction == self.instructionDefs['LDI']:

                self.isRunning= False
                self.pc+= 1

            else:
                self.isRunning= False


        print('opCode', opCode)
        print('numOps', numOps)
        print('isALU', isALU)
        print('setsPC', setsPC)
        print('instID', instID)
        # `LDI register immediate`
        # Set the value of a register to an integer.
        # Machine code:
        # ```
        # 10000010 00000rrr iiiiiiii
        # 82 0r ii

        # incase of LDI 

