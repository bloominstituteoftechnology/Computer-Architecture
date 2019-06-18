; Demonstrate calls
;
; Expected output:
; 20
; 30
; 36
; 60

; MAIN

    LDI R1,Mult2Print  ; Load R1 with the subroutine address

    ; multiply a bunch of numbers by 2 and print them
    LDI R0,10
    CALL R1

    LDI R0,15
    CALL R1

    LDI R0,18
    CALL R1

    LDI R0,30
    CALL R1

    HLT

; Mult2Print
;
; Multiply a number in R0 by 2 and print it out

Mult2Print:
    ADD R0,R0  ; or fake it by adding it to itself
    PRN R0
    RET