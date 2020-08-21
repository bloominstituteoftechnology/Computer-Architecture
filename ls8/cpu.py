"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256     # ram = [0,0,0, 0, 0.. -> 256 0's]
        self.reg = [0] * 8       # register-on the cpu.. reg = [0,0,0,0,0,0,0,0]
        self.pc = 0              # Program Counter - the index into memory of the currently-executing instruction
        self.flag = 0b00000000   # FLAG FOR CMP
        # save in reg 6
        
    def load(self):
        """Load a program into ram."""

        filename = sys.argv[1]
        address = 0

        with open(filename) as f:
            for line in f:
                
                line = line.split("#")[0].strip()
                
                if line == "":
                    continue
                
                else:
                    self.ram[address] = int(line, 2)
                    address += 1
    
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
        
        # --- CMP ---
        
        elif op == "CMP":
            value_1 = self.reg[reg_a]
            value_2 = self.reg[reg_b]
            
            if value_1 > value_2:  
                self.flag = 0b00000010
                
            elif value_1 == value_2:  
                self.flag = 0b00000001
                
            elif value_1 < value_2:  
                self.flag = 0b00000100
        
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
        CALL = 0b01010000 # Call
        RET = 0b00010001 # RET
        ADD = 0b10100000 # ADD - DO IT!
        SP = 7 # Stack Pointer
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        self.reg[SP] = 244  # 0xf4 top of stack, also 0xf4
        
        running = True
        
        while running:
            
            ir = self.ram[self.pc] # Instruction Register
            
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
    
            if ir == HLT:
                running = False
                self.pc += 1

            elif ir == LDI:
            # Set the value of a register to an integer.
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
            
            # CALL: The PC is set to the address stored in the given register. 
            # We jump to that location in RAM and execute the first instruction in the subroutine. 
            # The PC can move forward or backwards from its current location.

            elif ir == CALL:
                SP -= 1
                self.ram[SP] = self.pc + 2 
                regnum = operand_a
                self.pc = self.reg[regnum]

            # RET: Pop the value from the top of the stack and store it in the PC.

            elif ir == RET:
                self.pc = self.ram[SP]
                SP += 1

            # ADD: Add the value in two registers and store the result in registerA.

            elif ir == ADD:
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3
            
            # ----------------------------SPRINT CHALLENGE-----------------------------------------
            
            # CMP - comparison function - Set Flags based on CMP status
            # set flags correctly
            
            # values inside the registers
            # change to reg 6
            # put to alu
            
            elif ir == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            # JMP: Jump to the address stored in the given register.
            # Set the PC to the address stored in the given register.

            elif ir == JMP:
                address = self.reg[operand_a]
                self.pc = address

            # JEQ: If equal flag is set (true), jump to the address stored in the given reg.

            elif ir == JEQ:
                if self.flag == 0b00000001:
                    address = self.reg[operand_a]
                    self.pc = address
                else:
                    self.pc += 2

            # JNE: If E flag is clear (false, 0), jump to the address stored in the given reg.

            elif ir == JNE: 
                if self.flag & 0b00000001 == 0b00000000:
                    address = self.reg[operand_a]
                    self.pc = address
                else:
                    self.pc += 2
            
            else:
                print(f"Invalid instruction {ir} at address {self.pc}")
                sys.exit(1)
            
            # read value where the pointer is pointing
            
                
                
                
            
            
            
                
            
            
            
            
            
            
            
            
            
            
            
        
