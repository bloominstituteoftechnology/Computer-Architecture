"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        # GENERAL-PURPOSE REGISTERS:
        self.reg = [0] * 8
        # --> R0
        # --> R1
        # --> R2
        # --> R3
        # --> R4
        # --> R5: RESERVED FOR INTERRUPT MASK (IM)
        # --> R6: RESERVED FOR INTERRUPT STATUS (IS)
        # --> R7: RESERVED FOR STACK POINTER (SP)

        # INTERNAL REGISTERS:
        # --> (PC)  PROGRAM COUNTER --------- ADDRESS OF THE CURRENTLY EXECUTING INSTRUCTION
        self.pc = 0
        # --> (IR)  INSTRUCTION REGISTER ---- CONTAINS A COPY OF THE CURRENTLY EXECUTING INSTRUCTION
        self.ir = 0
        # --> (MAR) MEMORY ADDRESS REGISTER - HOLDS THE MEMORY ADDRESS CURRENTLY BEING READ OR WRITTEN
        self.mar = 0
        # --> (MDR) MEMORY DATA REGISTER ---- HOLDS THE VALUE TO WRITE OR THE VALUE JUST READ
        self.mdr = 0
        # --> (FL)  FLAG REGISTER ----------- HOLDS THE CURRENT FLAG STATUS
        self.fl = 0

        self.running = True

        # INITIALIZE THE STACKPOINTER
        self.reg[7] = 0xF4

    # `RAM_READ()` - SHOULD ACCEPT THE ADDRESS TO READ AND RETURN THE VALUE STORED
    def ram_read(self, address):
        return self.ram[address]

    # `RAM_WRITE()` - SHOULD ACCEPT A VALUE TO WRITE AND THE ADDRESS TO WRITE IT TO
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(filename) as file:
            for line in file:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == "":
                    continue
                value = int(num, 2)
                self.ram_write(address, value)
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
        while self.running:
            command_to_execute = self.ram_read(self.pc)
            operation_1 = self.ram_read(self.pc + 1)
            operation_2 = self.ram_read(self.pc + 2)

            self.execute_instruction(
                command_to_execute, operation_1, operation_2)

    def execute_instruction(self, instruction, operation_1, operation_2):
        if instruction == LDI:
            self.reg[operation_1] = operation_2
            self.pc += 3
        elif instruction == PRN:
            print(self.reg[operation_1])
            self.pc += 2
        elif instruction == HLT:
            self.running = False
            self.pc += 1
        else:
            print("INVALID INSTRUCTION")
            pass
