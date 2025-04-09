from app.database import engine, Base
from fastapi import FastAPI
from app.router import rotas_produto, rotas_carrinho, rotas_pagamento, userfuncao, pedidofuncao

# 🔴 Inicializa o FastAPI ANTES de incluir as rotas
app = FastAPI()

# 🔵 Incluindo as rotas na aplicação
app.include_router(rotas_produto.router)
app.include_router(rotas_carrinho.router)
app.include_router(rotas_pagamento.router)
app.include_router(userfuncao.router)
app.include_router(pedidofuncao.router)

# 🔵 Cria as tabelas no banco de dados (se não existirem)
def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

@app.get("/")
def home():
    return {"Seja Bem-vindo à API"}
