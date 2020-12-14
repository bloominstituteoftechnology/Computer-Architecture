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
HLT
