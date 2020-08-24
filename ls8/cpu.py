"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = True
        self.pc = 0
        self.reg[7] = 0xf4  # STACK POINTER
        self.flags = [False] * 8  # FLAGS REGISTER (Sprint-Challenge)

    def ram_read(self, MAR):
        """
        Accepts the address to read and returns the value stored
        there.

        Input: MAR: _Memory Address Register_ ... address to read
        """
        if MAR < len(self.ram) - 1:
            return self.ram[MAR]

        else:
            return "INDEX ERROR: Requested address out of memory range."

    def ram_write(self, MDR, MAR):
        """
        Accepts a value to write, and the address to write it to.

        Inputs: MAR: _Memory Address Register_ ... address to write to
                MDR: _Memory Data Register_ ... data to write
        """
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("USAGE: ls8.py progname.ls8")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    temp = line.split()

                    if len(temp) == 0:
                        continue

                    if temp[0][0] == '#':
                        continue

                    try:
                        # > convert binary string to integer
                        self.ram[address] = int(temp[0], 2)

                    except ValueError:
                        print(f"Invalid number: {temp[0]}")
                        sys.exit(1)

                    address += 1

        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        if address == 0:
            print("Program was empty!")
            sys.exit(3)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        # Add condition for CMP (Sprint-Challenge)
        elif op == "CMP":
            # Can set flags per rules in spec
            equal = self.flags[7]
            greater_than = self.flags[6]
            less_than = self.flags[5]
            # If they are equal, set the Equal `E` flag to 1 (True),
            # otherwise set it to 0 (False)
            if self.reg[reg_a] == self.reg[reg_b]:
                equal = True
                greater_than = False
                less_than = False
            # If a is greater ...
            elif self.reg[reg_a] > self.reg[reg_b]:
                equal = False
                greater_than = True
                less_than = False
            # If b is greater ...
            else:
                equal = False
                greater_than = False
                less_than = True

            # Set flags to values determined by conditionals
            self.flags[5:] = [less_than, greater_than, equal]

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

        # Using binary codes
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        ADD = 0b10100000
        CALL = 0b01010000
        RET = 0b00010001
        # Sprint-Challenge Instructions
        JMP = 0b01010100
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110

        while self.running:

            # HLT Instruction - aka halt, stop running
            if self.ram[self.pc] == HLT:
                self.running = False

            # LDI Instruction - Set the value of a register to an integer.
            if self.ram[self.pc] == LDI:
                num_to_load = self.ram[self.pc + 2]
                reg_index = self.ram[self.pc + 1]
                self.reg[reg_index] = num_to_load

                self.pc += 3  # 3-byte instruction
                # print("LDI")

            # PRN Instruction - Print numeric value stored in the given register.
            # Print to the console the decimal integer value that is stored in
            # the given register.
            if self.ram[self.pc] == PRN:
                reg_to_print = self.ram[self.pc + 1]
                print(self.reg[reg_to_print])

                self.pc += 2  # 2-byte instruction

            # MUL Instruction - Multiply the values in two registers together
            # and store the result in registerA.
            if self.ram[self.pc] == MUL:
                first_reg = self.ram[self.pc + 1]
                sec_reg = self.ram[self.pc + 2]
                first_factor = self.reg[first_reg]
                sec_factor = self.reg[sec_reg]
                product = first_factor * sec_factor

                print(product)

                self.pc += 3  # 3-byte instruction

            # PUSH Instruction - Push the value in the given register on the
            # stack.
            if self.ram[self.pc] == PUSH:
                # print(f"PUSHING {self.ram[self.pc]}")
                # Decrement the `SP`
                self.reg[7] -= 1
                # print("DECREMENTED SP")

                # Copy the value in the given register
                reg_num = self.ram[self.pc + 1]
                # print("COPIED VALUE")
                value = self.reg[reg_num]  # We want to push this value
                # print(f"GOT VALUE {value}")

                # Add it to the address pointed to by `SP`
                top_of_stack_addr = self.reg[7]
                self.ram[top_of_stack_addr] = value

                self.pc += 2  # 2-byte instruction
                # print("PUSH COMPLETE")

            # POP Instruction - Pop the value at the top of the stack into the
            # given register.
            if self.ram[self.pc] == POP:
                # Find register for pop and copy
                top_of_stack_addr = self.reg[7]
                value = self.ram[top_of_stack_addr]

                # Copy the value from the address pointed to by `SP`
                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = value  # We want to pop this value

                # Increment `SP`
                self.reg[7] += 1

                self.pc += 2  # 2-byte instruction

            # ADD Instruction - Add the value in two registers and store the result in registerA.
            # The ADD instruction
            if self.ram[self.pc] == ADD:
                first_reg = self.ram[self.pc + 1]
                sec_reg = self.ram[self.pc + 2]
                self.alu('ADD', first_reg, sec_reg)
                self.pc += 3

            # CALL instruction - Calls a subroutine (function) at the address
            # stored in the register.
            if self.ram[self.pc] == CALL:
                # We will be PUSHing so we must decrement the Stack Pointer
                self.reg[7] -= 1
                SP = self.reg[7]
                # Then we want the address of the next instruction, for when
                # the subroutine has completed
                addr_next_instruction = self.pc + 2
                # And we put that address on the stack
                self.ram[SP] = addr_next_instruction
                # Next we find register we'll be CALLing from and the address
                # that is in that register
                reg_to_call = self.ram[self.pc + 1]
                addr_to_goto = self.reg[reg_to_call]
                # And we set the PC to that address
                self.pc = addr_to_goto
                # print("Called")

            # RET instruction - Return from subroutine
            if self.ram[self.pc] == RET:
                # We will be POPping so we don't decrement the Stack Pointer
                SP = self.reg[7]
                # We want the address at the top of the stack...
                addr_to_pop = self.ram[SP]
                # ...So that we can set PC to that address
                self.pc = addr_to_pop
                # After we pop we increment the Stack Pointer
                self.reg[7] += 1

            # Sprint-Challenge Instructions

            # CMP instruction - Compare the values in two registers.
            if self.ram[self.pc] == CMP:
                # CMP is handled by ALU, so we need the arguments for alu
                # IE the registers that carry the values that will be used
                first_reg = self.ram[self.pc + 1]
                sec_reg = self.ram[self.pc + 2]
                # Next we call the alu
                self.alu('CMP', first_reg, sec_reg)
                # Finally we increment the pc by 3 to the next instruction
                self.pc += 3

            # JMP instruction - Jump to the address stored in the given
            # register.
            if self.ram[self.pc] == JMP:
                # First we need the register that holds the to-jump address
                reg_to_jump = self.ram[self.pc + 1]
                # and then we need the address
                addr_to_jump = self.reg[reg_to_jump]
                # Finally we set the PC to that address
                self.pc = addr_to_jump

            # JEQ instruction - If `equal` flag is set (true), jump to the
            #                   address stored in the given register.
            if self.ram[self.pc] == JEQ:
                # JEQ's argument is a register that contains an address that may be jumped to
                # First we need that register and the address that it holds
                reg_to_jump = self.ram[self.pc + 1]
                addr_to_jump = self.reg[reg_to_jump]
                # Next we check the equality flag
                if self.flags[7] is True:
                    # If the flag is set, we jump
                    self.pc = addr_to_jump
                else:
                    # If not, we move to the next instruction
                    self.pc += 2

            # JNE instruction - If `E` flag is clear (false, 0), jump to the
            #                   address stored in the given register.
            if self.ram[self.pc] == JNE:
                # JNE works much like JEQ
                # First we need the register and the address that it holds
                reg_to_jump = self.ram[self.pc + 1]
                addr_to_jump = self.reg[reg_to_jump]
                # Next we check the equality flag
                if self.flags[7] is False:
                    # If the flag is clear, we jump
                    self.pc = addr_to_jump
                else:
                    # If not, we move to the next instruction
                    self.pc += 2

            # # Handle "BAD" Input
            # else:
            #     print(f"Invalid instruction {self.ram[self.pc]} at address {self.pc}")
            #     sys.exit(1)


if __name__ == "__main__":

    cpu = CPU()

    print("Before write:", cpu.ram_read(250))

    cpu.ram_write(3, 250)

    print("After write:", cpu.ram_read(250))
