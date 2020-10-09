HLT = 0b00000001
PRN = 0b01000111 
LDI = 0b10000010
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0
        self.reg[7] = 0xF4
        self.pc = 0
        
        self.branchtable = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            PUSH: self.push
        }
        
        
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    def ram_read(self, key):
        return self.ram[key]
    
    def ram_write(self, mar, mdr):
        mar %= 256
        
        self.ram[mar] = mdr
    def run(self):
        running = True
        breakpoint()
        while running:
            IR = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc +1)
            op_b = self.ram_read(self.pc +2)
            
            num_ops = IR >> 6
            
            is_alu_op = ((IR >> 5) & 0b001)
            
            if is_alu_op:
                self.alu(IR, op_a, op_b)
            else:
                self.branchtable[IR](op_a, op_b)
             
    def hlt(self) :
        self.running = False
        
    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b   
                
    def prn (self, op_a, op_B):
        print(self.reg[op_a])  
        
    def push (self, op_a, op_b):
        # decrement the SP
        self.reg[7]-=1
        
        #Get the value from reg
        value =self.reg[op_a]
        #put it on the stack at the SP   
        SP = self.reg[7]  
        self.ram_write(SP, value)
        print(self.ram_read(SP))
        
    def pop (self, op_a, op_b):
        SP = self.reg[7]   
        value = self.ram_read(SP)
        
        self.reg[op_a]=value
        
        self.reg[7] +=1
        
        