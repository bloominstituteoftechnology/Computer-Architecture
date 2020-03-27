"""CPU functionality."""

import sys
from time import time

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256        # Memory
        self.reg = [0] * 8          # General-purpose numeric registers R0-R7
        self.pc = 0                 # Program Counter
        self.ir = 0                 # Instruction Register
        self.mar = 0                # Memory Address Register
        self.mdr = 0                # Memory Data Register
        self.fl = [0] * 8           # 8-bit Flags Register
        
        self.reg[7] = 0xF4          # set stack pointer


    def load(self, filepath, *args):
        """Load a program into memory."""

        address = 0

        with open(filepath, 'r') as f:
            program = f.read().splitlines()
            f.close()

        program = [line[:8] for line in program if line and line[0] in ['0', '1']]
        print(program)

        for instruction in program:
            self.ram[address] = int(instruction, 2)
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(self.fl)
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, val, addr):
        self.ram[addr] = val

    def run(self, debug=False):
        """Run the CPU."""
        global running
        running = True

        handler = Branch(cpu=self)
        timing = time()
        while running == True:
            if debug:
                self.trace()
            if time() - timing  >= 1:
                self.reg[6] = 1
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.ir = self.pc
            instruction = self.ram[self.ir]
            try:
                handler.run(instruction, operand_a, operand_b)
            except Exception as e:
                print("hmmmm ", bin(instruction), e, operand_a, operand_b)
                exit()
            masked_interrupts = self.reg[5] & self.reg[6]
            # for i in range(8):
            #     interrupt_happened = ((masked_interrupts >> i) & 1) == 1
            #     if interrupt_happened:
            #         self.fl[6] = 0
            #         self.reg[7] -= 1
            #         self.ram[self.reg[7]] = self.pc 
            #         self.reg[7] -= 1
            #         self.ram[self.reg[7]] = self.fl
            #         for j in range(7):
            #             self.reg[7] -= 1
            #             self.ram[self.reg[7]] = self.reg[j]
            #         self.pc = self.ram[i]
            #         break

        exit()

