"""CPU functionality."""

import sys
import os

"""
 Inventory what is here
 Implement the CPU constructor
 Add RAM functions ram_read() and ram_write()
 Implement the core of run()
 Implement the HLT instruction handler
 Add the LDI instruction
 Add the PRN instruction
 """

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.registers[7] = 0XF4
        self.ram = [0] * 256
        self.pc = 0
        self.halted = False
        self.stack_point_register = 7

    def decimal_to_binary(self,x):
        return int(bin(x)[:2])

    def load(self, file_name):
        """Load a program into memory."""
        current = 0
        temp = []
        try:
            with open(file_name) as my_file:
                for line in my_file:
                    comment_split = line.split("#")
                    maybe_binary_number = comment_split[0]

                    try:
                        x = int(maybe_binary_number, 2)
                        self.ram[current] = x
                        temp.append(x)
                        current += 1
                    except: 
                        continue
        except FileNotFoundError:
            print(os.getcwd())
            print("file not found")
            sys.exit(1)                   

        # space_for_stack = 128 - len(temp)
        # self.ram += [0] * space_for_stack


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
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
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()

    def run(self):
        """Run the CPU."""
        
        self.registers[self.stack_point_register] = len(self.ram) - 1

        while not self.halted:
            command_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(command_to_execute, operand_a, operand_b)

        print(self.ram)
    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == HLT:
            self.halted = True
        elif instruction == PRN:
            print(self.registers[operand_a])
            self.pc += 2
        elif instruction == LDI:
            self.registers[operand_a] = operand_b
            self.pc += 3
        elif instruction == MUL:
            self.registers[operand_a] = self.registers[operand_a] * self.registers[operand_b]
            self.pc += 3

        elif instruction == PUSH:
            self.registers[self.stack_point_register] -= 1
            register_to_get_value_in = self.ram[self.pc + 1]
            value_in_register = self.registers[register_to_get_value_in]

            self.ram[self.registers[self.stack_point_register]] = value_in_register

            self.pc += 2

        elif instruction == POP:
            register_to_pop_value_in = self.ram[self.pc + 1]
            self.registers[register_to_pop_value_in] = self.ram[self.registers[self.stack_point_register]]

            self.registers[self.stack_point_register] += 1

            self.pc += 2

        else:
            print("ERROR")








            # # LDI instruction
            # if command_to_execute == 130:
            #     spot_to_store = self.ram[self.pc + 1]
            #     value_to_store = self.ram[self.pc + 2]

            #     self.registers[spot_to_store] = value_to_store

            #     self.pc += 3

            # # PRN instruction
            # elif command_to_execute == 71:
            #     selected_register = self.ram[self.pc + 1]
            #     print(self.registers[selected_register])
            #     self.pc += 2

            # # HLT instruction
            # elif command_to_execute == 1:
            #     running = False

            # # EXCEPTION
            # else:
            #     print("ERROR INCORRECT COMMAND")

        
