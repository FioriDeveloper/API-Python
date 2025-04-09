from decimal import Decimal
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Numeric
from pydantic import BaseModel, ConfigDict
from app.database import Base




# tabela que representa os produtos que vão
# dentro do carrinho
class ItemCarrinho(Base):
    __tablename__ = "itens_carrinho"

    id = Column(Integer, primary_key=True)
    id_carrinho = Column(Integer, ForeignKey('carrinhos.id'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_produto = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)

    # Relacionamento com o produto
    produto = relationship("Produto", backref="itens_carrinho")

    # Relacionamento com o carrinho
    carrinho = relationship("Carrinho", back_populates="itens")

class ItemCarrinhoCreate(BaseModel):
    id_usuario: int
    id_carrinho: int
    id_produto: int
    quantidade: int
    preco: Decimal

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)