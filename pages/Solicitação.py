import streamlit as st
from models.Pedidos import Solicitacao as P
import services.connect as C
from time import sleep
from streamlit_js_eval import streamlit_js_eval

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

st.sidebar.page_link('./pages/HomeFilial.py', label='Home')
st.sidebar.page_link('./pages/Status_Pedidos.py')

st.title('Solicitação de Recolhimento')


with st.form('Register'):
    col1, col2 = st.columns(2)
    P.filial = col1.text_input("Filial", value=st.session_state['Usuário'])
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
        try:
            if P.validar(P) == 'no':
                st.error('Verifique os dados inseridos, todos são obrigatórios, exceto o pedido novo.')
                sleep(3)
            else: 
                P.arquivo = C.upload_arquivo(P.arquivo, P.pedido) 
                teste = C.solicitacao(P)
                if teste == 'Pedido já cadastrado.':
                    st.error(teste)
                else:
                    st.warning(teste)
                    sleep(2)
                    streamlit_js_eval(js_expressions="parent.window.location.reload()")
        except:
                st.error('Ocorreu um erro, favor tente novamente.')
                sleep(1)
                st.rerun()
