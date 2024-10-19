import requests
from bs4 import BeautifulSoup
from time import sleep
from analisador import analisar,carregar_arquivo
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import io
import tempfile

url = 'https://www.bing.com/search?q=geladeiras+frostfree+grandes'

# Fazer a solicitação HTTP
response = requests.get(url)

# Verificar se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Analisar o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    # Encontrar elementos específicos (exemplo: links)
    links = soup.find_all('a')
    lista_links= []
    # Imprimir os links
    for link in links:
        pagina = link.get('href')
        if "https://www" in str(pagina):
            try:
                lista_links.append(pagina)
            except:
                pass
    print(lista_links)
    lista_htmls = []
    for endereco in lista_links:
        try:
            resposta =requests.get(endereco)
            html = BeautifulSoup(resposta.content,'html.parser')
            lista_htmls.append(html)
        except:
            print("Não foi possível acessar esse site")
    lista_paginas = []
    print(lista_htmls)
    for html in lista_htmls:
        links_produtos = html.find_all("a")
        lista_paginas.append(links_produtos)
    links_produtos_da_pagina = []
    for lista in lista_paginas:
        for item in lista:
            href = item.get("href")
            links_produtos_da_pagina.append(href[:3])
    print(links_produtos_da_pagina)        
    lista_infos_produtos = []
    for info in links_produtos_da_pagina:
        try:
            acesso = requests.get(info)
            acesso_info = BeautifulSoup(acesso.content,'html.parser')
            lista_infos_produtos.append(acesso_info)
        except:
            print("Não foi possível acessar esse produto")
    texto = ''
    lista_conclusoes = []
    print(lista_infos_produtos)
    for info in lista_infos_produtos:
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt',encoding='utf-8') as temp:
        # Escreve o conteúdo do StringIO no arquivo temporário
            temp.write(str(info))
            # Obtém o caminho do arquivo temporário
            caminho_arquivo_temp = temp.name
        print(caminho_arquivo_temp)
        conclusao = str(carregar_arquivo("Nesse arquivo, extraia informações do produto como preço, vendedor, resumo das infos técnicas,site em que está sendo vendido e link de compra do produto. Me informe somente essas informações",caminho_arquivo_temp))
        lista_conclusoes.append(conclusao)
    print(lista_conclusoes)
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt',encoding='utf-8') as temp_conclusao:
        # Escreve o conteúdo do StringIO no arquivo temporário
            temp_conclusao.write(str(lista_conclusoes))
            # Obtém o caminho do arquivo temporário
            caminho_arquivo_temp_conclusao = temp_conclusao.name
    print(carregar_arquivo("Nessa lista python de avaliações de produtos, observe os preços e as configurações e me diga, qual é o melhor produto, seu preço, site, vendedor e link para compra",caminho_arquivo_temp_conclusao))
else:
    print(f'Erro ao acessar a página: {response.status_code}')
