; Keyboard.asm
;
; A simple program to test the keyboard and echo to console.
;
; Does not interpret anything; CR just moves the cursor to the start of the
; line, BS doesn't work, etc.

; Hook the keyboard interrupt

    LDI R0,0xF9          ; R0 holds the interrupt vector for I1 (keyboard)
    LDI R1,IntHandler    ; R1 holds the address of the handler
    ST R0,R1             ; Store handler addr in int vector
    LDI R5,2             ; Enable keyboard interrupts
    LDI R0,Loop
Loop:
    JMP R0               ; Infinite spin loop

; Interrupt handler
IntHandler:
    LDI R0,0xF4          ; Memory location of most recent key pressed
    LD R1,R0             ; load R1 from that memory address
    PRA R1               ; Print it
    IRET