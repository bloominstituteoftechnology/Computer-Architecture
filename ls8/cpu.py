"""CPU functionality."""
import sys
sys.path.insert(
    0, "/Users/jing/Documents/git-repositories/python-practice/Computer-Architecture/ls8/examples/")
# store the binary operation code
op_bits = {
    "LDI": 0b10000010,
    "PRN": 0b01000111,
    "HLT": 0b00000001,
    "MUL": 0b10100010,
    "POP": 0b01000110,
    "PUSH": 0b01000101,
    "MUL": 0b10100010,
    "CALL": 0b01010000,
    "RET": 0b00010001,
    "CMP": 0b10100111,
    "JMP": 0b01010100,
    "JEQ": 0b01010101,
    "JNE": 0b01010110,
}
# # swtich so key is the opcode, value is the readable func name
# bits_op = {a:b for b, a in op_bits.items()}

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256  # 256 bytes of memory # this holds data that CPU will process
        self.register = [0]*8 # 8 general-purpose registers # this holds data that CPU is currently processing
        self.PC = 0b00000000 # internal register for program counter
        self.running = True 
        self.SP = 0b00000111 # stack pointer
    
    def ram_read(self, MAR):
        # read RAM from cpu register MAR (memory address register)
        return self.ram[MAR]

    def ram_write(self, MAR, value):
        # write value to cpu register 
        self.ram[MAR] =  value
    
    def load(self):
        """Load a program into memory. 
        Open a program file, read its contents and 
        save appropriate data into RAM"""
        address = 0 # for temporary load program
        # read program file 
        #filename = "./examples/mult.ls8"
        filename = sys.argv[1]
        
        with open(filename) as f:
            # print([b for a, b in enumerate(f)])
            for line in f:
                line = line.split("#")                
                try:
                    x = int(line[0], 2)  # base 10 number
                    # print(x)
                except ValueError:
                    continue
                # store file content in ram
                self.ram_write(address, x)
                address += 1

       
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB": 
            self.register[reg_a] -= self.register[reg_b]
        elif op == "CMP":            
            if self.register[reg_a] == self.register[reg_b]:
                self.flag = 0b00000001
            elif self.register[reg_a] > self.register[reg_b]:
                self.flag = 0b00000010
            elif self.register[reg_a] < self.register[reg_b]:
                self.flag = 0b00000100
            else:
                self.flag = 0b00000000
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')
        print()
    
    def ldi(self, operand_a, operand_b):
        # load immediately, store a value in a register
        self.register[operand_a] = operand_b

    def prn(self, operand_a):
        # print a value stored in a register
        print(self.register[operand_a])

    def hlt(self):
        # halt the cpu
        self.running = False
        #sys.exit(0) # exit python

    def mul(self, operand_a, operand_b):
        self.register[operand_a] *= self.register[operand_b]
    
    def push(self, value):
        # decrement SP
        self.register[self.SP] -=1
        reg_num = self.ram[self.PC+1]
        # get the value from the register
        value = self.ram_read([reg_num])
        # store it at the stack pointer
        self.ram_write(self.register[self.SP], value)
     
    def pop(self, operand):
        # get the value from the pointer, write to ram at address operand
        top_of_stack_addr = self.register[self.SP]
        value = self.ram_read(top_of_stack_addr)
        self.ram_write(operand, value)
        # increment SP
        self.register[self.SP] += 1

    def call_fun(self, fun, operand_a=None, operand_b=None):
        # to call cpc subroutines
        branch_table = {
            "LDI": self.ldi,
            "PRN": self.prn,
            "HLT": self.hlt,
            "MUL": self.mul,
            "POP": self.pop,
            "PUSH": self.push,
            "MUL": self.mul,
            "CALL": self.call,
            "RET": self.ret,
            "CMP": self.cmp,
            "JMP": self.jmp,
            "JEQ": self.jeq,
            "JNE": self.jne,
        }
        # to find the number of operands,
        # mask for the first two bits, shift right by 6
        num_operands = (op_bits[fun] & 0b11000000) >> 6
        self.PC += (num_operands + 1)
        # return the function
        branch_table[fun](operand_a, operand_b)

    def run(self):
        """Run the CPU."""
        while self.running:  
            # read address in register PC and store it in IR        
            IR = self.ram_read(self.PC)  # instruction register
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)    
            
            # get instruction
            #self.call_fun(op_table[IR])
            
            if IR in op_bits.values:
                IR_readable = op_bits[IR]
                self.call_fun[op_table])
                print(f"IR {IR}")
           

            else:
                print(f"unknow instruction {IR} at address {self.PC}")
                sys.exit(1)

            
"""         if IR not in op_bits.values:
                print("Instruction not prescribed")
                sys.exit(1)

            if IR == op_bits["LDI"]:
                self.ram_write(operand_a, operand_b)
                self.PC += 3

            elif IR == op_bits["PRN"]:
                print(self.ram_read(operand_a))
                self.PC += 2

            elif IR == op_bits["HLT"]:
                self.running = False
                self.PC += 1
"""


if __name__=="__main__":
    cpu = CPU()
    cpu.load()
    cpu.run()
