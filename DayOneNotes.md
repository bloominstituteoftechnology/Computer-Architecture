# Computer Architecture: Basics & Number Bases - Day One

#### "In this module, we will learn the basics of how a computer is constructed and functions. Additionally we'll practice manipulating numbers in binary and hexadecimal."

#### `What is a CPU Word?`
  - `CPU Word`: The natural size of a piece of data with which the CPU can interact. Usually written down in the bit 'size' of the CPU. (ex: "This is a 64-bit CPU.")
  
  - The CPU can quickly perform math and other operations on data it word size.
  
  - It can also work with other size data as well, though it might not be as quick.

#### `How does RAM work?`
  - Random Access Memory (RAM): Think of this as a big array of bytes that can be retrieved by index, just like a regular array.
  
  - In memory `parlance`*, the index into memory is referred to as an 'address' or a 'pointer'
  
  - When you have the address of a value (AKA a pointer to that value), you can retrieve that value stored at that address.

- *`parlance:` a particular way of speaking or using words, especially a way common to those with a particular job or interest.

#### `How do parts of the CPU communicate?`
The most important things a CPU needs to communicate with other parts of the computer are:
   
   - `The RAM `: Temporarily holds data needed to be processed from peripheral
   - `Data Bus`: Carries data between parts
    

#### `What is a CPU Instruction?`
  - A byte or sequence of bytes in RAM that the computer knows how to interpret and perform actions based on input.

  - There are instructions to do:
    - Math: ADD and SUB
    - Value Comparison: CMP
    - Memory Jump: JMP

  - *The exact instruction names and values vary depending on architecture*


#### `What is a CPU Register?`
  - The CPU has a fixed, small number of special storage locations built in.
  - Usually there are 16 or 32 of these
  - The have fixed names, such as R0, R1, R2, and so on.
  - *Details vary on architecture*
  - Think of them like variables you have at your disposal to use with the various instructions.


