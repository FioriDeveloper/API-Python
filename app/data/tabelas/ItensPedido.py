from decimal import Decimal
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Numeric
from pydantic import BaseModel, ConfigDict
from app.database import Base



# Tabela que representa os produtos que vão
# dentro do pedido
class ItensPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    id_produto = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

    produto = relationship("Produto", backref="itens_pedido")  # Relacionamento com a tabela Produto
    pedido = relationship("Pedido", back_populates="itens")  # Relacionamento com a tabela Pedido


class ItensPedidoCreate(BaseModel):
    id_pedido: int
    id_produto: int
    quantidade: int
    preco_unitario: Decimal

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
