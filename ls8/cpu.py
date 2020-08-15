"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # We need 256 bytes of Ram, 8 registers, a counter, to assign memory for the stack, and continuous variable
        self.ram = [None] * 256
        self.registers = [None] * 8
        self.registers[7] = 0xF0 # 240. I need to ask if it's better to use a consistent number base if possible
        self.running = True
        self.pc = 0
        # Adding flags register 
        self.fl = [False] * 8


    def ram_read(self, address):
        # Accepts the address and returns the value from Ram
        return(self.ram[address])    

    def ram_write(self, value, address):
        # Accepts a value and address and assigns to Ram
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        # We're going to un-hardcode the machine code
        if len(sys.argv) < 2:
            print("Insufficient arguments")
            print("Usage: filename file_to_open")
            sys.exit()

        address = 0
        
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')
                    potential_num = comment_split[0]

                    if potential_num == '':
                        continue
                    
                    if potential_num[0] == '1' or potential_num[0] == '0':
                        num = potential_num[:8]

                        self.ram[address] = int(num, 2)
                        address += 1
        
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')


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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc

        elif op == "CMP":
            equal = self.fl[7]
            greater_than = self.fl[6]
            less_than = self.fl[5]
            if self.registers[reg_a] == self.registers[reg_b]:
                equal = True
                greater_than = False
                less_than = False
            elif self.registers[reg_a] > self.registers[reg_b]:
                equal = False
                greater_than = True
                less_than = False
            else:
                equal = False
                greater_than = False
                less_than = True

            self.fl[5:] = [less_than, greater_than, equal]
            
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
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD =  0b10100000
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        while self.running:
            # The HLT instruction
            if self.ram[self.pc] == HLT:
                self.running = False
            
            # The LDI instruction
            if self.ram[self.pc] == LDI:
                num_to_load = self.ram[self.pc + 2]
                reg_index = self.ram[self.pc + 1]
                self.registers[reg_index] = num_to_load
                self.pc += 3
            
            # The PRN instruction
            if self.ram[self.pc] == PRN:
                reg_to_print = self.ram[self.pc + 1]
                print(self.registers[reg_to_print])
                self.pc += 2
            
            # THe MUL instruction
            if self.ram[self.pc] == MUL:
                first_reg = self.ram[self.pc + 1]
                sec_reg = self.ram[self.pc + 2]
                first_factor = self.registers[first_reg]
                sec_factor = self.registers[sec_reg]
                product = first_factor * sec_factor
                print(product)
                self.pc += 3
            
            # The ADD instruction
            if self.ram[self.pc] == ADD:
                first_reg = self.ram[self.pc + 1]
                sec_reg = self.ram[self.pc + 2]
                self.alu('ADD', first_reg, sec_reg)
                self.pc += 3
            
            # The CMP instruction
            if self.ram[self.pc] == CMP:
                # CMP is handled by ALU, so we need the arguments for alu
                # IE the registers that carry the values that will be used
                first_reg = self.ram[self.pc + 1]
                sec_reg = self.ram[self.pc + 2]
                # Next we call the alu
                self.alu('CMP', first_reg, sec_reg)
                # Finally we increment the pc by 3 to the next instruction
                self.pc += 3
            
            # The JMP instruction
            if self.ram[self.pc] == JMP:
                # First we need the register that holds the to-jump address
                reg_to_jump = self.ram[self.pc + 1]
                # and then we need the address
                addr_to_jump = self.registers[reg_to_jump]
                # Finally we set the PC to that address
                self.pc = addr_to_jump
            
            # The JEQ instruction
            if self.ram[self.pc] == JEQ:
                # JEQ's argument is a register that contains an address that may be jumped to
                # First we need that register and the address that it holds
                reg_to_jump = self.ram[self.pc + 1]
                addr_to_jump = self.registers[reg_to_jump]
                # Next we check the equality flag
                if self.fl[7] is True:
                    # If the flag is set, we jump
                    self.pc = addr_to_jump
                else:
                    # If not, we move to the next instruction
                    self.pc += 2
            
            # The JNE instruction
            if self.ram[self.pc] == JNE:
                # JNE works much like JEQ
                # First we need the register and the address that it holds
                reg_to_jump = self.ram[self.pc + 1]
                addr_to_jump = self.registers[reg_to_jump]
                # Next we check the equality flag
                if self.fl[7] is False:
                    # If the flag is clear, we jump
                    self.pc = addr_to_jump
                else:
                    # If not, we move to the next instruction
                    self.pc += 2

            # The PUSH instruction
            if self.ram[self.pc] == PUSH:
                # When PUSHing, we must first we decrement the stack pointer
                self.registers[7] -= 1
                # Next we find the register for PUSHing and that register's value
                reg_to_push = self.ram[self.pc + 1]
                num_to_push = self.registers[reg_to_push]
                # Next we copy the number to memory (ram)
                SP = self.registers[7]
                self.ram[SP] = num_to_push
                self.pc += 2
            
            # The POP instruction
            if self.ram[self.pc] == POP:
                # When POPping, we don't decrement the Stack Pointer...
                SP = self.registers[7]
                # ...because we want the value at the most recent position of the Stack Pointer
                num_to_pop = self.ram[SP]
                # Next we find the register for POPping and copy the number into that register
                reg_to_pop = self.ram[self.pc + 1]
                self.registers[reg_to_pop] = num_to_pop
                # After we POP we increment the Stack Pointer to the new 'most recent' position
                self.registers[7] += 1 
                self.pc += 2
            
            # The CALL instruction
            if self.ram[self.pc] == CALL:
                # We will be PUSHing so we must decrement the Stack Pointer
                self.registers[7] -= 1
                SP = self.registers[7]
                # Then we want the address of the next instruction, for when the subroutine has completed
                addr_next_instruction = self.pc + 2
                # And we put that address on the stack
                self.ram[SP] = addr_next_instruction
                # Next we find register we'll be CALLing from and the address that is in that register
                reg_to_call = self.ram[self.pc + 1]
                addr_to_goto = self.registers[reg_to_call]
                # And we set the PC to that address
                self.pc = addr_to_goto

            # The RET instruction
            if self.ram[self.pc] == RET:
                # We will be POPping so we don't decrement the Stack Pointer
                SP = self.registers[7]
                # We want the address at the top of the stack...
                addr_to_pop = self.ram[SP]
                # ...So that we can set PC to that address
                self.pc = addr_to_pop
                # After we pop we increment the Stack Pointer
                self.registers[7] += 1
