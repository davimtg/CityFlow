import json

def formatar_sinal(sinal_node):
    """Converte a tupla do sinal (que agora já recebe números inteiros) em dicionário."""
    if not sinal_node: return None
    if sinal_node[0] == 'sinal_ref': return {"referencia": sinal_node[1]}
    return {"verde_s": sinal_node[1][1], "vermelho_s": sinal_node[1][2]}

def ast_para_dicionario(ast):
    """Varre a AST, aplica as regras SEMÂNTICAS e converte para dicionário usando comprehensions."""
    if not ast or ast[0] != 'programa': return {}

    resultado = {"sinais_globais": {}, "ruas": [], "cruzamentos": []}
    ruas_declaradas = set()
    sinais_declarados = set()

    # PASSAGEM 1: Extrair e validar Ruas e Sinais
    for decl in ast[1]:
        if decl[0] == 'sinal_global':
            nome = decl[1]
            if nome in sinais_declarados: raise ValueError(f"Sinal global '{nome}' duplicado.")
            sinais_declarados.add(nome)
            resultado["sinais_globais"][nome] = {"verde_s": decl[2][1], "vermelho_s": decl[2][2]}

        elif decl[0] == 'rua':
            nome = decl[1]
            if nome in ruas_declaradas: raise ValueError(f"A rua '{nome}' já foi declarada anteriormente.")
            ruas_declaradas.add(nome)
            
            # Utilizando list comprehensions para varrer a AST de forma enxuta
            itens = decl[2]
            tamanho = next((i[1] for i in itens if i[0] == 'tamanho'), None)
            mao = next((i[1] for i in itens if i[0] == 'mao'), None)
            sinais = [{"posicao_m": i[1], "configuracao": formatar_sinal(i[2])} for i in itens if i[0] == 'sinal_rua']
            
            resultado["ruas"].append({"id": nome, "tamanho_m": tamanho, "mao": mao, "sinais_internos": sinais})

    # PASSAGEM 2: Validar Cruzamentos
    for decl in ast[1]:
        if decl[0] == 'cruzamento':
            itens = decl[1]
            
            entradas = [{"rua": i[1], "posicao_m": i[2]} for i in itens if i[0] == 'entrada']
            for e in entradas:
                if e["rua"] not in ruas_declaradas: raise ValueError(f"Cruzamento cita rua não declarada: '{e['rua']}'.")

            rotas = []
            for i in itens:
                if i[0] == 'par':
                    if i[1] not in ruas_declaradas or i[2] not in ruas_declaradas:
                        raise ValueError(f"Rota usa rua não declarada ({i[1]} -> {i[2]}).")
                    rotas.append({"origem": i[1], "destino": i[2], "sinal_especifico": formatar_sinal(i[3])})

            sinal_padrao = next((formatar_sinal(i[1]) for i in itens if i[0] == 'sinal_default'), None)
            
            resultado["cruzamentos"].append({
                "entradas": entradas,
                "sinal_padrao": sinal_padrao,
                "rotas": rotas
            })

    return resultado

def exportar(ast, nome_arquivo="mapa_compilado.json"):
    """Tenta converter a AST e escrever o arquivo (materializar o JSON)."""
    try:
        dict_dados = ast_para_dicionario(ast)
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dict_dados, f, indent=4, ensure_ascii=False)
        print(f"[COMPILADOR] Sucesso! AST exportada para: '{nome_arquivo}'.")
    except ValueError as ve:
        print(f"\n[FALHA SEMÂNTICA] {ve}")
    except Exception as e:
        print(f"\n[ERRO CRÍTICO] Falha ao salvar a AST em JSON: {e}")