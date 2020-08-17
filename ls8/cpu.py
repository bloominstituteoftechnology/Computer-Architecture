import sys

class CPU:
    def __init__(self):
        # Memory and general pupose registers
        self.ram = [None] * 256
        self.register = [0] * 8
        self.pc = 0 

        # Internal registers (values between 0-255)
        self.PC = self.register[0] # Program Counter, address of the currently executing instruction
        self.IR = self.register[1] # Instruction Register, contains a copy of the currently executing instruction
        self.MAR = self.register[2] # contains the address that is being read or written to
        self.MDR = self.register[3] # contains the data that was read or the data to write
        self.FL = self.register[4] # Flags

        # Reserved internal registers
        self.IM = self.register[5] # Interupt mask
        self.IS = self.register[6] # Interupt status
        self.IP = self.register[7] # Stack pointer

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        return None

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
            self.ram_read(self.pp),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        # PRINT TO SEE WHAT IS LOADED INTO RAM (OPCODES)
        #for instruction in self.ram:
            #if instruction != None:
                #print('Number', instruction)
                #print("Binary{0:b}".format(instruction))

        program_counter = self.pc
        instruction = self.ram[program_counter] # Grabbing instruction from memory based on program counter
        self.register[1] = instruction # Saving to instruction register
        run = True

        while run:
            # Grabbing next two instructions in case they're needed using ram_read
            operand_a = self.ram_read(program_counter + 1)
            operand_b = self.ram_read(program_counter + 2)

            ''' IF/ELSE CLAUSES '''
            # HLT - Halt command
            if instruction == 0b00000001:
                run = False

            # LDI - Set the value of a register to an integer.
            elif instruction == 0b10000010:
                self.register[operand_a] = operand_b # This sets register a with the value b (0,8)
                self.pc += 3

            # PRN - Prints the next opcode    
            elif instruction == 0b01000111:
                self.pc += 2
                print(self.register[operand_a])

            # Point Counter Update/Run update
            program_counter = self.pc # Get new Program Counter
            instruction = self.ram[program_counter] # Grab Instruction
            self.register[1] = instruction # Saving to instruction register

        return None
