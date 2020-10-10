'''
Branchtable for O(1) access to instruction functions
'''
class Branchtable():
    def __init__(self, cpu):
        self.branchtable = {}

        # instructions
        self.branchtable[0x82] = self.ldi
        self.branchtable[0x47] = self.prn
        self.branchtable[0xA2] = self.mul
        # use reference to cpu class to make updates
        self.cpu = cpu

    def ldi(self, *args):
        '''
        sets the value of a register to a specified integer value
        '''
        r = args[0]
        value = args[1]
        self.cpu.reg[r] = value

    def prn(self, *args):
        '''
        Print value at stored in specified register
        '''
        r = args[0]
        print(self.cpu.reg[r])

    def mul(self, *args):
        '''
        Multiply values passed in registers
        '''
        op = 'MUL'
        r_a = args[0]
        r_b = args[1]
        self.cpu.alu(op, r_a, r_b)

    def contains(self, instruction):
        if instruction in self.branchtable:
            return True
        else:
            return False

    def instruction(self, instruction):
        return self.branchtable[instruction]


