import sys

class CPU:
    def __init__(self):
        # Memory and general pupose registers
        self.ram = [None] * 256
        self.register = [0] * 8

        # Program Counter
        self.pc = 0 

        # # Internal registers (values between 0-255)
        # self.PC = self.register[0] # Program Counter, address of the currently executing instruction
        # self.IR = self.register[1] # Instruction Register, contains a copy of the currently executing instruction
        # self.MAR = self.register[2] # contains the address that is being read or written to
        # self.MDR = self.register[3] # contains the data that was read or the data to write
        # self.FL = self.register[4] # Flags

        # # Reserved internal registers
        # self.IM = self.register[5] # Interupt mask
        # self.IS = self.register[6] # Interupt status
        # self.IP = self.register[7] # Stack pointer

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

        # PRINT TO SEE WHAT IS LOADED INTO RAM (OPCODES)
        #for instruction in self.ram:
            #if instruction != None:
                #print('Number', instruction)
                #print("Binary{0:b}".format(instruction))

        program_counter = self.pc
        instruction = self.ram[program_counter] # Grabbing instruction from memory based on program counter
        run = True
        stack_pointer = 244 # F4

        while run:
            # Grabbing next two instructions in case they're needed using ram_read
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            #print('OPS AT START OF LOOP', operand_a, operand_b)
            #print('----------------')
            #for item in self.register:
            #    print(item)
            # print('----------------')

            ''' IF/ELSE CLAUSES '''
            # HLT - Halt command
            if instruction == 0b00000001:
                run = False
 
            # LDI - Set the value of a register to an integer.
            elif instruction == 0b10000010:
                #print('LDI')
                #print('index', operand_a, 'value', operand_b)
                self.register[operand_a] = operand_b # This sets register a with the value b (0,8)
                self.pc += 3
                #print('asdfasdf', self.register[operand_a])
                # 10000010 >> 6 = 00000010 = 2

            # PRN - Prints the next opcode    
            elif instruction == 0b01000111:
                #print('PRN')
                self.pc += 2
                print(self.register[operand_a])
                # 01000111 >> 5 = 00000001 = 1

            # MUL - Multiply 2 registers together and save result to the first register (SHOULD USE ALU)
            elif instruction == 0b10100010:
                #print('MUL')
                self.pc += 3
                #print('OPS', operand_a, operand_b)
                #print('MULOP1', self.register[operand_a])
                #print('MULOP2', self.register[operand_b])
                self.alu('MUL', operand_a, operand_b)
                #print('AFTER ALU')
                #print('MULOP1', self.register[operand_a])
                #print('MULOP2', self.register[operand_b])

            # ADD - Add 2 registers together and save result to the first register (SHOULD USE ALU)
            elif instruction == 0b10100000:
                #print('ADD')
                self.pc += 3
                self.alu('ADD', operand_a, operand_b)

            # PUSH
            elif instruction == 0b01000101:
                #print('PUSH')
                stack_pointer -= 1 # Decriment the index for our stack in ram
                self.ram[stack_pointer] = self.register[operand_a]
                #print(self.ram[stack_pointer])
                self.pc += 2

            # POP
            elif instruction == 0b01000110:
                '''
                1. Copy the value from the address pointed to by `SP` to the given register.
                2. Increment `SP`.
                '''
                #print('POP')
                if stack_pointer < 244:
                    self.register[operand_a] = self.ram[stack_pointer]
                    #print(self.register[operand_a])

                    stack_pointer += 1
                else:
                    print('Can\'t push onto an empty stack!')

                self.pc += 2

            # CALL
            elif instruction == 0b01010000:
                #print('CALL')
                # push the return address on to the stack
                stack_pointer -= 1
                #print('current stack point', stack_pointer)
                #print('setting this stack index in ram', self.ram[stack_pointer])
                self.ram[stack_pointer] = self.pc + 2
                #print('with this value', self.ram[stack_pointer])

                # Set the PC to the subroutines address
                self.pc = self.register[operand_a]
                
            # RET
            elif instruction == 0b00010001:
                #print('RET')
                # POP return address from stack to store in pc
                self.pc = self.ram[stack_pointer]
                stack_pointer += 1

            # INVALID
            else:
                print("Invalid Instruction:")
                run = False
                


            # Point Counter Update/Run update
            program_counter = self.pc # Get new Program Counter
            instruction = self.ram[program_counter] # Grab Instruction
