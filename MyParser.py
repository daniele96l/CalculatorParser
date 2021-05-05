#######################################
# IMPORTS
#######################################

from strings_with_arrows import *
import sys
#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'

#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#######################################
# TOKENS
#######################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'
TT_VAR_A = 'VAR_A'
TT_VAR_B = 'VAR_B'
TT_VAR_C = 'VAR_C'
variableName = ''
OPERATORS = 'MUL','DIV','PLUS', 'MINUS'
alphabet = 'a','b','c','d','e','f','g','h','i','l','m','n','o','p','q','r','s','t','u','v','z','x','y','w','j'

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        variableName = ''


        while self.current_char != None: #self si riferisce alla stringa
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number()) #inserisco il numero della cifra dentro il token
            elif self.current_char == '+':
                variableName = ''
                tokens.append(TT_PLUS)
                self.advance()
            elif self.current_char == '-':
                tokens.append(TT_MINUS)
                self.advance()
            elif self.current_char == '*':
                tokens.append(TT_MUL)
                self.advance()
            elif self.current_char == '/':
                tokens.append(TT_DIV)
                self.advance()
            elif self.current_char == '(':
                tokens.append(TT_LPAREN)
                self.advance()
            elif self.current_char == ')':
                tokens.append(TT_RPAREN)
                self.advance()
            elif self.current_char.isalpha():  #qui inserire il riconoscimento di variabili a più lettere
                TT_VAR_A = 'VAR_A'
                variableName = 'VAR_B'   #il valore delle variabile deve essere tra quelli previsti altrimenti da un invalid sysntax error
                self.advance()
                if(self.current_char not in alphabet):

                    tokens.append(variableName) #qui devo fare in modo di appendere la mia nuova variabile ch'è costituita da più lettere
                    #tokens.append(Token(TT_VAR_A, pos_start=self.pos))
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                print("illegal char")
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")


        tokens.append(Token(TT_EOF)) #il token di fine stringa
        return tokens

            #DEVO FARE UN CHECK PER EVITARE "B+++++B"

    def make_number(self): #questo serve per i numeri, ovvero le costanti
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0: #differenza tra numero in virgola o intero
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)


#######################################
# NODES
#######################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


class BinOpNode: #crep il branch dell'albero
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def createBranch(self):
        print(self.left_node, self.op_tok, self.right_node, "New branch")
        if(self.left_node or self.right_node) in OPERATORS:
            print("Error, expected a variable or function after the operator")
            sys.exit(1)
        else:
            node = f'({self.left_node}, {self.op_tok}, {self.right_node})'
            return node
        #E SE IO MODIFICASSI QUI LA LISTA DEI TOKEN METTENDO SEMPLICEMENTE LE PARENTESI A FIANCO DEI NODI? 

# PARSER

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        print(tokens, "tokens appena presi dal parser")


    def term(self):   #the grammar how a factor works

        tok = self.tokens
        #quello che devo andare a fare ora è trovare la prima "*" e creare il primo branch
        for i in range(len(tok)):
            if(tok[i] == "MUL"):
                b = BinOpNode(tok[i-1],tok[i],tok[i+1])
                return b.createBranch()


#######################################
# RUN
#######################################

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens = lexer.make_tokens()

    # Generate AST
    parser = Parser(tokens)
    ast = parser.term()
    print(ast)                 #questo è il mio primo banch ch'è stato ritornato

   # ast = parser.parse()

while True:
    text = input('basic > ')
    run('<stdin>',text)



