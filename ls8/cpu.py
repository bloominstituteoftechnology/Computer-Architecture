"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.flag = 0b00000000
        self.reg[7] = 0xf4
        self.running = False
        self.branchTable = {
            130: self.ldi,
            71: self.prn,
            162: self.mult,
            160: self.add,
            1: self.halt,
            85: self.jeq_run,
            86: self.jne_run,
            69: self.pushy,
            70: self.poppy,
            80: self.cal,
            17: self.retrn,
            84: self.jump,
            167: self.cmp_run
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        try:
            if len(sys.argv) < 2:
                print(f'Error from {sys.argv[0]}): missing file name argument')
                sys.exit(1)

            with open(sys.argv[1]) as f:
                code_line = 0
                for line in f:
                    split_line = line.split("#")[0]
                    stripped_line = split_line.strip()
                    # print(int(stripped_line, 2))
                    if stripped_line != "":
                        command = int(stripped_line, 2)
                        # print(command, code_line)

                        self.ram[address] = command
                        code_line += 1
                        address += 1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            print("(Did you double check the file name?)")
        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op):
        """ALU operations."""
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 2
        elif op == 'MUL':
            # print("multiply")
            result = self.reg[reg_a] * self.reg[reg_b]
            self.pc += 2
            return result
        elif op == "CMP":
            # print("reg_a vs reg_b", reg_a, reg_b)
            if self.reg[reg_a] < self.reg[reg_b]:
                # print("less than")
                self.flag = 0b00000100
            if self.reg[reg_a] > self.reg[reg_b]:
                # print("greater than")
                self.flag = 0b00000010
            if self.reg[reg_a] == self.reg[reg_b]:
                # print("equal")
                self.flag = 0b00000001
            self.pc += 3
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

    def ldi(self):
        self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
        self.pc += 3

    def prn(self):
        print("Printing", self.reg[self.ram[self.pc+1]])
        self.pc += 2

    def halt(self):
        # print("Halt")
        self.running = False

    def mult(self):
        print("alu", self.alu("MUL"))

    def add(self):
        print("alu add", self.alu("ADD"))

    def pushy(self):
        self.reg[7] -= 1
        register_address = self.ram[self.pc + 1]
        value = self.reg[register_address]
        self.ram[self.reg[7]] = value
        self.pc += 2

    def poppy(self):
        value = self.ram[self.reg[7]]
        register_address = self.ram[self.pc + 1]
        self.reg[register_address] = value
        self.reg[7] += 1
        self.pc += 2

    def cal(self):
        next_command_address = self.pc + 2
        self.reg[7] -= 1
        SP = self.reg[7]
        self.ram[SP] = next_command_address
        register_num_jump = self.ram[self.pc + 1]
        address_to_jump_to = self.reg[register_num_jump]
        self.pc = address_to_jump_to

    def retrn(self):
        SP = self.reg[7]
        return_address = self.ram[SP]
        self.reg[7] += 1
        self.pc = return_address

    def cmp_run(self):
        print("alu cmp", self.alu("CMP"))

    def jeq_run(self):
        if self.flag == 1:
            # print("it is true")
            address = self.ram[self.pc + 1]
            jump_address = self.reg[address]
            self.pc = jump_address
        else:
            self.pc += 2

    def jne_run(self):
        # print("JNE")
        if self.flag == 4 or self.flag == 2:
            # print("jne true")
            address = self.ram[self.pc + 1]
            # print(address)
            jump_address = self.reg[address]
            # print("jump address", jump_address)
            self.pc = jump_address
        else:
            self.pc += 2

    def jump(self):
        # print("JUMP")
        given_address = self.ram[self.pc + 1]
        address_to_jump_to = self.reg[given_address]
        # print(address_to_jump_to)
        self.pc = address_to_jump_to

    def run(self):
        self.running = True

        while self.running:
            instruction = self.ram_read(self.pc)
            # print(instruction, "instruction")
            # operand_a = self.ram_read(self.pc+1)
            # operand_b = self.ram_read(self.pc+2)
            try:
                self.branchTable[instruction]()

            except Exception:
                print(
                    f'Could not find that particular instruction.{instruction}')
                self.running = False
                break

    # def run(self):
    #     ldi = 130
    #     prn = 71
    #     mul = 162
    #     hlt = 1
    #     """Run the CPU."""
    #     self.running = True

    #     while self.running:
    #         instruction = self.ram_read(self.pc)
    #         operand_a = self.ram_read(self.pc+1)
    #         operand_b = self.ram_read(self.pc+2)
    #         if instruction == ldi:
    #             self.reg[operand_a] = operand_b
    #             self.pc += 3
    #             print("first loop")
    #         elif instruction == prn:
    #             print("Printing", self.reg[operand_a])
    #             self.pc += 2
    #         elif instruction == hlt:
    #             print("Halt")
    #             self.running = False
    #         elif instruction == mul:
    #             print("alu", self.alu("MUL", operand_a, operand_b))
    #         else:
    #             print(
    #                 f'Could not find that particular instruction.{instruction}')

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
