"""CPU functionality."""

import sys

## ALU ops
ADD = 0b10100000 # 00000aaa 00000bbb
SUB = 0b10100001 # 00000aaa 00000bbb
MUL = 0b10100010 # 00000aaa 00000bbb
DIV = 0b10100011 # 00000aaa 00000bbb
MOD = 0b10100100 # 00000aaa 00000bbb
INC = 0b01100101 # 00000rrr
DEC = 0b01100110 # 00000rrr
CMP = 0b10100111 # 00000aaa 00000bbb
AND = 0b10101000 # 00000aaa 00000bbb
NOT = 0b01101001 # 00000rrr
OR  = 0b10101010 # 00000aaa 00000bbb
XOR = 0b10101011 # 00000aaa 00000bbb
SHL = 0b10101100 # 00000aaa 00000bbb
SHR = 0b10101101 # 00000aaa 00000bbb

## PC mutators
CALL = 0b01010000 # 00000rrr
RET  = 0b00010001 #
INT  = 0b01010010 # 00000rrr
IRET = 0b00010011 #
JMP  = 0b01010100 # 00000rrr
JEQ  = 0b01010101 # 00000rrr
JNE  = 0b01010110 # 00000rrr
JGT  = 0b01010111 # 00000rrr
JLT  = 0b01011000 # 00000rrr
JLE  = 0b01011001 # 00000rrr
JGE  = 0b01011010 # 00000rrr

## Other
NOP = 0b00000000
HLT = 0b00000001 
LDI  = 0b10000010 # 00000rrr iiiiiiii
LD   = 0b10000011 # 00000aaa 00000bbb
ST   = 0b10000100 # 00000aaa 00000bbb
PUSH = 0b01000101 # 00000rrr
POP  = 0b01000110 # 00000rrr
PRN  = 0b01000111 # 00000rrr
PRA  = 0b01001000 # 00000rrr

