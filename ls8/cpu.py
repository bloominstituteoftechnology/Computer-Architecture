"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0] * 256
        self.gen_reg =  { 
                0 : 0b1101010,   # clear to 0b0 on boot
                1 : 0b0000000,
                2 : 0b0001000,
                3 : 0b0000000,
                4 : 0b0000000,
                5 : 0b0000000,    # R5  interrupt mask
                6 : 0b0000000,    # IS  interrupt status
                7 : 0b11110100     # SP  stack pointer   # init to 0b0 
            }
        self.int_reg =  { 
                        'PC': 0b0000000,    # PC program counter
                        'IR': 0b0000000,    # IR instruction register
                        'MAR': 0b0000000,   # MAR memory address register  
                        'MDR': 0b0000000,   # memory data register
                        'FL': 0b0000000,    # flags
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

    # def dump_mem(self):
    #     print(f' mem size: {len(self.memory)}\n ****** DUMP  *******')
        
    #     for i in range(0, len(self.memory), 8):
    #         for j in range(i, len(self.memory), 8):
    #             end = i + 7
    #             # print(f' i {i }  :  j {i + 8}')
    #             print(f' {self.memory[i:end]}  mem {i } : {end} ')
    #             break        

    def dump_mem(self):
        print(f' mem size: {len(self.memory)}\n ****** DUMP  *******')
        
        for i in range(len(self.memory) - 1, 0, -8):
            for j in range(len(self.memory) - 1, i - 8, -8):
                end = i - 7
                # print(f' i {i }  :  j {end}')
                print(f' {self.memory[end: i]}  mem {i } : {end} ')
                break    

    def read_gen_reg_b(self, reg):
        return bin(self.gen_reg[reg])   

    def read_gen_reg_h(self, reg):
        return hex(self.gen_reg[reg])

    def read_gen_reg_d(self, reg):
        bin_val = int(reg, 2)
        return self.gen_reg[bin_val]    

    def return_bin(self, reg_val):
        return bin(reg_val)

    def read_reg(self, reg_type = 'gen_reg', reg = '0', base = 'None'):
        # reg_v = f'self.reg_type'
        # print(f'reg_v {reg_v} ')
        # if base == 'hex':
        #     return hex(reg_v[reg])
        # elif base == 'bin':
        #     return bin(reg_v[reg])    
        # else:
        #      return reg_v    

        if reg_type == 'gen_reg':
            if base == 'hex':
                return self.read_gen_reg_h(reg)
            elif base == 'bin':
                return bin(self.gen_reg[reg])
            else:
                return self.gen_reg[reg]

        elif reg_type == 'int_reg':
            if base == 'hex':
                return hex(self.int_reg[reg])
            elif base == 'bin':
                return self.return_bin(self.int_reg[reg])
            else:
                return self.int_reg[reg]               

   



    def check_valid_h(self, val):
        test_val = str(int(val, 16))
        if test_val >= '0' and test_val <= '255':
            # val = int(val, 16)
            # print(type(val))
            return val

        else:
            return None            



    def write_reg_h(self, reg_type, reg, val):
        if self.check_valid_h(val): 
            if reg_type == 'gen_reg':    
                self.gen_reg[reg] = val
            elif reg_type == 'int_reg':
                self.int_reg[reg] = val
            else:
                return None    



            



cpu = CPU()
# print(f' memory is {cpu.memory} ')  
cpu.dump_mem()
print(cpu.read_gen_reg_b(0))   # 0b1101010
print(f' used a binary register val')
print(cpu.read_gen_reg_d('010'))

print(cpu.read_gen_reg_h(0))   # 0x6a
print(cpu.read_reg('gen_reg', 0, 'hex'))  # 0x6a
print(cpu.read_reg('gen_reg', 0, 'bin'))  # 0b1101010
print(cpu.read_reg('gen_reg', 0))     # 106
print(cpu.read_reg('int_reg', 'FL', 'hex'))  # 0x7
print(cpu.read_reg('int_reg', 'FL', 'bin'))  # 0b111
print(cpu.read_reg('int_reg', 'FL'))         # 7

print(cpu.check_valid_h('FF'))
print(cpu.check_valid_h('0c0'))
print(cpu.check_valid_h('0b010'))  # bin returns None
print(cpu.check_valid_h('122'))   # dec returns none

cpu.write_reg_h('int_reg', 'FL', 'EF')
print(cpu.read_reg('int_reg', 'FL'))

