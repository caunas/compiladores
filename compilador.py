
# PLY é uma lib própria para criação de compiladores.
# .lex é o módulo de análise léxica
import ply.lex as lex

# Palavras reservadas da linguagem C
reserved = {
    'auto': 'AUTO',
    'break': 'BREAK',
    'case': 'CASE',
    'char': 'CHAR',
    'const': 'CONST',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'do': 'DO',
    'double': 'DOUBLE',
    'else': 'ELSE',
    'enum': 'ENUM',
    'extern': 'EXTERN',
    'float': 'FLOAT',
    'for': 'FOR',
    'goto': 'GOTO',
    'if': 'IF',
    'int': 'INT',
    'long': 'LONG',
    'register': 'REGISTER',
    'return': 'RETURN',
    'short': 'SHORT',
    'signed': 'SIGNED',
    'sizeof': 'SIZEOF',
    'static': 'STATIC',
    'struct': 'STRUCT',
    'switch': 'SWITCH',
    'typedef': 'TYPEDEF',
    'union': 'UNION',
    'unsigned': 'UNSIGNED',
    'void': 'VOID',
    'volatile': 'VOLATILE',
    'while': 'WHILE'
}

# Lista de tokens
tokens = [
    'IDENTIFIER',
    'NUMBER',
    'STRING',
    'CHAR_LITERAL',

    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'ASSIGN', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
    'AND', 'OR', 'NOT',
    'BITAND', 'BITOR', 'BITXOR', 'BITNOT',
    'LSHIFT', 'RSHIFT',
    'INCREMENT', 'DECREMENT',
    'PLUS_ASSIGN', 'MINUS_ASSIGN',
    'TIMES_ASSIGN', 'DIVIDE_ASSIGN', 'MOD_ASSIGN',
    'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN',
    'LSHIFT_ASSIGN', 'RSHIFT_ASSIGN',
    'ARROW',

    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA',
    'DOT', 'COLON', 'QUESTION'
] + list(reserved.values())


# Operadores com mais de um caractere
# As regras de string do PLY priorizam expressões mais longas.
t_LSHIFT_ASSIGN = r'<<='
t_RSHIFT_ASSIGN = r'>>='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_AND_ASSIGN = r'&='
t_OR_ASSIGN = r'\|='
t_XOR_ASSIGN = r'\^='

t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_ARROW = r'->'
t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'

# Operadores de um caractere
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_ASSIGN = r'='
t_LT = r'<'
t_GT = r'>'
t_NOT = r'!'
t_BITAND = r'&'
t_BITOR = r'\|'
t_BITXOR = r'\^'
t_BITNOT = r'~'

# Delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_COLON = r':'
t_QUESTION = r'\?'


# Identificadores e palavras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


# Números inteiros e de ponto flutuante
def t_NUMBER(t):
    r'0[xX][0-9a-fA-F]+|(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?'
    if t.value.lower().startswith('0x'):
        t.value = int(t.value, 16)
    elif any(c in t.value for c in '.eE'):
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


# Strings
def t_STRING(t):
    r'"([^\\\n]|\\.)*"'
    return t


# Literais de caracteres
def t_CHAR_LITERAL(t):
    r"'([^\\\n]|\\.)'"
    return t


# Comentários de uma ou várias linhas
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//[^\n]*)'
    t.lexer.lineno += t.value.count('\n')
    # Não retorna token: o comentário é ignorado


# Contagem de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignorar espaços, tabulações e etc
t_ignore = ' \t\r'


# Tratamento de caracteres inválidos
def t_error(t):
    print(
        f"Caractere ilegal {t.value[0]!r} "
        f"na linha {t.lexer.lineno}"
    )
    t.lexer.skip(1)


# Instancia do o analisador léxico em um objeto
lexer = lex.lex()


# Exemplo de utilização
if __name__ == '__main__':
    
    # BTW: Atualizar para suportar o nome do arquivo via args
    with open('hello.c', 'r') as f:
        codigo = f.read()

    lexer.input(codigo)

    while True:
        token = lexer.token()
        if token is None:
            break

        print(
            f"Tipo: {token.type:<15} "
            f"Valor: {token.value!r:<22} "
            f"Linha: {token.lineno}"
        )
