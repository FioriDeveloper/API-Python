from decimal import Decimal
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Numeric, ForeignKey
from pydantic import BaseModel
from app.database import Base


class Carrinho(Base):
    __tablename__ = "carrinhos"

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)

    # Relacionamento com os itens do carrinho (ItensCarrinho)
    itens = relationship("ItemCarrinho", back_populates="carrinho")

    # Relacionamento com o usuário
    usuario = relationship("Usuario", back_populates="carrinhos")

# classe que lida melhor com as respostas da requisição http
class CarrinhoCreate(BaseModel):
    id_usuario: int
    valor_total: Decimal


    class Config:
        orm_mode = True

