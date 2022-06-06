#!/usr/bin/env python3

import lexer

class Parser:
    """
    Parses the hack assembly program line by line with the very important assumption
    that there are no errors in the program.
    """
    # Types of Instructions as integer constants (address, compute, label)
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    L_INSTRUCTION = 2

    def __init__(self, file):
        self.lexer = lexer.Lex(file)
        self._init_instruction_info()

    def _init_instruction_info(self):
        """
        Helper method to initialize each of the the instruction types.
        """
        self._instruction_type = -1
        self._symbol = ""
        self._dest = ""
        self._jump = ""
        self._dest = ""

    def _a_instruction(self):
        """
        Address instruction with possible values:
            * @number: @45, @29
            * @symbol: @i, @n, @LOOP, @END. Here, are variables and LOOP and END are labels
                       previously declared in the program.
        """
        self._instruction_type = Parser.A_INSTRUCTION
        _, self._symbol = self.lexer.next_token()
        # tok_type, self._symbol = self.lexer.next_token()

    def _l_instruction(self):
        """
        Label/symbol instrution declared as (LABEL_NAME), e.g., (LOOP) or (END)
        """
        self._instruction_type = Parser.L_INSTRUCTION
        _, self._symbol = self.lexer.next_token()
        # tok_type, self._symbol = self.lexer.next_token()

    def _c_instruction(self, token, value):
        """
        Compue instruction with possible values:
            * dest=comp;jump
            * dest=comp
            * comp;jump
            * comp
        """
        self._instruction_type = Parser.C_INSTRUCTION
        comp_tok, comp_val = self._get_dest(token, value)
        self._get_comp(comp_tok, comp_val)
        self._get_jump()

    def _get_dest(self, token, value):
        """Returns the 'dest' part of the compute instruction if it exists."""
        tmp_tok, tmp_val = self.lexer.peek_token()
        if tmp_tok == lexer.OPERATION and tmp_val == "=":
            self.lexer.next_token()
            self._dest = value
            comp_tok, comp_val = self.lexer.next_token()
        else:
            comp_tok, comp_val = token, value
        return comp_tok, comp_val

    def _get_comp(self, token, value):
        """Returns the 'comp' part of the compute instruction."""
        if token == lexer.OPERATION and (value == "-" or value == "!"):
            tmp_tok, tmp_val = self.lexer.next_token()
            self._comp = value + tmp_val
        elif token == lexer.NUMBER or token == lexer.SYMBOL:
            self._comp = value
            tmp_tok, tmp_val = self.lexer.peek_token()
            if tmp_tok == lexer.OPERATION and tmp_val != ";":
                self.lexer.next_token()
                _, tmp_val_2 = self.lexer.next_token()
                self._comp += tmp_val + tmp_val_2

    def _get_jump(self):
        """Returns the 'jump' part of the compute instruction if it exists."""
        token, value = self.lexer.next_token()
        if token == lexer.OPERATION and value == ";":
            # jump_tok, jump_val = self.nexer.next_token()
            _, jump_val = self.lexer.next_token()
            self._jump = jump_val

    @property
    def instruction_type(self):
        return self._instruction_type

    @property
    def symbol(self):
        return self._symbol

    @property
    def dest(self):
        return self._dest

    @property
    def comp(self):
        return self._comp

    @property
    def jump(self):
        return self._jump

    def has_more_instructions(self):
        return self.lexer.has_more_instructions()

    def advance(self):
        """Advance in the program and fetch the next line in the file."""
        self._init_instruction_info()

        self.lexer.next_instruction()
        token, val = self.lexer.curr_token

        if token == lexer.OPERATION and val == '@':
            self._a_instruction()
        elif token == lexer.OPERATION and val == '(':
            self._l_instruction()
        else:
            self._c_instruction(token, val)

