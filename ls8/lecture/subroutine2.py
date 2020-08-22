# Stacks and calls in higher level languages


def mult2(x, y):
    z = x*y
    return z
    
def main():
    a = 2
    
    b = mult2(a, 7)

    print(b)

main()

print("Done")
"""
PC         Stack
------------------
15
           2 (a)               |
           0 (b)               | main's stack frame
           17 (return addr)    |
     
           2 (x)               |
           7 (y)               | mult2's stack frame
           14 (z)              |
11 at the equal sign

now delete the mult2's stack frame after return 14 to b in main's stack frame        


Each time you call, a new stack frame is allocated
Each time you return, the stack frame is deallocated



"""

Python variables
--------------------
>>> a = "hello"
>>> id(a) # return a's address
>>> b = a  # a, b has the same address
