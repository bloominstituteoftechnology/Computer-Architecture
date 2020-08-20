# Class IV Notes

## Subroutines Notes

```py
# Subroutines
# -----------

# Assembly language version of functions

# They don't accept arguments
# They don't return values

# ex

def foo():
    print("Hello")
    print("World") <-- PC

foo()

foo()

foo()
```

## Stack Frames
```py
"""
Stack

699: a: 2       |
698: b: ??      | main's stack frame 
697: retaddr 1  |

696: x: 2        |
695: y: 7        |
694: z: ??       | mult2's stack frame
693: retaddr 2   |
"""
def mult2(x, y):
    z = x * y <--PC
    return z

def main():
    a = 2
    
    # retaddr 2
    # v
    b = mult2(a, 7)

    print(b)
```