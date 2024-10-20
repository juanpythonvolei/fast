import streamlit as st
from models import *

st.image('https://static.vecteezy.com/system/resources/previews/026/147/094/non_2x/vintage-magnifying-glass-chalk-sketch-on-blackboard-background-hand-drawn-illustration-retro-style-vector.jpg')

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
    usuario = st.text_input(label="",placeholder="Insira seu usuário")
    senha= st.text_input(label="",placeholder="Insira sua senha")
    if usuario and senha:
            if int(senha) == session.query(Usuario).filter(Usuario.nome == usuario).first().senha:
                st.switch_page("pages/Consulta.py")
                login = usuario
else:
    novo_usuario = st.text_input(label="",placeholder="Insira seu novo usuário")
    nova_senha= st.text_input(label="",placeholder="Insira sua nova senha")
    if novo_usuario and nova_senha:
        try:
            if int(nova_senha) == session.query(Usuario).filter(Usuario.nome == novo_usuario).first().senha:
                st.error("Você não pode utlizar essa senha")
        except:
            add_user(novo_usuario,nova_senha)
            st.switch_page("pages/Consulta.py")
            login = novo_usuario
