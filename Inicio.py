import streamlit as st
from models import *

st.image('https://miro.medium.com/v2/resize:fit:1200/1*8AlWn7eMF5To4ZBKfuGhiQ.jpeg')

st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #FFA421;
        color: white; /* Cor do texto na barra lateral */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body {
        background-color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
    <style>
       [aria-expanded='true'] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

css = """
<style>
.centered-image {
    display: block;
    margin: 0 auto;
}
</style>
"""
toggle = st.toggle("Já tenho uma conta")

if toggle:
    usuario = st.text_input(label="Usuário",placeholder="Insira seu usuário")
    senha= st.text_input(label="Senha",placeholder="Insira sua senha")
    if usuario and senha:
            verificar_usuario = session.query(Usuario).filter(Usuario.nome == usuario).firt()
            if verificar_usuario:
                if int(senha) == session.query(Usuario).filter(Usuario.nome == usuario).first().senha:
                    st.switch_page("pages/Consulta.py")
                else:
                    st.error("Senha do usuário está incorreta")
else:
    novo_usuario = st.text_input(label="Novo Usuário",placeholder="Insira seu novo usuário")
    nova_senha= st.text_input(label="Nova Senha",placeholder="Insira sua nova senha")
    if novo_usuario and nova_senha:
        try:
            if novo_usuario == session.query(Usuario).filter(Usuario.nome == novo_usuario).first().nome:
                st.error("Você não pode utlizar esse usuário")
        except:
            add_user(novo_usuario,nova_senha)
            st.switch_page("pages/Consulta.py")
