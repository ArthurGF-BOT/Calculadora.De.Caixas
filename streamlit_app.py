import streamlit as st
import time
import pandas as pd

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

# Filtro de produto (exemplo de futuro com possibilidade de mais produtos)
produto_selecionado = st.selectbox("Selecione o produto:", ["CVC"])

# Tabela informativa com as caixas disponíveis (agora com a coluna 'Produto')
st.markdown("### Caixas disponíveis:")
tabela_caixas = pd.DataFrame([
    {"ID da Caixa": f"Caixa {caixa['id']}", "Capacidade": caixa["capacidade"], "Produto": caixa["produto"]}
    for caixa in caixas
])

# Convertendo a tabela em HTML para centralizar os valores
tabela_caixas_html = tabela_caixas.to_html(index=False, escape=False)

# Estilizando a tabela para centralizar todas as células usando CSS
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

# Exibindo a tabela centralizada
st.markdown(tabela_caixas_html, unsafe_allow_html=True)

# Campo de entrada
quantidade = st.number_input("Quantidade de caixas pequenas (apenas número par):", min_value=1, step=1, value=2)

# Verificando se o número inserido é par
if quantidade % 2 != 0:
    st.error("Por favor, insira um número par para a quantidade de caixas.")

# Função de cálculo
def calcular_distribuicao(quantidade):
    restante = quantidade
    resultado = []

    for caixa in caixas:
        if restante <= 0:
            break
        qtd = restante // caixa["capacidade"]
        if qtd > 0:
            resultado.append((caixa["id"], qtd, caixa["capacidade"]))
            restante -= qtd * caixa["capacidade"]

    if restante > 0:
        for caixa in caixas:
            if caixa["capacidade"] >= restante:
                resultado.append((caixa["id"], 1, caixa["capacidade"]))
                break

    return resultado

# Cálculo de aproveitamento
def calcular_aproveitamento(distribuicao, total):
    usado = sum(q * cap for _, q, cap in distribuicao)
    return (total / usado) * 100 if usado else 0

# Botão de ação
if quantidade % 2 == 0 and st.button("Calcular"):
    with st.spinner("Calculando..."):
        time.sleep(0.5)

    dist = calcular_distribuicao(quantidade)
    aproveitamento = calcular_aproveitamento(dist, quantidade)
    total_usado = sum(q * cap for _, q, cap in dist)

    # Exibe resultado da distribuição como texto
    st.markdown("## Resultado da distribuição:")
    for id_caixa, qtd, _ in dist:
        st.markdown(f"- **Caixa {id_caixa}:** {qtd} unidades")

    st.markdown(f"**Total embalado:** {quantidade} caixas pequenas")
    st.markdown(f"**Capacidade usada:** {total_usado}")
    st.markdown(f"**Aproveitamento:** {aproveitamento:.2f}%")

    st.success("Distribuição calculada com sucesso!")
