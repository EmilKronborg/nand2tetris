#!/usr/bin/env python3

class Code:
    """The code module decodes parsed instructions based on the three builtin tables: _DEST, _COMP, and _JUMP."""

    # Destination codes
    _DEST = {
        '':    '000',
        'M':   '001',
        'D':   '010',
        'MD':  '011',
        'A':   '100',
        'AM':  '101',
        'AD':  '110',
        'AMD': '111'
    }

    # Comp codes
    _COMP = {
        '0':   '0101010',
        '1':   '0111111',
        '-1':  '0111010',
        'D':   '0001100',
        'A':   '0110000',
        '!D':  '0001101',
        '!A':  '0110001',
        '-D':  '0001111',
        '-A':  '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        'M':   '1110000',
        '!M':  '1110001',
        '-M':  '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101'
    }

    # Jump codes
    _JUMP = {
        '':    '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }

    def __init__(self):
        pass

    def gen_a_instruction(self, address):
        """Returns an A instruction from given memory address."""
        return self.int_to_binary(address)

    def gen_c_instruction(self, dest_bits, comp_bits, jump_bits):
        """Returns a C instruction from dest, comp, and jump parts."""
        return '111' + self.comp_bits(comp_bits) + self.dest_bits(dest_bits) + self.jump_bits(jump_bits)

    def dest_bits(self, d):
        """Returns the corresponding binary code for the given 'dest' code."""
        return self._DEST[d]

    def comp_bits(self, c):
        """Returns the corresponding binary code for the given 'comp' code."""
        return self._COMP[c]

    def jump_bits(self, j):
        """Returns the corresponding binary code for the given 'jump' code."""
        return self._JUMP[j]

    def int_to_binary(self, int_value):
        """Converts an integer value to a binary string."""
        return f"{int(int_value):016b}"
