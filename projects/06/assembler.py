#!/usr/bin/env python3

import sys

import decoder
import parser
import symbol_table


class Assembler:
    """
    This is the main class which translates and assembly file into machine code for the Hack computer.
    As suggested in the course, Assembler is implemented as two passes, where the first pass builds
    the symbol table and the second pass decodes to binary and writes to the output file.

    Usage: python3 assembler.py prog.asm
    """
    def __init__(self):
        self.base_address = 16
        self.symbol_table = symbol_table.SymbolTable()

    @staticmethod
    def get_hack_file(asm_file):
        """Substitute '.asm' with '.hack' from the given input file and use that as the
           name for the resulting binary (hack) file.
        """
        if asm_file.endswith('.asm'):
            return asm_file.replace('.asm', '.hack')
        else:
            return asm_file + '.hack'

    def _get_address(self, symbol):
        """Helper method to look up the address of a decimal value, label, or variable."""
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbol_table.contains(symbol):
                self.symbol_table.add_entry(symbol, self.base_address)
                self.base_address += 1
            return self.symbol_table.get_address(symbol)

    def first_pass(self, file):
        """Build the symbol table and map labels to their respective memory locations."""
        parse = parser.Parser(file)
        curr_address = 0
        while parse.has_more_instructions():
            parse.advance()
            instruction_type = parse.instruction_type
            if instruction_type in [parse.A_INSTRUCTION, parse.C_INSTRUCTION]:
                curr_address += 1
            elif instruction_type == parse.L_INSTRUCTION:
                self.symbol_table.add_entry(parse.symbol, curr_address)


    def second_pass(self, asm_file, hack_file):
        """Generate Hack machine code and write the result to a .hack file."""
        parse = parser.Parser(asm_file)
        with open(hack_file, 'w', encoding='utf-8') as hack_file:
            decode = decoder.Code()
            while parse.has_more_instructions():
                parse.advance()
                instruction_type = parse.instruction_type
                if instruction_type == parse.A_INSTRUCTION:
                    hack_file.write(decode.gen_a_instruction(self._get_address(parse.symbol)) + '\n')
                elif instruction_type == parse.C_INSTRUCTION:
                    hack_file.write(decode.gen_c_instruction(parse.dest, parse.comp, parse.jump) + '\n')
                elif instruction_type == parse.L_INSTRUCTION:
                    pass

    def assemble(self, file):
        """The main method that runs the first and second pass of the assembly proccess."""
        self.first_pass(file)
        self.second_pass(file, self.get_hack_file(file))

# Only allow a single input file
if len(sys.argv) != 2:
    sys.exit("Only 1 input file is allowed \nUsage: python3 assembler.py prog.asm")
else:
    asm_file = sys.argv[1]

hack_assembler = Assembler()
hack_assembler.assemble(asm_file)

