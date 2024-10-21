from database import *
from sqlalchemy.orm import sessionmaker
import streamlit as st

session = sessionmaker(bind=engine)
session = session()

@st.dialog("Deseja realmente continuar")
def confirmar(function):
    confirmar = st.button('Confirmar')
    if confirmar:
        st.success(function)

def add_user(name,password):
    new_user = Usuario(nome=name,senha=password)
    session.add(new_user)
    session.commit()
    return f"Usuário {name} cadastrado com sucesso"

def query_user(name):
    query = session.query(Usuario).filter(Usuario.nome == name).first()
    return f"O Usuário {name} possúi a seguinte senha: {query.senha}"

def add_search(search,user,theme):
    search = Pesquisa(pesquisa=search,usuario=user,tema=theme)
    session.add(search)
    session.commit()
    return f"Pesquisa {search.pesquisa} adicionada com sucesso"

def query_search(user,theme):
    searches = session.query(Pesquisa).filter(Pesquisa.usuario==user,Pesquisa.tema == theme).all()
    return [item.pesquisa for item in searches]

def query_search_all():
    searches = session.query(Pesquisa).all()
    return [f"{item.pesquisa}-{item.usuario}" for item in searches]
def delete_user(user):
    usuario_existente = session.query(Usuario).filter(Usuario.nome == user).first()
    if usuario_existente:
        session.delete(usuario_existente)
        session.commit()
        return f"Usuário {usuario_existente.nome} deletado com sucesso"
    else:
        return f"Usuário {user} não existe"
    
def update_user(user,elemento,informação):
    usuario_existente = session.query(Usuario).filter(Usuario.nome == user).first()
    if usuario_existente:
        if elemento == 'nome': 
            usuario_existente.nome = informação
            session.commit()
        elif elemento == 'senha':
            usuario_existente.senha = informação
        return f"Usuário {usuario_existente.nome} Atualizado no item {elemento} com sucesso"
    else:
        return f"Usuário {user} não existe"

