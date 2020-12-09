"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MULT = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0 
        self.fl = 0
        self.running = True
        self.halted = False
        #self.reg = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.stack_pointer = 7
        self.memory = []
        """ self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111 """

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val

    def load(self, args):
        """Load a program into memory."""
        # My implementation
        program_code = []
        
        try:
            with open(f"ls8/examples/{args}") as ls8_file:
                for line in ls8_file:
                    line_split = line.split("#")
                    possible_binary_number = line_split[0]
                    try:
                        new_binary_number = int(possible_binary_number, 2)
                        program_code.append(new_binary_number)
                    except:
                        print(f"Unable to cast '{possible_binary_number}' to an integer")
                        continue
        except FileNotFoundError:
            print("File Not Found")
            
        print("program code!!!!!!!!!!!", program_code)
        stack_space = 256 - len(program_code)
        memory = program_code + [0] * stack_space
        
        self.reg[self.stack_pointer] = len(memory) - 1
        print('memory', memory)
        #########################################################################################
        ############################################################################### From Class
        """ address = 0

        with open(args) as my_file:
            for line in my_file:
                comment_split = line.split("#")
                maybe_binary_number = comment_split[0]
                try:
                    x = int(maybe_binary_number, 2)
                    self.ram_write(x, address)
                    address += 1
                except:
                    continue """


        ##########################################################################################

        

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

        for instruction in memory:
            self.ram[address] = instruction
            address += 1
        print(self.ram, 'ram')


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == MULT:
            print('regs', reg_a, reg_b)
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
            
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
        while self.halted == False:
            instruction = self.ram_read(self.pc)
            #print('instruction', "{0:b}".format(instruction))

             
            """ if instruction == PRN:
                val_to_print = self.ram[self.pc + 1]
                print(self.reg[val_to_print])
                self.pc += 2
                print('prn ran')
            elif instruction == LDI:
                reg_to_store = self.ram[self.pc + 1]
                val_to_store = self.ram[self.pc + 2]
                self.reg[reg_to_store] = val_to_store
                self.pc += 3
                print('ldi ran')
            elif instruction == HLT:
                print('hlt ran')
                self.halted = True
            else:
                unknown_instruction = "{0:b}".format(instruction)
                print(f"Instruction Unknown {unknown_instruction}")
                sys.exit(1) """
            
            # From class
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(instruction, operand_a, operand_b)
                
        # From class
    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == HLT:
            print('hlt ran')
            self.halted = True

        elif instruction == PRN:
            print(self.reg[operand_a])
            self.pc += 2
            print('prn ran')

        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3
            print(f'ldi ran --{operand_b} store in reg{operand_a}')

        elif instruction == MULT:
            """ self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
            
            print('mult ran') """
            self.alu(instruction, operand_a, operand_b)
            self.pc += 3
            print('mult ran')
        elif instruction == PUSH:
            self.reg[self.stack_pointer] -= 1
            reg_to_retrieve_val = operand_a
            val_in_reg = self.reg[reg_to_retrieve_val]
            self.ram[self.reg[self.stack_pointer]] = val_in_reg
            self.pc += 2
            
            print('push --- val in ram', self.ram[self.reg[self.stack_pointer]] )
        elif instruction == POP:
            reg_to_pop = operand_a
            
            self.reg[reg_to_pop] = self.ram[self.reg[self.stack_pointer]]
            print(f'pop ran --{self.ram[self.reg[self.stack_pointer]]}in reg{reg_to_pop}')
            self.reg[self.stack_pointer] += 1
            self.pc += 2
           
        ##### MULT FROM CLASS
        """ elif instruction == MULT:
            self.reg[operand_a] *= self.reg[operand_b]
            self.pc += 3 """