LDI R1, 0 ; loop index
LDI R2, 7 ; number of lines to print

MainLoopStart:
    CMP R1, R2
    LDI R0, MainLoopEnd
    JGE R0
    LDI R0, 1
    SHL R0, R1 ; number of chars to print 
    LDI R3, PrintN
    CALL R3
    INC R1
    LDI R0, MainLoopStart
    JMP R0

MainLoopEnd:
    HLT

; R0 arg corresponds to number of chars to print
PrintN:
    PUSH R1
    PUSH R2
    PUSH R3
    LDI R1, 1
    
    PrintNLoopStart:
        CMP R1, R0
        LDI R2, PrintNLoopEnd
        JGT R2
        LDI R2, PrintAsterisk
        CALL R2
        INC R1
        LDI R2, PrintNLoopStart
        JMP R2

    PrintNLoopEnd:
        LDI R3, Newline
        LD R2, R3
        PRA R2
        POP R3
        POP R2
        POP R1
        RET

PrintAsterisk:
    PUSH R0
    PUSH R1
    LDI R0, Asterisk
    LD R1, R0 ; load the * character into R0
    PRA R1
    POP R1
    POP R0
    RET

Asterisk:
    ds *

Newline:
    db 0x0a