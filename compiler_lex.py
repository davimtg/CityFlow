import ply.lex as lex

tokens = [
    'ID_RUA',
    'MEDIDA_M',
    'TEMPO_S',
    'CHAVE_ESQ',
    'CHAVE_DIR',
    'DOIS_PONTOS',
    'VIRGULA',
    'variavel_mf',
    'string_mf',
    'numero_mf',
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

# Símbolos simples
t_CHAVE_ESQ   = r'\{'
t_CHAVE_DIR   = r'\}'
t_DOIS_PONTOS = r':'
t_VIRGULA     = r','

# Medida em metros — deve vir ANTES de t_numero_mf
def t_MEDIDA_M(t):
    r'[0-9]+m'
    return t

# Tempo em segundos — deve vir ANTES de t_numero_mf
def t_TEMPO_S(t):
    r'[0-9]+s'
    return t

# Identificadores e palavras reservadas
# CORRIGIDO: aceita minúsculo para alcançar as reservadas
def t_ID_RUA(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID_RUA')
    return t

# Erros léxicos — variável mal formada (começa com dígito)
# CORRIGIDO: sem espaços ao redor do |
def t_variavel_mf(t):
    r'[0-9]+[a-zA-Z_]+'
    print(f"Erro Léxico: Variável mal formada '{t.value}' na linha {t.lineno}")
    return t

# Erros léxicos — número sem unidade ou com unidade inválida
# CORRIGIDO: exclui 'm' e 's' do range de letras inválidas; sem espaços no |
def t_numero_mf(t):
    r'[0-9]+[a-ln-rt-zA-Z]+|[0-9]+'
    print(f"Erro Léxico: Número mal formado '{t.value}' na linha {t.lineno}")
    return t

# Erros léxicos — string aberta sem fechamento
def t_string_mf(t):
    r'"[^"\n]*'
    print(f"Erro Léxico: String mal formada '{t.value}' na linha {t.lineno}")
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal: '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()