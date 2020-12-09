"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
CALL = 0b01010000
RET  = 0b00010001
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100
NOT = 0b01101001
OR = 0b10101010
AND = 0b10101000
XOR = 0b10101011

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.reg[6] = 0 # flags reg
        self.pc = 0
        self.branchtable = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            PUSH: self.push,
            POP: self.pop, 
            CALL: self.call,
            RET: self.ret,
            #JEQ: self.jeq,
            #JNE: self.jne,
            #JMP: self.jmp
        }


    def load(self):
        """Load a program into memory."""

        if (len(sys.argv)) != 2:
            print('remember to pass the second file name')
            print('usage: python fileio.py <second_filename.py>')
            sys.exit()
        try: 
            with open(sys.argv[1]) as f:
                address = 0
                for line in f:
                    possible_binary = line[:line.find('#')]
                    # if no comment on line
                    if possible_binary == '':
                        continue # passes rest of loop
                    denary_int = int(possible_binary, 2)
                    self.ram[address] = denary_int
                    address += 1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found ')
            sys.exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == ADD: # add
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL: # multiply 
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == CMP: # compare 
            # less than
            if self.reg[reg_a] < self.reg[reg_b]:
                self.reg[6] = 0b00000100
            # greater than 
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.reg[6] = 0b00000010
            # equal to
            else:
                self.reg[6] = 0b00000001
        elif op == SHL: # shift left
            decimal = self.reg[reg_a] << self.reg[reg_b]
            self.reg[reg_a] = f"{decimal:#010b}"
        elif op == SHR:   # shift right
            decimal = self.reg[reg_a] >> self.reg[reg_b]
            self.reg[reg_a] = f"{decimal:#010b}"
        elif op == MOD: # modulo, get remainder
            # cannot divide by 0
            if self.reg[reg_b] == 0:
                # halt
                self.hlt(reg_a, reg_b)
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op == NOT: # store bitwise not
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == OR: # store bitwise or
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == AND: # store bitwise and
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == XOR: # store bitwise xor
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")


    def ram_read(self, address):
        return self.ram[address]


    def ram_write(self, address, data):
        self.ram[address] = data


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
        IR = []
        self.running = True 
        while self.running:
            IR = self.ram[self.pc] # instruction register
            num_args = IR >> 6
            is_alu_op = (IR >> 5) & 0b001
            operand_a = self.ram_read(self.pc+1) 
            operand_b = self.ram_read(self.pc+2)
            is_alu_op = (IR >> 5) & 0b001 == 1
            if is_alu_op:
                self.alu(IR, operand_a, operand_b)
            else:
                self.branchtable[IR](operand_a, operand_b)
            # check if command sets PC directly
            sets_pc = (IR >> 4) & 0b0001 == 1
            if not sets_pc:
                # increment pc here
                self.pc += 1 + num_args


    def hlt(self, operand_a, operand_b):
        self.running = False

    
    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b


    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
    

    def jmp(self, operand_a, operand_b):

        reg_idx = self.reg[operand_a]

        self.pc = reg_idx


    def push(self, operand_a, operand_b):
        # decrement the SP.
        self.reg[7] -= 1
        # copy the value in the given register to the address pointed to by SP
        value = self.reg[operand_a]
        # copy to the address at stack pointer
        SP = self.reg[7]
        self.ram[SP] = value


    def pop(self, operand_a, operand_b):
        # get SP
        SP = self.reg[7]
        # get address pointed to by SP
        value = self.ram[SP]
        # Copy the value from the address pointed to by SP to the given register.
        self.reg[operand_a] = value
        # increment SP
        self.reg[7] += 1

    def call(self, operand_a, operand_b):
        # PUSH
        return_address = self.pc + 2
        # decrement the SP, stored in R7 
        self.reg[7] -= 1
        # store the value at the SP address
        SP = self.reg[7]
        # the return address is 8 as we can see by looking ahead by 2
        self.ram[SP] = return_address
        # ram (command) at 7 contains 1
        reg_idx = self.ram[self.pc+1]
        # reg 1 contains 24
        subroutine_address = self.reg[reg_idx]
        # pc is at 24
        self.pc = subroutine_address 


    def ret(self, operand_a, operand_b):
        # Return from subroutine.
        # Pop value from top of stack 
        SP = self.reg[7]
        return_address = self.ram[SP]
        #store it in the PC
        self.pc = return_address
        # increment stack
        self.reg[7] += 1


if __name__ == '__main__':
    cpu = CPU()
    cpu.load()
    cpu.run()