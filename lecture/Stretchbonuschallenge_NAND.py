def NAND(a, b):
    return ~(a & b)  # "NOT (a AND b)"

def NOT(a):
    # Challenge: make this using only NAND
    # return ~(a)
    return NAND(a, a)

def AND(a, b):
    # return (a & b)
    return NOT(NAND(a, b))

def NOR(a, b):
    # return ~(a | b)
    return (NOT(a) & NOT(b))

def OR(a, b):
    # return (a | b)
    return NOT(NOR(a, b))

def XOR(a, b):
    # return (a ^ b)
    return AND(OR(a, b), NOT(AND(a, b)))

if __name__ == "__main__":
    assert(NAND(0, 0)&0x1 == 1)
    assert(NAND(0, 1)&0x1 == 1)
    assert(NAND(1, 0)&0x1 == 1)
    assert(NAND(1, 1)&0x1 == 0)

    assert(NOT(1)&0x1 == 0)
    assert(NOT(0)&0x1 == 1)

    assert(AND(0, 0) == 0)
    assert(AND(0, 1) == 0)
    assert(AND(1, 0) == 0)
    assert(AND(1, 1) == 1)

    assert(NOR(0, 0)&0x1 == 1)
    assert(NOR(0, 1)&0x1 == 0)
    assert(NOR(1, 0)&0x1 == 0)
    assert(NOR(1, 1)&0x1 == 0)

    assert(OR(0, 0) == 0)
    assert(OR(0, 1) == 1)
    assert(OR(1, 0) == 1)
    assert(OR(1, 1) == 1)

    assert(XOR(0, 0) == 0)
    assert(XOR(0, 1) == 1)
    assert(XOR(1, 0) == 1)
    assert(XOR(1, 1) == 0)

