#!/usr/bin/env python3

class SymbolTable:
    symbols = {
        "SP":     "0000000000000000",
        "LCL":    "0000000000000001",
        "ARG":    "0000000000000010",
        "THIS":   "0000000000000011",
        "THAT":   "0000000000000100",
        "R0":     "0000000000000000",
        "R1":     "0000000000000001",
        "R2":     "0000000000000010",
        "R3":     "0000000000000011",
        "R4":     "0000000000000100",
        "R5":     "0000000000000101",
        "R6":     "0000000000000110",
        "R7":     "0000000000000111",
        "R8":     "0000000000001000",
        "R9":     "0000000000001001",
        "R10":    "0000000000001010",
        "R11":    "0000000000001011",
        "R12":    "0000000000001100",
        "R13":    "0000000000001101",
        "R14":    "0000000000001110",
        "R15":    "0000000000001111",
        "SCREEN": "0110000000000000",
        "KBD":    "0100000000000000",
    }

    def __init__(self):
        pass

    # TODO: Can some of these methods be rewritten as lambdas instead?
    def is_address_instruction(self, line):
        return line.startswith("@")

    def is_compute_instruction(self, line):
        return "=" in line or ";" in line

    def is_label(self, line):
        return line.startswith("(") and line.endswith(")")

    def label_value(self, line):
        return line.replace("(", "").replace(")", "").strip()

    def decimal_to_binary(self, decimal_value):
        return f"{int(decimal_value):016b}"

    def build_symbol_table(self, lines):
        _current_line = 0
        _base_address = 16
        """Increment the current line if it is an address or a compute instruction.
           Otherwise, add the label to the symbol table.
        """
        for line in lines:
            if self.is_address_instruction(line) or self.is_compute_instruction(line):
                _current_line += 1
            elif self.is_label(line):
                cur_label = self.label_value(line)
                print(f"Line {_current_line} ({_current_line + 8}) holds {cur_label}")
                self.symbols[self.label_value(line)] = self.decimal_to_binary(_current_line + 1)
        """Add address instructions starting from memory location 16."""
        for line in lines:
            if self.is_address_instruction(line):
                value = line[1:]
                if value not in self.symbols and not value.isnumeric():
                    self.symbols[value] = self.decimal_to_binary(_base_address)
                    _base_address += 1
        return self.symbols

