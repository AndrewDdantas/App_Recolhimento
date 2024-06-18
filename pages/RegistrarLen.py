import streamlit as st
import pandas as pd
import services.connect as C
from time import sleep

st.set_page_config(
    page_title="Solicitação de Recolhimento",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",  # Pode ser "wide" ou "centered"
    initial_sidebar_state="collapsed",  # Pode ser "auto", "expanded", ou "collapsed"
)

try:
    log = st.session_state['Login']
except:
    st.switch_page('./main.py')


if 'df' not in st.session_state:
    data = {'Filial': [],
        'Pedido': [],
        'Transportadora': [],
        'Nota':[]}
    st.session_state['df'] = pd.DataFrame(data)

elif not st.session_state['df'].empty:
    st.dataframe(st.session_state['df'], hide_index=True)
    button_registrar = st.button("Gerar Lote")

try:
    if button_registrar:
        with st.spinner('Lote sendo gerado......'):
            lote = C.registrar_pedidos(st.session_state['df'])
            st.session_state['df'] = pd.DataFrame()
        st.warning(f'Foi gerado o Lote: {lote}')
        st.rerun()
except:
    ''

with st.form('Solicitar'):
    filial = st.number_input('Filial', step=1)
    pedido = st.number_input('Pedido', step=1, min_value=900000000)
    transportadora = st.selectbox('Transportadora', C.transportadoras())
    nota = st.file_uploader('Nota Fiscal')

    submit = st.form_submit_button('Inserir em Lote')

    if submit:
        nota = C.upload_arquivo(nota,pedido)
        new_row = {'Filial': filial,
        'Pedido': pedido,
        'Transportadora': transportadora,
        'Nota': nota}
        new_df = pd.DataFrame([new_row])
        st.session_state['df'] = pd.concat([st.session_state['df'], new_df], ignore_index=True)
        st.rerun()
