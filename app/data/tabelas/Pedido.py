from decimal import Decimal
from multiprocessing.connection import arbitrary_address
from turtle import config_dict

from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, DateTime, func
from pydantic import BaseModel, ConfigDict, Field
from app.data.tabelas.Usuario import Usuario
from app.data.tabelas.ItensPedido import ItensPedido
from app.database import Base




class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    endereco = Column(String, nullable=False)
    status_pedido = Column(String, nullable=False)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = Column(DateTime, nullable=True)

    # relacionamentos para acessar os dados dos usuarios e os itens do 
    # pedido
    usuario = relationship("Usuario", backref="pedidos")
    itens = relationship("ItensPedido", back_populates="pedido")
    pagamento = relationship("Pagamento", back_populates="pedido")



    model_config =  ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

# classe que lida melhor com as respostas da requisição http
class PedidoCreate(BaseModel):
    id_usuario: int
    valor_total: Decimal
    endereco: str
    status_pedido: str
    criado_em: datetime = Field(default_factory=datetime.utcnow)
    atualizado_em: datetime = None

    #Responsável por fazer o Pydantic permitir o uso do DateTime, no caso usamos o datetime do Python não do SQL
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)







