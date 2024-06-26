import streamlit as st

try:
    log = st.session_state['Login']
except:
    st.switch_page('./main.py')

st.title('SEJA BEM VINDO AO APP DO ATENDIMENTO CD 2650')

st.text('O que você deseja?')
c1, c2 = st.columns(2)
c1.page_link('./pages/Solicitação.py')
c1.page_link('./pages/Status_Pedidos.py')
c2.page_link('./pages/Registrar_Saida_Loja.py')
c2.page_link('./pages/Consulta_Saida_Loja.py')
