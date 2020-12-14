OP1 = 0b10101010
OP2 = 0b11110000


class Foo:

    def __init__(self):
        # Set up the branch table
        self.branchtable = {}
        self.branchtable[OP1] = self.handle_op1
        self.branchtable[OP2] = self.handle_op2

    def handle_op1(self, a):
        print("op 1: " + a)

    def handle_op2(self, a):
        print("op 2: " + a)

    def run(self):
        # Example calls into the branch table
        ir = OP1
        self.branchtable[ir]("foo")

        ir = OP2
        self.branchtable[ir]("bar")


c = Foo()
c.run()
