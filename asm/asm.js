/* DEPRECATED: use asm.py instead */

/**
 * Assembler for LS-8 v4.0
 * 
 * Example code:
 * 
 *  INC R0   ; A comment
 *  Label1:
 *  DEC R2
 *  LDI R3,Label1
 * 
 *  DS A String that is declared
 *  DB 0x0a   ; a hex byte
 *  DB 12   ; a decimal byte
 *  DB 0b0001 ; a binary byte
 */

const fs = require('fs');
const readline = require('readline');

// Process command line

const args = process.argv.slice(2);
let input, output;

if (args.length === 0) {
  input = process.stdin;
  output = process.stdout.fd;

} else if (args.length === 1) {
  input = fs.createReadStream(args[0]);
  output = process.stdout.fd;

} else if (args.length == 2) {
  input = fs.createReadStream(args[0]);
  output = fs.openSync(args[1], 'w');

} else {
  console.error("usage: asm infile.asm [outfile.ls8]");
  process.exit(1);
}

// Set up the readline interface

const rl = readline.createInterface({
  input: input
});

// Set up the symbol table
const sym = {};

// Operands:
const ops = {
  "ADD":  { type: 2, code: '10100000' },
  "AND":  { type: 2, code: '10101000' },
  "CALL": { type: 1, code: '01010000' },
  "CMP":  { type: 2, code: '10100111' },
  "DEC":  { type: 1, code: '01100110' },
  "DIV":  { type: 2, code: '10100011' },
  "HLT":  { type: 0, code: '00000001' },
  "INC":  { type: 1, code: '01100101' },
  "INT":  { type: 1, code: '01010010' },
  "IRET": { type: 0, code: '00010011' },
  "JEQ":  { type: 1, code: '01010101' },
  "JGE":  { type: 1, code: '01011010' },
  "JGT":  { type: 1, code: '01010111' },
  "JLE":  { type: 1, code: '01011001' },
  "JLT":  { type: 1, code: '01011000' },
  "JMP":  { type: 1, code: '01010100' },
  "JNE":  { type: 1, code: '01010110' },
  "LD":   { type: 2, code: '10000011' },
  "LDI":  { type: 8, code: '10000010' },
  "MOD":  { type: 2, code: '10100100' },
  "MUL":  { type: 2, code: '10100010' },
  "NOP":  { type: 0, code: '00000000' },
  "NOT":  { type: 1, code: '01101001' },
  "OR":   { type: 2, code: '10101010' },
  "POP":  { type: 1, code: '01000110' },
  "PRA":  { type: 1, code: '01001000' },
  "PRN":  { type: 1, code: '01000111' },
  "PUSH": { type: 1, code: '01000101' },
  "RET":  { type: 0, code: '00010001' },
  "SHL":  { type: 2, code: '10101100' },
  "SHR":  { type: 2, code: '10101101' },
  "ST":   { type: 2, code: '10000100' },
  "SUB":  { type: 2, code: '10100001' },
  "XOR":  { type: 2, code: '10101011' },
};

// Type to function mapping
const typeF = {
  0: out0,
  1: out1,
  2: out2,
  8: out8,
};

// Set up the machine code output
const code = [];

// Current code address (for labels)
let addr = 0;

// Source line number
let line = 0;

// Regex for matching lines
// Capturing groups: label, opcode, operandA, operandB
const regex = /(?:(\w+?):)?\s*(?:(\w+)\s*(?:(\w+)(?:\s*,\s*(\w+))?)?)?/;

// Regex for capturing DS and DB data
const regexDS = /(?:(\w+?):)?\s*DS\s*(.+)/i;
const regexDB = /(?:(\w+?):)?\s*DB\s*(.+)/i;

/**
 * Pass 1
 * 
 * Read the source code lines
 * Parse labels, opcodes, and operands
 * Record label offsets
 * Emit machine code
 */
rl.on('line', (input) => {
  line++;

  // Strip comments
  const commentIndex = input.indexOf(';');
  if (commentIndex !== -1) {
    input = input.substr(0, commentIndex);
  }

  // Normalize
  input = input.trim();

  // Ignore blank lines
  if (input === '') {
    return;
  }

  //console.log(input);
  const m = input.match(regex);

  if (m) {
    let [, label, opcode, opA, opB] = m;
    
    label = uppercase(label);
    opcode = uppercase(opcode);
    opA = uppercase(opA);
    opB = uppercase(opB);

    //console.log(label, opcode, opA, opB);

    // Track label address
    if (label) {
      sym[label] = addr;
      //console.log("Label " + label + ": " + addr);
      code.push(`# ${label} (address ${addr}):`);
    }

    if (opcode !== undefined) {
      switch (opcode) {
        case 'DS':
          handleDS(input);
          break;
        case 'DB':
          handleDB(input);
          break;
        default:
          {
            // Check operand count
            checkOps(opcode, opA, opB);

            // Handle opcodes
            const opInfo = ops[opcode];
            const handler = typeF[opInfo.type];
            handler(opcode, opA, opB, opInfo.code);
          }
          break;
      }
    }

  } else {
    console.log("No match: " + input);
    process.exit(3);
  }

});

