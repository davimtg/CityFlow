# CityFlow

## Tabela Semântica
| Produções | Regras Semânticas |
| --- | --- |
| P → P₁ decl | { P.cod = P₁.cod \|\| decl.cod } |
| P → decl | { P.cod = decl.cod } |
| decl → rua_decl | { decl.cod = rua_decl.cod } |
| decl → saida_decl | { decl.cod = saida_decl.cod } |
| rua_decl → **rua** STRING **{** attr_list **}** | { verifica_duplicado(STRING.val); insere_simbolo(STRING.val, attr_list.attrs); rua_decl.cod = geracod(STRING.val, "=", attr_list.attrs) } |
| attr_list → attr_list₁ attr | { verifica_unicidade(attr_list₁.attrs, attr.nome); attr_list.attrs = merge(attr_list₁.attrs, attr.nome, attr.valor); attr_list.cod = attr_list₁.cod \|\| attr.cod } |
| attr_list → attr | { attr_list.attrs = criar_mapa(attr.nome, attr.valor); attr_list.cod = attr.cod } |
| attr → **tamanho** **:** MEDIDA_M **;** | { attr.nome = "tamanho"; attr.valor = MEDIDA_M.val; attr.cod = geracod("tamanho", "=", MEDIDA_M.val) } |
| attr → **mao** **:** tipo_mao **;** | { attr.nome = "mao"; attr.valor = tipo_mao.val; attr.cod = geracod("mao", "=", tipo_mao.val) } |
| tipo_mao → **dupla** | { tipo_mao.val = "dupla" } |
| tipo_mao → **unica** | { tipo_mao.val = "unica" } |
| saida_decl → **saida de** STRING₁ **em** MEDIDA_M₁ **para** STRING₂ **em** MEDIDA_M₂ sinal_opt **;** | { verifica_existe(STRING₁.val); verifica_existe(STRING₂.val); verifica_posicao(STRING₁.val, MEDIDA_M₁.val); verifica_posicao(STRING₂.val, MEDIDA_M₂.val); temp = geratemp(); saida_decl.cod = geracod(temp, "=", "saida", STRING₁.val, "+", MEDIDA_M₁.val, "→", STRING₂.val, "+", MEDIDA_M₂.val) \|\| sinal_opt.cod } |
| sinal_opt → **{** tempo_list **}** | { verifica_obrigatorios(tempo_list.tempos, "verde", "vermelho"); sinal_opt.cod = tempo_list.cod } |
| sinal_opt → ε | { sinal_opt.cod = "" } |
| tempo_list → tempo_list₁ tempo_item | { verifica_unicidade(tempo_list₁.tempos, tempo_item.nome); tempo_list.tempos = merge(tempo_list₁.tempos, tempo_item.nome, tempo_item.valor); tempo_list.cod = tempo_list₁.cod \|\| tempo_item.cod } |
| tempo_list → tempo_item | { tempo_list.tempos = criar_mapa(tempo_item.nome, tempo_item.valor); tempo_list.cod = tempo_item.cod } |
| tempo_item → **verde** **:** TEMPO_S **;** | { tempo_item.nome = "verde"; tempo_item.valor = TEMPO_S.val; tempo_item.cod = geracod("verde", "=", TEMPO_S.val) } |
| tempo_item → **vermelho** **:** TEMPO_S **;** | { tempo_item.nome = "vermelho"; tempo_item.valor = TEMPO_S.val; tempo_item.cod = geracod("vermelho", "=", TEMPO_S.val) } |