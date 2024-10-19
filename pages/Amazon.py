import requests
from analisador import *
from models import *
from analista import *
usuarios = [elemento.nome for elemento in session.query(Usuario).all()]
col1,col2 = st.columns(2)
with col1:
    selecao_usuario = st.selectbox(label="Selecione seu usuário",options=usuarios,index=None)
if selecao_usuario:
    with col2:
        senha_input = st.text_input(label="",placeholder="Insira sua senha")
if selecao_usuario and senha_input:
    if int(senha_input) == session.query(Usuario).filter(Usuario.nome == selecao_usuario).first().senha:
        produto = st.text_input(label='',placeholder='Insira o produto desejado')

        if produto:
                col3,col4 = st.columns(2)
                with col3:
                    analise = st.button("Analisar produtos")
                if analise:
                        resposta = avaliar_busca(inciar_busca(produto))
                        add_search(search=resposta['resposta'],user=selecao_usuario,theme=produto)
                        enviar_email("juanpablozonho@gmail.com",f"Pesquisa do Produto {produto}",resposta['resposta'])
                        st.info(resposta['resposta'])
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
                          dict_resposta = interpretar_busca(buscar_produtos(inciar_busca(produto)))
                          st.info(f'''
{dict_resposta['sobre']}
{dict_resposta['descrição']}
{dict_resposta['informações']}'''
)
                          
#print(interpretar_busca(buscar_produtos('B0BXB6GFP8')))
