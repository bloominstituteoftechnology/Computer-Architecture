"""CPU functionality."""

import sys
# print(sys.argv)
# sys.exit(0)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7
        self.reg = [0] * 8
        self.address = 0
        self.flag = 0b00000000
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.ADD = 0b10100000
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110 

    def load(self, path):
        """Load a program into memory."""

        with open(path) as f:
            for line in f:
            # try:              
                line = line.strip().split("#",1)[0]
                if line == '':
                    continue
                line = int(line, 2)
                self.ram[self.address] = line
                self.address += 1
                # print(line)
                if len(sys.argv) != 2:
                    print("usage: ls8.py filename")
                    sys.exit(1)
                if ValueError:
                    pass
            # except ValueError:
            #     pass

        # address = 0

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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == self.ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address=None):
        # v = self.ram[address]
        return self.ram[address]

    def ram_write(self, value=None, address=None):
        self.ram[address] = value
        return self.ram[address]      

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            self.pc,
            self.flag,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        )

        for i in range(8):
            print(" %02X" % self.reg[i])

        print()    

    def run(self):
        """Run the CPU."""
        # self.trace()
        # print('start')
        self.reg[self.sp] = 0xf4
        running = True
        while running:
            IR = self.ram_read(self.pc)
            print('IR:', IR)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == self.LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == self.PRN:
                print(self.reg[operand_a])
                self.pc += 2
                # self.trace()
                # print('PRN')
            elif IR == self.HLT:
                running = False
            elif IR == self.ADD:
                self.alu(IR, operand_a, operand_b)
                self.pc += 3
                self.trace()
                print('ADD')
            elif IR == self.MUL:
                # self.reg[operand_a] *= self.reg[operand_b]
                self.alu(IR, operand_a, operand_b)
                self.pc += 3
                self.trace()
                print('MUL')
            elif IR == self.PUSH:
                # decrement stack pointer
                self.reg[self.sp] -= 1

                # keep R7 in the range 00-FF
                self.reg[self.sp] &= 0xff

                # get register value
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

                # Store in memory
                address_to_push_to = self.reg[self.sp]
                self.ram[address_to_push_to] = value
                self.pc += 2
            elif IR == self.POP:
                # Get value from RAM
                address_to_pop_from = self.reg[self.sp]
                value = self.ram[address_to_pop_from]

                # Store in the given register
                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = value

                # Increment SP
                self.reg[self.sp] += 1
                self.pc += 2
            elif IR == self.CALL:
                # Get address of the next instruction
                return_addr = self.pc + 2

                # Push that on the stack
                self.reg[self.sp] -= 1
                address_to_push_to = self.reg[self.sp]
                self.ram[address_to_push_to] = return_addr

                # Set the PC to the subroutine address
                reg_num = self.ram[self.pc + 1]
                subroutine_addr = self.reg[reg_num]

                self.pc = subroutine_addr
            elif IR == self.RET:
                # Get return address from the top of the stack
                address_to_pop_from = self.reg[self.sp]
                return_addr = self.ram[address_to_pop_from]
                self.reg[self.sp] += 1

                # Set the PC to the return address
                self.pc = return_addr
            elif IR == self.CMP:
                if self.reg[operand_a] == self.reg[operand_b]:
                    self.flag = 0b00000001
                elif self.reg[operand_a] > self.reg[operand_b]:
                    self.flag = 0b00000010
                # elif self.reg[operand_a] < self.reg[operand_b]:
                #     self.flag = 0b00000100
                else:
                    self.flag = 0b00000000
                self.pc += 3
            elif IR == self.JMP:                
                self.address = self.reg[self.ram[self.pc + 1]]
                self.pc = self.address
            elif IR == self.JEQ:
                if self.flag == 0b00000001:
                    self.address = self.reg[self.ram[self.pc + 1]]
                    self.pc = self.address
                else:
                    self.pc += 2
            elif IR == self.JNE:
                if self.flag == 0b00000000:
                    self.address = self.reg[self.ram[self.pc + 1]]
                    self.pc = self.address
                else:
                    self.pc += 2     
            else:
                print({IR})
                running = False