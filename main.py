""" -LEXICAL ANALYZER- """

'''
 Created by: Kenneth R. Aponte
 Date: 08/28/2022
 Student number: 802-19-9075
'''

import ply.lex as lex
import ply.yacc as yacc

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
    'WHITESPACE'
] + list(reserved.values())



#Ignores
t_ignore = ' \t'#TODO: verify if this works
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
    r'[a-zA-z][a-zA-Z0-9]*'
    #this handles the case for the 'ID' and ALL of the reserved words in the reserved dictionary
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUM(t):
    r'\d+'
    #finds every number regardless of it starting with a 0 or not, if it does the 0 at the front gets removed by converting it to a string
    t.value = int(t.value)
    #TODO: verify if this is right
    return t


def t_newLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    print('\n')
    #no return


#error handling
def t_error(t):
    print('Invalid character', t.value[0])
    t.lexer.skip(1)


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
    #building the lexer
    lexer = lex.lex()

    #gets the data from the file name or path provided
    data = getDataFromFile()

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



#calls the main function
if __name__ == '__main__':
    main()
