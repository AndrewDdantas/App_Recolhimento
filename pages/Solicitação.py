import streamlit as st
from streamlit_autorefresh import st_autorefresh
from models.Pedidos import Solicitacao as P
import services.connect as C
from time import sleep


try:
    log = st.session_state['Login']
except:
    st.switch_page('./main.py')

st_autorefresh(interval=1000 * 60, limit=100, key="teste_atualizacao")


st.title('Solicitação de Recolhimento')


with st.form('Register'):
    col1, col2 = st.columns(2)
    P.filial = col1.number_input("Filial", step=1)
    P.pedido = col2.number_input("Pedido", step=1)
    P.pedido_novo = col1.number_input("Pedido Novo", step=1)
    P.item = col2.number_input("Item", step=1)
    P.descricao = col1.text_input("Descrição", value=None)
    P.motivo = col2.text_input("Motivo", value=None)
    P.obs = col1.text_input("Observação", value=None)
    P.destino = col2.selectbox('Destino', ['','Filial', 'Dqs'])
    P.regiao = col1.text_input('Região', value=None)

    P.arquivo = st.file_uploader('Documentação')

    button_submit = st.form_submit_button('Registrar')
    
    if button_submit:

        if P.validar(P) == 'no':
            st.error('Verifique os dados inseridos.')
            sleep(1)
            st.rerun()
        else: 
            P.arquivo = C.upload_arquivo(P.arquivo, P.pedido) 
            teste = C.solicitacao(P)
            if teste == 'Pedido já cadastrado.':
                st.error(teste)
            else:
                st.warning(teste)
