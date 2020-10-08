"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Random Access Memory
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0

        # list of opcodes
        self.branchtable = {}
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
        self.branchtable[0b00000001] = self.HLT
        self.branchtable[0b01000101] = self.PUSH
        self.branchtable[0b01000110] = self.POP

        # assigned list of opcodes to a memory in RAM
        self.ram[0xF5] = self.branchtable


        # assigned registers[7] with top of the stack
        self.registers[7] = self.ram[int("F4", 16)]
        
        # stack pointer
        self.SP = self.registers[7]



    def LDI(self):
        self.registers[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
        self.pc += 3
        return True

    def PRN(self):
        print(self.registers[self.ram[self.pc + 1]])
        self.pc += 2
        return True

    def HLT(self):
        return False

    def PUSH(self):
        self.SP -= 1
        self.ram[self.SP] = self.registers[self.ram[self.pc + 1]]
        self.pc += 2
        return True

    def POP(self):
        self.registers[self.ram[self.pc+1]] = self.ram[self.SP]
        self.SP += 1
        self.pc += 2
        return True

    def JMP(self):
        self.pc = self.registers[self.ram[self.pc + 1]]

    def CALL(self):
        return_addy = self.pc + 2

        # self.registers[7] is the stack pointer
        self.registers[7] -= 1

        self.ram[self.registers[7]] = return_addy

        # subroutine address(points to the register address after the CALL binary code is called)
        self.pc = self.registers[self.ram[self.pc + 1]]
    
    def RET(self):
        # pc set to what is on top of the stack
        self.pc = self.ram[self.registers[7]]
        self.registers[7] += 1


         



    def load(self):
        """Load a program into memory."""
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

        address = 0

        if(len(sys.argv) != 2):
            print('forgot to pass a second file')
            sys.exit()

        try:
            with open(sys.argv[1]) as f:
                for line in f:

                    # everything with a '#' marks as a comment which we will disregard
                    possible_num = line[:line.find('#')]

                    # check if its a line
                    if possible_num == '':
                        continue  

                    instruction = int(possible_num, 2)
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            sys.exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "SUB":
            self.registers[reg_a] -= self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        elif op == "DIV":
            self.registers[reg_a] //= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ALU_OPERS(self, op):
        if op == 0b10100000:
            return 'ADD'
        elif op == 0b10100001:
            return 'SUB'
        elif op == 0b10100010:
            return 'MUL'
        elif op == 0b10100011:
            return 'DIV'
        elif op == 0b10100111:
            return 'CMP'
        elif op == 0b01101001:
            return 'NOT'
        elif op == 0b10100100:
            return 'MOD'
        elif op == 0b10101000:
            return 'AND'
        elif op == 0b10101010:
            return 'OR'
        elif op == 0b10101011:
            return 'XOR'
        elif op == 0b10101101:
            return 'SHR'
        elif op == 0b10101100:
            return 'SHL'
        elif op == 0b01100101:
            return 'INC'
        elif op == 0b01100110:
            return 'DEC'

    def PC_MANIP(self, op):

        if op == 0b01010000:
            self.CALL()
        elif op == 0b01010010:
            return 'INT'
        elif op == 0b00010011:
            return 'IRET'
        elif op == 0b01010101:
            return 'JEQ'
        elif op == 0b01011010:
            return 'JGE'
        elif op == 0b01010111:
            return 'JGT'
        elif op == 0b01011001:
            return 'JLE'
        elif op == 0b01011000:
            return 'JLT'
        elif op == 0b01010100:
            self.JMP()
        elif op == 0b01010110:
            return 'JNE'
        elif op == 0b00010001:
            self.RET()
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
            print(" %02X" % self.registers[i], end='')


    def run(self):
        """Run the CPU."""   
        instructions = self.ram[int("F5", 16)]
  
        running = True     

        while running:
            ir = self.ram_read(self.pc)
            # alu operation
            is_alu_op = (ir >> 5) & 0b001 == 1
            # program counter manipulation operation
            pc_manip = (ir >> 4) & 0b0001 == 1

            if is_alu_op:
                operation_type = self.ALU_OPERS(ir)
                self.alu(operation_type,self.ram[self.pc + 1], self.ram[self.pc + 2] )
                self.pc += 3
            elif pc_manip:
                self.PC_MANIP(ir)

            else:
                running = instructions[ir]()





            # if ir == LDI:
            #     self.registers[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
            #     self.pc += 2
                
            # elif ir == PRN:
            #     print(self.registers[self.ram[self.pc + 1]])
            #     self.pc += 1

            # elif ir == 162:
            #     self.alu('MUL',self.ram[self.pc + 1], self.ram[self.pc + 2] )
            #     self.pc += 2

            # elif ir == HLT:
            #     running = False
            






    def ram_read(self, mar, mdr = ""):
        mdr = self.ram[mar]

        return mdr
    
    # def ram_write(self, mar, mdr = ""):
    #     return self.ram[mar] = mdr
