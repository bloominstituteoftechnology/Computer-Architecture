; Code to test the Sprint Challenge
;
; Expected output:
; 1
; 4
; 5

LDI R0,10
LDI R1,20
LDI R2,Test1
CMP R0,R1
JEQ R2       ; Does not jump because R0 != R1
LDI R3,1
PRN R3       ; Prints 1

Test1:

LDI R2,Test2
CMP R0,R1
JNE R2       ; Jumps because R0 != R1
LDI R3,2
PRN R3       ; Skipped--does not print

Test2:

LDI R1,10
LDI R2,Test3
CMP R0,R1
JEQ R2      ; Jumps becuase R0 == R1
LDI R3,3
PRN R3      ; Skipped--does not print

Test3:

LDI R2,Test4
CMP R0,R1
JNE R2      ; Does not jump because R0 == R1
LDI R3,4
PRN R3      ; Prints 4

Test4:

LDI R3,5
PRN R3      ; Prints 5
LDI R2,Test5
JMP R2      ; Jumps unconditionally
PRN R3      ; Skipped-does not print

Test5:

HLT

