import streamlit as st

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

def calcular_distribuicao(quantidade, limiar=0.51):
    restante = quantidade
    resultado = []

    for i, caixa in enumerate(caixas):
        if restante <= 0:
            break

        capacidade = caixa["capacidade"]

        qtd_completa = restante // capacidade

        if qtd_completa > 0:
            resultado.append((caixa["id"], qtd_completa, capacidade))
            restante -= qtd_completa * capacidade

        if 0 < restante < capacidade:
            if restante >= limiar * capacidade:
                resultado.append((caixa["id"], 1, capacidade))
                restante = 0
            else:
                caixa_menor_encontrada = False
                for c_menor in reversed(caixas):
                    if c_menor["capacidade"] >= restante:
                        resultado.append((c_menor["id"], 1, c_menor["capacidade"]))
                        restante = 0
                        caixa_menor_encontrada = True
                        break
                if not caixa_menor_encontrada:
                    resultado.append((caixa["id"], 1, capacidade))
                    restante = 0

    return resultado

def calcular_aproveitamento(distribuicao, total):
    usado = sum(q * cap for _, q, cap in distribuicao)
    return (total / usado) * 100 if usado else 0

# Configuração da página
st.set_page_config(page_title="Distribuição de Caixas", layout="centered")

st.title("📦 Distribuição de Caixas para Embalagem")

quantidade = st.number_input("Quantidade de caixas pequenas:", min_value=1, step=1)

if st.button("Calcular"):
    dist = calcular_distribuicao(quantidade)
    aproveitamento = calcular_aproveitamento(dist, quantidade)
    total_usado = sum(q * cap for _, q, cap in dist)

    st.markdown("## Resultado:")
    for id_caixa, qtd, _ in dist:
        st.markdown(f"- **{qtd}x Caixa {id_caixa}**")

    st.markdown(f"**Total embalado:** {quantidade} caixas pequenas")
    st.markdown(f"**Capacidade usada:** {total_usado}")
    st.markdown(f"**Aproveitamento:** {aproveitamento:.2f}%")

    st.success("Distribuição calculada com sucesso!")
