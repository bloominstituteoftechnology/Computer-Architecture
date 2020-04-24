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
        self.register = [0] * 8 # Setting up 8 general-purpose resgisters
        self.pc = 0 # Program Counter
        self.flag = 0
        self.register[7] = 0xF4
        self.configure_branchtable()
        self.configure_alu_branchtable()
        
        
    def configure_branchtable(self):
        self.branchtable = {}
        for key in inst_dict:
            value = inst_dict[key]
            self.branchtable[value] = getattr(self, "handle_" + key.lower())
            
            
    def configure_alu_branchtable(self):
        self.alu_branchtable = {}
        for key in alu_dict:
            value = alu_dict[key]
            self.alu_branchtable[value] = getattr(self, "alu_handle_" + key.lower())


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
        
        
    # ------------------==-=== Helper Methods ===-==------------------
     
    # OP
    def operand_helper(self, inst, op_a=None, op_b=None):
        params = (inst & 11000000) >> 6
        if params == 0:
            self.branchtable[inst]()
        if params == 1:
            # pass op_a into dispatch
            self.branchtable[inst](op_a)
        if params == 2:
            # pass both args into dispatch
            self.branchtable[inst](op_a, op_b)

    # ALU
    def alu_helper(self, inst, op_a, op_b):
        self.alu_branchtable[inst](op_a, op_b)
            

    # ------------------==-=== Op Methods ===-==------------------
    
    def handle_hlt(self):
        exit()
        
    def handle_ldi(self, op_a, op_b):
        reg_num = op_a
        value = op_b
        self.register[reg_num] = value
        
    def handle_prn(self, op_a):
        reg_num = op_a
        value = self.register[reg_num]
        print(value)
        
    def handle_push(self, op_a):
        self.register[SP] -= 1
        reg_num = op_a
        value = self.register[reg_num]
        address = self.register[SP]
        self.ram_write(address, value)
    
    def handle_pop(self, op_a):
        reg_num = op_a
        address = self.register[SP]
        value = self.ram[address]
        self.register[reg_num] = value
        self.register[SP] += 1
        
    def handle_call(self, op_a):
        # Compute return address
        self.register[SP] -= 1
        return_addr = self.register[SP]
        # 
        self.ram_write(return_addr, self.pc + 2)
        
        reg_num = self.ram_read(op_a)
        dest_addr = self.register[reg_num]
        self.pc = dest_addr

    def handle_ret(self):
        # Pop return address from top of stack
        return_addr = self.ram_read(self.register[SP])
        self.register[SP] += 1
        
        # Set the PC
        self.pc = return_addr
        
    # ------------------==-=== ALU Op Methods ===-==------------------

    def alu_handle_cmp(self, reg_a, reg_b):
        if self.register[reg_a] == self.register[reg_b]:
            self.flag = 0b1
        elif self.register[reg_a] > self.register[reg_b]:
            self.flag = 0b10
        else:
            self.flags = 0b100

    def alu_handle_mul(self, reg_a, reg_b):
        self.register[reg_a] *= self.register[reg_b]
        
    def alu_handle_add(self, reg_a, reg_b):
        self.register[reg_a] += self.register[reg_b]
        
    def alu_handle_sub(self, reg_a, reg_b):
        self.register[reg_a] -= self.register[reg_b]

    # ------------------==-=== Run Method ===-==------------------
    
    def run(self):
        """Run the CPU."""
        while True:
            inst = self.ram_read(self.pc)
            params = (inst & 0b11000000) >> 6
            use_alu = ((inst & 0b00100000) >> 5)
            set_pc = ((inst & 0b00010000) >> 4)
            
            operand_a = None
            operand_b = None
            
            if params >= 1:
                operand_a = self.ram_read(self.pc + 1)
            if params >= 2:
                operand_b = self.ram_read(self.pc + 2)
                
            if use_alu:
                # self.alu(inst, operand_a, operand_b)
                self.alu_helper(inst, operand_a, operand_b)
            
            elif inst in self.branchtable:
                self.operand_helper(inst, operand_a, operand_b)
            else:
                print("Unknown Instruction: ", hex(inst), bin(inst))
                exit()

                
            if set_pc:
                pass
            else:
                self.pc += (params + 1)
            
    
    # ------------------==-=== Debug Helper ===-==------------------        
    
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
            print(" %02X" % self.register[i], end='')

        print()
