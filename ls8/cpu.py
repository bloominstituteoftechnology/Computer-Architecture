"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
# Step 1: Add the constructor to cpu.py

    def __init__(self):
        """Construct a new CPU."""
        # RAM
        # create 256 bytes of RAM
        self.ram = [0] * 256
        # create 8 registrars
        self.reg = [0] * 8  # 8 general-purpose registers, like variables, R0, R1, R2 .. R7
        # internal registers
        # set the program counter to 0
        self.pc = 0  # Program Counter, index of the current instruction
        self.halted = False
        self.ir = 0
        self.reg[7] = 0xF4
        self.sp = self.reg[7]
        # self.branch_table = {
        # self.ldi = 0b10000010,
        # self.prn = 0b01000111,
        # ADD: self.alu,
        # DIV: self.alu,
        # SUB: self.alu,
        # AND: self.alu,
        # OR: self.alu
        # }

# Step 2: Add RAM functions
    def ram_read(self, address):
        """
        This reads a value at its designated address of RAM
        """
        return self.ram[address]

    def ram_write(self, value, address):
        """
        This writes a value to RAM at its designated address
        """
        self.ram[address] = value

        # For now, we've just hardcoded a program:

# Step 7: Un-hardcode the machine code
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000, #registrar 0
        #     0b00001000, # value 8
        #     0b01000111, # PRN R0
        #     0b00000000, #print value in first registrar
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
    def load(self, filename):
        """Load a program into memory."""

        address = 0
        # -- Load program ---
        with open(filename, ) as f:
            for line in f:
                # print(line)
                line = line.split("#")
                line = line[0].strip()
                # except ValueError:
                # Our command needs to be casted and set to base 2
                if line == '':
                    continue
                # print('value is: ' + str(value))
                # will assign are converted value into the next entry in our RAM
                self.ram[address] = int(line, 2)
                # after it is entered into RAM, it will increment the address value by 1
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB":
        #     self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == " DIV":
        #     self.reg[reg_a] //= self.reg[reg_b]
        # elif op == "AND":
        #     self.reg[reg_a] &= self.reg[reg_b]
        # elif op == "OR":
        #     self.reg[reg_a] |= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

        # if op == "ADD":
        #     self.reg[reg_a] += self.reg[reg_b]
        # # elif op == "SUB": etc
        # else:
        #     raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """
        Run the CPU:
        The core running of our built CPU
        """
       # Step 4: Implement the HLT instruction handler
        HLT = 0b00000001  # Instruction handler
        # Step 5: Add the LDI instruction
        LDI = 0b10000010  # instruction
        # Step 6: Add the PRN instruction
        PRN = 0b01000111  # PRN instruction

        ADD = 0b10100000
        SUB = 0b10100001
        MUL = 0b10100010
        DIV = 0b10100011

        AND = 0b10101000
        OR = 0b10101010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        # kept in a while loop to continue working through passed in commands.
        running = True
        # Step 9: Beautify your run() loop
        while running == True:
            # print(f"PC:{self.pc}")
            """
            Lets load our function now. This will write our pre-written commands in the program variable to our RAM.

            The instructions will loaded and cycle through our RAM.
            """
            instruction = self.ram[self.pc]

            # Halt our CPU and exit
            if instruction == HLT:
                running = False
                self.pc += 1
            # checking if instruction is to set registrar to integer:
            # From Spec:
            # `LDI register immediate`
            # Will set the value of a register to an integer.
            # The first value sets which registrar will assign the integer
            # The second value determines what that value is
            # The PC (program counter) goes one forward to see the value
            elif instruction == LDI:
                # one RAM entries out determines which registrar is loaded:
                reg_slot = self.ram_read(self.pc + 1)
                # two RAM entries out determines what value is loaded
                int_value = self.ram_read(self.pc + 2)

                # The registrar at slot reg_slot is being assigned the int_value both
                # determined from RAM above
                self.reg[reg_slot] = int_value
                # the program counter is set 3 entries ahead
                # one for the current instruction
                # one for the integer value
                # one for the registrar slot
                # 3 bit operation
                self.pc += 3
            # Writing logic for if the Print function is called
            elif instruction == PRN:
                # import pdb; pdb.set_trace()
                # loading which registrar slot should be preinted
                # print(self.reg[reg_num1]) # print our stored value
                reg_slot = self.ram_read(self.pc + 1)
                # prints the value at that registrar slot
                print(self.reg[reg_slot])
                # print("RAM: ", self.ram)
                # print("REG: ", self.reg)
                # print("Value", value)
                # inriments by two
                # one for the current instruction
                # one for the reg_slot
                self.pc += 2
            elif instruction == MUL:
                # if MUL is called, it will grab the next two values in our program counter
                # Step 8: Implement a Multiply and Print the Result
                # to find out what values in the registrar are going to be multiplied:
                reg_num1 = self.ram[self.pc+1]  # register
                reg_num2 = self.ram[self.pc+2]  # value
                self.alu('MUL', reg_num1, reg_num2)
                # 3 bit operation
                self.pc += 3
                # if ADD is called:
            elif instruction == ADD:
                # This will grab the next values in our program counter.
                # and will know which values in our registrar will be added
                reg_num1 = self.ram[self.pc+1]  # register
                reg_num2 = self.ram[self.pc+2]  # value
                self.alu('ADD', reg_num1, reg_num2)
                # 3 bit operation
                self.pc += 3

            # Step 10: Implement System Stack
            # PUSH
            elif instruction == PUSH:
                # This will determine which registrar is pushing their value to the stack:
                reg_slot = self.ram[self.pc+1]
                val = self.reg[reg_slot]
                # decriment the stack pointer
                self.sp -= 1
                # now we will push the value pulled from our registar to the stack:
                self.ram[self.sp] = val
                # 2 bit operation
                self.pc += 2
                # POP
            elif instruction == POP:
                # This will determine which registrar will get popped from the stack:
                reg_slot = self.ram[self.pc+1]
                # now  the value of the registrar is updated
                # at the reg_slot with its assigned value:
                value = self.ram[self.sp]
                self.reg[reg_slot] = value
                # now will incriment the stack pointer:
                self.sp += 1
                # 2 bit operation
                self.pc += 2
                # CALL
            elif instruction == CALL:
                # Since the CALL spec has the address after the CALL instruction.
                # We will designate the
                return_address = self.pc + 2
                # now will decriment the stack pointer by 1
                self.sp -= 1
                # will assign the new top of the stack  value of our returned address:
                self.ram[self.sp] = return_address
                # with the return addres now stored.
                # We need to determine which registar slot is now used for our called function
                reg_slot = self.ram[self.pc+1]
               # Step 11: Implement Subroutine Calls
                # The subroutine location is the value at that designated reg_slot:
                subroutine_location = self.reg[reg_slot]
                # Our program counter is now set to the location of that subroutine
                self.pc = subroutine_location
            elif instruction == RET:
                return_address = self.ram[self.sp]
                # now will incriment the stack pointer:
                self.sp += 1
                # return our address:
                self.pc = return_address
            else:
                print(f"unknown instruction {instruction} at address {IR}")
                print(f"Our program counter value is: {self.pc}")
                print(f"The command issued was: {self.ram_read(self.pc)}")
                sys.exit(1)
