"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg= [0] * 8
        # set the SP
        self.reg[7]= 0xf4
        self.ram= [0] * 256
        # Program Counter, address of the currently executing instruction
        self.pc= 0
        # flags
        self.fl= 0
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

    def stackPush(self, value):
        # print('stackPush')
        # decrement SP
        self.reg[7]-= 1
        self.ram_write(value, self.reg[7])

    def stackPop(self):
        # print('stackPop')
        value= self.ram_read(self.reg[7])
        # increment SP
        self.reg[7]+= 1
        return value

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
                # print('HLT')
                self.isRunning= False
                self.pc+= 1

            # LDI 10000010 00000rrr iiiiiiii
            elif IR == '10000010':
                # print('LDI')
                self.reg[operand_a]= operand_b
                self.pc+= 3

            # PRN 01000111 00000rrr
            elif IR == '01000111':
                val= self.reg[operand_a]
                print(val)
                self.pc+= 2
            
            # MUL 10100010 00000aaa 00000bbb
            elif IR == '10100010':
                # print('MULT')
                self.alu('MUL', operand_a, operand_b)
                self.pc+= 3
            
            # ADD 10100000 00000aaa 00000bbb
            elif IR == '10100000':
                # print('ADD')
                self.alu('ADD', operand_a, operand_b)
                self.pc+= 3

            # SUB 10100001 00000aaa 00000bbb
            elif IR == '10100001':
                # print('SUB')
                self.alu('SUB', operand_a, operand_b)
                self.pc+= 3
            
            # DIV 10100011 00000aaa 00000bbb
            elif IR == '10100011':
                # print('DIV')
                if operand_b != 0:
                    self.alu('DIV', operand_a, operand_b)
                    self.pc+= 3
                else:
                    print('Cannot divide by 0')
                    self.isRunning= False
                    self.pc+= 1

            # PUSH 01000101 00000rrr
            elif IR == '01000101':
                # print('PUSH')
                value= self.reg[operand_a]
                self.stackPush(value)
                self.pc+= 2
                
            #POP 01000110 00000rrr
            elif IR == '01000110':
                # print('POP')
                reg_addr= operand_a
                value= self.stackPop()
                self.reg[reg_addr]= value
                self.pc+= 2

            # CALL 01010000 00000rrr
            elif IR == '01010000':
                # print('CALL')
                # The address of the ***instruction*** _directly after_ `CALL` is pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
                instrAddr= self.pc+ 2
                self.stackPush(instrAddr)
                # The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.
                self.pc= self.reg[operand_a]

            # RET 00010001
            elif IR == '00010001':
                # print('RET')
                # Pop the value from the top of the stack and store it in the `PC`.
                popVal= self.stackPop()
                self.pc= popVal



                
