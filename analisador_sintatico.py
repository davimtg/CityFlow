import ply.yacc as yacc
from lexer import tokens, lexer

# ─────────────────────────────────────────
#  PROGRAMA
# ─────────────────────────────────────────

def p_programa(p):
    '''programa : declaracao_lista'''
    p[0] = ('programa', p[1])

def p_declaracao_lista_multi(p):
    '''declaracao_lista : declaracao_lista declaracao'''
    p[0] = p[1] + [p[2]]

def p_declaracao_lista_um(p):
    '''declaracao_lista : declaracao'''
    p[0] = [p[1]]

def p_declaracao(p):
    '''declaracao : decl_sinal_global
                  | decl_rua
                  | decl_cruzamento'''
    p[0] = p[1]

# ─────────────────────────────────────────
#  CORPO DO SINAL  { verde: Xs; vermelho: Xs; }
# ─────────────────────────────────────────

def p_corpo_sinal(p):
    '''corpo_sinal : CHAVE_ESQ KW_VERDE DOIS_PONTOS TEMPO_S PONTO_VIRGULA KW_VERMELHO DOIS_PONTOS TEMPO_S PONTO_VIRGULA CHAVE_DIR'''
    p[0] = ('corpo_sinal', p[4], p[8])

# ─────────────────────────────────────────
#  SINAL GLOBAL  →  sinal nome { verde: Xs; vermelho: Xs; }
# ─────────────────────────────────────────

def p_decl_sinal_global(p):
    '''decl_sinal_global : KW_SINAL ID corpo_sinal'''
    p[0] = ('sinal_global', p[2], p[3])

# ─────────────────────────────────────────
#  RUA
# ─────────────────────────────────────────

def p_decl_rua(p):
    '''decl_rua : KW_RUA STRING CHAVE_ESQ rua_item_lista CHAVE_DIR'''
    p[0] = ('rua', p[2], p[4])

def p_rua_item_lista_multi(p):
    '''rua_item_lista : rua_item_lista rua_item'''
    p[0] = p[1] + [p[2]]

def p_rua_item_lista_um(p):
    '''rua_item_lista : rua_item'''
    p[0] = [p[1]]

def p_rua_item(p):
    '''rua_item : rua_tamanho
                | rua_mao
                | rua_sinal_ref
                | rua_sinal_inline'''
    p[0] = p[1]

def p_rua_tamanho(p):
    '''rua_tamanho : KW_TAMANHO DOIS_PONTOS MEDIDA_M PONTO_VIRGULA'''
    p[0] = ('tamanho', p[3])

def p_rua_mao(p):
    '''rua_mao : KW_MAO DOIS_PONTOS mao_valor PONTO_VIRGULA'''
    p[0] = ('mao', p[3])

def p_mao_dupla(p):
    '''mao_valor : KW_DUPLA'''
    p[0] = 'dupla'

def p_mao_unica(p):
    '''mao_valor : KW_UNICA'''
    p[0] = 'unica'

# sinal em Xm nome;
def p_rua_sinal_ref(p):
    '''rua_sinal_ref : KW_SINAL KW_EM MEDIDA_M ID PONTO_VIRGULA'''
    p[0] = ('sinal_rua', p[3], ('sinal_ref', p[4]))

# sinal em Xm { verde: Xs; vermelho: Xs; }
def p_rua_sinal_inline(p):
    '''rua_sinal_inline : KW_SINAL KW_EM MEDIDA_M corpo_sinal'''
    p[0] = ('sinal_rua', p[3], ('sinal_inline', p[4]))

# ─────────────────────────────────────────
#  CRUZAMENTO
# ─────────────────────────────────────────

def p_decl_cruzamento(p):
    '''decl_cruzamento : KW_CRUZAMENTO CHAVE_ESQ cruzamento_item_lista CHAVE_DIR'''
    p[0] = ('cruzamento', p[3])

def p_cruzamento_item_lista_multi(p):
    '''cruzamento_item_lista : cruzamento_item_lista cruzamento_item'''
    p[0] = p[1] + [p[2]]

