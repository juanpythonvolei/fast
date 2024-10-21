import requests
from analisador import *
from models import *
from analista import *
import streamlit as st

senha = 4488

admin_usuario = st.text_input(label='',placeholder='Insira o usuário administrador')
senha_admin = st.text_input(label='',placeholder="Insira a senha do administrador")

if admin_usuario == 'Juan' and senha_admin == senha:
    selecao = st.selectbox(label='',placeholder="Selecione uma opção",options=['Alterar usuário','Alterar Senha','Excluir Usuário'])
    if selecao == 'Alterar Usuário':
        usuario_atual = st.text_input("Insira seu usuário atual")
        novo_usuario= st.text_input("Insira seu novo usuário")
        if usuario_atual and novo_usuario:
            st.info(update_user(usuario_atual,'nome',novo_usuario))
    elif selecao == 'Alterar Senha':
        usuario_atual = st.text_input("Insira seu usuário atual")
        senha_atual= st.text_input("Insira sua senha atual")
        nova_senha= st.text_input("Insira sua nova senha")
        if usuario_atual and senha_atual and nova_senha:
            st.info(update_user(usuario_atual,'senha',nova_senha))
    elif selecao == 'Excluir Usuário':
        usuario_atual = st.text_input("Selecione o usuário para a exclusão")
        if usuario_atual:
            st.info(delete_user(usuario_atual))
