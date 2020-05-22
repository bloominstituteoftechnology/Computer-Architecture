"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # program counter
        self.pc = 0 # program counter
        # 8 new registers
        self.reg = [0] * 8 # register
        # memory storage for ram
        self.ram = [0] * 256
        self.sp = 0xf3 # stack pointer - points at the value at the top of the stack 
        """L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
        G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
        E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise."""


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8 Set the value of a register to an integer.
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0 Print numeric value stored in the given register. Print to the console the decimal integer value that is stored in the given register.
        #     0b00000000,
        #     0b00000001, # HLT - Halt the CPU
        # ]
        with open(sys.argv[1]) as f: # python ls8.py examples/print9.ls8
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2) # convert base 10 to binary
                #print(v)
                self.ram[address] = v # use ram instead of memory
                address += 1


        # for instruction_register in program:
        #     self.ram[address] = instruction_register
        #     address += 1


    def alu(self, op, operand_a, operand_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[operand_a] += self.reg[operand_b]
        elif op == "MUL":
            """Multiply the values in two registers together and store the result in registerA.

            Machine code:
            ```
            10100010 00000aaa 00000bbb
            A2 0a 0b
            ```"""
            self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
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
        """Run the CPU.
        read the memory address that's stored in register `PC`, and store
        that result in `IR`, the _instruction_register Register_
        
        read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` 
        and `operand_b` in case the instruction_register needs them.
        
        the `PC` needs to be updated to point to the next instruction_register 
        for the next iteration of the loop in `run()`"""

        # self.branchtable = {}
        # self.branchtable['0b00000001'] = self.handle_hlt
        # self.branchtable['0b10000010'] = self.handle_ldi
        # self.branchtable['0b01000111'] = self.handle_prn
        # self.branchtable['0b10100010'] = self.handle_mul

        # while True:
        # self.ir = self.ram[self.pc]
        # operand_a = self.ram_read(self.pc+1)
        # operand_b = self.ram_read(self.pc+2)
        # self.branchtable[self.ir]('t')

        # _instruction_register Register_ contains a copy of the currently executing instruction_register

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101
        RET = 0b00010001
        CALL = 0b01010000
        ADD = 0b10100000

        #read the memory address that's stored in register `PC`, and store that result in `IR`
        while True:
            instruction_register = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if instruction_register == HLT:
                # Halt the CPU (and exit the emulator).
                break
            elif instruction_register == LDI:
                # Set the value of a register to an integer.
                self.reg[operand_a] = operand_b
                # print('LDI pc + 3')
                self.pc = self.pc + 3
            elif instruction_register == PRN:
                print(self.reg[operand_a])
                # print('PRN pc + 2')
                self.pc = self.pc + 2
            elif instruction_register == MUL:
                print(self.reg[operand_a] * self.reg[operand_b])
                # print('MUL pc + 3')
                self.pc = self.pc + 3
            elif instruction_register == POP:
                self.reg[operand_a] = self.ram_read(self.sp+1)
                self.sp += 1
                self.pc += 2
            elif instruction_register == PUSH:
                self.ram_write(self.sp, self.reg[operand_a])
                self.pc += 2
                self.sp -= 1
            elif instruction_register == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif instruction_register == CALL:
                self.sp -= 1
                self.ram_write(self.sp, self.pc+2)
                self.pc = self.reg[operand_a]
            elif instruction_register == RET:
                # Return from subroutine. Pop the value from the top of the stack and store it in the PC
                # next instruction to add to stack, 
                self.pc = self.ram_read(self.sp)
                self.sp += 1
            else:
                print(f'instruction_register{hex(instruction_register)} not recognized')
                break
            

    def handle_hlt(self):
        sys.exit()

    def handle_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        print('LDI pc + 3')
        self.pc = self.pc + 3

    def handle_prn(self, operand_a):
        print(self.reg[operand_a])
        print('PRN pc + 2')
        self.pc = self.pc + 2

    def handle_mul(self, operand_a, operand_b):
        print(self.reg[operand_a] * self.reg[operand_b])
        print('MUL pc + 3')
        self.pc = self.pc + 3

    def ram_read(self, address_to_read):
        """accept the address to read and return the value stored
there."""
        return self.ram[address_to_read]

    def ram_write(self, address_to_read, register_to_write_to):
        """accept a value to write, and the address to write it to."""

        self.ram[address_to_read] = register_to_write_to
