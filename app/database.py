from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#URL do banco de dados, provavelmente usaremos o SQL LITE
SQLALCHEMY_DATABASE_URL = "sqlite:///./tabela.db"

#Criando a instância global de Base
Base = declarative_base()

#Cria o mecanismo para fazer a conexão com o banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

