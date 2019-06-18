; interrupts.ls8
;
; Hook the timer interrupt
;
; Expected output: sequence of "A"s, one per second.

    LDI R0,0xF8          ; R0 holds the interrupt vector for I0 (timer)
    LDI R1,IntHandler    ; R1 holds the address of the handler
    ST R0,R1             ; Store handler addr in int vector
    LDI R5,1             ; Enable timer interrupts
    LDI R0,Loop
Loop:
    JMP R0               ; Infinite spin loop

; Interrupt handler
IntHandler:
    LDI R0,65            ; Load R0 with 'A'
    PRA R0               ; Print it
    IRET
