; Stack tester
;
; Expected output:
; 2
; 4
; 1

LDI R0,1
LDI R1,2
PUSH R0
PUSH R1
LDI R0,3
POP R0
PRN R0  ; "2"

LDI R0,4
PUSH R0
POP R2
POP R1
PRN R2  ; "4"

PRN R1  ; "1"
HLT
