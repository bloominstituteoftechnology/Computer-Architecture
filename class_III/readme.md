# Class III Notes

## CPU Stack Notes

```sh
CPU Stack
---------

> PUSH
> POP

Some things to keep in mind:
To have a stack, need to store the data somewhere

In the `ls8`, we could use the `ram` for storage

- Store pushed items in `RAM`
- `Pointer` to the top of the `stack`
```

---

`PUSH` and `POP`
```py
elif ir == 5:  # PUSH
        # Decrement the stack pointer
        registers[7] -= 1

        # Get value from register
        reg_num = memory[pc + 1]
        value = registers[reg_num]  # We want to push this value

        # Store it on the stack
        top_of_stack_addr = registers[7]
        memory[top_of_stack_addr] = value

        pc += 2  # 2-byte instruction

        print(f"stack: {memory[0xE4:0xF5]}")

elif ir == 6:  # POP
    # Copy the value from the address pointed to by `SP`
    reg_num = memory[pc + 1]
    value = registers[reg_num]  # Want to pop this value

    # Add it to the given register.
    top_of_stack_addr = registers[7]
    memory[top_of_stack_addr] = value

    # Increment the stack pointer
    registers[7] += 1

    pc += 2  # 2-byte instruction
```