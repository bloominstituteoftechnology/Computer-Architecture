"""CPU functionality."""

import sys



OP1 = 0b00000001
OP2 = 0b10000010
OP3 = 0b01000101
OP4 = 0b10100010
OP5 = 0b01000111
OP6 = 0b01000110
OP7 = 0b01010000
OP8 = 0b00010001
OP9 = 0b10100000
OP10 = 0b10100111
OP11 = 0b01010100
OP12 = 0b01010110
OP13 = 0b01010101
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""   
        self.ram = [0] * 256
        self.reg = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.pc = 0
        self.sp = 7
        self.fl_reg = 0b00000000
        self.branchtable = {}
        self.branchtable[OP1] = self.halt
        self.branchtable[OP2] = self.ldi
        self.branchtable[OP3] = self.push
        self.branchtable[OP4] = self.mult
        self.branchtable[OP5] = self.prn 
        self.branchtable[OP6] = self.pop
        self.branchtable[OP7] = self.call
        self.branchtable[OP8] = self.ret
        self.branchtable[OP9] = self.add
        self.branchtable[OP10] = self.compare
        self.branchtable[OP11] = self.jmp
        self.branchtable[OP12] = self.jne
        self.branchtable[OP13] = self.jeq
    

    def halt(self):
        sys.exit()

    def ldi(self):
        self.pc += 1
        index = self.ram[self.pc]
        self.reg[index] = self.ram[self.pc + 1]
        self.pc += 2

    def push(self):
        # Decrement the SP
        self.reg[self.sp] -= 1
        # Get register number
        index = self.ram[self.pc + 1]
        # Get value out of register
        val = self.reg[index]
        # Store value in memory at SP
        self.ram[self.reg[self.sp]] = val
        self.pc += 2

    def mult(self):
        self.pc += 1
        operand1 = self.reg[self.ram[self.pc]]
        self.pc += 1
        operand2 = self.reg[self.ram[self.pc]]
        self.reg[self.ram[self.pc - 1]] = operand1 * operand2
        self.pc += 1

    def prn(self):
        self.pc += 1
        index = self.ram[self.pc]
        print(self.reg[index])
        self.pc += 1

    def pop(self):
        # copy value from current SP
        val = self.ram[self.reg[self.sp]]
        # insert value into given register
        self.reg[self.ram[self.pc + 1]] = val
        # increment SP by 1
        self.reg[self.sp] += 1
        self.pc += 2

    def call(self):
        # Push the return address on the stack
        return_address = self.pc + 2
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = return_address

        # Set the PC to the address of the function
        self.pc = self.reg[self.ram[self.pc + 1]]

    def ret(self):
        # Pop the return address off the stack
        return_addr = self.ram[self.reg[self.sp]] 
        self.reg[self.sp] += 1
        # Set the PC to the return address
        self.pc = return_addr

    def add(self):
        # get our values
        operand1 = self.reg[self.ram[self.pc + 1]]
        operand2 = self.reg[self.ram[self.pc + 2]]
        # set first register value to sum
        self.reg[self.ram[self.pc + 1]] = operand1 + operand2
        self.pc += 3

    def compare(self):
        if self.reg[self.ram[self.pc + 1]] == self.reg[self.ram[self.pc + 2]]:
            # set equal flag to 1
            self.fl_reg = 0b00000001
            self.pc += 3
        elif self.reg[self.ram[self.pc + 1]] < self.reg[self.ram[self.pc + 2]]:
            # set less than flag to 1
            self.fl_reg = 0b00000100
            self.pc += 3
        elif self.reg[self.ram[self.pc + 1]] > self.reg[self.ram[self.pc + 2]]:
            # set greater than flag to 1
            self.fl_reg = 0b00000010
            self.pc += 3

    def jmp(self):
        # set pc to address in given reg
        self.pc = self.reg[self.ram[self.pc + 1]]

    def jne(self):
        # if not equal flag, jump to given reg
        if self.fl_reg != 0b00000001:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else: self.pc += 2

    def jeq(self):
        # if equal flag, jump to given reg
        if self.fl_reg == 0b00000001:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else: self.pc += 2

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            print("No program specified. Please specify a program.")
            sys.exit(1)

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
                self.ram[address] = v
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
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        halted = False
        while not halted:
            process = self.ram[self.pc]
            self.branchtable[process]()
                


