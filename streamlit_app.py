import streamlit as st
import pandas as pd

st.set_page_config(page_title="Distribuição de Caixas", layout="wide")

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

    for caixa in caixas:
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
                for c_menor in reversed(caixas):
                    if c_menor["capacidade"] >= restante:
                        resultado.append((c_menor["id"], 1, c_menor["capacidade"]))
                        restante = 0
                        break
                else:
                    resultado.append((caixa["id"], 1, capacidade))
                    restante = 0

    return resultado

def calcular_aproveitamento(distribuicao, total):
    usado = sum(q * cap for _, q, cap in distribuicao)
    return (total / usado) * 100 if usado else 0

st.title("📦 Distribuição de Caixas para Embalagem")

with st.form("formulario"):
    quantidade = st.number_input("Quantidade de caixas pequenas:", min_value=1, step=1)
    calcular = st.form_submit_button("Calcular")

if calcular:
    distribuicao = calcular_distribuicao(quantidade)
    aproveitamento = calcular_aproveitamento(distribuicao, quantidade)
    total_usado = sum(q * cap for _, q, cap in distribuicao)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("## 📦 Resultado:")
        st.markdown("### Detalhamento por caixa:")

        restantes = quantidade
        for id_caixa, qtd, capacidade in distribuicao:
            for _ in range(qtd):
                if restantes >= capacidade:
                    dentro = capacidade
                else:
                    dentro = restantes
                restantes -= dentro
                st.markdown(f"- **Caixa {id_caixa}**: {dentro} caixinhas")

        st.markdown("")
        st.markdown(f"**Total embalado:** {quantidade} caixas pequenas")
        st.markdown(f"**Capacidade usada:** {total_usado}")
        st.markdown(f"**Aproveitamento:** {aproveitamento:.2f}%")
        st.success("Distribuição calculada com sucesso!")

    with col2:
        st.markdown("## 📊 Tabela Resumo")
        dados_tabela = []
        restantes = quantidade
        for id_caixa, qtd, capacidade in distribuicao:
            for _ in range(qtd):
                if restantes >= capacidade:
                    dentro = capacidade
                else:
                    dentro = restantes
                restantes -= dentro
                dados_tabela.append({
                    "Caixa": id_caixa,
                    "Capacidade": capacidade,
                    "Caixinhas por unidade": dentro
                })

        df = pd.DataFrame(dados_tabela)
        resumo = df.groupby(["Caixa", "Capacidade", "Caixinhas por unidade"]).size().reset_index(name="Quantidade de caixas")
        st.dataframe(resumo, use_container_width=True)
