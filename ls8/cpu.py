"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # get the top of the stack
        self.sp_address = 7
        # total CPU memory
        self.ram = [0] * 256
        # lambda CPU to print 8
        self.reg = [0] * 8
        # Program Counter, address of the currently executing instruction
        self.pc = self.reg[0]
        #LDI = memory address2 has address of memory address 1 and separately memory address 1 has some value,
        # so here we are trying to retrieve a data indirectly. 
        # LDI = 1
        # PRN = 2
        # HLT = 3
        # Instruction Registry, contains a copy of the currently executing instruction
        self.instruction_registry = 0 
        # Instruction Registry Dictionary: (This is step 1 to building the handler, similar to program load) 
        self.instruction_registry = {
            0b00000001: self.HLT_HANDLER, # 1
            0b10000010: self.LDI_HANDLER, # 130
            0b01000111: self.PRN_HANDLER, 
            0b10100010: self.MUL_HANDLER,
            0b01000110: self.POP_HANDLER,
            0b01000101: self.PUSH_HANDLER
        }
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
    def MUL_HANDLER(self):
        # get two values:
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        # ALU MUL
        self.alu("MUL", reg_a, reg_b)
        # then advance the counter 
        self.pc += 3
    #stop the program:
    def HLT_HANDLER(self):
        sys.exit(0)
    # read stuff frommemory
    def LDI_HANDLER(self):
        # Get the address and value from Memory
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        # Write it to the registry
        self.reg[address] = value
        # Advance the Program Counter
        self.pc += 3

    def PRN_HANDLER(self):
        # Get the address
        address = self.ram_read(self.pc + 1)
        # Print the value
        print(self.reg[address])
        # Advance the Program Counter
        self.pc += 2
    
    def POP_HANDLER(self):
        # get the value from memory with stack pointer(cursor)
        address = self.ram_read(self.pc + 1)
        val = self.ram[self.reg[7]]
        # now copy the val to the registry
        self.reg[address] = val
        # increment the pointer
        self.reg[7] += 1
        # then the pc
        self.pc += 2
    
    def PUSH_HANDLER(self):
        # get the value from memory with stack pointer(cursor)
        address = self.ram_read(self.pc + 1)
        val = self.reg[address]
        
        # decrement the pointer
        self.reg[7] -= 1
        # copy it to the stack
        self.ram[self.reg[7]] = val
        # then the pc
        self.pc += 2
    
    def CALL_HANDLER(self, reg_a, reg_b):
        #compute pc value and push onto stack:
        self.reg[self.sp_address] -= 1
        self.ram[self.reg[self.sp_address]] = self.pc + 2
        # set the pc to the value in the given register
        self.pc = self.reg[reg_a]

    def load(self, file):
        """Load a program into memory."""
        try:
            with open(file) as f:

                address = 0
                for line in f:
                # split the lines with coments
                    comments = line.strip().split('#')
                # take the first element of the line
                    strings = comments[0].strip()
                # skip empty lines
                    if strings == "":
                        continue
                # convert the line to an int
                    int_value = int(strings, 2)
                # save to memory
                    self.ram[address] = int_value
                # increment the adress counter
                    address += 1
                # then close the file
                f.close()
        # exception for try block if file npot found
        except FileNotFoundError:
            print("there are no requested files")
            sys.exit(2)
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in file:
            self.ram[address] = instruction
            address += 1


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
        '''
        * `LDI`: load "immediate", store a value in a register, or "set this register to
        this value".
        * `PRN`: a pseudo-instruction that prints the numeric value stored in a
        register.
        * `HLT`: halt the CPU and exit the emulator.
        '''
        while True:
            op = self.ram[self.pc]
            # Get dictionary entry then execute returned instruction
            instruction = self.instruction_registry[op]
            instruction()
        