def p_cruzamento_item_lista_um(p):
    '''cruzamento_item_lista : cruzamento_item'''
    p[0] = [p[1]]

def p_cruzamento_item(p):
    '''cruzamento_item : cruzamento_entrada
                       | cruzamento_par_simples
                       | cruzamento_par_com_corpo
                       | cruzamento_sinal_ref
                       | cruzamento_sinal_inline'''
    p[0] = p[1]

# "Nome da Rua" em Xm ;
def p_cruzamento_entrada(p):
    '''cruzamento_entrada : STRING KW_EM MEDIDA_M PONTO_VIRGULA'''
    p[0] = ('entrada', p[1], p[3])

# sinal default por referência
def p_cruzamento_sinal_ref(p):
    '''cruzamento_sinal_ref : KW_SINAL ID PONTO_VIRGULA'''
    p[0] = ('sinal_default', ('sinal_ref', p[2]))

# sinal default inline
def p_cruzamento_sinal_inline(p):
    '''cruzamento_sinal_inline : KW_SINAL corpo_sinal'''
    p[0] = ('sinal_default', ('sinal_inline', p[2]))

# ─────────────────────────────────────────
#  PAR DE/PARA
# ─────────────────────────────────────────

# de "A" para "B" ;
def p_cruzamento_par_simples(p):
    '''cruzamento_par_simples : KW_DE STRING KW_PARA STRING PONTO_VIRGULA'''
    p[0] = ('par', p[2], p[4], None)

# de "A" para "B" { sinal ... }
def p_cruzamento_par_com_corpo(p):
    '''cruzamento_par_com_corpo : KW_DE STRING KW_PARA STRING CHAVE_ESQ par_sinal CHAVE_DIR'''
    p[0] = ('par', p[2], p[4], p[6])

# sinal dentro do par — referência
def p_par_sinal_ref(p):
    '''par_sinal : KW_SINAL ID PONTO_VIRGULA'''
    p[0] = ('sinal_ref', p[2])

# sinal dentro do par — inline
def p_par_sinal_inline(p):
    '''par_sinal : KW_SINAL corpo_sinal'''
    p[0] = ('sinal_inline', p[2])

# ─────────────────────────────────────────
#  ERRO
# ─────────────────────────────────────────

def p_error(p):
    if p:
        input_str = p.lexer.lexdata
        line_start = input_str.rfind('\n', 0, p.lexpos) + 1
        col = (p.lexpos - line_start) + 1
        print(f"Erro Sintático: token inesperado '{p.value}' ({p.type}). Linha {p.lineno}, Coluna {col}")
    else:
        print("Erro Sintático: fim de arquivo inesperado.")

# ─────────────────────────────────────────
#  BUILD
# ─────────────────────────────────────────

parser = yacc.yacc()


if __name__ == '__main__':
    import sys
    import os
    from ast_to_json import exportar

    # 1. Verifica se o usuário passou um arquivo de entrada no terminal
    if len(sys.argv) < 2:
        print("Erro: Nenhum arquivo informado.")
        print("Uso correto: python parser.py <nome_do_arquivo.cf>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    # 2. Verifica se o arquivo realmente existe na pasta
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        sys.exit(1)

    # 3. Lê o código-fonte do arquivo
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            codigo_fonte = f.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

    print(f"[{caminho_arquivo}] Analisando o código...")
    
    # 4. Executa o parser com o texto lido
    ast = parser.parse(codigo_fonte, lexer=lexer)
    
    # 5. Gera o JSON de saída dinamicamente
    if ast:
        # Extrai o nome base (ex: transforma 'meu_bairro.cf' em 'meu_bairro.json')
        nome_base = os.path.splitext(caminho_arquivo)[0]
        nome_json = f"{nome_base}.json"
        
        print("Sintaxe correta! Gerando a árvore...")
        exportar(ast, nome_json)
    else:
        print("Erro: A compilação falhou devido a problemas estruturais no código fonte.")