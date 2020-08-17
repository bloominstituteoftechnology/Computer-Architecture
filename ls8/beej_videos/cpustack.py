'''
CPU Stack
---------

Built into the CPU
PUSH 
POP

WHT DO YOU NEED FOR A STACK?
* Store items in RAM - Best choice
    * Store items in registers - VERY LIMITED
* Pointer to the top of the stack - SP (stack pointer) - Stored at R7



EXAMPLE OF MEMORY MAP:
| FF  I7 vector         |    Interrupt vector table
| FE  I6 vector         |
| FD  I5 vector         |
| FC  I4 vector         |
| FB  I3 vector         |
| FA  I2 vector         |
| F9  I1 vector         |
| F8  I0 vector         |
| F7  Reserved          |
| F6  Reserved          |
| F5  Reserved          |
| F4  Key pressed       |    Holds the most recent key pressed on the keyboard
| F3  Start of Stack    |
| F2  [more stack]      |    Stack grows down
| ...                   |
| 01  [more program]    |
| 00  Program entry     |
  ^
  THIS IS THE ADDRESS
        ^
        THIS IS WHAT IS STORED



'''