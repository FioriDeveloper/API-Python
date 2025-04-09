import  streamlit as st
import  webbrowser
#from timetest import data, hora #Import da API de hora e data.
import requests
import time

#API DATA E HORA
api_url = "https://timeapi.io/api/Time/current/ip?ipAddress=187.255.99.16"

response = requests.get(api_url)

if response.status_code == 200:
    dados = response.json()

    data = dados["date"]
    hora = dados["time"]

    print(f"Data: {data}")
    print(f"Hora: {hora}")

#--------------------------------



#StreamLit Code
st.title("Bem vindo a API :)")
st.write(f"Agora são: {hora}, Dia:{data}")# Referência da variável.

if st.button("Função Adicionar Usuário"):
    st.markdown("[Clique aqui para acessar](https://www.google.com)")



st.write("Função de Produtos: \n dd")

