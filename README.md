# CityFlow

## Tabela Semântica
| Produções | Regras Semânticas |
| --- | --- |
| P → P₁ decl | { P.cod = P₁.cod || decl.cod } |
| P → decl | { P.cod = decl.cod } |
| decl → rua_decl | { decl.cod = rua_decl.cod } |
| decl → saida_decl | { decl.cod = saida_decl.cod } |
| rua_decl → **rua** id **{** attr_list **}** | { insere_simbolo(id.nome, attr_list.attrs); rua_decl.cod = geracod(id.nome "=" attr_list.attrs) } |
| attr_list → attr_list₁ **,** attr | { attr_list.attrs = attr_list₁.attrs || attr.val; attr_list.cod = attr_list₁.cod || attr.cod } |
| attr_list → attr | { attr_list.attrs = attr.val; attr_list.cod = attr.cod } |
| attr → **tamanho** **:** MEDIDA_M | { attr.val = MEDIDA_M.num; attr.cod = geracod("tamanho" "=" MEDIDA_M.num) } |
| attr → **mao** **:** tipo_mao | { attr.val = tipo_mao.val; attr.cod = geracod("mao" "=" tipo_mao.val) } |
| tipo_mao → **dupla** | { tipo_mao.val = "dupla" } |
| tipo_mao → **unica** | { tipo_mao.val = "unica" } |
| saida_decl → **saida de** id₁ **em** med₁ **para** id₂ **em** med₂ sinal_opt | { verifica_existe(id₁.nome); verifica_existe(id₂.nome); verifica_posicao(id₁.nome, med₁.num); verifica_posicao(id₂.nome, med₂.num); temp = geratemp(); saida_decl.cod = geracod(temp "= saida" id₁.nome "+" med₁.num "→" id₂.nome "+" med₂.num) || sinal_opt.cod } |
| sinal_opt → **{** sinal_decl **}** | { sinal_opt.cod = sinal_decl.cod } |
| sinal_opt → ε | { sinal_opt.cod = " " } |
| sinal_decl → **sinal** **:** tempo_list | { verifica_ciclo(tempo_list.verde, tempo_list.vermelho); sinal_decl.cod = geracod("sinal" "=" tempo_list.verde "+" tempo_list.vermelho) } |
| tempo_list → tempo_list₁ **,** tempo_item | { tempo_list.verde = tempo_list₁.verde || tempo_item.verde; tempo_list.vermelho = tempo_list₁.vermelho || tempo_item.vermelho; tempo_list.cod = tempo_list₁.cod || tempo_item.cod } |
| tempo_list → tempo_item | { tempo_list.verde = tempo_item.verde; tempo_list.vermelho = tempo_item.vermelho; tempo_list.cod = tempo_item.cod } |
| tempo_item → **verde** TEMPO_S | { tempo_item.verde = TEMPO_S.num; tempo_item.cod = geracod("verde" "=" TEMPO_S.num) } |
| tempo_item → **vermelho** TEMPO_S | { tempo_item.vermelho = TEMPO_S.num; tempo_item.cod = geracod("vermelho" "=" TEMPO_S.num) } |