import requests
from analisador import *
from models import *
from analista import *
import speech_recognition as sr 
import pyttsx3


usuarios = [elemento.nome for elemento in session.query(Usuario).all()]
col1,col2 = st.columns(2)
with col1:
    selecao_usuario = st.selectbox(label="",options=usuarios,index=None,placeholder='Selecione seu usuário')
if selecao_usuario:
    with col2:
        senha_input = st.text_input(label="",placeholder="Insira sua senha")
if selecao_usuario and senha_input:
    if int(senha_input) == session.query(Usuario).filter(Usuario.nome == selecao_usuario).first().senha:
        col3,col4 = st.columns(2)
        with col3:
            produto = st.text_input(label='',placeholder='Insira o produto desejado')
        with col4:
            audio_value = st.experimental_audio_input("Faça sua pergunta")
            if audio_value:
                rec = sr.Recognizer()
                with sr.AudioFile(audio_value) as arquivo_audio:
                    audio = rec.record(arquivo_audio)
                    produto = rec.recognize_google(audio,language ='pt-BR ')
        if produto or audio_value:
                col3,col4 = st.columns(2)
                with col3:
                    analise = st.button("Analisar produtos")
                if analise:
                        with st.spinner('Buscando'):
                            resposta = avaliar_busca(inciar_busca(produto))
                        add_search(search=resposta['resposta'],user=selecao_usuario,theme=produto)
                        enviar_email("juanpablozonho@gmail.com",f"Pesquisa do Produto {produto}",resposta['resposta'])
                        bot = st.chat_message('assistant')
                        bot.write(resposta['resposta'])
                        ouvir = st.button('ouvir')
                        if ouvir:
                            engine = pyttsx3.init()
                            engine.setProperty("volume", 1) 
                            engine.setProperty("rate", 200)
                            engine.setProperty("voice", "brazil") 
                            engine.say("Olá")
                        pop_over = st.popover(label="Faça o donwload do arquivo")
                        with pop_over:
                            download = st.download_button(
                                    label="Faça o download do checklist no formato Excel",
                                    data=convert_df_to_excel(resposta['df']),
                                    file_name=f"Pesquisa do produto {produto}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                    )
                            if download:
                                st.success("Arquivo baixado com sucesso")
                with col4:
                     busca = st.button("Pesquisar informações do produto")
                if busca:
                    with st.spinner('Realizando busca'):
                          dict_resposta = interpretar_busca(buscar_produtos(inciar_busca(produto)))
                    bot = st.chat_message('assistant')
                    bot.write(f'''
{dict_resposta['sobre']}
-------------------------
{dict_resposta['descrição']}
----------------------------
{dict_resposta['informações']}'''
)
                          
#print(interpretar_busca(buscar_produtos('B0BXB6GFP8')))
