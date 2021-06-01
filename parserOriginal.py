#######################################
# IMPORTS
#######################################
import sys
import collections
from strings_with_arrows import *

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
TT_OP = 'MUL','DIV','PLUS','MINUS',
alphabet = 'a','b','c','d','e','f','g','h','i','l','m','n','o','p','q','r','s','t','u','v','z','x','y','w','j','k'
TT_FUNC = "Func"
DIGITS = '0123456789'
Forbidden = '.',',','%','£',


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
    insidefunction = False
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
        functionName = ''
        digit = ''
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif (self.current_char in DIGITS ):

                variableName = ''
                functionName = ''
               # print(self.current_char)
                digit =+ int(self.current_char)
                self.advance()
               # tokens.append(self.make_number())
                while (str(self.current_char) in str(DIGITS)):
                    digit = str(digit) + str(self.current_char)
                    self.advance()

                tokens.append(Token(digit, pos_start=self.pos))

            elif self.current_char == '+':
                digit = ''
                functionName = ''
                variableName = ''
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                digit = ''
                variableName = ''
                functionName = ''
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                digit = ''
                variableName = ''
                functionName = ''
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                digit = ''
                variableName = ''
                functionName = ''
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char.isalpha() or (self.current_char in DIGITS and insidefunction == True):  #qui inserire il riconoscimento di variabili a più lettere
                variableName = variableName + self.current_char  # il valore delle variabile deve essere tra quelli previsti altrimenti da un invalid sysntax error
                functionName = functionName + self.current_char
                digit = ''
                self.advance()
                if (self.current_char not in alphabet): #quando troviamo un carattere diverso da "alfabeto" possiamo chiudere la variabile
                    if(self.current_char == '('):
                        insidefunction = True

                        functionName = functionName + self.current_char
                        self.advance()

                        while(self.current_char in (DIGITS) or self.current_char in alphabet):
                            functionName = functionName + str(self.current_char)
                            self.advance()
                          #  print("Funzione " + functionName)

                        if (self.current_char == ')'):
                            insidefunction = False
                            functionName = functionName + self.current_char
                           # print("function " + functionName)
                            tokens.append(Token(functionName, pos_start=self.pos))
                            self.advance()

                        if(functionName[-2] == '('): #se tra le parentesi non c'è nin
                            print("Syntax error")
                            sys.exit()
                    else:
                       # print("Variabile: " + variableName)
                        tokens.append(Token(variableName,pos_start=self.pos))  # qui devo fare in modo di appendere la mia nuova variabile ch'è costituita da più lettere
                    # tokens.append(Token(TT_VAR_A, pos_start=self.pos))
            elif self.current_char == '(':
                digit = ''
                variableName = ''
                functionName = ''
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                digit = ''
                variableName = ''
                functionName = ''
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

       # print(tokens)
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
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

        if dot_count == 0:
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


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node


    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'



class UnaryOpNode:
    def __init__(self, op_tok, node):

        self.op_tok = op_tok
        self.node = node


    def __repr__(self):
        if(str(self.op_tok) in TT_OP):
            print("1")
            return InvalidSyntaxError
        return f'({self.op_tok}, {self.node})'


#######################################
# PARSE RESULT   la prima cosa che viene chiamata
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error #controlla se il risultato del check di quel nodo è fattibile
            return res.node #in caso positivo ritorna il nodo carino c:

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok #vado avanti finchè non raggiungo la fine

    def parse(self):
        res = self.expr()  #METODO esp chiamerà term che a sua volta chiamerà factor, mi ritorna un nodo binario
        #res non è altro che l'espressione
        if not res.error and self.current_tok.type != TT_EOF:
            print("2")
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,"Expected '+', '-', '*' or '/'" ))
        return res

    ###################################

    def factor(self): #serve solo per fare un check degli errori ed eventialmente ritorna ritorna il nodo (singolo token)
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance()) #passo il nodo al res.register per controllare che sia carino c:
            factor = res.register(self.factor()) #il factor è il mio fattore, ovvero il mio "elemento" base
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor)) #credo quindi il primo fattore, che sarà il nodo

        elif tok.type == TT_LPAREN:
            res.register(self.advance())  #passo il nodo al res.register per controllare che sia carino c:
            expr = res.register(self.expr()) #il factor è il mio fattore, ovvero il mio "elemento" base
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                print("3")
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,"Expected ')'"))
        elif tok.type not in Forbidden:
            res.register(self.advance())
            return res.success(NumberNode(tok))  # creo quindi il nodo del fattore che sarà il numero o la variabile


        print("4")
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end,"Expected int or float"))

    def term(self):  # questo aiuta a dare l'ordine di esecuzione
        #print("creo il term")
        return self.bin_op(self.factor, (TT_MUL, TT_DIV)) #viene creato il nodo binario prima con la moltiplicazione
    #Poi la moltiplciazione chiama anche factor, che va a "avanti" e vede se ci sono altre robe come "+ -" oppure le parentesi


    def expr(self): #PRIMA COSA CHE VIENE CHIAMATA DURANTE IL PARSING
        #print(self.term())
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS)) #poi viene chiamato il term

    ###################################

    def bin_op(self, func, ops): #dentro func c'è il fattore
        res = ParseResult()
        left = res.register(func()) #nodo SINISTRO ---- func non è altro che il term

        if res.error: return res

        while self.current_tok.type in ops: #se il current token è nei token accettati dal tipo di operazioni del nodo binaio
            op_tok = self.current_tok
            res.register(self.advance()) #vado avanti e prendo il prossimo token
            right = res.register(func()) #da qui estraggo il nodo a DESTRO

            if res.error: return res

            left = BinOpNode(left, op_tok, right)

        return res.success(left)
