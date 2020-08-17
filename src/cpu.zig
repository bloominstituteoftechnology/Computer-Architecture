const std = @import("std");

const MAX_FILE_SIZE = 1024 * 1024 * 1024;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer std.debug.assert(!gpa.deinit());
    const allocator = &gpa.allocator;

    if (std.os.argv.len != 2) {
        std.log.err(.LS8ToBin, "Incorrect usage. Correct usage:\n\n\t{} ./<filename>.ls8.bin", .{std.os.argv[0]});
        std.os.exit(1);
    }

    // Get the input filepath
    const filename_len = std.mem.len(std.os.argv[1]);
    const filename = std.os.argv[1][0..filename_len];

    // Get the contents of the input file
    const cwd = std.fs.cwd();
    const program = try cwd.readFileAlloc(allocator, filename, MAX_FILE_SIZE);
    defer allocator.free(program);

    // Initialize CPU
    var cpu = Cpu.init();

    // Load program into memory
    std.mem.copy(u8, &cpu.memory, program);

    try cpu.run();
}

pub const Cpu = struct {
    memory: [256]u8,
    registers: [8]u8,

    /// Address of the currently executing instruction
    program_counter: u8,

    /// Contains a copy of the currently executing instruction
    instruction_register: u8,

    /// The memory address we're reading or writing
    memory_address_register: u8,

    /// The data to write or the value just read from memory
    memory_data_register: u8,

    /// How two numbers compared to each other
    flags: packed struct {
        less_than: bool,
        greater_than: bool,
        equal: bool,
    },

    /// Which register holds the Interrupt Mask
    pub const IM = 5;

    /// Which register holds the Interrupt Status
    pub const IS = 6;

    /// Which register holds the Stack Pointer
    pub const SP = 7;

    /// The initial value of the stack register
    pub const MEM_ADDR_KEY_PRESSED = 0xF4;

    /// The initial value of the stack register
    pub const STACK_INIT = 0xF3;

    pub fn init() @This() {
        var registers = [_]u8{0} ** 8;
        registers[SP] = STACK_INIT;

        return .{
            // Initialize ram to 0
            .memory = [_]u8{0} ** 256,
            .registers = registers,
            .program_counter = 0,
            .instruction_register = 0,
            .memory_address_register = 0,
            .memory_data_register = 0,
            .flags = .{
                .less_than = false,
                .greater_than = false,
                .equal = false,
            },
        };
    }

    pub fn run(this: *@This()) !void {
        const stdout = std.io.getStdOut().writer();
        while (true) {
            const instruction = try Instruction.decode(this.memory[this.program_counter]);
            switch (instruction) {
                .NOP => {},
                .HLT => break,
                .LDI => {
                    const register = this.memory[this.program_counter + 1];
                    const immediate = this.memory[this.program_counter + 2];
                    this.registers[register] = immediate;
                },
                .PRN => {
                    const register = this.memory[this.program_counter + 1];
                    const value = this.registers[register];
                    try stdout.print("{}", .{value});
                },
                else => {},
            }
            if (!instruction.sets_program_counter()) {
                var result: u8 = 0;
                const did_overflow = @addWithOverflow(u8, this.program_counter, instruction.number_operands() + 1, &result);
                this.program_counter = result;
            }
        }
    }
};

pub const Instruction = enum(u8) {
    /// Perform no operation
    NOP = 0b00000000,

    /// Halt execution
    HLT = 0b00000001,

    /// Add
    ADD = 0b10100000,

    /// Divide
    DIV = 0b10100011,

    /// Multiply
    MUL = 0b10100010,

    /// Modulus
    MOD = 0b10100100,

    /// Bitwise AND
    AND = 0b10101000,

    /// Bitwise NOT
    NOT = 0b01101001,

    /// Bitwise OR
    OR = 0b10101010,

    /// Call subroutine
    CALL = 0b01010000,

    /// Compare
    CMP = 0b10100111,

    /// If equal flag is set, jump to the given address
    JEQ = 0b01010101,

    /// If greater than flag or the equal flag are set, jump to the given address
    JGE = 0b01011010,

    /// If greater than flag is set, jump to the given address
    JGT = 0b01010111,

    /// If less than flag or the equal flag are set, jump to the given address
    JLE = 0b01011001,

    /// If less than flag is set, jump to the given address
    JLT = 0b01011000,

    /// Loads the data into registerA from the address in registerB
    LD = 0b10000011,

    /// Set registerA to the immediate value
    LDI = 0b10000010,

    /// Decrement
    DEC = 0b01100110,

    /// Increment
    INC = 0b01100101,

    /// Run an interrupt
    INT = 0b01010010,

    /// Return from an interrupt handler
    IRET = 0b00010011,

    /// Print the register as an ASCII value
    PRA = 0b01001000,

    /// Print the register as a number
    PRN = 0b01000111,

    pub fn number_operands(this: @This()) u2 {
        const val = @enumToInt(this);
        return @intCast(u2, (0b11000000 & val) >> 6);
    }

    pub fn alu_instruction(this: @This()) bool {
        const val = @enumToInt(this);
        return (0b00100000 & val) != 0;
    }

    pub fn sets_program_counter(this: @This()) bool {
        const val = @enumToInt(this);
        return (0b00010000 & val) != 0;
    }

    pub fn decode(val: u8) !@This() {
        return switch (val) {
            @enumToInt(@This().NOP) => .NOP,
            @enumToInt(@This().HLT) => .HLT,
            @enumToInt(@This().MUL) => .MUL,
            @enumToInt(@This().LDI) => .LDI,
            @enumToInt(@This().PRN) => .PRN,
            else => error.InvalidInstruction,
        };
    }
};
