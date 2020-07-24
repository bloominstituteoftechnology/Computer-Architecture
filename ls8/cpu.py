"""CPU functionality."""
import sys

print(sys.argv[1])
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # internal registers
        self.PC = 0
        self.IR = None
        self.FL = None
        self.MAR = None
        self.MDR = None
        # others
        self.ram = [None] * 256
        self.reg = [0] * 8
        self.running = True
        # stack pointer
        self.sp = 7

        # decimal conversions of instructions
        LDI = 130
        MUL = 162
        PRN = 71
        HLT = 1
        PUSH = 69
        POP = 70
        ADD = 160
        CALL = 80
        RET = 17
        CMP = 167
        JEQ = 85
        JNE = 86
        JMP = 84

        # initialize branchtable to hold functions
        self.branchtable = {}
        self.branchtable[LDI] = self.ldi
        self.branchtable[ADD] = self.add
        self.branchtable[MUL] = self.mul
        self.branchtable[PRN] = self.prn
        self.branchtable[HLT] = self.hlt
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        self.branchtable[CMP] = self.cmp
        self.branchtable[JEQ] = self.jeq
        self.branchtable[JNE] = self.jne
        self.branchtable[JMP] = self.jmp

    def run(self):
        """Run the CPU."""
        # read the memory address that is stored in register 
        # self.ram[self]
        # store the result of the above in IR
        # check if op code is in the IR
        # self.IR = self.ram_read(self.PC)
        # self.branchTavle[self.IR]()
        # check the current instruction and evaluates it
        while self.running:
            self.IR = self.ram_read(self.PC)
            self.branchtable[self.IR]()
        
    def ram_read(self, address):
        self.MAR = address
        self.MDR = self.ram[self.MAR]
        return self.MDR

    def ram_write(self, address, value):
        self.MAR = address
        self.MDR = value
        self.ram[self.MAR] = self.MDR

    def ldi(self):
        '''
        an LDI instruction takes two operands loaded into ram
        '''
        # get operands
        
        operand_a = self.ram_read(self.PC+1)
        operand_b = self.ram_read(self.PC+2)
        # load to register
        self.reg[operand_a] = operand_b
        # increment program counter by 3 to skip one and three
        self.PC += 3

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("usage: file ls8.py")
            sys.exit(1)

        filename = sys.argv[1];
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()

                    if num == '':
                        continue

                    # convert the binary strings to integer values
                    val = int(num, 2)
                    # then store in the ram
                    self.ram[address] = val
                    # move to the next line
                    address += 1
                    # print(line)
        except FileNotFoundError:
            print("File not found")
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            self.FL = 0x00
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = self.FL | 0b00000001
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = self.FL | 0b00000100
            if self.reg[reg_a] > self.reg[reg_b]:
                self.FL = self.FL | 0b00000010
        elif op == "ADD":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
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

    def add(self):
        # get operands
        operand_a = self.ram_read(self.PC+1)
        operand_b = self.ram_read(self.PC+2)
        # call alu function to handle the arithmetic
        self.alu('ADD', operand_a, operand_b)
        # increment program counter by 3
        self.PC += 3

    def mul(self):
        # load operands with their respective register
        operand_a = self.ram_read(self.PC+1)
        operand_b = self.ram_read(self.PC+2)
        # call alu function to handle the arithmetic
        self.alu('MUL', operand_a, operand_b)
        # increment program counter by 3
        self.PC += 3

    def prn(self):
        # get operand
        operand_a = self.ram_read(self.PC+1)
        # print the value
        print(self.reg[operand_a])
        # increment program counter by 2
        self.PC += 2

    def hlt(self):
        # set running to False
        self.running = False

    def push(self):
        # get the register address from ram
        reg = self.ram_read(self.PC+1)
        # get the value from register
        val = self.reg[reg]
        # decrement stack pointer
        self.reg[self.sp] -= 1
        # set new value to ram
        self.ram[self.reg[self.sp]] = val
        # increment program counter by 2
        self.PC += 2

    def pop(self):
        # get the register address from ram
        reg = self.ram_read(self.PC+1)
        # get the value from register
        val = self.ram_read(self.reg[self.sp])
        # increment stack pointer
        self.reg[self.sp] += 1
        # set new value to reg
        self.reg[reg] = val
        # increment program counter by 2
        self.PC += 2

    def call(self):
        # setup
        reg = self.ram_read(self.PC + 1)
        # CALL
        self.reg[self.sp] -= 1  # decrement sp
        # push pc + 2 on to the stack
        self.ram_write(self.reg[self.sp], self.PC + 2)
        # set pc to subroutine
        self.PC = self.reg[reg]

    def ret(self):
        self.PC = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def cmp(self):
        reg_a = self.ram_read(self.PC+1)
        reg_b = self.ram_read(self.PC+2)
        # call alu function to handle the arithmetic
        self.alu('CMP', reg_a, reg_b)
        self.PC += 3

    def jeq(self):
        reg_a = self.ram_read(self.PC+1)
        operand_a = self.reg[reg_a]
        if self.FL == 1:
            self.PC = operand_a
        else:
            self.PC += 2

    def jne(self):
        reg_a = self.ram_read(self.PC+1)
        operand_a = self.reg[reg_a]
        if self.FL == 0:
            self.PC = operand_a
        else:
            self.PC += 2

    def jmp(self):
        reg_a = self.ram_read(self.PC+1)
        operand_a = self.reg[reg_a]
        self.PC = operand_a

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

