from sqlalchemy import create_engine, Column, Integer, String, Float,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st 
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column("id",Integer, primary_key=True,autoincrement=True)
    nome = Column("nome",String)
    senha = Column("senha",Integer)

    def __init__(self,nome,senha):
        self.nome = nome
        self.senha = senha

class Pesquisa(Base):
    __tablename__ = 'pesquisas'

    id = Column("id_pesquisa",Integer,primary_key=True,autoincrement=True)
    pesquisa = Column("pesquisa",String)
    tema = Column("tema",String)
    usuario =  Column('usuario',ForeignKey("usuarios.id"))

    def __init__(self,pesquisa,tema,usuario):
        self.pesquisa = pesquisa
        self.tema = tema
        self.usuario = usuario


engine = create_engine(st.secrets['db'])
base =Base.metadata.create_all(engine)
