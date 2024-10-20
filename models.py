from database import *
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=engine)
session = session()

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

def query_search_all(user):
    searches = session.query(Pesquisa).filter(Pesquisa.usuario==user).all()
    return [item.pesquisa for item in searches]


