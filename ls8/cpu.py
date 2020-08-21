import sys

class CPU:
    def __init__(self):
        # Memory and general pupose registers
        self.ram = [None] * 256
        self.register = [0] * 8

        # Program Counter
        self.pc = 0 # Register 7 reserved

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        return None

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()
                    #print(line)
                    if n == '':
                        continue

                    val = int(n, 2)
                    # store val in memory
                    self.ram[address] = val
                    address += 1
                    #  print(f"{x:08b}: {x:d}")

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
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

        program_counter = self.pc
        instruction = self.ram[program_counter] # Grabbing instruction from memory based on program counter
        run = True
        stack_pointer = 244 # F4

        while run:
            # Grabbing next two instructions in case they're needed using ram_read
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

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
                print(self.register[operand_a])
                self.pc += 2

            # MUL - Multiply 2 registers together and save result to the first register (SHOULD USE ALU)
            elif instruction == 0b10100010:
                self.pc += 3
                self.alu('MUL', operand_a, operand_b)

            # ADD - Add 2 registers together and save result to the first register (SHOULD USE ALU)
            elif instruction == 0b10100000:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            # PUSH
            elif instruction == 0b01000101:
                stack_pointer -= 1
                self.ram[stack_pointer] = self.register[operand_a]
                self.pc += 2

            # POP
            elif instruction == 0b01000110:
                if stack_pointer < 244:
                    self.register[operand_a] = self.ram[stack_pointer]
                    stack_pointer += 1
                else:
                    print('Can\'t push onto an empty stack!')
                self.pc += 2

            # CALL
            elif instruction == 0b01010000:
                stack_pointer -= 1
                self.ram[stack_pointer] = self.pc + 2
                self.pc = self.register[operand_a]
                
            # RET
            elif instruction == 0b00010001:
                self.pc = self.ram[stack_pointer]
                stack_pointer += 1

            # CMP - Compare and set flag accordingly (REG 4 reserved for flag)
            elif instruction == 0b10100111:
                if self.register[operand_a] == self.register[operand_b]:
                    eflag = 1
                    gflag = 0
                    lflag = 0
                elif self.register[operand_a] > self.register[operand_b]:
                    eflag = 0
                    gflag = 1
                    lflag = 0
                else:
                    eflag = 0
                    gflag = 0
                    lflag = 1
                self.pc += 3

            # JEQ - If `equal` flag is set (true), jump to the address stored in the given register. 01010110
            elif instruction == 0b01010101:
                if eflag == 1:
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2

            # JNE - If `E` flag is clear (false, 0), jump to the address stored in the given register.
            elif instruction == 0b01010110:
                if eflag == 0:
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2

            # JMP - Jump to the address stored in the given register. Set the `PC` to the address stored in the given register.
            elif instruction == 0b01010100:
                self.pc = self.register[operand_a]

            # INVALID
            else:
                print("Invalid Instruction:")
                run = False
                
            # Point Counter Update/Run update
            program_counter = self.pc # Get new Program Counter
            instruction = self.ram[program_counter] # Grab Instruction
