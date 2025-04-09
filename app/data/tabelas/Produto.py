from decimal import Decimal

from sqlalchemy import Column, Integer, String, Numeric
from pydantic import BaseModel, ConfigDict
from app.database import Base

from typing import Optional



#Definição das colunas da tabela de Produtos
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer,primary_key=True)
    nome = Column(String, index=True, nullable=False)
    descricao = Column(String)

    categoria = Column (String, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    qnt_estoque = Column(Integer, nullable=False, default= 0)



# classe que lida melhor com as respostas da requisição http
class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None

    categoria: str
    preco: Decimal
    qnt_estoque: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