#######################################
# Optimize
#######################################

class Optimizer:

    #a*a*a+a = (((a, MUL, a), MUL, a), PLUS, a)

    def __init__(self,ast):
        self.ast = ast
        self.scan()
        tmp = []

    def pop_left(self,ast):
        if hasattr(ast, 'left_node'):
            #print(ast.left_node)
            return self.pop_left(ast.left_node)
        else:
            return ast

    def pop_right(self, ast):
        if hasattr(ast, 'right_node'):
            #print(ast.right_node)
            return self.pop_right(ast.right_node)
        else:
            return ast

    def scan(self):
        #print(self.pop_left(self.ast))
        self.pop_right(self.ast)


#######################################
# OptimizeSelvaggio
#######################################

class OptimizerSelvaggio:

    #a*a*a+a = (((a, MUL, a), MUL, a), PLUS, a)
    op = '+','-'

    def __init__(self,text):
        self.text = text
        terms = []

        index = 1
        terms = self.scan(terms, index)
        position = self.findCommon(terms)
        self.newstring = self.saveAndDelete(terms,position)

    def scan(self, terms, index):

        for i in range(2*len(self.text)): #questo è quello che causa avere un vettore troppo lungo
            terms.append('')

        terms[0] += '+'
        for i in range(len(self.text)):  #divido in terms
            if(self.text[i] not in self.op):
                #print(self.text[i])
                terms[index] += self.text[i]

            if((self.text[i] == '+') or (self.text[i] == '-') ):
                index += 1
                terms[index] += self.text[i]
                index += 1


        for i in range(len(self.text)):  #tolgo gli spazi vuoti
            terms[:] = [item for item in terms if item != '']




        return terms

    def findCommon(self, terms):
        indx = 0
        m= 0
        multichar = []


        position = terms.copy()

        for i in range(len(position)):
            position[i] = ''
            multichar.append('')

        for i in range(len(terms)):  # questo va a vedere se la variabile è "lunga" o "corta"

            if (('*' in terms[i]) or ('/' in terms[i]) or len(terms[i]) == 1):
                multichar[m] = True
                m += 1
            elif(len(terms[i]) > 1):
                multichar[m] = False
                m += 1

        #print(multichar)

        for i in range(len(terms)):
            for y in range(len(terms)):
                if((terms[i] in terms[y]) or (terms[y] in terms[i])): #qui vado a trovare le posizioni di dove la stessa variabile è ripetuta
                    if(i!= y and (terms[y] and terms[i]) != ("+" or "-") and multichar[y] and multichar[i]):
                        position[indx] = ''.join(sorted(set(terms[i]).intersection(set(terms[y]))))  #vorrei che mettessi il numero corrispondente a quante volte la variabile si presenta

                indx += 1
            indx = 0

        #print("terms")
        #print(terms)
        #print("Position")
        #print(position)
        return position

    def saveAndDelete(self,terms,position):
        fun_pos = []

        for i in range(len(terms)):
            fun_pos.append('')
            fun_pos[i] = True

            if '(' in terms[i] and len(terms[i]) > 1:
                fun_pos[i] = False


        #print("fun_pos")
        #print(fun_pos)

        newString = []
        checkPos = []
        optimization = []
        z = 0
        y = 0
        w = 0

        for i in range(len(terms)):
            checkPos.append('')
            optimization.append('')

        for i in range(3*len(terms)):  # questo è quello che causa avere un vettore troppo lungo
            newString.append('')

        finalString = newString.copy()

        for i in range(len(terms)): #elimino gli spazi in position
            if(position[i] != '' and position[i] not in checkPos and position[i] not in self.op and fun_pos[i]): #le variabili che salvo
                    checkPos[y] = position[i]  #devo fare questa associazione solo se la variabile di position che nella stessa i ha associato un true in multichar
                    y+=1

        checkPos = list(filter(None, checkPos))
        #print("variabili da mettere in comune - chekpos")
        #print(checkPos)

        y = 0
        rimosso = False
        entrato = False

        # terms[y]
        # ['a', '+', 'b', '+', 'a']   #devo in qualche modo raggruppare vicino le 'a'

        # position[i]
        # ['a', '', '', '', 'a']

        # chekpos[z]
        # ['a'] le uniche variabili che si ripetono

        for z in range(len(checkPos)): #raggruppo i termini che hanno una variabile in comune
            newString[w] = '+'+  checkPos[z] #prima metto la lettera
            w+= 1
            newString[w] = '*('  #apro la parentesi
            w+=1
            for y in range(len(terms)):
                if ((checkPos[z] in terms[y])): #l'ordine deve essere dettato da quelli in "checkpos"
                    if(y-1>0):
                        newString[w] = terms[y-1] #gestisco il segno
                        w+=1
                    for k in range(len(terms[y])):  #qui vado a rimuovere la variabile che essendo in comune è stata portata fuori
                         #print(terms[y][k])
                         if (fun_pos[y]):
                            if(not rimosso and terms[y][k] in checkPos):
                                newString[w] += '1'
                                rimosso = True
                            else:
                                newString[w] += terms[y][k]  # metto il simbolo
                                optimization[y] = '1'

                    rimosso = False
                    entrato = False
                    w += 1
            newString[w] = ')'   #chiudo la parentesi
            w+=1


        for i in range(len(terms)):
            if str(checkPos) not in str(terms[i]) and optimization[i] != '1' and terms[i] != '+' and terms[
                i] not in checkPos and terms[i] != '-':
                newString[w] += terms[i - 1]  # la variabile non presente
                w += 1
                newString[w] += terms[i]  # la variabile non presente
                w += 1

        #print("New string")
        #print(newString)
        return newString

    def Getter(self):
        return self.newstring

