import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import time

#Converter o DataFrame para csv e disponibilizar para download
@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')

#Mensagem de sucesso para download do csv
def mensagem_sucesso():
    sucesso = st.success('Download do CSV concluído!', icon="✅" )
   #Remover a mensagem de sucesso após 5 segundos 
    time.sleep(5)
    sucesso.empty()

#titulo da página
st.title('DADOS BRUTOS')

#Acessar os dados
url= 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json()) 
#Mudando o formato da data para datetime
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

#Mostrar o filtro acima do DataFrame
with st.expander('Colunas'):
    #Selecionar as colunas que deseja mostrar
    colunas=st.multiselect('Selecione as colunas',list(dados.columns),list(dados.columns))

#Criando os filtros
st.sidebar.title('Filtros')
#Filtro de produto
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())
#Filtro de preço do produto
with st.sidebar.expander('Preço do produto'):
                                                          #Selecionar 2 valores ao mesmo tempo
    preco = st.slider('Selecione o preço',0, 5000,(0, 5000))
#Filtro de data da compra
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Seleciona a data da compra', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))
#Filtro categoria do produto
with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione a categoria', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())
#Filtro de Frete
with st.sidebar.expander('Frete'):
    frete = st.slider('Valor do frete', 0, 250, (0, 250))
#Filtro Vendedor
with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect('Selecione o vendedor', dados['Vendedor'].unique(), dados['Vendedor'].unique())
#Filtro Local da Compra
with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect('Selecione o local da compra', dados['Local da compra'].unique(), dados['Local da compra'].unique())
#Avaliação da Compra
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra', 1,5, value= (1,5))
#Filtro tipo de pagamento
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())
#Filtro Quantidade de Parcelas
with st.sidebar.expander('Quantidade de parcelas'):
    parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1, 24))
   
#Filtragem das colunas
query = '''
Produto in @produtos and \
`Categoria do Produto` in @categoria and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedor and \
`Local da compra` in @local_compra and \
@avaliacao[0]<= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@parcelas[0] <= `Quantidade de parcelas` <= @parcelas[1]
'''
dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

#Outra forma de fazer a filtragem das colunas
#dados_filtrados = dados[
    #(dados["Produto"].isin(produtos)) &
    #(dados["Preço"].between(preco[0], preco[1])) &
    #(dados["Data da Compra"].between(pd.to_datetime(data_compra[0]), pd.to_datetime(data_compra[1]))) &
    #(dados["Categoria do Produto"].isin(categoria)) &
    #(dados["Frete"].between(frete[0], frete[1])) &
    #(dados["Vendedor"].isin(vendedor)) &
    #(dados["Local da compra"].isin(local_compra)) &
    #(dados["Avaliação da compra"].between(avaliacao[0], avaliacao[1])) &
    #(dados["Tipo de pagamento"].isin(tipo_pagamento)) &
    #(dados["Quantidade de parcelas"].between(parcelas[0], parcelas[1]))
#]

#Mostrar DataFrame completo na página
st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.')

#Botão de download do csv
st.markdown('Escreva um nome para o arquivo csv:')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Fazer o downloado do CSV', data=convert_csv(dados), file_name=nome_arquivo, mime='text/csv', on_click=mensagem_sucesso)
