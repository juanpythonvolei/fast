import streamlit as st
from analisador import *
from analista import *
from models import *
from database import *
import speech_recognition as sr 
import pyttsx3

tab1,tab2 = st.tabs(['Consulta',"Assistente"])

with tab1:
    usuarios = [elemento.nome for elemento in session.query(Usuario).all()]
    temas = [item.tema for item in session.query(Pesquisa).all()]
    
    selecao_usuario = st.selectbox(label="Selecione seu usuário",options=usuarios,index=None)
    selecao_tema = st.selectbox(label="Selecione seu tema",options=[item.tema for item in session.query(Pesquisa).filter(Pesquisa.usuario == selecao_usuario).all()],index=None)
    
    if selecao_usuario and selecao_tema:
        pesquisas = query_search(selecao_usuario,selecao_tema)
    
        col1,col2  = st.columns(2)
        with col1:
            if len(pesquisas) > 0:
                st.metric(value=len(pesquisas),label="Total de pesquisas para esse tema")
            else:
                st.info("Usuário não realizou pesquisas sobre esse tema")
        with col2:
            st.metric(label="Total de pesquisas do usuário",value=len([item for item in session.query(Pesquisa).filter(Pesquisa.usuario == selecao_usuario)]))
        for pesquisa in pesquisas:
            st.info(pesquisa)
    with tab2:
        audio_value = st.experimental_audio_input("Faça sua pergunta")
        if audio_value:
            bot = st.chat_message('assistant')
            rec = sr.Recognizer()
            with sr.AudioFile(audio_value) as arquivo_audio:
                audio = rec.record(arquivo_audio)
                texto = rec.recognize_google(audio,language ='pt-BR ')
            resposta = analisar(texto,str(query_searches_all())
            bot.write(resposta)   

