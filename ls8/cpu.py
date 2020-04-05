"""CPU functionality."""

import sys
# Binary equivalents of instructions
HLT = 0b00000001
MUL = 0b10100010
LDI = 0b10000010
PRN = 0b01000111
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


sp = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
         # 8 general-purpose registers
        self.reg = [0] * 8
        # hold 256 bytes of memory
        self.ram = [0] * 256
        self.pc = 0
        self.halted = False
        self.flag = 0b00000000

        self.branchtable = {}

        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret
        self.branchtable[ADD] = self.handle_add
        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[JEQ] = self.handle_jeq
        self.branchtable[JNE] = self.handle_jne

        # set the stack pointer to be at this position
        self.reg[sp] = self.ram[0xF4]


    def handle_hlt(self):
        self.halted = True
    
    def handle_ldi(self):
        # sets a specified register to a specified value

        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
        self.pc += 3
    
    # Print numeric value stored in the given register
    def handle_prn(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2
    
    def handle_mul(self):
        num_1 = self.ram_read(self.pc + 1)
        num_2 = self.ram_read(self.pc + 2)
        self.alu(MUL, num_1, num_2)
        self.pc +=3
    
    def handle_push(self):
        # setup
        reg_num = self.ram_read(self.pc + 1)
        value = self.reg[reg_num]

        # push
        self.reg[sp] -= 1
        self.ram[self.reg[sp]] = value
        self.pc += 2
    
    def handle_pop(self):
        # setup
        reg_num = self.ram_read(self.pc + 1)
        # Set the value at the memory to the sp
        value = self.ram[self.reg[sp]]

        # pop
        # Copy the value from the address pointed to by `SP` to the given register.
        self.reg[reg_num] = value
        self.reg[sp] += 1
        self.pc += 2
    def handle_call(self):
        reg_num = self.ram_read(self.pc + 1)
        self.reg[sp] -= 1
        self.ram[self.reg[sp]] = self.pc + 2
        self.pc = self.reg[reg_num]
    
    def handle_ret(self):
        # pop from top of the stack and store in the pc
        self.pc = self.ram[self.reg[sp]]
        self.reg[sp] += 1

    def handle_add(self):
        num_1 = self.ram_read(self.pc + 1)
        num_2 = self.ram_read(self.pc + 2)
        self.alu(ADD, num_1, num_2)
        self.pc += 3

    def handle_cmp(self):
        num_1 = self.ram_read(self.pc + 1)
        num_2 = self.ram_read(self.pc + 2)
        self.alu(CMP, num_1, num_2)
        self.pc += 3

    def handle_jmp(self):
        reg_num = self.ram_read(self.pc + 1)
        # set the pc to the address in the register
        self.pc = self.reg[reg_num]

    def handle_jeq(self):
        reg_num = self.ram_read(self.pc + 1)
        if self.flag == 1:
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def handle_jne(self):
        reg_num = self.ram_read(self.pc + 1)
        if self.flag != 1:
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2
        
    def ram_read(self, address):
        # memory address register
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self,file_name):
        """Load a program into memory."""

        try:
            address = 0
            file_name = sys.argv[1]
            with open(file_name) as file:
                for line in file:
                    comment_split = line.split("#")[0]
                    num = comment_split.strip()
                
                    if num == "":
                        continue

                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1
                
        except FileNotFoundError:
            print("file not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == CMP:
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
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
        while  not self.halted:
            ir = self.ram[self.pc]

            if ir == 0 or None:
                print("I did not understand this command")
                sys.exit(1)

            self.branchtable[ir]()

print(sys.argv[1])