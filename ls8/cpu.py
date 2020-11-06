"""CPU functionality."""
import sys
import os.path
HLT  = 0b00000001
LDI  = 0b10000010
PRN  = 0b01000111
MUL  = 0b10100010
PUSH = 0b01000101
POP  = 0b01000110
CALL = 0b01010000
RET  = 0b00010001
ADD  = 0b10100000
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        # 256-byte RAM, each element is 1 byte (can only store integers 0-255)
        self.ram = [0] * 256
        
        # R0-R7: 8-bit general purpose registers, R5 = interrupt mask (IM), 
        # R6 = interrupt status (IS), R7 = stack pointer (SP)
        self.reg = [0] * 8
        # Internal Registers
        self.pc = 0 # Program Counter: address of the currently executing instruction
        self.ir = 0 # Instruction Register: contains a copy of the currently executing instruction
        self.mar = 0 # Memory Address Register: holds the memory address we're reading or writing
        self.mdr = 0 # Memory Data Register: holds the value to write or the value just read
        self.fl = 0 # Flag Register: holds the current flags status
        self.halted = False
        # Initialize the Stack Pointer
        # SP points at the value at the top of the stack (most recently pushed), or at address F4 if the stack is empty.
        self.reg[7] = 0xF4 # 244 # int('F4', 16)
        # Setup Branch Table
        self.branchtable = {}
        self.branchtable[HLT] = self.execute_HLT
        self.branchtable[LDI] = self.execute_LDI
        self.branchtable[PRN] = self.execute_PRN
        self.branchtable[MUL] = self.execute_MUL
        self.branchtable[PUSH] = self.execute_PUSH
        self.branchtable[POP] = self.execute_POP
        self.branchtable[CALL] = self.execute_CALL
        self.branchtable[RET] = self.execute_RET
        self.branchtable[ADD] = self.execute_ADD

    # Property wrapper for SP (Stack Pointer)
    
    @property
    def sp(self):
        return self.reg[7]
    
    @sp.setter
    def sp(self, a):
        self.reg[7] = a & 0xFF

    # Computed Properties

    @property
    def operand_a(self):
        return self.ram_read(self.pc + 1)

    @property
    def operand_b(self):
        return self.ram_read(self.pc + 2)

    @property
    def instruction_size(self):
        return ((self.ir >> 6) & 0b11) + 1
    
    def instruction_sets_pc(self):
        return ((self.ir >> 4) & 0b0001) == 1
    
    # CPU Methods

    def ram_read(self, mar):
        if mar >= 0 and mar < len(self.ram):
            return self.ram[mar]
        else:
            print(f"Error: Attempted to read from memory address: {mar}, which is outside of the memory bounds.")
            return -1
    def ram_write(self, mar, mdr):
        if mar >= 0 and mar < len(self.ram):
            self.ram[mar] = mdr & 0xFF
        else:
            print(f"Error: Attempted to write to memory address: {mar}, which is outside of the memory bounds.")
    def load(self):
        """Load a program into memory."""
        address = 0
        file_name = "ls8/examples/call.ls8"
       # file_path = os.path.join(os.path.dirname(__file__), file_name)
        try:
            with open(file_name) as f:
                for line in f:
                    num = line.split("#")[0].strip() # "10000010"
                    try:
                        instruction = int(num, 2)
                        self.ram[address] = instruction
                        address += 1
                    except:
                        continue
        except:
            print(f'Could not find file named: {file_name}')
            sys.exit(1)
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
    # Run Loop
    def run(self):
        """Run the CPU."""
        while not self.halted:
# Fetch the next instruction (it is decoded lazily using computed properties)
            self.ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if not self.instruction_sets_pc():
                self.pc += self.instruction_size
            #self.execute_instruction(operand_a, operand_b)
            # Execute the instruction
            print(bin(self.ir))
            print(self.pc)
            if self.ir in self.branchtable:
                self.branchtable[self.ir]()
            else:
                print(f"Error: Could not find instruction: {self.ir} in branch table.")
                sys.exit(1)

            # Increment the program counter if necessary
            if not self.instruction_sets_pc:
                self.pc += self.instruction_size

    def execute_instruction(self, operand_a, operand_b):
        if self.ir in self.branchtable:
            self.branchtable[self.ir](operand_a, operand_b)
        else:
            print(f"Error: Could not find instruction: {self.ir} in branch table.")
            sys.exit(1)
    
    # Define operations to be loaded into the branch table
    def execute_HLT(self):
        self.halted = True
    
    def execute_LDI(self):
        self.reg[self.operand_a] = self.operand_b
    
    def execute_PRN(self):
        print(self.reg[self.operand_a])
    
    def execute_MUL(self):
        self.reg[self.operand_a] *= self.reg[self.operand_b]
    
    def execute_PUSH(self):
        self.sp -= 1
        self.mdr = self.reg[self.operand_a]
        self.ram_write(self.sp, self.mdr)
    
    def execute_POP(self):
        self.mdr = self.ram_read(self.sp)
        self.reg[self.operand_a] = self.mdr
        self.sp += 1

    def execute_CALL(self):
        self.sp -= 1
        self.ram_write(self.sp, self.pc + self.instruction_size)
        print(self.instruction_size)
        self.pc = self.reg[self.operand_a]

    def execute_RET(self):
        self.pc = self.ram_read(self.sp)
        self.sp += 1

    def execute_ADD(self):
        self.reg[self.operand_a] += self.reg[self.operand_b] 
