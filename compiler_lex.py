import ply.lex as lex

def find_column(input_str, token):
    """Calcula a coluna do token baseada na última quebra de linha."""
    line_start = input_str.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


tokens = [
    'ID',
    'MEDIDA_M',
    'TEMPO_S',
    'CHAVE_ESQ',
    'CHAVE_DIR',
    'DOIS_PONTOS',
    'PONTO_VIRGULA',
    'STRING',
    'variavel_mf',
    'string_mf'
]

reserved = {
    'rua':      'KW_RUA',
    'tamanho':  'KW_TAMANHO',
    'saida':    'KW_SAIDA',
    'de':       'KW_DE',
    'para':     'KW_PARA',
    'em':       'KW_EM',
    'mao':      'KW_MAO',
    'dupla':    'KW_DUPLA',
    'unica':    'KW_UNICA',
    'sinal':    'KW_SINAL',
    'verde':    'KW_VERDE',
    'vermelho': 'KW_VERMELHO',
}

tokens += list(reserved.values())


t_CHAVE_ESQ     = r'\{'
t_CHAVE_DIR     = r'\}'
t_DOIS_PONTOS   = r':'
t_PONTO_VIRGULA = r';'


def t_COMMENT_MULTILINE(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_COMMENT(t):
    r'//.*'
    pass


def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t

def t_string_mf(t):
    r'"[^"\n]*'
    col = find_column(t.lexer.lexdata, t)
    print(f"Erro Léxico: String mal formada '{t.value}'. Linha {t.lineno}, Coluna {col}")
    return t


def t_MEDIDA_M(t):
    r'[0-9]+m(?![a-zA-Z_À-ÿ])'
    return t

def t_TEMPO_S(t):
    r'[0-9]+s(?![a-zA-Z_À-ÿ])'
    return t

def t_variavel_mf(t):
    r'[0-9]+[a-zA-Z_À-ÿ]+'
    col = find_column(t.lexer.lexdata, t)
    print(f"Erro Léxico: Variável ou número mal formado '{t.value}'. Linha {t.lineno}, Coluna {col}")
    return t


def t_ID(t):
    r'[a-zA-ZÀ-ÿ_][a-zA-Z0-9À-ÿ_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t


t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    col = find_column(t.lexer.lexdata, t)
    print(f"Erro Léxico: Caractere ilegal '{t.value[0]}'. Linha {t.lineno}, Coluna {col}")
    t.lexer.skip(1)


lexer = lex.lex()