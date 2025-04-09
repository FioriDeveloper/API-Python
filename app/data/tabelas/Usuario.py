from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict
from app.database import Base




# Tabela que representa os Usuários
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement= True, index = True )
    nome = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    endereco = Column(String, nullable=False)
    senha = Column(String, nullable=False)

    #Relacionamento com os carrinho. 
    # Todo usuario tem um carrinho
    carrinhos = relationship("Carrinho", back_populates="usuario")

    
     

    

    def __init__ (self, nome,email, endereco, senha):
        self.nome = nome 
        self.email = email
        self.endereco = endereco
        self.senha = senha
        
        

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    endereco: str
    senha : str

    model_config = ConfigDict(from_attributes=True)



