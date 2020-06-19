"""CPU functionality."""


import sys

# setup consts for op codes
LDI = 0b10000010  # LDI R0,8 130
PRN = 0b01000111  # PRN R0, 71
HLT = 0b00000001  # HLT
MUL = 0b10100010  # Multiply
ADD = 0b10100000  # Addition
PUSH = 0b01000101
POP = 0b01000110
RET = 0b00010001
CALL = 0b01010000


SP = 7  # SP assign to be use R7 per spec

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Step 1 creating a 256 byts of memory and
        # 8 general-purpose registers also
        # add PC program counter
        
        self.ram = [0] * 256  # create 256 bites memeory
        self.reg = [0] * 8 # 8 bit register
        self.pc = 0 # program counter PC

        # Step 2 add ram methods
        # CPU contains two internal registers used for memory operation:
        # they are: Memory Address Register(MAR) and Memeory Data Register(MDR)
        # MAR contains the address that is being read or written to
        # MDR contains the data that was read or
        # the data to write .
        
    # RAM_READ should accept  the address to read and
    # return the value stored there.
    def ram_read(self, mar):
        return self.ram[mar]

    # RAM_WRITE should accept a value to write, and
    # the address to write it to.
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0

            # open file with open()
            with open(filename) as f:
                for line in f:
                    better_line = line.strip().split('#')  # strip the white space
                    value = better_line[0].strip() # take the string number

                    if value != '':
                        # string to integer
                        num = int(value, 2) # converting a binary string to a number
                        self.ram[address] = num
                        address += 1
                    else:
                        continue
        
        except FileExistsError:
            print('ERRL file no found')
            sys.exit(2)



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        # Addition
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # Sutraction
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        # Multiplication
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # Division
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
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

    def run(self, filename):
        """Run the CPU."""
        # load the program into the memory
        self.load(filename)

        # run the program
        while True:
            # program counter
            pc = self.pc
            # Operation to start
            op = self.ram_read(pc)

            # Instruction register
            if op == LDI:
                self.reg[self.ram_read(pc + 1)] = self.ram_read(pc + 2)
                self.pc += 3
            elif op == PRN:
                print(self.reg[self.ram_read(pc + 1)])
                self.pc +=2

            # multiplication
            elif  op == MUL:
                # access 2 registers and mul
                a = self.ram_read(pc + 1)
                b = self.ram_read(pc + 2)
                # call ALU
                self.alu('MUL', a, b)
                # move to prog counter
                self.pc += 3

            # addition
            elif op == ADD:
                # access register and add them
                a = self.ram_read(pc + 1)
                b = self.ram_read(pc + 2)
                # call the ALU
                self.alu("ADD", a, b)
                self.pc += 3

            # system stack
            elif op == PUSH:
                # decremating
                self.reg[SP] -= 1
                # grab the current MA SP point to
                stack_address = self.reg[SP]
                # get a register number from the instruction
                register_num = self.ram_read(pc + 1)
                # get value out of the register
                value = self.reg[register_num]
                # werite the register value to a postition in the stack
                self.ram_write(stack_address, value)
                self.pc += 2

            # system stack
            elif op == POP:
                # get the value from the memory
                stack_value = self.ram_read(self.reg[SP])
                # get the register number from instaruction in memory
                register_num = self.ram_read(pc + 1)
                # set the value of a register to the value held in the stack
                self.reg[register_num] = stack_value
                # increment SP
                self.reg[SP] += 1 
                self.pc += 2

            # subroutine CALLS
            elif op == CALL:
                # decrement the SP
                self.reg[SP] -= 1
                # get the current MA that SP points to 
                stack_address = self.reg[SP]
                # get return MA
                returned_address = pc + 2
                # add return address to the stack
                self.ram_write(stack_address, returned_address)
                # set PC to the value in regirster
                register_num = self.ram_read(pc + 1)
                self.pc = self.reg[register_num]

            elif op == RET:
                # pop returnr MA off the stack
                # store poped MA in the PC
                self.pc = self.ram_read(self.reg[SP])
                self.reg[SP] += 1

            elif op == HLT:
                sys.exit(1)

            else:
                print("ERR: Unknown input:\t", op)
                sys.exit(1)
if len(sys.argv) == 2:
    filename = sys.argv[1]

    c = CPU()
    c.run(filename)
else:
    # err message
    print("""ERR: PLEASE PROVIDE A FILE NAME\n
    ex python cpu.py examples/FILENAME""")
    sys.exit(2)
            #`IR`: Instruction Register, contains a copy of the currently executing instruction
#filename = 'examples/print8.ls8'
