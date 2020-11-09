"""CPU functionality."""

import os.path
from os import path

import sys


class CPU:
    """Main CPU class."""

    ## NOT SURE WHAT TO DO ABOUT LISTING INVENTORY ##

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        program = []

        if len(sys.argv) != 2:
            print("Wrong number of arguments, please pass file name")
            sys.exit(1)

        with open(sys.argv[1]) as f:
            for line in f: 
                # Split the line on the comment character (#)
                line_split = line.split('#')
                # Extract the command from the split line
                # It will be the first value in our split line
                command = line_split[0].strip()
                if command == '':
                    continue
                
                program.append(command)

        # print("Program from Load: ", program)

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            
            self.ram_write(address, instruction)
            
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
        
        running = True

        # Program Counter
        pc = 0

        # Stack Pointer
        sp = 7

        # registers[sp] == the current top of our stack
        self.registers[sp] = 256


        while running:
            # Read Line by Line from Memory
            instruction = self.ram[pc]

            if instruction == '10000010':
                
                reg_location = '0b' + self.ram[pc + 1]

                value_to_store = self.ram[pc + 2]

                self.registers[int(reg_location,2)] = value_to_store

                pc += 3

            elif instruction == '01000111':

                reg_location = '0b' + self.ram[pc + 1]

                print(int('0b'+self.registers[int(reg_location,2)],2))

                pc += 2

            elif instruction == '00000001':

                running = False

                pc += 1
            
            elif instruction == '10100010':

               
                reg_location_1 = '0b' + self.ram[pc + 1]

                reg_location_2 = '0b' + self.ram[pc + 2]

                num_8 = self.registers[int(reg_location_1, 2)]

                num_9 = self.registers[int(reg_location_2, 2)]

                result = int(num_8, 2) * int(num_9, 2)
                
                self.registers[int(reg_location_1,2)] = bin(result)[2:]

                pc += 3

            elif instruction == '01000101':
                
                # Push
                
                # Read the given register address
                reg_location = '0b' + self.ram[pc + 1]

                value_to_push = self.registers[int(reg_location, 2)]

                # # Move the stack pointer down
                self.registers[sp] -= 1

                # # Write the value to push, into the top of stack
                self.ram_write(self.registers[sp], value_to_push)  

                pc += 2

            elif instruction == '01000110':
            
                # Pop
                
                # Read the given register address
                reg_address = '0b' + self.ram_read((pc + 1))
                
                # Read the value at the top of the stack
                # store that into the register given
                self.registers[int(reg_address, 2)] = self.ram_read(self.registers[sp])
                
                # move the stack pointer back up
                self.registers[sp] += 1
                
                pc += 2

            
        #     elif command == CALL:
        #         # Push the return address onto the stack
        #         # Move the SP down
        #         registers[SP] -= 1
        #         # Write the value of the next line to return to in the code
        #         memory[registers[SP]] = pc + 2
        #         # Set the PC to whatever is given to us in the register
        #         reg_num = memory[pc + 1]
        #         print(memory[-10:])
        #         pc = registers[reg_num]
        # ​
        #     elif command == RET:
        #         # Pop the top of the stack and set the PC to the value of what was popped
        #         pc = memory[registers[SP]]
        #         registers[SP] += 1
        #         # Pop
        #         pass

            else: 
                
                print(f"Unknown Instruction: {instruction} - PC: {pc}")

                sys.exit(1) 
