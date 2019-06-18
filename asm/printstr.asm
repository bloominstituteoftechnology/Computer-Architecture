; Prints Hello, world!
;
; Declares a subroutine that prints a string at a given address
;
; Expected output: Hello, world!

	LDI R0,Hello         ; address of "Hello, world!" bytes
	LDI R1,14            ; number of bytes to print
	LDI R2,PrintStr      ; address of PrintStr
	CALL R2              ; call PrintStr
	HLT                  ; halt

; Subroutine: PrintStr
; R0 the address of the string
; R1 the number of bytes to print

PrintStr:

	LDI R2,0            ; SAVE 0 into R2 for later CMP

PrintStrLoop:

	CMP R1,R2           ; Compare R1 to 0 (in R2)
	LDI R3,PrintStrEnd  ; Jump to end if we're done
	JEQ R3         

	LD R3,R0            ; Load R3 from address in R0
	PRA R3              ; Print character

	INC R0              ; Increment pointer to next character
	DEC R1              ; Decrement number of characters

	LDI R3,PrintStrLoop ; Keep processing
	JMP R3

PrintStrEnd:

	RET                 ; Return to caller

; Start of printable data

Hello:

	ds Hello, world!
	db 0x0a             ; newline

