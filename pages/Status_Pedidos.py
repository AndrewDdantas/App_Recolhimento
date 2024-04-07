import streamlit as st
from services.connect import consultar_pedidos

st.set_page_config(
    page_title="Status dos Pedidos",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",  # Pode ser "wide" ou "centered"
    initial_sidebar_state="collapsed",  # Pode ser "auto", "expanded", ou "collapsed"
)
st.sidebar.page_link('./pages/HomeFilial.py', label='Home')
st.sidebar.page_link('./pages/Solicitação.py')

try:
    log = st.session_state['Login']
except:
    st.switch_page('./main.py')


st.title('Status Pedidos')

with st.form("FormStatus"):

    Ped = st.number_input('Pedido', step=1, label_visibility='hidden')
    button = st.form_submit_button('Consultar')

    if button:
        st.table(consultar_pedidos(Ped, st.session_state['Usuário']).assign(hack='').set_index('hack'))
    else:
        st.table(consultar_pedidos(filial=st.session_state['Usuário']).assign(hack='').set_index('hack'))