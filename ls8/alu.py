'''
ALU package for quick lookup and manipulation of alu functionality
'''
class ALU():
    def __init__(self, cpu):
        self.alu_ops = {}

        # operations
        self.alu_ops['ADD'] = self.add
        self.alu_ops['SUB'] = self.sub
        self.alu_ops['MUL'] = self.mul
        self.alu_ops['DIV'] = self.div
        self.alu_ops['CMP'] = self.cmp

        
        # use reference to cpu class to make updates
        self.cpu = cpu

    def add(self, a, b):
        self.cpu.reg[a] += self.cpu.reg[b]
        self.cpu.reg[a] & 0xFF

    def sub(self, a, b):
        self.cpu.reg[a] -= self.cpu.reg[b]
        self.cpu.reg[a] & 0xFF

    def mul(self, a, b):
        self.cpu.reg[a] *= self.cpu.reg[b]
        self.cpu.reg[a] & 0xFF

    def div(self, a, b):    
        if b == 0:
            raise Exception("Can't divide by zero")
            # halt program
            self.cpu.halt = True
            
        self.cpu.reg[reg_a] /= self.cpu.reg[reg_b]
        self.cpu.reg[a] & 0xFF

    def cmp(self, a, b):
        '''
        Compare the values in two registers.
        Sets the flag in cpu based on result
        '''
        # reset flag
        self.cpu.fl = 0

        # compare values
        if self.cpu.reg[a] < self.cpu.reg[b]:
            self.cpu.fl = self.cpu.fl ^ 0b00000100
        elif self.cpu.reg[a] > self.cpu.reg[b]:
            self.cpu.fl = self.cpu.fl ^ 0b00000010
        else:
            self.cpu.fl = self.cpu.fl ^ 0b00000001

    def contains(self, operation):
        if operation in self.alu_ops:
            return True
        else:
            return False

    def operation(self, instruction):
        return self.alu_ops[instruction]

