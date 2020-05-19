"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = {k:0 for k in range(0,8)}
        self.register[7] = 0xF4
        self.pc = 0
        self.fl = None
        self.ram = [0]*256

        self.id_to_alu_ops = {
            '0000':'ADD',
            '0001':'SUB',
            '0010':'MUL',
            '0011':'DIV',
            '0100':'MOD',
            '0101':'INC',
            '0110':'DEC',
            '0111':'CMP',
            '1000':'AND',
            '1001':'NOT',
            '1010':'OR',
            '1011':'XOR',
            '1100':'SHL',
            '1101':'SHR'
        }

    def load(self, filename='./examples/print8.ls8'):
        
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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            pass
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

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
            print(" %02X" % self.register[i], end='')

        print()

    def ram_read(self, position):
        return self.ram[position]

    def ram_write(self, position, value):
        self.ram[position] = value

    def run(self):
        """Run the CPU."""
        halted = False

        while not halted:
            current_instruct = self.ram_read(self.pc)
            decoded = self.decode(current_instruct)
            self.pc += 1

            # If decoded is none, then we know we hit a halt
            if decoded is None:
                halted = True

            # If the decoded instruction is for the alu
            elif decoded['is_alu']:
                # First get the id of the operation
                id_ = bin(decoded['id'])[2:].zfill(4)
                # Then using the id to alu ops dict, determine
                # the actual operation
                op = self.id_to_alu_ops[id_]
                # Initialize reg_a and reg_b to default None
                reg_a, reg_b = None,None
                # Will always have to read reg_a from ram
                reg_a = self.ram_read(self.pc)
                # Increment the counter
                self.pc += 1
                # If the number of operands is two, read reg_b
                if decoded['num_operands'] == 2:
                    reg_b = self.ram_read(self.pc)
                    self.pc += 1

                # Call the ALU to execute the op on the registers
                self.alu(op, reg_a, reg_b)

            # If the decoded instruction is not for the ALU
            else:
                if decoded['id'] == 0b0010: # LDI
                    register = self.ram_read(self.pc)
                    self.pc += 1
                    value = self.ram_read(self.pc)
                    self.pc += 1
                    self.register[register] = value
                elif decoded['id'] == 0b0111: # PRN
                    register = self.ram_read(self.pc)
                    self.pc += 1
                    print(self.register[register])
        
        sys.exit(1)
            

    def decode(self, instruction):
        instruction = bin(instruction)[2:].zfill(8)
        if instruction == "00000001":
            return None
        else:
            output = {
                'num_operands':None,
                'is_alu':False,
                'sets_pc':False,
                'id':0
            }
            output['num_operands'] = int(instruction[:1],2)+1
            output['is_alu'] = bool(int(instruction[2],2))
            output['sets_pc'] = bool(int(instruction[3],2))
            output['id'] = int(instruction[4:], 2)
            return output
        