class Branch:

    def __init__(self, cpu):
        self.cpu = cpu
        self.branchtable = {}
        self.branchtable[0b10100000] = self.handle_ADD
        self.branchtable[0b10110000] = self.handle_ADDI
        self.branchtable[0b10101000] = self.handle_AND
        self.branchtable[0b01010000] = self.handle_CALL
        self.branchtable[0b10100111] = self.handle_CMP
        self.branchtable[0b01100110] = self.handle_DEC 
        self.branchtable[0b10100011] = self.handle_DIV
        self.branchtable[0b00000001] = self.handle_HLT                              
        self.branchtable[0b01100101] = self.handle_INC 
        self.branchtable[0b01010010] = self.handle_INT 
        self.branchtable[0b00010011] = self.handle_IRET 
        self.branchtable[0b01010101] = self.handle_JEQ
        self.branchtable[0b01011010] = self.handle_JGE
        self.branchtable[0b01010111] = self.handle_JGT 
        self.branchtable[0b01011001] = self.handle_JLE     
        self.branchtable[0b01011000] = self.handle_JLT     
        self.branchtable[0b01010100] = self.handle_JMP   
        self.branchtable[0b01010110] = self.handle_JNE   
        self.branchtable[0b10000011] = self.handle_LD
        self.branchtable[0b10000010] = self.handle_LDI                
        self.branchtable[0b10100100] = self.handle_MOD   
        self.branchtable[0b10100010] = self.handle_MUL     
        self.branchtable[0b00000000] = self.handle_NOP  
        self.branchtable[0b01101001] = self.handle_NOT 
        self.branchtable[0b10101010] = self.handle_OR 
        self.branchtable[0b01000110] = self.handle_POP
        self.branchtable[0b01001000] = self.handle_PRA 
        self.branchtable[0b01000111] = self.handle_PRN                     
        self.branchtable[0b01000101] = self.handle_PUSH 
        self.branchtable[0b00010001] = self.handle_RET 
        self.branchtable[0b10101100] = self.handle_SHL 
        self.branchtable[0b10101101] = self.handle_SHR 
        self.branchtable[0b10000100] = self.handle_ST 
        self.branchtable[0b10100001] = self.handle_SUB 
        self.branchtable[0b10101011] = self.handle_XOR
    
    def handle_ADD(self, instruction, operand_a, operand_b):
        self.cpu.alu("ADD", operand_a, operand_b)
    def handle_ADDI(self, instruction, operand_a, operand_b):
        self.cpu.reg[operand_a] += operand_b
    def handle_AND(self, instruction, operand_a, operand_b):
        pass
    def handle_CALL(self, instruction, operand_a, operand_b):
        self.cpu.reg[7] -= 1
        self.cpu.ram[self.cpu.reg[7]] = operand_a
        #TODO
    def handle_CMP (self, instruction, operand_a, operand_b):
        reg_a = self.cpu.reg[operand_a]
        reg_b = self.cpu.reg[operand_b]
        if reg_a == reg_b:
            self.cpu.fl[7] = 1
        else:
            self.cpu.fl[7] = 0

        if reg_a < reg_b:
            self.cpu.fl[5] = 1
        else:
            self.cpu.fl[5] = 0

        if reg_a > reg_b:
            self.cpu.fl[6] = 1
        else:
            self.cpu.fl[6] = 0
    def handle_DEC (self, instruction, operand_a, operand_b):
        pass
    def handle_DIV (self, instruction, operand_a, operand_b):
        pass
    def handle_HLT(self, instruction, operand_a, operand_b):
        print("quit")
        global running
        running = False   
    def handle_INC (self, instruction, operand_a, operand_b):
        pass
    def handle_INT (self, instruction, operand_a, operand_b):
        pass
    def handle_IRET(self, instruction, operand_a, operand_b):
        pass
    def handle_JEQ(self, instruction, operand_a, operand_b):
        if self.cpu.fl[7]:
            self.cpu.pc = self.cpu.reg[operand_a]
        else:
            self.cpu.pc += 2
    def handle_JGE(self, instruction, operand_a, operand_b):
        pass
    def handle_JGT (self, instruction, operand_a, operand_b):
        pass
    def handle_JLE (self, instruction, operand_a, operand_b):
        pass
    def handle_JLT (self, instruction, operand_a, operand_b):
        pass
    def handle_JMP (self, instruction, operand_a, operand_b):
        self.cpu.pc = self.cpu.reg[operand_a]
    def handle_JNE (self, instruction, operand_a, operand_b):
        if not self.cpu.fl[7]:
            self.cpu.pc = self.cpu.reg[operand_a]
        else:
            self.cpu.pc += 2
    def handle_LD (self, instruction, operand_a, operand_b):
        pass
    def handle_LDI(self, instruction, operand_a, operand_b):
        self.cpu.reg[operand_a] = operand_b 
    def handle_MOD (self, instruction, operand_a, operand_b):
        self.cpu.alu("MOD", operand_a, operand_b)
    def handle_MUL(self, instruction, operand_a, operand_b):
        self.cpu.reg[operand_a] = self.cpu.reg[operand_a] * self.cpu.reg[operand_b]
    def handle_NOP (self, instruction, operand_a, operand_b):
        pass
    def handle_NOT (self, instruction, operand_a, operand_b):
        self.cpu.alu("NOT", operand_a, operand_b)
    def handle_OR (self, instruction, operand_a, operand_b):
        self.cpu.alu("OR", operand_a, operand_b)
    def handle_POP(self, instruction, operand_a, operand_b):
        self.cpu.reg[operand_a] = self.cpu.ram[self.cpu.reg[7]]
        self.cpu.reg[7] += 1
    def handle_PRA(self, instruction, operand_a, operand_b):
        pass
    def handle_PRN(self, instruction, operand_a, operand_b):
        print(self.cpu.reg[operand_a]) 
    def handle_PUSH(self, instruction, operand_a, operand_b):
        self.cpu.reg[7] -= 1
        self.cpu.ram[self.cpu.reg[7]] = self.cpu.reg[operand_a]  
    def handle_RET(self, instruction, operand_a, operand_b):
        pass
    def handle_SHL(self, instruction, operand_a, operand_b):
        self.cpu.alu("SHL", operand_a, operand_b)
    def handle_SHR(self, instruction, operand_a, operand_b):
        self.cpu.alu("SHR", operand_a, operand_b)
    def handle_ST(self, instruction, operand_a, operand_b):
        self.cpu.ram[self.cpu.reg[operand_a]] = self.cpu.reg[operand_b]
    def handle_SUB(self, instruction, operand_a, operand_b):
        pass
    def handle_XOR(self, instruction, operand_a, operand_b):
        self.cpu.alu("XOR", operand_a, operand_b)



    def run(self, instruction, OP1, OP2):
        try:
            # run instruction
            # print("input:", bin(instruction), OP1, OP2)
            self.branchtable[instruction](instruction, OP1, OP2)
            
            # increment program counter if necessary
            if instruction & 0b00010000 == 0b00000000:
                if instruction < 64:
                    self.cpu.pc += 1
                if instruction > 64 and instruction <= 127:
                    self.cpu.pc += 2
                if instruction > 127:
                    self.cpu.pc += 3
        except Exception as e:
            print("exception:", e)
            exit()

