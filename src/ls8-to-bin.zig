const std = @import("std");
const cpu = @import("./cpu.zig");

const MAX_FILE_SIZE = 1024 * 1024 * 1024;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer std.debug.assert(!gpa.deinit());
    const allocator = &gpa.allocator;

    if (std.os.argv.len != 2) {
        std.log.err(.LS8ToBin, "Incorrect usage. Correct usage:\n\n\t{} ./<filename>.ls8", .{std.os.argv[0]});
        std.os.exit(1);
    }

    // Get the input filepath
    const filename_len = std.mem.len(std.os.argv[1]);
    const filename = std.os.argv[1][0..filename_len];

    // Append `.bin` to the filepath to get the output file path
    const output_filepath = try std.fmt.allocPrint(allocator, "{}.bin", .{filename});
    defer allocator.free(output_filepath);

    // Get the contents of the input file
    const cwd = std.fs.cwd();
    const contents = try cwd.readFileAlloc(allocator, filename, MAX_FILE_SIZE);
    defer allocator.free(contents);

    // Convert the LS8 text into actually binary LS8
    const bytes = try ls8_to_bin(allocator, contents);
    defer allocator.free(bytes);

    // Write the binary file
    try cwd.writeFile(output_filepath, bytes);
}

pub fn ls8_to_bin(allocator: *std.mem.Allocator, text: []const u8) ![]u8 {
    var bin = std.ArrayList(u8).init(allocator);
    errdefer bin.deinit();

    var line_iterator = std.mem.tokenize(text, "\n");
    while (true) {
        const opcode_byte = (try next_byte(&line_iterator)) orelse break;
        const opcode = try cpu.Instruction.decode(opcode_byte);

        try bin.append(@enumToInt(opcode));

        var num_operands = opcode.number_operands();
        while (num_operands != 0) : (num_operands -= 1) {
            const operand = (try next_byte(&line_iterator)) orelse return error.UnexpectedEndOfFile;

            try bin.append(operand);
        }
    }

    return bin.toOwnedSlice();
}

pub fn next_byte(line_iterator: *std.mem.TokenIterator) !?u8 {
    // There can be empty lines (or lines just for comments), and we want to find
    // the next non empty line
    while (true) {
        const line = line_iterator.next() orelse return null;
        if (try line_to_byte(line)) |byte| {
            return byte;
        }
    }
}

pub fn line_to_byte(line: []const u8) !?u8 {
    // Remove comments and whitespace
    const comment_start = std.mem.lastIndexOfScalar(u8, line, '#') orelse line.len;
    const without_comment = line[0..comment_start];
    const without_whitespace = std.mem.trim(u8, without_comment, "\r\n\t ");

    if (std.mem.eql(u8, without_whitespace, "")) {
        // Ignore empty lines
        return null;
    }

    // Parse the binary number
    return try std.fmt.parseInt(u8, without_whitespace, 2);
}
