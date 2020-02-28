

def toBinString(number):
    compare = 128
    out = ""
    for i in range(8):
        if compare & number > 0:
            out += "1"
        else:
            out += "0"
        compare = compare >> 1
    return out


print(toBinString(1))
print(toBinString(2))
print(toBinString(3))
print(toBinString(4))
print(toBinString(5))
print(toBinString(12))
print(toBinString(16))
