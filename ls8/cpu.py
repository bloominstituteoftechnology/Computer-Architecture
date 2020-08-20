"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256     # ram = [0,0,0, 0, 0.. -> 256 0's]
        self.reg = [0] * 8       # register-on the cpu.. reg = [0,0,0,0,0,0,0,0]
        self.pc = 0              # Program Counter - the index into memory of the currently-executing instruction
        
    def load(self):
        """Load a program into ram."""

        filename = sys.argv[1]
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
        
        with open(filename) as f:
            for line in f:
                
                line = line.split("#")[0].strip()
                
                if line == "":
                    continue
                
                else:
                    self.ram[address] = int(line, 2)
                    address += 1
                
                print(line)

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    # ask for tomorrow, not needed for day 1/2
    
    def ram_read(self, address):
        return self.ram[address]
        
    
    def ram_write(self, value, address):
        self.ram[adress] = value
        return value
    
    def alu(self, op, reg_a, reg_b):
        """ALU / Math operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
            
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
        
        # Codes
        HLT = 0b00000001 # Halt/ Stop
        LDI = 0b10000010 # Assign 
        PRN = 0b01000111 # Print numeric value stored in the given register
        MUL = 0b10100010 # Multiply 
        PUSH = 0b01000101 # Push
        POP = 0b01000110 # Pop
        CALL = 0B01010000
        RET = 0B00010001
        SP = 7 # Stack Pointer
        self.reg[SP] = 244 # top of stack, also 0xf4
        
        running = True
        
        while running:
            ir = self.ram[self.pc] # Instruction Register
            
            reg_a = self.ram[self.pc + 1]   # first register value
            reg_b = self.ram[self.pc + 2]   # second register value
            
            if ir == HLT:
                running = False
                self.pc += 1

            elif ir == LDI:
            #Set the value of a register to an integer.
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] = value
                self.pc += 3

            elif ir == PRN:
                reg_num = self.ram[self.pc +1]
                print(self.reg[reg_num])
                self.pc += 2

            elif ir == MUL:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] *= self.reg[value]
                self.pc += 3

            elif ir == PUSH:
                # Decrement SP
                self.reg[7] -= 1
                 # Get value from register
                reg_num = self.ram[self.pc +1]
                value = self.reg[reg_num]

                #store it on the stack
                top_stack = self.reg[7]
                self.ram[top_stack] = value
                self.pc +=2

            elif ir == POP:
                reg_num = self.ram[self.pc +1]
                self.reg[reg_num] = self.ram[self.reg[7]]

                self.reg[7] += 1

                self.pc += 2
            
            # The CALL instruction
            elif self.ram[self.pc] == CALL:
                # Add the pushing & must decrement the SP
                self.reg[7] -= 1
                SP = self.reg[7]
                # get the address of the next instruction for when subroutine is complete
                addr_next_instruction = self.pc + 2
                # then put that address on the stack
                self.ram[SP] = addr_next_instruction
                # then find the reg to call from and the address in that reg
                reg_to_call = self.ram[self.pc + 1]
                addr_to_go_to = self.reg[reg_to_call]
                # and set the pc to that address
                self.pc = addr_to_go_to

            # The RET instruction
            elif self.ram[self.pc] == RET:
                # This is an instance of pop so don't decrement the SP
                SP = self.reg[7]
                # Get the address at the top of the stack
                addr_to_pop = self.ram[SP]
                # and set PC to that address
                self.pc = addr_to_pop
                # After pop then increment the SP
                self.reg[7] += 1
        
            # else:
            #     print(f"Invalid instruction {ir} at address {pc}")
            #     sys.exit(1)
            
            # read value where the pointer is pointing
            
                
                
                
            
            
            
                
            
            
            
            
            
            
            
            
            
            
            
        
