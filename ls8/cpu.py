"""CPU functionality."""

import sys

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

        program = ['0b'+line[:8] for line in program if line and line[0] in ['0', '1']]
        print(program)

        for instruction in program:
            self.ram[address] = eval(instruction)
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

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, val, addr):
        self.ram[addr] = val

    def run(self, debug=False):
        """Run the CPU."""
        running = True

        while running == True:
            if debug:
                self.trace()
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.ir = self.pc
            instruction = self.ram[self.ir]
            if instruction == 0b10100000: 
                pass   #ADD
            elif instruction == 0b10101000: 
                pass   #AND
            elif instruction == 0b01010000: 
                pass   #CALL register
            elif instruction == 0b01100110: 
                pass   #DEC
            elif instruction == 0b10100011: 
                pass   #DIV
            elif instruction == 0b00000001:         #HLT
                print("quit")
                running = False                                 
            elif instruction == 0b01100101: 
                pass   #INC
            elif instruction == 0b01010010: 
                pass   #INT
            elif instruction == 0b00010011: 
                pass   #IRET
            elif instruction == 0b01010101: 
                pass   #JEQ
            elif instruction == 0b01011010: 
                pass   #JGE
            elif instruction == 0b01010111: 
                pass   #JGT
            elif instruction == 0b01011001: 
                pass   #JLE
            elif instruction == 0b01011000: 
                pass   #JLT
            elif instruction == 0b01010100: 
                pass   #JMP
            elif instruction == 0b01010110: 
                pass   #JNE
            elif instruction == 0b10000011: 
                pass   #LD
            elif instruction == 0b10000010:         #LDI
                self.reg[operand_a] = operand_b                 
                self.pc += 3
            elif instruction == 0b10100100: 
                pass   #MOD
            elif instruction == 0b10100010:         #MUL
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]     
                self.pc += 3
            elif instruction == 0b00000000: 
                pass   #NOP
            elif instruction == 0b01101001: 
                pass   #NOT
            elif instruction == 0b10101010: 
                pass   #OR
            elif instruction == 0b01000110:         #POP
                self.reg[operand_a] = self.ram[self.reg[7]]
                self.reg[7] += 1
                self.pc += 2   
            elif instruction == 0b01001000: 
                pass   #PRA
            elif instruction == 0b01000111:         #PRN
                print(self.reg[operand_a])                      
                self.pc += 2
            elif instruction == 0b01000101:         #PUSH 
                self.reg[7] -= 1
                self.ram[self.reg[7]] = self.reg[operand_a]
                self.pc += 2   
            elif instruction == 0b00010001: 
                pass   #RET
            elif instruction == 0b10101100: 
                pass   #SHL
            elif instruction == 0b10101101: 
                pass   #SHR
            elif instruction == 0b10000100: 
                pass   #ST
            elif instruction == 0b10100001: 
                pass   #SUB
            elif instruction == 0b10101011: 
                pass   #XOR
            else:
                print("hmmmm ", instruction)
                exit()
        exit()




