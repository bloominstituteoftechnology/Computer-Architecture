"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [None] * 256
        self.gen_reg =  { 
                'R0': 0b1101010,
                'R1': 0b0000000,
                'R2': 0b0000000,
                'R3': 0b0000000,
                'R4': 0b0000000,
                'R5': 0b0000000,    # R5  interrupt mask
                'R6': 0b0000000,    # IS  interrupt status
                'R7': 0b0000000     # SP  stack pointer
            }
        self.int_reg =  { 
                        'PC': 0b0000000,    # PC program counter
                        'IR': 0b0000000,    # IR instruction register
                        'MAR': 0b0000000,   # MAR memory address register  
                        'MDR': 0b0000000,   # memory data register
                        'FL': 0b0000111,    # flags
                    }
        
        
        pass

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
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
        pass

    def dump_mem(self):
        print(f' mem size: {len(self.memory)}\n ****** DUMP  *******')
        
        for i in range(0, len(self.memory), 8):
            for j in range(i, len(self.memory), 8):
                end = i + 7
                # print(f' i {i }  :  j {i + 8}')
                print(f' {self.memory[i:end]}  mem {i } : {end} ')
                break        

    def read_gen_reg_b(self, reg):
        return bin(self.gen_reg[reg])   

    def read_gen_reg_h(self, reg):
        return hex(self.gen_reg[reg])

    def return_bin(self, reg_val):
        return bin(reg_val)

    def read_reg(self, reg_type, reg, base):
        if reg_type == 'gen_reg':
            if base == 'hex':
                return self.read_gen_reg_h(reg)
            if base == 'bin':
                return bin(self.gen_reg[reg])   
        elif reg_type == 'int_reg':
            if base == 'hex':
                return hex(self.int_reg[reg])
            if base == 'bin':
                return self.return_bin(self.int_reg[reg])            


cpu = CPU()
# print(f' memory is {cpu.memory} ')  
cpu.dump_mem()
print(cpu.read_gen_reg_b('R0'))
print(cpu.read_gen_reg_h('R0'))
print(cpu.read_reg('gen_reg', 'R0', 'hex'))
print(cpu.read_reg('gen_reg', 'R0', 'bin'))
print(cpu.read_reg('int_reg', 'FL', 'hex'))
