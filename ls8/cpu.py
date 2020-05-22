"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = {k:0 for k in range(0,8)}
        self.register[7] = 0xF4
        self.pc = 0
        self.fl = 0b00000000 # 00000LGE
        self.ram = [0]*256

        self.alu_ops = {
            0b0000:self.ADD,
            0b0001:self.SUB,
            0b0010:self.MUL,
            0b0011:self.DIV,
            0b0100:self.MOD,
            0b0101:self.INC,
            0b0110:self.DEC,
            0b0111:self.CMP,
            0b1000:self.AND,
            0b1001:self.NOT,
            0b1010:self.OR,
            0b1011:self.XOR,
            0b1100:self.SHL,
            0b1101:self.SHR,
            0b1111:self.ADDI
        }

        self.pc_mutators = {
            0b0000:self.CALL,
            0b0001:self.RET,
            0b0010:self.INT,
            0b0011:self.IRET,
            0b0100:self.JMP,
            0b0101:self.JEQ,
            0b0110:self.JNE,
            0b0111:self.JGT,
            0b1000:self.JLT,
            0b1001:self.JLE,
            0b1010:self.JGE,
        }

        self.others = {
            0b0000:self.NOP,
            0b0001:self.HLT,
            0b0010:self.LDI,
            0b0011:self.LD,
            0b0100:self.ST,
            0b0101:self.PUSH,
            0b0110:self.POP,
            0b0111:self.PRN,
            0b1000:self.PRA
        }

    def load(self, filename='./examples/call.ls8'):
        
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        if len(sys.argv) > 1:
            filename = './examples/'+sys.argv[1]

        program = open(filename)

        for line in program:
            string_val = line.split("#")[0].strip()
            if string_val == '':
                continue
            v = int(string_val, 2)
            self.ram[address] = v
            address += 1

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def ram_read(self, position):
        self.pc += 1
        return self.ram[position]

    def ram_write(self, position, value):
        self.ram[position] = value

    def run(self):
        """Run the CPU."""
        self.halted = False
        self.interrupted = False

        while not self.halted:
            if not self.interrupted:
                maskedInterrupts = self.register[6] & self.register[5]
                counter = 0
                while maskedInterrupts != 0b0:
                    if maskedInterrupts & 0b1 == 1:
                        print('interrupted')
                        self.interrupted == True
                        break
                    else:
                        counter += 1
                        maskedInterrupts = maskedInterrupts >> 1
            
                if self.interrupted:
                    # Clear the bit in the IS register
                    self.register[6] = 0b0
                    # Push 'PC' register onto stack
                    self.register[7] -= 1
                    self.ram[self.register[7]] = self.pc
                    # Push FL register onto stack
                    self.register[7] -= 1
                    self.ram[self.register[7]] = self.fl
                    # Push Registers R0-R6 onto stack
                    for x in self.register[:7]:
                        self.register[7] -= 1
                        self.ram[self.register[7]] = x
                    # The address of the appropriate handler is looked
                    # up in the interrupt vector table
                    self.pc = self.ram[0xff-(8-counter)]

            
            current_instruct = self.ram_read(self.pc)
            decoded = self.decode(current_instruct)
            print((self.pc, decoded))

            # If the instruction uses the ALU
            if decoded['is_alu']:
                func = self.alu_ops[decoded['id']]
            # If the instruction sets the PC
            elif decoded['sets_pc']:
                func = self.pc_mutators[decoded['id']]
            # If it does neither of the above
            else:
                func = self.others[decoded['id']]

            if func is not None:
                # Finally call the func if given
                if decoded['num_operands'] == 0:
                    func()
                elif decoded['num_operands'] == 1:
                    reg_a = self.ram_read(self.pc)
                    func(reg_a)
                elif decoded['num_operands'] == 2:
                    reg_a = self.ram_read(self.pc)
                    reg_b = self.ram_read(self.pc)
                    func(reg_a, reg_b)
        
        sys.exit(0)

    # ALU Operations
    def ADD(self, reg_a, reg_b):
        self.register[reg_a] += self.register[reg_b]

    def SUB(self, reg_a, reg_b):
        self.register[reg_a] -= self.register[reg_b]

    def MUL(self, reg_a, reg_b):
        self.register[reg_a] *= self.register[reg_b]

    def DIV(self, reg_a, reg_b):
        self.register[reg_a] /= self.register[reg_b]

    def MOD(self, reg_a, reg_b):
        remainder = self.register[reg_a]%self.register[reg_b]
        if remainder == 0:
            print("Error, Remained is 0")
            self.halted = True
        else:
            self.register[reg_a] = remainder

    def INC(self, reg_a):
        self.register[reg_a] += 1

    def DEC(self, reg_a):
        self.register[reg_a] -= 1

    def CMP(self, reg_a, reg_b):
        val_a = self.register[reg_a]
        val_b = self.register[reg_b]

        if val_a == val_b:
            self.fl = 0b00000001
        elif val_a > val_b:
            self.fl = 0b00000010
        elif val_a < val_b:
            self.fl = 0b00000100
        else:
            self.fl = 0b0

    def AND(self, reg_a, reg_b):
        self.register[reg_a] &= self.register[reg_b]

    def NOT(self, reg_a):
        self.register[reg_a] = ~self.register[reg_a]

    def OR(self, reg_a, reg_b):
        self.register[reg_a] |= self.register[reg_b]

    def XOR(self, reg_a, reg_b):
        self.register[reg_a] ^= self.register[reg_b]

    def SHL(self, reg_a, reg_b):
        self.register[reg_a] <<= self.register[reg_b]

    def SHR(self, reg_a, reg_b):
        self.register[reg_a] >>= self.register[reg_b]

    def ADDI(self, reg_a, val):
        self.register[reg_a] += val

    # PC Mutators
    def CALL(self, reg):
        self.register[7] -= 1
        self.ram[self.register[7]] = self.pc
        self.pc = self.register[reg]

    def RET(self):
        self.pc = self.ram[self.register[7]]
        self.register[7] += 1

    def INT(self, reg_a):
        self.register[6] = self.register[reg_a]

    def IRET(self):
        # Registers R6-R0 are popped off the stack in that order
        for x in range(6,-1,-1):
            self.register[x] = self.ram[self.register[7]]
            self.register[7] += 1
        # The FL register is popped off the stack
        self.fl = self.ram[self.register[7]]
        self.register[7] += 1
        # The Return address is popped off the stack and stored in PC
        self.pc = self.ram[self.register[7]]
        self.register[7] += 1
        # Interrupts are re-enabled
        self.interrupted = False

    def JMP(self, reg_a):
        self.pc = self.register[reg_a]

    def JEQ(self, reg_a):
        a = bool(self.fl & 0b00000001)
        if a:
            self.pc = self.register[reg_a]

    def JNE(self, reg_a):
        a = bool(self.fl & 0b00000001)
        if not a:
            self.pc = self.register[reg_a]

    def JGT(self, reg_a):
        a = bool((self.fl & 0b00000010) >> 1)
        if a:
            self.pc = self.register[reg_a]

    def JLT(self, reg_a):
        a = bool((self.fl & 0b00000100) >> 2)
        if a:
            self.pc = self.register[reg_a]

    def JLE(self, reg_a):
        a = bool((self.fl & 0b00000100) >> 2)
        b = bool(self.fl & 0b00000001)
        if a or b:
            self.pc = self.register[reg_a]

    def JGE(self, reg_a):
        a = bool((self.fl & 0b00000010) >> 1)
        b = bool(self.fl & 0b00000001)
        if a or b:
            self.pc = self.register[reg_a]

    # Other Funcs
    def NOP(self):
        pass

    def HLT(self):
        self.halted = True

    def LDI(self, reg_a, val):
        self.register[reg_a] = val

    def LD(self, reg_a, reg_b):
        self.register[reg_a] = self.ram[self.register[reg_b]]

    def ST(self, reg_a, reg_b):
        self.ram[self.register[reg_a]] = self.register[reg_b]

    def PUSH(self, reg_a):
        self.register[7] -= 1
        self.ram[self.register[7]] = self.register[reg_a]
    
    def POP(self, reg_a):
        self.register[reg_a] = self.ram[self.register[7]]
        self.register[7] += 1

    def PRN(self, reg_a):
        value = self.register[reg_a]
        print(value)

    def PRA(self, reg_a):
        value = self.register[reg_a]
        print(chr(value))
        

    def decode(self, instruction):
        instruction = bin(instruction)[2:].zfill(8)
        output = {
            'num_operands':None,
            'is_alu':False,
            'sets_pc':False,
            'id':0
        }
        output['num_operands'] = int(instruction[:2],2)
        output['is_alu'] = bool(int(instruction[2],2))
        output['sets_pc'] = bool(int(instruction[3],2))
        output['id'] = int(instruction[4:], 2)
        return output
        
