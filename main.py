import streamlit as st
from time import sleep
import services.connect as C

st.title("Bem vindo ao app de insucesso do Magazine Luiza.")

User = st.text_input('Usuário')

Pass = st.text_input("Senha")

login_button = st.button("Login")

if login_button:
    if Pass == '123':
        st.session_state['Usuário'] = User
        st.session_state['Login'] = 'Logado'
        st.write('Login realizado com sucesso!')
        sleep(2)
        st.switch_page('./pages/Solicitação.py')
        
    else:
        st.write("Favor verificar os dados.")
        