/**
 * Pass 2
 * 
 * Output the code, substituting in any symbols
 */
rl.on('close', () => {
  // Pass two

  // Output result
  for (let i = 0; i < code.length; i++) {
    let c = code[i];

    // Replace symbols
    if (c.substr(0,4) == 'sym:') {
      let s = c.substr(4).trim();

      if (s in sym) {
        c = p8(sym[s]);
      } else {
        console.error('unknown symbol: ' + s);
        process.exit(2);
      }
    }

    fs.writeSync(output, c + '\n');
  }
});

/**
 * Check operands for sanity with a particular opcode
 */
function checkOps(opcode, opA, opB) {

  // Makes sure we have right operand count
  function checkOpsCount(desired, found) {
    if (found < desired) {
      console.error(`Line ${line}: missing operand to ${opcode}`);
      process.exit(1);
    } else if (found > desired) {
      console.error(`Line ${line}: unexpected operand to ${opcode}`);
      process.exit(1);
    }
  }

  // Make sure we know this opcode at all
  if (!(opcode in ops)) {
    console.error(`line ${line}: unknown opcode ${opcode}`);
    process.exit(2);
  }

  const type = ops[opcode].type;

  const totalOperands = (opA !== undefined? 1: 0) + (opB !== undefined? 1: 0);

  if (type === 0 || type === 1 || type === 2) {
    // 0, 1, or 2 register operands
    checkOpsCount(type, totalOperands);

  } else if (type === 8) {
    // LDI r,i or LDI r,label
    checkOpsCount(2, totalOperands);
  }
}

/**
 * Get a register number from a string, e.g. "R2" -> 2
 */
function getReg(op, fatal=true) {
  const m = op.match(/R([0-7])/);

  if (m === null) {
    if (fatal) {
      console.error(`Line ${line}: unknown register ${op}`);
      process.exit(1);
    } else {
      return null;
    }
  }

  return m[1]|0;
}

/**
 * Return a value as an 8-digit binary number
 */
function p8(v) {
  return v.toString(2).padStart(8, '0');
}

/**
 * Helper function to uppercase a string
 */
function uppercase(s) {
  if (s === undefined || s === null) {
    return s;
  }

  return s.toUpperCase();
}

/**
 * Handle opcodes with zero operands
 */
function out0(opcode, opA, opB, machineCode) {
  code.push(`${machineCode} # ${opcode}`);

  addr++;
}

/**
 * Handle opcodes with one operand
 */
function out1(opcode, opA, opB, machineCode) {
  let regA = getReg(opA);
  code.push(`${machineCode} # ${opcode} ${opA}`);
  code.push(p8(regA));

  addr += 2;
}

/**
 * Handle opcodes with two operands
 */
function out2(opcode, opA, opB, machineCode) {
  let regA = getReg(opA);
  let regB = getReg(opB);

  code.push(`${machineCode} # ${opcode} ${opA},${opB}`);
  code.push(p8(regA));
  code.push(p8(regB));

  addr += 3;
}

/**
 * Handle LDI opcode (type 8)
 */
function out8(opcode, opA, opB, machineCode) {
  let regA = getReg(opA);
  let valB = parseInt(opB);
  let outB;

  if (isNaN(valB)) {
    // If it's not a value, it might be a symbol
    outB = `sym:${opB}`;
  } else {
    outB = p8(valB);
  }

  code.push(`${machineCode} # ${opcode} ${opA},${opB}`);
  code.push(p8(regA));
  code.push(outB);

  addr += 3;
}

/**
 * Handle DS pseudo-opcode
 */
function handleDS(input) {
  const m = input.match(regexDS);
  
  if (m === null || m[2] === '') {
    console.error(`line ${line}: missing argument to DS`);
    process.exit(2);
  }

  const data = m[2];

  for (let i = 0; i < data.length; i++) {
    let printChar = data.charAt(i);

    if (printChar === ' ') {
      printChar = '[space]';
    }

    code.push(`${p8(data.charCodeAt(i))} # ${printChar}`);
  }

  addr += data.length;
}

/**
 * Handle the DB pseudo-opcode
 */
function handleDB(input) {
  const m = input.match(regexDB);
  
  if (m === null || m[2] === '') {
    console.error(`line ${line}: missing argument to DB`);
    process.exit(2);
  }

  const data = m[2];

  let val = parseInt(data);

  if (isNaN(val)) {
    console.error(`line ${line}: invalid integer argument to DB`);
    process.exit(2);
  }

  // Force to byte size
  val &= 0xff;

  code.push(`${p8(val)} # ${data}`);

  addr += 1;
}
