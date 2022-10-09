""" -LEXICAL ANALYZER- """

'''
 Created by: Kenneth R. Aponte
 Date created: 08/28/2022
 Student number: 802-19-9075
'''


import ply.lex as lex
import ply.yacc as yacc


#------------TOKENS------------

#reserved tokens
reserved = {
    'def': 'DEF',
    'var': 'VAR',
    'Int': 'INT',
    'if': 'IF',
    'else': 'ELSE'
}

# tokens
tokens = [
    'ID',
    'NUM',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'BECOMES',
    'EQ',
    'NE',
    'LT',
    'GT',
    'LE',
    'GE',
    'PLUS',
    'MINUS',
    'STAR',
    'SLASH',
    'PCT',
    'COMMA',
    'SEMI',
    'COLON',
    'ARROW',
    'COMMENT',
] + list(reserved.values())



#Ignores
t_ignore = ' \t'
t_ignore_COMMENT = r'\/\/.*'  #ignores the whole line except for line breaks

#Simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

#the following tokens were specified in a decreasing order to check for cases like ('==' vs '='), the '==' is checked first.
t_EQ = r'\=\='
t_NE = r'\!\='
t_LE = r'\<\='
t_GE = r'\>\='
t_ARROW = r'\=\>'

t_BECOMES = r'\='
t_LT = r'\<'
t_GT = r'\>'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_STAR = r'\*'
t_SLASH = r'\/'
t_PCT = r'\%'
t_COMMA = r'\,'
t_SEMI = r'\;'
t_COLON = r'\:'


#More complicated tokens
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    #this handles the case for the 'ID' and ALL of the reserved words in the reserved dictionary
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUM(t):
    r'\d+'
    return t


def t_newLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    print('\n')
    pass
    #no return


#error handling
def t_error(t):
    #if its none of the above tokens then it is an invalid character
    print('Invalid character', t.value[0])
    t.lexer.skip(1)


#-------- END OF TOKENS--------





#---------- GRAMMAR (ASSIGNMENT #2)---------
def p_empty(p):
     'empty :'
     pass


def p_defdefs(p):
    '''defdefs : defdef defdefs
                | defdef '''
    pass

def p_defdef(p):
    ''' defdef : DEF ID LPAREN parmsopt RPAREN COLON type BECOMES LBRACE vardefsopt defdefsopt expras RBRACE '''
    pass

def p_parmsopt(p):
    ''' parmsopt : parms
                | empty '''
    pass

def p_parms(p):
    ''' parms : vardef COMMA parms
                | vardef '''
    pass

def p_vardef(p):
    ''' vardef : ID COLON type '''
    pass

def p_type(p):
    ''' type : INT
            | LPAREN typesopt RPAREN ARROW type '''
    pass

def p_typesopt(p):
    ''' typesopt : types
                | empty '''
    pass

def p_types(p):
    ''' types :  type COMMA types
            | type '''
    pass

def p_vardefsopt(p):
    ''' vardefsopt :  VAR vardef SEMI vardefsopt
                    | empty '''
    pass

def p_defdefsopt(p):
    ''' defdefsopt : defdefs
                    | empty '''
    pass

def p_expras(p):
    ''' expras : expra SEMI expras
                | expra '''
    pass

def p_expra(p):
    ''' expra : ID BECOMES expr
                | expr '''
    pass

def p_expr(p):
    ''' expr : IF LPAREN test RPAREN LBRACE expras RBRACE ELSE LBRACE expras RBRACE
            | term
            | expr PLUS term
            | expr MINUS term '''
    pass

def p_term(p):
    ''' term : factor
            | term STAR factor
            | term SLASH factor
            | term PCT factor '''
    pass

def p_factor(p):
    ''' factor : ID
            | NUM
            | LPAREN expr RPAREN
            | factor LPAREN argsopt RPAREN '''
    pass

def p_test(p):
    ''' test : expr NE expr
            |  expr LT expr
            |  expr LE expr
            |  expr GE expr
            |  expr GT expr
            |  expr EQ expr
            '''
    pass

def p_argsopt(p):
    ''' argsopt : args
                | empty '''
    pass

def p_args(p):
    ''' args : expr COMMA args
            | expr '''
    pass

def p_error(p):
    print("Syntax error in input!", p)
    pass

#-------------------------------------------

# -----MAIN FUNCTIONS-----

#get data from a file
def getDataFromFile():
    try:
        fileName = str(input('\nPlease specify the name of your file: '))
        fH = open(fileName)
        text = fH.read()
        return text

    except:
        print('Invalid file name provided.')
        return None


def main():
    #gets the data from the file name or path provided
    data = getDataFromFile()

    #building the lexer
    lexer = lex.lex()


    #if the file exists it will continue
    if data == None:
        return

    lexer.input(data)

    print('\n----THE FOLLOWING TOKENS WERE FOUND----\n')

    while True:
        tok = lexer.token()
        if not tok:
            print('\n----NO MORE TOKENS FOUND----\n')
            break #completed
        print('In row ' + str(tok.lineno) + ', found a ' + tok.type + ' with a value of ' + str(tok.value))

    #building the parser
    parser = yacc.yacc(start='defdef')

    result = parser.parse(data) #no result expected yet



#calls the main function
if __name__ == '__main__':
    main()
