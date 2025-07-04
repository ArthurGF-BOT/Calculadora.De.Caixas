import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Caixas", layout="wide")

# Dados das caixas
caixas_cvc = sorted([
    {"id": 9, "capacidade": 4},
    {"id": 12, "capacidade": 6},
    {"id": 15, "capacidade": 18},
    {"id": 16, "capacidade": 27},
    {"id": 19, "capacidade": 16},
    {"id": 20, "capacidade": 41},
    {"id": 21, "capacidade": 48}
], key=lambda x: x["capacidade"], reverse=True)

caixas_map = sorted([
    {"id": 9, "capacidade": 4},
    {"id": 12, "capacidade": 6},
    {"id": 15, "capacidade": 18},
    {"id": 16, "capacidade": 27},
    {"id": 19, "capacidade": 5},
    {"id": 20, "capacidade": 10},
    {"id": 21, "capacidade": 18}
], key=lambda x: x["capacidade"], reverse=True)

# Funções
def calcular_distribuicao(quantidade, caixas, limiar=0.51):
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

# Título
st.title("Cálculo de Distribuição de Caixas")

# Estado
if "calcular" not in st.session_state:
    st.session_state.calcular = False

# Entradas
produto = st.selectbox("Selecione o produto:", ['CVC', 'MAP'])
quantidade = st.number_input("Quantidade de caixinhas:", min_value=1, value=1, step=1)

# Botão
if st.button("Calcular"):
    st.session_state.calcular = True

# Resultado
if st.session_state.calcular:
    caixas = caixas_cvc if produto == 'CVC' else caixas_map
    distribuicao = calcular_distribuicao(quantidade, caixas)
    aproveitamento = calcular_aproveitamento(distribuicao, quantidade)
    total_usado = sum(q * cap for _, q, cap in distribuicao)

    st.subheader(f"Resultado para produto {produto}")
    st.markdown("**Distribuição das caixas:**")

    restantes = quantidade
    linhas = []

    for id_caixa, qtd, capacidade in distribuicao:
        st.write(f"{qtd}x Caixa {id_caixa}")
        for _ in range(qtd):
            dentro = capacidade if restantes >= capacidade else restantes
            restantes -= dentro
            linhas.append({
                'Caixa': id_caixa,
                'Capacidade': capacidade,
                'Caixinhas por unidade': dentro
            })

    st.markdown("---")
    st.markdown(f"**Total embalado:** {quantidade} caixinhas")
    st.markdown(f"**Capacidade usada:** {total_usado}")
    st.markdown(f"**Aproveitamento:** {aproveitamento:.2f}%")

    # Tabela resumo
    df = pd.DataFrame(linhas)
    resumo = df.groupby(['Caixa', 'Capacidade', 'Caixinhas por unidade']) \
               .size().reset_index(name='Quantidade de caixas')

    styled_table = resumo.style.set_properties(**{
        'text-align': 'center'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'center')]
    }])

    st.markdown("### Tabela Resumo")
    st.dataframe(styled_table, use_container_width=True, hide_index=True)
