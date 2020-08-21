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
        # flags:`FL` bits: `00000LGE`
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

        elif op == 'CMP':
            if self.reg[reg_a] > self.reg[reg_b]:
                return 'g'
            elif self.reg[reg_a] < self.reg[reg_b]:
                return 'l'
            elif self.reg[reg_a] == self.reg[reg_b]:
                return 'e'

        elif op == 'AND':
            return reg_a & reg_b

        elif op == 'OR':
            return reg_a | reg_b

        elif op == 'XOR':
            return reg_a ^ reg_b

        elif op == 'NOT':
            return ~reg_a

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
                instrAddr= self.pc+ 2
                self.stackPush(instrAddr)
                self.pc= self.reg[operand_a]

            # RET 00010001
            elif IR == '00010001':
                # print('RET')
                popVal= self.stackPop()
                self.pc= popVal

            # CMP 10100111 00000aaa 00000bbb
            elif IR == '10100111':
                # print('CMP')
                # Compare the values in two registers.
                # ALU operation
                comp= self.alu('CMP', operand_a, operand_b)
                # `FL` bits: `00000LGE`
                if comp == 'l':
                    self.fl= 0b00000100
                elif comp == 'g':
                    self.fl= 0b00000010
                elif comp == 'e':
                    self.fl= 0b00000001
                self.pc+= 3
            
            # JEQ 01010101 00000rrr
            elif IR == '01010101':
                # print('JEQ')
                # `FL` bits: `00000LGE`
                if self.fl == 0b00000001:
                    self.pc= self.reg[operand_a]
                else:
                    self.pc+= 2

            # JGT 01010111 00000rrr
            elif IR == '01010111':
                # print('JGT')
                if self.fl == 0b00000010:
                    self.pc = self.reg[operand_a]
                else: 
                    self.pc+= 2

            # JLT 01011000 00000rrr
            elif IR  == '01011000':
                # print('JLT')
                if self.fl == 0b00000100:
                    self.pc= self.reg[operand_a]
                else: 
                    self.pc+= 2
            
            # JMP 01010100 00000rrr
            elif IR == '01010100':
                # print('JMP')
                self.pc= self.reg[operand_a]

            # JNE 01010110 00000rrr
            elif IR == '01010110':
                # print("JNE")
                if self.fl != 0b00000001:
                    self.pc = self.reg[operand_a]
                else: 
                    self.pc+= 2
            
            # AND 10101000 00000aaa 00000bbb
            elif IR == '10101000':
                res= self.alu('AND', self.reg[operand_a], self.reg[operand_b])
                self.reg[operand_a]= res
                self.pc+= 3

            # OR 10101010 00000aaa 00000bbb
            elif IR == '10101010':
                res= self.alu('OR', self.reg[operand_a], self.reg[operand_b])
                self.reg[operand_a]= res
                self.pc+= 3

            # XOR 10101011 00000aaa 00000bbb
            elif IR == '10101011':
                res= self.alu('XOR', self.reg[operand_a], self.reg[operand_b])
                self.reg[operand_a]= res
                self.pc+= 3

            # NOT 01101001 00000rrr
            elif IR == '01101001':
                res= self.alu('NOT', self.reg[operand_a], None)
                self.reg[operand_a]= res
                self.pc+= 2
                
            


