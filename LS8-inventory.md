# File Inventory for LS8 Repository

## Directory Map

Computer-Architechture\
	.gitignore
	FAQ.md
	LS8-cheatsheet.md
	LS8-spec.md
	README.md
	asm\
        README.md
        asm.js
        buildall
        call.asm
        interrupts.asm
        keyboard.asm
        mult.asm
        print8.asm
        printstr.asm
        sctest.asm
        stack.asm
        stackoverflow.asm
    ls8\
        README.md
        cpu.py
        ls8.py
        examples\
            call.ls8
            interrupts.ls8
            keyboard.ls8
            mult.ls8
            print8.ls8
            printstr.ls8
            sctest.ls8
            stack.ls8
            stackoverflow.ls8

## File Descriptions

### Computer-Architecture

- .gitignore

Ensures repo stays neat and tidy, i.e. free of pycache files.

- FAQ.md

Answers to low-level conceptual and implementation questions.

- LS8-cheatsheet.md

Simplified psudo-code explanation of LS8-spec.md

- LS8-spec.md

Explains what each type of element in memory array is and how it works with the others.

- README.md

Self Explanatory

### asm

TODO

### ls8

- README.md 

Self Expalantaory

- cpu.py

Defines CPU class for use in ls8.py.

- ls8.py

Loads and runs instance of cpu from cpu.py.

### examples

- call.ls8
- interrupts.ls8

Contains memeory array elements for imitating time library functionality.

- keyboard.ls8
- mult.ls8

Contains memory array elements for multiplying 8 and 9 together.

- print8.ls8

Contains memory array elements for printing the number 8.

- printstr.ls8
- sctest.ls8
- stack.ls8

Contains memory array elements for implementing a stack.

- stackoverflow.ls8