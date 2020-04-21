import sys

LDI = 0b10000010 
PRN = 0b01000111 
HLT = 0b00000001
MUL = 0b10100010

PUSH = 0b01000101   
POP = 0b01000110    
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
SP = 7  

# Sprint challenge 
CMP = 0b10100111
JMP = 0b01010100 
JEQ = 0b01010101
JNE = 0b01010110 
LT = 0b00000100
GT = 0b00000010
EQ = 0b00000001




class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        # construct RAM + REG + PC 
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0       # program counter is the address of currently executing instructions 
        self.fl = 0
        self.bt = {        
            LDI: self.op_ldi,
            PRN: self.op_prn,
            HLT: self.op_hlt,
            ADD: self.op_add,
            MUL: self.op_mul,
            POP: self.op_pop,
            PUSH: self.op_push,
            CALL: self.op_call,
            RET: self.op_ret,
            CMP: self.op_cmp, 
            JMP: self.op_jmp,
            JEQ: self.op_jeq,  
            JNE: self.op_jne 
        }

    def op_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def op_prn(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def op_hlt(self, operand_a, operand_b):
        sys.exit(0)

    def op_add(self):
        self.alu("ADD", self.ram_read(self.pc + 1), self.ram_read(self.pc+2))

    def op_mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

    def op_pop(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop_val()

    def op_push(self, operand_a, operand_b):
        self.push_val(self.reg[operand_a])

    def op_call(self, operand_a, operand_b):
        self.push_val(self.pc + 2)
        self.pc = self.reg[operand_a]

    def op_ret(self):
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] += 1
    def op_cmp(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
    def op_jmp(self, operand_a, operand_b):
        # set the PC to the address stored in the given register 
        self.pc = self.reg[operand_a]
    def op_jeq(self, operand_a, operand_b):
        # if equal flag is set (true), jump to the address stored in the given register
        if self.fl == EQ: 
            self.pc = self.reg[operand_a]
        else: 
            self.pc += 2
    def op_jne(self, operand_a, operand_b):
        # if equal flag is clear (false, 0) jump to the address stored in the given register
        if not self.fl == EQ: 
            self.pc = self.reg[operand_a]
        else: 
            self.pc += 2
    





    def ram_read(self, mar):
        #mar = memory address register // mdr = memory data register 
        #read the address and write out the number (data) 
        mdr = self.ram[mar]
        return mdr
    
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def push_val(self, val):
        self.reg[SP] -= 1
        self.ram_write(val, self.reg[SP])

    def pop_val(self):
        val = self.ram_read(self.reg[SP])
        self.reg[SP] += 1
        return val






    def load(self, filename):
        """Load a program into memory."""
        try: 
            address = 0
            #open the file
            with open(sys.argv[1]) as f:
                # read every line 
                for line in f: 
                    # parse out comments 
                    comment_split = line.strip().split("#")
                    #c cast number string to int 
                    value = comment_split[0].strip() 
                    # ignore blank lines 
                    if value == "":
                        continue 
                    instruction = int(value, 2)
                    # populate memory array 
                    self.ram[address] = instruction 
                    address += 1
        except: 
            print("cant find file")
            sys.exit(2)




    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # ADDING SUBTRACTION
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        ## ADDING MULTIPLICATION
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = LT 
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = GT 
            else: 
                self.fl = EQ
        else:
            raise Exception("Unsupported ALU operation")

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
            print(" %02X" % self.reg[i], end='')

        print()



    def run(self):
        """Run the CPU."""    
        while True: 
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            instruction_length = (instruction >> 6) + 1
            instruction_set_pc = ((instruction >> 4) & 0b1 )== 1
            
            if instruction in self.bt:
                self.bt[instruction](operand_a, operand_b)
            #check if opcode instructions sets the pc
            # If not, increment pc by instruction length
            if instruction_set_pc != 1:
                self.pc += instruction_length