import streamlit as st
import time

# Lista de caixas disponíveis (ordenadas por capacidade decrescente)
caixas = sorted([
    {"id": 9,  "capacidade": 4},
    {"id": 12, "capacidade": 6},
    {"id": 15, "capacidade": 18},
    {"id": 16, "capacidade": 27},
    {"id": 19, "capacidade": 16},
    {"id": 20, "capacidade": 41},
    {"id": 21, "capacidade": 48}
], key=lambda x: x["capacidade"], reverse=True)

st.set_page_config(page_title="Distribuição de Caixas", layout="centered")

# Título com ícone de caixa
st.title("📦 Distribuição de Caixas para Embalagem")

# Campo de entrada
quantidade = st.number_input("Quantidade de caixas pequenas:", min_value=1, step=1, value=1)

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
if st.button("Calcular"):
    with st.spinner("Calculando..."):
        time.sleep(0.5)

    dist = calcular_distribuicao(quantidade)
    aproveitamento = calcular_aproveitamento(dist, quantidade)
    total_usado = sum(q * cap for _, q, cap in dist)

    # Exibição do resultado
    st.markdown("## Resultado:")
    for id_caixa, qtd, _ in dist:
        st.markdown(f"- **{qtd}x Caixa {id_caixa}**")
    
    st.markdown(f"**Total embalado:** {quantidade} caixas pequenas")
    st.markdown(f"**Capacidade usada:** {total_usado}")
    st.markdown(f"**Aproveitamento:** {aproveitamento:.2f}%")

    # Confirmação visual
    st.success("Distribuição calculada com sucesso!")
