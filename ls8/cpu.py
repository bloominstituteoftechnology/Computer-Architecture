"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg= [0] * 8
        self.ram= [0] * 256
        self.bootUp()
        # Program Counter, address of the currently executing instruction
        self.pc= 0
        self.fl= 0

    def bootUp(self):
        # reset registers
        for r in range(len(self.reg)-1):
            if r < 7:
                self.reg[r]= 0
            elif r == 7:
                self.reg[r]= 0xF4
        self.isRunning= True

    # MAR contains the address that is being read or written to. The MDR contains the data that was read or the data to write.
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        self.ram[MAR]= MDR

    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) != 2:
            print('Usage: ls8.py "program name"')
            sys.exit(1)

        try:
            with open(f'examples/{sys.argv[1]}') as f:
                for line in f:
                    line= line.strip()
                    temp= line.split()

                    if len(temp) == 0:
                        continue
                        
                    if temp[0][0] == '#':
                        continue
                    
                    try:
                        self.ram_write(temp[0], address)

                    except ValueError:
                        print(f'Invalild number: {temp[0]}')
                        sys.exit(1)

                    address+= 1

        except FileNotFoundError: 
            print(f'Couldn\'t open: {sys.argv[1]}')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == 'DIV':
            self.reg[reg_a] /= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

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
        """Run the CPU."""

        while self.isRunning:
            # Instruction Register
            IR= str(self.ram_read(self.pc))

            # `AABCDDDD`
            #  `AA` Number of operands for this opcode, 0-2
            numOps= IR[:2]
            # * `B` 1 if this is an ALU operation
            isALU= IR[2:3]
            # * `C` 1 if this instruction sets the PC
            setsPc= IR[3:4]
            # * `DDDD` Instruction identifier
            isntID= IR[4:]

            # set the operands as needed
            if int(numOps,2 ) == 2:
                operand_a= int(self.ram_read(self.pc+ 1), 2)
                operand_b= int(self.ram_read(self.pc+ 2), 2)
            elif int(numOps, 2) == 1:
                operand_a= int(self.ram_read(self.pc+ 1), 2)

            # HTL 00000001 
            if IR == '00000001':
                self.isRunning= False
                self.pc+= 1

            # LDI 10000010 00000rrr iiiiiiii
            elif IR == '10000010':
                self.reg[operand_a]= operand_b
                self.pc+= 3

            # PRN 01000111 00000rrr
            elif IR == '01000111':
                val= self.reg[operand_a]
                print(val)
                self.pc+= 2
            
            # MUL 10100010 00000aaa 00000bbb
            elif IR == '10100010':
                self.alu('MUL', operand_a, operand_b)
                self.pc+= 3

            # SUB 10100001 00000aaa 00000bbb
            elif IR == '10100001':
                self.alu('SUB', operand_a, operand_b)
                self.pc+= 3
            
            # DIV 10100011 00000aaa 00000bbb
            elif IR == '10100011':
                if operand_b != 0:
                    self.alu('DIV', operand_a, operand_b)
                    self.pc+= 3
                else:
                    print('Cannot divide by 0')
                    self.isRunning= False
                    self.pc+= 1
