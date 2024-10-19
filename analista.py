import requests
from bs4 import BeautifulSoup
from time import sleep
from analisador import analisar
import pandas as pd
import streamlit as st
from io import BytesIO
from models import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import tempfile
def pegar_infos_gerais_mercado_livre(link,produto):
    try:
        url = f"{link}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        info_geral = soup.find(class_='ui-pdp-description__content')
        vendedor = soup.find(class_="ui-pdp-color--BLACK ui-pdp-size--LARGE ui-pdp-family--SEMIBOLD ui-seller-data-header__title non-selectable")
        preco = soup.find(class_="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact")
        imagem = soup.find(class_="ui-pdp-gallery__column__variation-gallery")
        link_imagem = imagem.get("src")
        dict_mercado_livre = {'vendedor':vendedor.text,'preco':preco.text,'infos':info_geral.text,'produto':produto,'link':link,"link imagem":link_imagem}
        return dict_mercado_livre
    except:
        pass
def pesquisar_mercado_livre(produto):
    lista_mercado_livre = []
    url = f"https://lista.mercadolivre.com.br/{produto}"
    response = requests.get(url)
    pagina = BeautifulSoup(response.content, "html.parser")
    elemento_titulo = pagina.find(class_="ui-search-results ui-search-results--without-disclaimer")
    lista = elemento_titulo.find('ol')
    for item in lista:
            tags = item.find_all("a")
            for tag in tags:
                link = tag.get("href")
                dict = pegar_infos_gerais_mercado_livre(link,produto)
                if dict in lista_mercado_livre:
                     pass
                else:
                    lista_mercado_livre.append(dict)
    return lista_mercado_livre        

def pesquisar(produto):
    lista_dfs = []
    if produto:
            texto_mercado_livre = ''
            for item in pesquisar_mercado_livre(produto):
                try:
                    info_mercado_livre = f'''Vendedor: {item['vendedor']}
                    item: {item['infos']}
                    Preço: {item['preco']}
                    link: {item['link']}
                    Produto: {item['produto']}'''
                    texto_mercado_livre += info_mercado_livre
                    df_unico = pd.DataFrame(item,index=[1])

                    lista_dfs.append(df_unico)
                except:
                    pass               
            df_final = pd.concat(lista_dfs)         
            resposta = analisar("Qual é o produto mais vantajoso a ser comprado levando em consideração a qualidade tecnica e seu preço ?. Me diga além disso, o nome de seu vendedor,o link para o produto do site, e faça uma tabela decrescente em relação ao preço dos demais produtos,seus vendedores e seus links de compra",texto_mercado_livre)
            return {"resposta":resposta,"pesquisa":df_final}
    
@st.cache_data
def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            processed_data = output.getvalue()
            return processed_data  
    
def inciar_busca(produto):
    url = "https://real-time-amazon-data.p.rapidapi.com/search"

    querystring = {"query":f"{produto}","page":"1","country":"BR","sort_by":"RELEVANCE","product_condition":"ALL","is_prime":"false","deals_and_discounts":"NONE"}

    headers = {
        "x-rapidapi-key": st.secrets['x-rapidapi-key'],
        "x-rapidapi-host": st.secrets['real-time-amazon-data.p.rapidapi.com']
    }
    lista_respostas = []
    response = requests.get(url, headers=headers, params=querystring)
    resposta = response.json()
    for produto in resposta['data']['products']:
        nome_produto = produto['product_title']
        link_produto = produto['product_url']
        preco_pruduto  = str(produto['product_minimum_offer_price']).replace("\xa0","").strip()
        entrega = produto['delivery']
        opcoes_compra  = produto['sales_volume']
        ass = produto['asin']
        resulado = {"nome do produto":nome_produto,
                    "link de compra":link_produto,
                    "preço do produto":preco_pruduto,
                    "entrega":entrega,
                    "opcoes de compra":opcoes_compra,
                    "Assinatura":ass
                    }
        if resulado in lista_respostas:
            pass
        else:
            lista_respostas.append(resulado)
    return lista_respostas

def avaliar_busca(lista_produtos):  
    dfs = [pd.DataFrame(item,index=[1]) for item in lista_produtos]
    df_final = pd.concat(dfs)
    
    return {"resposta":analisar("Você está vendo uma lista de dicionários python. Cada dicionário, corresponde a informações sobre um produto específico. Me diga qual item é o mais economicamente vantajoso. Faça isso, construindo uma resposta que contenha seu preço,  nome, link de compra. Retorne ainda uma tabela do segundo item mais vantaso em diante.", str(lista_produtos)),"df":df_final}

def buscar_produtos(lista_ass):
    for ass in lista_ass:
        assinatura = ass['Assinatura']
    url = "https://real-time-amazon-data.p.rapidapi.com/product-details"

    querystring = {"asin":f"{assinatura}","country":"BR"}

    headers = {
        "x-rapidapi-key":st.secrets['x-rapidapi-key'],
        "x-rapidapi-host": st.secrets['real-time-amazon-data.p.rapidapi.com']
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()

def interpretar_busca(busca):
    infos = ''
    sobre = ''
    for item in busca['data']['about_product']:
        sobre += item
    descricao = busca['data']['product_description']
    informacoes = list(busca['data']['product_information'].values())
    for info in informacoes:
        infos += f'{info}\n'
    return {"sobre":sobre,
            "descrição":descricao,
            "informações":infos}    


def enviar_email(destinatario, assunto, mensagem):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = "juanpablozonho@gmail.com"
    senha = st.secrets['email_senha']
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'plain'))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.close()
        return st.success("E-mail enviado com sucesso!")
    except Exception as e:
        return st.error(f"Falha ao enviar o e-mail: {e}")

