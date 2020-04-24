"""CPU functionality."""

import sys
from ls8Instructions import *


IM = 5 # Interrupt Mask Index
IS = 6 # Interrupt Status Index
SP = 7 # Stack Pointer Index
    
class CPU:
    """Main CPU class."""
    

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # RAM capacity of 256 bytes
        self.ir = [0] * 8 # Setting up 8 general-purpose resgisters
        self.pc = 0 # Program Counter
        self.flags = 0
        self.ir[SP] = 0xF4
        self.branchtable = {}
        self.branchtable[inst_dict["HLT"]] = self.handle_hlt
        self.branchtable[inst_dict["LDI"]] = self.handle_ldi
        self.branchtable[inst_dict["PRN"]] = self.handle_prn
        self.branchtable[inst_dict["MUL"]] = self.handle_mult
        self.branchtable[inst_dict["PUSH"]] = self.handle_push
        self.branchtable[inst_dict["POP"]] = self.handle_pop
        self.branchtable[inst_dict["CALL"]] = self.handle_call
        self.branchtable[inst_dict["RET"]] = self.handle_ret

    def load(self, program_filepath):
        """Load a program into memory."""

        address = 0

        with open(program_filepath) as f:
            for line in f:
                line = line.split("#")
                line = line[0].strip()
        
                if line == '':
                    continue
                # line = int(line) # For the daily project we want int(line, 2) <- saying we want base 2 for binary
                self.ram[address] = int(line, 2)
        
                address += 1
            
    
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR


    def alu(self, op, reg_a, reg_b):
        
        opcodes = {
            0b10100000: "ADD",
            0b10100010: "MULT"
        }
        
        """ALU operations."""

        if opcodes[op] == "ADD":
            self.ir[reg_a] += self.ir[reg_b]
        elif opcodes[op] == "MULT":
            self.ir[reg_a] *= self.ir[reg_b]
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
            print(" %02X" % self.ir[i], end='')

        print()
        
    def operand_helper(self, inst, op_a=None, op_b=None):
        params = (inst & 11000000) >> 6
        if params == 0:
            self.branchtable[inst]()
        if params == 1:
            # print(params)
            # pass op_a into dispatch
            self.branchtable[inst](op_a)
        if params == 2:
            # pass both args into dispatch
            self.branchtable[inst](op_a, op_b)
            


    def handle_hlt(self):
        exit()
        
    def handle_ldi(self, op_a, op_b):
        reg_num = op_a
        value = op_b
        self.ir[reg_num] = value
        
    def handle_prn(self, op_a):
        reg_num = op_a
        value = self.ir[reg_num]
        print(value)
        
    def handle_mult(self, op_a, op_b):
        reg_numA = op_a
        reg_numB = op_b
        self.alu("MULT", reg_numA, reg_numB)
        
    def handle_push(self, op_a):
        self.ir[SP] -= 1
        reg_num = op_a
        value = self.ir[reg_num]
        address = self.ir[SP]
        self.ram_write(address, value)
    
    def handle_pop(self, op_a):
        reg_num = op_a
        address = self.ir[SP]
        value = self.ram[address]
        self.ir[reg_num] = value
        self.ir[SP] += 1
        
    def handle_call(self, op_a):
        # Compute return address
        self.ir[SP] -= 1
        return_addr = self.ir[SP]
        
        # Push on the stack
        self.ram_write(return_addr, self.pc + 2)
        
        # Set the PC to the vaue in the given register
        reg_num = self.ram_read(op_a)
        dest_addr = self.ir[reg_num]
        self.pc = dest_addr
        # exit()

    def handle_ret(self):
        # Pop return address from top of stack
        return_addr = self.ram_read(self.ir[SP])
        self.ir[SP] += 1
        
        # Set the PC
        self.pc = return_addr


    def run(self):
        """Run the CPU."""
        while True:
            inst = self.ram_read(self.pc)
            params = (inst & 11000000) >> 6
            use_alu = ((inst & 0b00100000) >> 5)
            set_pc = ((inst & 0b00010000) >> 4)
            if params >= 1:
                operand_a = self.ram_read(self.pc + 1)
            if params >= 2:
                operand_b = self.ram_read(self.pc + 2)
                
            if use_alu:
                self.alu(inst, operand_a, operand_b)
            
            elif inst in self.branchtable:
                self.operand_helper(inst, operand_a, operand_b)
            else:
                print("Unknown Instruction: ", hex(inst), bin(inst))
                exit()

                
            if set_pc:
                pass
            else:
                self.pc += (params + 1)
            # print(self.pc)
            # print(inst)
            self.trace()
