import streamlit as st
from time import sleep
import services.connect as C

st.title("Bem vindo ao app de recolhimentos do Magazine Luiza CD 2650.")

with st.form('LoginForm')
    User = st.number_input('Filial',step=1)

    Pass = st.text_input("Senha")

    login_button = st.form_submit_button("Login")

    if login_button:
        if Pass == '123':
            st.session_state['Usuário'] = User
            st.session_state['Login'] = 'Logado'
            st.warning('Login realizado com sucesso!')
            sleep(2)
            st.switch_page('./pages/Solicitação.py')
            
        else:
            st.error("Favor verificar os dados.")
        

