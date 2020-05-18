"""CPU functionality."""

import sys

# LDI = 0
# HLT = 1
# PRN = 3


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.init_value = 0
        self.flag = 0b00000000

        
    def load(self, program):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                # print(line)
                #Ignore comments
                comment_split = line.strip().split("#")
                value = comment_split[0].strip()
                # print(comment_split) # [everything before #, everything after #]
                if value == '':
                    continue
                instruction = int(value, 2)#Passing in the value 2 turns the info into bianary 

                self.ram[address] = instruction
                address += 1


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

    def mult(self, a, b):
        pass

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR
    
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        ADD = 0b10100000
        MUL = 0b10100010
        CALL = 0b01010000 
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JNE = 0b01010110
        JEQ = 0b01010101

        running = True
        ir = None
        

        while running:
            command = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if command == HLT:
                running = False
                self.pc += 1
                sys.exit()
            elif command == LDI:
                self.reg[reg_a] = reg_b
                self.pc += 3
            elif command == PRN:
                print(self.reg[reg_a])
                self.pc += 2
            elif command == PUSH:
                #Select register
                reg = self.ram[self.pc+1]
                #Grab value from register
                val = self.reg[reg]
                # decrement memory address by one
                self.reg[self.sp] -= 1
                #Save value from register into memory
                self.ram[self.reg[self.sp]] = val
                #Increment pc
                self.pc += 2
            elif command == POP:
                #Register holding sp
                reg = self.ram[self.pc+1]
                #Value from place in memory
                val = self.ram[self.reg[self.sp]]
                #Save value into register we are currently using
                self.reg[reg] = val
                #Increment the pointer
                self.reg[self.sp] += 1
                #Increment pc by 2
                self.pc += 2
            elif command == ADD:
                self.alu("ADD", reg_a, reg_b)
                self.pc += 3
            elif command == MUL:
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3
            elif command == CALL:
                call_address = self.pc + 2
                self.reg[7] -= 1
                self.ram_write(call_address, self.reg[7])
                self.pc = self.reg[reg_a]
            elif command == RET:
                ret_address = self.reg[7]
                self.pc = self.ram_read(ret_address)
                self.reg[7] += 1
            elif command == CMP:
                if self.reg[reg_a] < self.reg[reg_b]:
                    self.flag = 0b00000100
                elif self.reg[reg_a]  > self.reg[reg_b]:
                    self.flag = 0b00000010
                if self.reg[reg_a]  == self.reg[reg_b]:
                    self.flag = 0b00000001
                self.pc += 3
            elif command == JMP:
                reg = self.ram[self.pc + 1]
                self.pc = self.reg[reg]
                pass
            elif command == JEQ:
                reg = self.ram[self.pc + 1]
                if self.flag == 0b00000001:
                    self.pc = self.reg[reg]
                else:
                    self.pc += 2
            elif command == JNE:
                reg = self.ram[self.pc + 1]
                if self.flag != 0b00000001:
                    self.pc = self.reg[reg]
                else:
                    self.pc += 2
            else:
                #If command is non recognizable
                print(f"Unknown command")
                running = False
                #Lets Crash :(
