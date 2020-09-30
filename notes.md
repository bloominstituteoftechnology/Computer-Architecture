# Computer Architecture - Basics, Number Bases

## Subjects
* Number bases and conversions (binary <-> decimal <-> Hex)
* Virtual Machines - ties into guided project
* Building a simple data-driven machine - carries out instructions in the machine's memory.

## Number bases and Conversions
* Computer is built out of transistors that can only have two states. 1 - on or 0 - off.

### Text in binary
* computer maps a number to a certain character
* Two main char encodings: unicode, ASCII
* ASCII has 7 bits (2^7) = 128 chars
* Unicode has 21 bits (2^21) = 2.1 million chars

### Images and video in binary
* images are compirsed of pixels
* each pixel is comprised of Red, Blue, and Green (RGB), which can be represented as a number.
* Therefore, RGB can be represented by binary
ie: RGB(123, 75, 255)

### Audio in binary
* Audio represented as a wave
* Wave can be represented as a series of numbers which can be represented in binary
* The more sample (bits) you get, the better the quality. 

### Code in binary
* Python uses an interpreter to convert file.py into lower-level code.
* Compiler - translates .py code to byte code (a lower level langauge)
* Virtual Machine - translates byte code to machine code that can be executed by the CPU.
* Check out that article because this is DOPE.
                            library moduels vv
source code -> compiler -> byte code -> virtual machine -> running code

### Converting to/from binary
* binary to decimal

multiply each place starting at 1s by 2^n-1

question:            1010
(1 * 2^3) + (0 * 2^2) + (1 * 2^1) + (0 * 2^0)
res:                 10

binary 10010 = decimal 18

* decimal to binary

To check how many binary digits there are in the decimal, increase by 2^n+1
Select the number that's the 2nd largest to each digit and subtract that w/ the decimal. Repeat until 0.

question: 53

64 32 16 8  4  2  1
0  1  1  0  1  0  1
53 - 32 - 16 - 5 - 1 = 0

res: 0110101

If computer has certain amount of bytes, add zeros to it accordingly.

* max number n binary digits can represent is 2^n-1

### Base 16/hexadecimal

* more readable and concise representation of binary
* each digit can be 0-9 and then a - f. a - f is 10 - 15.
* more readable to computers. Easier for binary to convert to hexadecimal.

### Converting from hexadecimal

* hex to dec

Similar to binary, but multiple each place by 16^n+1 starting from 1s.

hex A2F7 = dec 41,719

Starting at A ... (10 * 16^3) + (2 * 16^3) ...

Max digits in binary that can be represented is 16^n-1.

### converting between binary and hex

* binary to hex

Divide the binary into groups of 4 and then convert each group into it's hex value. Then concat it (not add)

1011 0011 0101 - binary
B    3    5    - hex

res: B35

If not dividable by four, group from the right to the left.

1 0111 - binary
1 7 - hex  

res: 17

* hex to binary

Translate each hex digit to it's 4 digit binary equivelent.

F12A -hex

1111 0001 0010 1010 - binary

### Virtual Machines

* virtual environment that functions as a virtual machine with it's own cpu, memory, network interface, storage..."

* run OS within another OS and behaves like it's own computer.

* Hypervisor - giving resources to VM from the hardware.

* VM actually thinks it's running it's own OS and hardware

### Samples of VM

* server virtualization - single host running multiple virtual machines. ie: VMWare

* mac virtualization apps - Parallels, OracleVM, VMWare Player, etc.

* python interpreter virtual machine - translate lower-level byte code (from .py files) to machien code that can be executed by the CPU

* allows you to use your hardware to run multiple systems.

## Building a simple data-driven machine

* reads instructions and values from memory.

* very similar to the project.

