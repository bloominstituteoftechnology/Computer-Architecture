### Day 1: Get `print8.ls8` running

- [X] Inventory what is here
- [ ] Implement the `CPU` constructor
- [ ] Add RAM functions `ram_read()` and `ram_write()`
- [ ] Implement the core of `run()`
- [ ] Implement the `HLT` instruction handler
- [ ] Add the `LDI` instruction
- [ ] Add the `PRN` instruction

```
computer-architecture/
├── asm/ # stretch territory
├── ls8/ # Lambda School 8-bit emulator
│   ├── examples/ # programs our emulator should run
│   ├── cpu.py # our CPU with operations as methods
            - self.memory = set of ordered instructions
            - self.register = our eight (R0-R7) built-in variables
            - self.pc = program counter register, index of current place in memory
            - self.ir = intruction register, index of current instruction (manipulating one or more entites in memory)
│   ├── ls8.py
            - imports, constructs, runs our CPU
│   └── README.md
├── FAQ.md
├── LS8-cheatsheet.md
├── LS8-spec.md
├── README.md
