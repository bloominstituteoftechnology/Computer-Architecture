"""CPU functionality."""
 
import sys
LDI = 0b10000010 # set a specific register to specific value 
PRN = 0b01000111 # print number
HLT = 0b00000001 # halt the Program
MUL = 0b10100010 # multiply two registers together and store a result in register A

PUSH = 0b01000101  # push instraction on to the stack
POP = 0b01000110   # instraction in to the stack 
CALL = 0b01010000 # jump to a subsroutine address
RET = 0b00010001 # go to return address after subroutine is done
# ADD = 0b10100000
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #! construct RAM + REG + PC 
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0       # program counter is the address of currently executing instructions 
        self.fl = 0 #flags
        self.bt = {        
            LDI: self.op_ldi,
            PRN: self.op_prn,
            HLT: self.op_hlt,
            # ADD: self.op_add,
            # MUL: self.op_mul,
            # POP: self.op_pop,
            # PUSH: self.op_push,
            # CALL: self.op_call,
            # RET: self.op_ret,
            
        }
        self.lines = 0


    #! instruction handlers
    def op_hlt(self): #! HLT
        sys.exit(0)

    def op_prn(self):
        reg = self.ram_read(self.pc + 1) #! PRN
        num = self.register[reg]
        print(num)
        self.pc += 2


    def op_ldi(self):
        reg = self.ram_read(self.pc + 1) #! LDI
        num = self.ram_read(self.pc + 2)
        self.register[reg] = num
        self.pc += 3

    def ram_read(self, mar):
        #mar = memory address register // mdr = memory data register 
        #read the address and write out the number (data) 
        mdr = self.ram[mar]
        return mdr
    
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    # print(line)
                    comment_split = line.strip().split("#")
                    # print(comment_split) # [everything before #, everything after #]
                    value = comment_split[0].strip()
                    # print(value, type(value))
                    if value == '':
                        continue
                    self.lines += 1
                    instruction = int(value, 2)
                    # populate a memory array
                    self.ram[address] = instruction# changing the command to int because it binary to change to the base 10 int
                    address += 1
        
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

        
        

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
        for _ in range(self.lines):
            ir = self.ram_read(self.pc)
            self.bt[ir]()
