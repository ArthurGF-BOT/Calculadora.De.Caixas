import streamlit as st

st.title("🔧 Teste mínimo Streamlit")

produto = st.selectbox("Selecione o produto:", ['CVC', 'MAP'])
st.write("Produto selecionado:", produto)

if st.button("Calcular"):
    st.success("Botão pressionado com sucesso!")
