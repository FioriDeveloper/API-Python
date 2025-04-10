import  streamlit as st
import  webbrowser
#from timetest import data, hora #Import da API de hora e data.
import requests
import time

#API DATA E HORA
api_url = "https://timeapi.io/api/Time/current/ip?ipAddress=177.255.90.16"

response = requests.get(api_url)

if response.status_code == 200:
    dados = response.json()

    data = dados["date"]
    hora = dados["time"]

    print(f"Data: {data}")
    print(f"Hora: {hora}")
#--------------------------------



#StreamLit Code
st.title("Bem vindo a API (CRUD):)")
st.write(f"Agora são: {hora}, Dia:{data}")# Referência da variável.


st.header("Essas sãos as funções")

st.subheader("Usuário:")
st.markdown("[Criar Usuário](http://127.0.0.1:8000/usuarios/criar_usuario)", unsafe_allow_html=True)
st.markdown("[Deletar Usuário](http://127.0.0.1:8000/usuarios/deletar_usuário)", unsafe_allow_html=True)

st.subheader("Pedido:")
st.markdown("[Criar Pedido](http://127.0.0.1:8000/pedido/criar_pedido)", unsafe_allow_html=True)
st.markdown("[Deletar Pedido](http://127.0.0.1:8000/pedido/deletar_pedido)", unsafe_allow_html=True)

st.subheader("Carrinho:")
st.markdown("[Consultar Carrinho Pelo ID do Usuário](http://127.0.0.1:8000/carrinho/consultar_carrinho_por_userId)", unsafe_allow_html=True)
st.markdown("[Salvar Novo Carrinho](http://127.0.0.1:8000/carrinho/consultar_carrinho_por_userId", unsafe_allow_html=True)
st.markdown("[Atualizar Carrinho](http://127.0.0.1:8000/carrinho/atualizar_carrinho)", unsafe_allow_html=True)
st.markdown("[Atualizar Item Carrinho](http://127.0.0.1:8000/carrinho/atualizar_item_carrinho", unsafe_allow_html=True)