#### `What does the CPU Clock represent?`
  - The number of times per second the CPU does some processing. (When they say your CPU is 3.2GHz, this is what they're referring to.)
  - Each time the clock cycles, the CPU does some more work
  - Some instructions take one clock cycle to complete but others might take several

#### `What is the System Bus?`
  - A collection of wires on the motherboard between the CPU, memory and peripherals.
    - The memory bus connects the CPU to the RAM
    - The I/O bus connects the CPU to peripherals
    - The control bus allows the CPU to say exactly what it wants to do on the bus (like read or write a byte)

#### `What size is the System Bus?`
Common Bus Sizes are:

  - 4 bits
  - 8 bits
  - 12 bits
  - 16 bits
  - 24 bits
  - 32 bits
  - 64 bits
  - 80 bits
  - 96 bits
  - 129 bits


#### `How does the CPU provide concurrency?`
  - Concurrency and Parallelism: The CPU can do multiple things at once through a variety of mechanisms, including having multiple cores, or other features such as *pipelining* or *hyperthreading*
    - Why is having multiple cores more efficient?
    [Multiple Core Processors: Is More Always Better?](https://www.lifewire.com/multiple-core-processors-832453)
      Multi-core Technology Advantages:
        - The computer will work faster for certain programs
        - The computer may not get as hot when it is turned on
        - The computer saves power by turning off sections that are not being used
        - More features can be added to the computer
        - The signals between different CPUs travel shorter distances, therefore they degrade less.
    - `What is Pipelining?`
    [What is pipelining? - Definition from WhatIs.com](https://whatis.techtarget.com/definition/pipelining)
        - With pipelining, the computer architecture allows the next instructions to be fetched *while* the processor is performing arithmetic operations
        - They are held in a `buffer` close to the processor until each instruction operation can be performed
        - Computer processor pipelining is sometimes divided into an instruction pipeline and an arithmetic pipeline
        - `Instruction Pipeline:` Represents the stages in which an instruction is moved through the processor, including being fetched, perhaps buffered, and then executed.
        - `Arithmetic Pipeline:` Represents the parts of an arithmetic operation that can be broken down and overlapped as they're performed.


### Challenge

##### `How long does it take the number of transistors on a CPU to double? What is the common name for this rule of thumb?`
The overall processing power for computers will double every two years. This is the Moore's Law computing term originating from ~1970.

##### `Why are registers necessary? Why not just use RAM?`
RAM can be pretty slow sometimes. Normally, it takes twice as many CPU cycles to fetch a byte from RAM than to access an internal register.

##### `Why is cache useful?`
Data will be placed in caches for faster accessibility time.

##### `What is a CPU word?`
 - `CPU Word`: The natural size of a piece of data with which the CPU can interact. Usually written down in the bit 'size' of the CPU. (ex: "This is a 64-bit CPU.")


##### `What is the system bus and how wide is it?`
  - A collection of wires on the motherboard between the CPU, memory and peripherals.
  - The system bus width is important because it determines how much data can be transmitted at once. Most popular bus sizes are 16-bit and 32-bit.

##### `Describe the pins that are on a CPU chip.`
[Pins on CPU chips](https://users.cs.fiu.edu/~downeyt/cda4101/cpu-pins.html)

##### `What is a CPU instruction?`
The instruction set provides commands to the processor to tell it what it needs to do (Machine Language)

---------------

## Learn to convert between and show understanding of decimal, binary, and hexadecimal

It's important to understand that when you have '12' apples on the table, it's still the same number of apples regardless of whether or not you say there are '12 apples' (decimal), 'C apples' (hexadecimal), or '1100 apples' (binary).

*The count of the number of items does not change just because we refer to it in a numbering system of a different base*

#### `On Bases`
The `base` of a numbering system refers to how many digits the numbering system has.
  
  - `Decimal numbers` : base - 10
  - `Binary numbers` : two digits, 0 and 1. base - 2
  - `Hexadecimal` : 16 digits, 0 - 9 then A- F. It's base - 16
  - `Octal`(rare) : base - 8
  
  
  
```
// All of these represent the number of apples on the table:

let numA = 12;     // decimal
let numB = 0xC;    // hexadecimal, leading 0x
let numC = 0b1100; // binary, leading 0b

numA === numB === numC; // TRUE!
```

#### `On Binary`
wut


#### `Converting Binary to Decimal`

JS: 
```
// Binary constants:

let myBinary = 0b101; // 101 binary is 5 decimal

// Converting a binary string to a Number

let myValue1 = Number('0b101');

// or

let myValue2 = parseInt('101', 2); // base 2

// All these print 5:
console.log(myBinary); // 5
console.log(myValue1); // 5
console.log(myValue2); // 5
```

By Hand:
```
+------ 8's place
|+----- 4's place
||+---- 2's place
|||+--- 1's place
||||
1010
```

*The above example has one 8, zero 4s, one 2, and zero 1s. That is, it has one 8 and one 2. One 8 and one 2 is 10, 8+2=10, so:*

```
1010 binary == 10 decimal.
```

#### Converting Decimal to Binary 

JS: 
```
// Decimal constants (just like normal)

const val = 123;

// Converting a decimal to a binary string

const binVal = val.toString(2); // convert to base 2 number string

console.log(`${val} decimal is ${binVal} in binary`);
```
*Note that the result is a string. This makes sense because you already had the number in val as a Number type; the only other way to represent it is as a string.*

By Hand:

Example: convert 123 decimal into binary. You have to come up with sum of the powers of two that add up to it.



STEP ONE - Start with the highest power of two that’s lower than the number: 64. We know we have zero 128s in the number, because it’s only 123. But there must be a 64 in there.

So let’s put a 1 in the 64s place:

```
1xxxxxx     All the x's are unknown
```

STEP 2 - Now we compute 123-64 because we’ve taken the 64 out of there. 123-64=59. So let’s go to the next power of two down: 32.

59 has a 32 in it, so that must be a 1 in the 32’s place, as well:

```
11xxxxx     All the x's are unknown
```

STEP 3 - Compute 59-32=27 and go down to the next power of two: 16. There’s one 16 in 27, so that’s a 1 in the 16s place:

```
111xxxx     All the x's are unknown
```

STEP 4 - Then we compute 27-16=11 and do the next power of two: 8. There’s 1 8 in 11, so that’s 1, too:

```
1111xxx     All the x's are unknown
```

STEP 5 - Then we compute 11-8=3 and do the next power of two: 4. There are zero 4s in

```
11110xx     All the x’s are unknown
```

We’re still at 3 decimal, but we drop to the next power of two: 2. There is one 2 in 3, so that’s a 1:

```
111101x     All the x's are unknown
```


STEP 6 - Compute 3-2=1, and drop to the last power of two: 1. There is one 1 in 1, so that’s a 1:

```
1111011 binary is 123 decimal
```


#### `Hexadecimal`
Hex is a base - 16 numbering system.


Counting to decimal 16 in hex:

```
0 1 2 3 4 5 6 7 8 9 A B C D E F 10
```

#### Converting Binary to Hex

If we have a 1-byte number, like `01101100`, we split it into segments of `4` bits and convets each of those to a hex digit.

```
00111100
```
split it into segments of `4` bits

```
0011 1100
```

convert to hex (or decimal then hex if that's more convenient):

```
0011 1100
 3    C      (C hex == 12 decimal == 1100 binary)
```

## Challenge

#### `Count to 0x20 in hex`
32

#### `What is 0x2F in binary?`
0b101111

#### `Convert 0b11011 to decimal`
27

#### `What is 0b11100111 in hex?`
0xE7

#### `What is 27 in binary?`
0b11011

#### `Write a program that outputs a value in binary. Hint: >> and &`

STEP 1 - if NUM > 1:
  - push NUM on stack
  - recursively call function with 'NUM / 2'
      
STEP 2 :
  - pop NUM from stack, divide it by 2 and print it's remainder.

```
# representation of a given number 
def bin(n) : 
    if n > 1 : 
        bin(n // 2) 
          
    print(n % 2,end = "") 
      
if __name__ == "__main__" : 
  
    bin(7) 
    print() 
    bin(4) 
```


*Now for some Jameson*