SP = 7  # stack pointer (SP) is always register 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add 256 bytes of memory and 
        # 8 general-purpose registers 
        # Also add properties for any internal registers you need, e.g. PC

        # memory = [0] * ???
        self.ram = [0] * 256
        # PC: Program Counter, address of the currently executing instruction
        self.PC = 0
        # IR: Instruction Register, contains a copy of the currently executing instruction
        self.IR = None

        # MAR: Memory Address Register, holds the memory address we're reading or writing
        # MDR: Memory Data Register, holds the value to write or the value just read
        # FL: Flags, see below


        # These registers only hold values between 0-255. After performing math on registers 
        # in the emulator, bitwise-AND the result with 0xFF (255) to keep the register values in that range.
        self.reg = [0] * 8
        # self.reg[0] = 0  # 0xFF or 0b1111 1111 or 256
        # self.reg[1] = 0
        # self.reg[2] = 0
        # self.reg[3] = 0
        # self.reg[4] = 0
        # self.reg[5] = 0 # interrupt mask (IM)
        # self.reg[6] = 0 # interrupt status (IS)
        self.reg[7] =  0xF4 # stack pointer (SP)
        # L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
        # G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
        # E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.
        # FL = 00000LGE
        self.FL = 0


    def load(self, programFile):
        """Load a program into memory."""
        print("loading:", programFile)
        address = 0
        try:
            with open(programFile) as f:
                for line in f:
                    num = line.split("#", 1)[0]

                    if num.strip() == '':  # ignore comment-only lines
                        continue

                    # print(int(num, 2))
                    self.ram[address] = int(num, 2)
                    address += 1
        except FileNotFoundError:
            print(f"ERROR: {programFile} not found")
            sys.exit(2)
        except IsADirectoryError:
            print(f"ERROR: {programFile} is a directory")
            sys.exit(3)

       
        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8  #130
        #     0b00000000,             #0
        #     0b00001000,             #8
        #     0b01000111, # PRN R0    #71
        #     0b00000000,             #0
        #     0b00000001, # HLT       #1
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # self.trace()
        running = True
        # running = False
        

        while running:
            # print("running")

            address = self.PC
            # print("address", address)

            command = self.ram[address]
            # print("instruction", instruction)
            self.IR = command
            # command = self.ram[self.IR]
            # print("command", command)

            ## ALU ops
            # ADD  10100000 00000aaa 00000bbb
                # ir = 0b10100000 AND
                # num_operands = (ir & 0b11000000) >> 6 # Do an AND mask and bit shift 6
                # num_operands => 2
            # SUB  10100001 00000aaa 00000bbb

            # MUL
            # MUL registerA registerB
            # Multiply the values in two registers together and store the result in registerA.
            # MUL  10100010 00000aaa 00000bbb
            if command == MUL:
                print("MUL")
                reg_a = self.ram[self.PC+1]
                reg_b = self.ram[self.PC+2]
                self.alu("MUL", reg_a, reg_b)
                self.PC += ((0b11000000 & command) >> 6) + 1
            # DIV  10100011 00000aaa 00000bbb
            # MOD  10100100 00000aaa 00000bbb
            # INC  01100101 00000rrr
            # DEC  01100110 00000rrr
            # CMP  10100111 00000aaa 00000bbb
            # AND  10101000 00000aaa 00000bbb
            # NOT  01101001 00000rrr
            # OR   10101010 00000aaa 00000bbb
            # XOR  10101011 00000aaa 00000bbb
            # SHL  10101100 00000aaa 00000bbb
            # SHR  10101101 00000aaa 00000bbb

            ## PC mutators
            # CALL 01010000 00000rrr
            # RET  00010001
            # INT  01010010 00000rrr
            # IRET 00010011
            # JMP  01010100 00000rrr
            # JEQ  01010101 00000rrr
            # JNE  01010110 00000rrr
            # JGT  01010111 00000rrr
            # JLT  01011000 00000rrr
            # JLE  01011001 00000rrr
            # JGE  01011010 00000rrr

            ## Other
            # NOP  00000000

            # HLT
            # Halt the CPU (and exit the emulator).
            # HLT 0b00000001 
            elif command == HLT:
                print("HLT")
                running = False

            # LDI register immediate
            # Set the value of a register to an integer.
            # LDI 0b10000010 00000rrr iiiiiiii
            elif command == LDI:
                print("LDI")

                register = self.ram[self.PC+1]
                integer = self.ram[self.PC+2]
                print("LDI register, integer", register, integer)
                self.reg[register] = integer
                # print("bit shift", ((0b11000000 & command) >> 6) + 1)
                self.PC += ((0b11000000 & command) >> 6) + 1
            
            # LD   10000011 00000aaa 00000bbb
            # ST   10000100 00000aaa 00000bbb

            # PUSH register
            # Push the value in the given register on the stack.
            # PUSH 01000101 00000rrr
            elif command == PUSH:
                print("PUSH")
                # 1. Decrement the `SP`.
                self.reg[SP] -= 1
                # 2. Copy the value in the given register to the address pointed to by SP.
                regnum = self.ram[self.PC+1]
                value = self.reg[regnum]
                self.ram[self.reg[SP]] = value
                # print("bit shift", ((0b11000000 & command) >> 6) + 1)
                self.PC += ((0b11000000 & command) >> 6) + 1

                # First decrement the stack pointer SP
                # copy the value in the register(Like reg[0]) into the place the SP is pointing
                # register[SP] -= 1            # Decrement SP
                # regnum = memory[pc + 1]       # Get the register number operand
                # value = register[regnum]     # get the value from taht register
                # memory[register[sp]] = value # store that value in memory at the SP
                # We might use ram read ram right functions
                # We start at F4
            # POP register
            # Pop the value at the top of the stack into the given register.
            # POP  01000110 00000rrr
            elif command == POP:
                print("POP")
                # 1. Copy the value from the address pointed to by `SP` to the given register.
                value = self.ram[self.reg[SP]]
                regnum = self.ram[self.PC + 1]
                self.reg[regnum] = value
                # 2. Increment `SP`.
                self.reg[SP] += 1
                # Copy the value from the stack pointer address into the given register
                # Increment the stack pointer
                # value = memory[register[SP]]
                # regnum = memory[pc + 1]
                # register[regnum] = value
                # register[SP] += 1
                self.PC += ((0b11000000 & command) >> 6) + 1

            # PRN
            # PRN register pseudo-instruction
            # Print numeric value stored in the given register.
            # Print to the console the decimal integer value that is stored in the given register.
            # PRN  01000111 00000rrr
            elif command == PRN:
                print("PRN")
                register = self.ram[self.PC+1]
                print(self.reg[register])
                self.PC += ((0b11000000 & command) >> 6) + 1

            # PRA  01001000 00000rrr

            else:
                print(f"unknown instruction {command}")
                sys.exit(1)

            address += 1
            # running = False
            # self.trace()
    
    def ram_read(self, address):
        """ ram_read() should accept the address to read and return the value stored there. """
        return self.ram[address]
        
    def ram_write():
        """ raw_write() should accept a value to write, and the address to write it to."""
        pass



# TRACE: 00 | 82 00 08 | 00 00 00 00 00 00 00 F4
# address 0
# running
# command 130
# LDI
# TRACE: 01 | 00 08 47 | 00 00 00 00 00 00 00 F4
# running
# command 130
# LDI
# TRACE: 02 | 08 47 00 | 00 00 00 00 00 00 00 F4
# running
# command 130
# LDI
# TRACE: 03 | 47 00 01 | 00 00 00 00 00 00 00 F4
# running
# command 130
# LDI
# TRACE: 04 | 00 01 00 | 00 00 00 00 00 00 00 F4
# running
# command 130
# LDI
# TRACE: 05 | 01 00 00 | 00 00 00 00 00 00 00 F4
# running
# command 130
# LDI
# TRACE: 06 | 00 00 00 | 00 00 00 00 00 00 00 F4
# running
