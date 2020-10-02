# making a binary number and then getting the value from the last two digits of the byte(8 bits)

val = 0b10000001

operandMask = 0b11000000

nVal = val & operandMask
nVal = nVal >> 6

print(nVal)

print("here is the binary rep of the same number")
print(bin(nVal))

# doing the XOR  of the the following
    
    
    
v = 0b10000001
print(v)
# the mask for the XORing
xMask = 0b10000000

s = v ^ xMask
print(s)

# checking to show how you can see the none
t = 0
if t:
    print("T is not none")
else:
    print("T is None")

#print(f"This is printing the amount the binary number from a string{int("0b00000001", base=0)}")


val = int("00000011", base=2)
print(val)
