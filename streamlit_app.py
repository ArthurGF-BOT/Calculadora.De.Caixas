import streamlit as st
import time
import pandas as pd
from itertools import combinations_with_replacement
from collections import Counter

# Lista de caixas disponíveis (ordenadas por capacidade decrescente)
caixas = sorted([
    {"id": 9,  "capacidade": 4, "produto": "CVC"},
    {"id": 12, "capacidade": 6, "produto": "CVC"},
    {"id": 15, "capacidade": 18, "produto": "CVC"},
    {"id": 16, "capacidade": 27, "produto": "CVC"},
    {"id": 19, "capacidade": 16, "produto": "CVC"},
    {"id": 20, "capacidade": 41, "produto": "CVC"},
    {"id": 21, "capacidade": 48, "produto": "CVC"}
], key=lambda x: x["capacidade"], reverse=True)

st.set_page_config(page_title="Distribuição de Caixas", layout="centered")

# Título com ícone de caixa
st.title("📦 Distribuição de Caixas PA")

# Filtro de produto (para expansão futura)
produto_selecionado = st.selectbox("Selecione o produto:", ["CVC"])

# Tabela informativa com as caixas disponíveis
st.markdown("### Caixas disponíveis:")
tabela_caixas = pd.DataFrame([
    {
        "ID da Caixa": f"Caixa {caixa['id']}",
        "Capacidade": caixa["capacidade"],
        "Produto": caixa["produto"]
    }
    for caixa in caixas
])

# Estilização da tabela
tabela_caixas_html = tabela_caixas.to_html(index=False, escape=False)
tabela_caixas_html = f"""
<style>
    .dataframe {{
        margin-left: auto;
        margin-right: auto;
        text-align: center;
        width: 100%;
    }}
    .dataframe th, .dataframe td {{
        text-align: center;
    }}
</style>
{tabela_caixas_html}
"""
st.markdown(tabela_caixas_html, unsafe_allow_html=True)

# Entrada de quantidade
quantidade = st.number_input("Quantidade de caixas pequenas:", min_value=1, step=1, value=1)

# Função para calcular a distribuição ideal
def calcular_distribuicao(quantidade):
    restante = quantidade
    resultado = []

    # Preenchimento inicial com maiores capacidades
    for caixa in caixas:
        if restante <= 0:
            break
        qtd = restante // caixa["capacidade"]
        if qtd > 0:
            resultado.append((caixa["id"], qtd, caixa["capacidade"]))
            restante -= qtd * caixa["capacidade"]

    # Se ainda sobrar, tentar encontrar melhor combinação para sobra
    if restante > 0:
        def encontrar_melhor_combinacao(restante):
            melhor_excesso = float('inf')
            melhor_combo = None
            for r in range(1, 5):  # Até 4 caixas combinadas
                for combo in combinations_with_replacement(caixas, r):
                    soma = sum(c["capacidade"] for c in combo)
                    if soma >= restante and (soma - restante) < melhor_excesso:
                        melhor_excesso = soma - restante
                        melhor_combo = combo
                        if melhor_excesso == 0:
                            return melhor_combo
            return melhor_combo

        melhor_combo = encontrar_melhor_combinacao(restante)
        if melhor_combo:
            contador = Counter([caixa["id"] for caixa in melhor_combo])
            for id_caixa, qtd in contador.items():
                capacidade = next(caixa["capacidade"] for caixa in caixas if caixa["id"] == id_caixa)
                resultado.append((id_caixa, qtd, capacidade))

    return resultado

# Cálculo de aproveitamento
def calcular_aproveitamento(distribuicao, total):
    usado = sum(min(cap * qtd, total - sum(min(cap * q, total) for _, q, cap in distribuicao[:i]))
                for i, (id_, qtd, cap) in enumerate(distribuicao))
    return (total / usado) * 100 if usado else 0

# Botão de ação
if st.button("Calcular"):
    with st.spinner("Calculando..."):
        time.sleep(0.5)

    dist = calcular_distribuicao(quantidade)
    total_caixas_grandes = sum(q for _, q, _ in dist)

    # Exibir resultados detalhados
    st.markdown("## Resultado da distribuição:")
    restante_para_embalar = quantidade
    for id_caixa, qtd, capacidade in dist:
        for _ in range(qtd):
            if restante_para_embalar <= 0:
                break
            armazenado = min(capacidade, restante_para_embalar)
            restante_para_embalar -= armazenado
            st.markdown(f"- **Caixa {id_caixa}** → {armazenado} caixinhas pequenas")

    total_usado = quantidade  # já usamos exatamente o que o usuário pediu
    capacidade_total_usada = sum(min(qtd * capacidade, quantidade - sum(min(c * q, quantidade) for _, q, c in dist[:i]))
                                 for i, (id_, qtd, capacidade) in enumerate(dist))
    aproveitamento = (total_usado / capacidade_total_usada) * 100 if capacidade_total_usada else 0

    # Exibir totais
    st.markdown(f"**Total embalado:** {total_usado} caixinhas pequenas")
    st.markdown(f"**Capacidade usada:** {capacidade_total_usada}")
    st.markdown(f"**Aproveitamento:** {aproveitamento:.2f}%")
    st.markdown(f"**Total de caixas grandes usadas:** {total_caixas_grandes}")

    st.success("Distribuição calculada com sucesso!")
