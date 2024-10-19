import google.generativeai as genai
import streamlit as st 
def analisar(pergunta,conteudo):
    
    genai.configure(api_key=st.secrets['ia'])
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role": "user", "parts": [{"text": conteudo}]}])
    response = chat.send_message(pergunta)
    return response.text


def carregar_arquivo(pergunta,conteudo):
    genai.configure(api_key=st.secrets['ia'])
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role":"user","parts":[genai.upload_file(conteudo)]}])
    response = chat.send_message(pergunta)
    return response.text



#print(carregar_arquivo("Este é meu código que visa criar um analista de preços. Quais melhorias você sugere?",r"C:\Users\juanz\OneDrive\Área de Trabalho\codigo.png"))
#print(carregar_arquivo("Do que se trata esse arquivo?",r"C:\Users\juanz\OneDrive\Área de Trabalho\video teste.mp4"))