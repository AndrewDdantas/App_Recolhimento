import streamlit as st

st.title('SEJA BEM VINDO AO APP DO ATENDIMENTO CD 2650')

st.text('O que você deseja?')
c1, c2 = st.columns(2)
c1.page_link('./pages/Solicitação.py')
c2.page_link('./pages/Status_Pedidos.py')