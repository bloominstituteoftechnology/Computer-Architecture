# Class I Notes

## Number Bases

The base number tells us how many digits we have

- **Base 2:** a.k.a Binary, digits 0-1
    - ex. 01010101
- **Base 8:** a.k.a Octal, digits 0-7
    - ex. 304611743
- **Base 10:** a.k.a Decimal, 0-9
    - ex. 19740
- **Base 16:** a.k.a Hexadecimal, digits 0-F (0-9, A-F)
    - ex. 397F03AB73
- **Base 64:** a.k.a Base 64, digits 0-9, a-z, A-Z, +, /
    - 9302Zjd73Hdr487Kx

---

## Memory

Think of memory in a computer as a big array of bytes, 8-bits per byte

The index into the memory array is AKA location / address / pointer

---

## BASIC Emulator

```py
# 1 - PRINT AARON
# 2 - HALT

memory = [
    1,
    1,
    1,
    2
]

running = True

pc = 0 #> Program Counter: the index into memory of the currently
       #> executing instruction

while running:
    ir = memory[pc] #> the instruction register

    if ir == 1:
        print("AARON")
        pc += 1

    elif ir == 2:
        running = False
        pc += 1
```