#######################################
# Stringa più presentabile
#######################################

class StringRefactoring():

    def __init__(self,text):
        self.text = text
        opt = self.refactor()
        self.calc(opt)


    def refactor(self):
        optimized = ''
        for i in self.text:
            optimized += i

        return  optimized

    def calc(self,opt):
        j = 0
        new = ''
        new2 = ''
        new3 = ''

        for i in range(len(opt)):
            #print(opt[i])
            if((opt[i] == '1') and opt[i+1] == ("*" or '/')): # 1*a = a
                new += ''
                j += 2
            else:
                if(j < len(opt)):
                    new += opt[j]
                    j+= 1

        j = 0


        if(new[-1] == ("+") or new[-1] == ("-") ): #tolgo un + o - alla fine
            for i in range(len(new)-1):
                new2 += new[i]
        else:
            for i in range(len(new)):
                new2 += new[i]

        for i in range(len(new2)):
            if(i+1 < len(new2)):
                if(new2[i]=='+' and new[i+1] ==')'):
                    print("Ok")
                    new3 += ''
                else:
                    new3 += new[i]
            else:
                new3 += new[i]


        print("Optimized string")
        print(new3)


#dobbiamo fare una roba tipo entrare dentro un espressione e vedere le cose che sono unite da term + term
#se uno dei factor dei term è in comune allora
#term + term -> factor(term-factor + term-factor)
#abc+adf -> a(b*c+d*f)

#######################################
# Test
#######################################

def Test():
    # --------------
    # Unit test cases
    # --------------
    # We are going to test separately the different part of the program

    # --------------
    # Test the lexer
    # --------------
    print("Testing the lexer")
    lexer = Lexer('<stdin>','z+a+c+a*b+func(x)')
    tokens, error = lexer.make_tokens()
    print("The lexer works, here there are the tokens")
    print(tokens)
    print("...")
    if error: return None, error

    # --------------
    # Test the parser
    # --------------
    print("Testing the parser")
    parser = Parser(tokens)  # instanzio il parser e gli passo i tokens
    ast = parser.parse()  # con i tokens passati al parser faccio il parsing
    print("The lexer works, here there is the parsing three")
    print(ast.node)
    print("...")


    # --------------
    # Test the optimizer
    # --------------
    print("Testing the optimizer")
    optimizer = OptimizerSelvaggio('z+a+c+a*b+func(x)')
    print("The optimizer works")
    refactor = StringRefactoring(optimizer.Getter())
    print("Now you can write your string in the command line to optimize it:")
    print("...")
    return ast.node, ast.error

#######################################
# RUN
#######################################

def run(fn, text):


    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens) #instanzio il parser e gli passo i tokens
    ast = parser.parse() #con i tokens passati al parser faccio il parsing

    print("This is the parsing three")
    print(ast.node)

    #Optimize
    optimizer = OptimizerSelvaggio(text)
    refactor = StringRefactoring(optimizer.Getter())
    return ast.node, ast.error