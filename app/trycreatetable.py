from app.database import engine
from app.data.tabelas.Pedido import Base  # Certifique-se de importar a classe Base

# Criar todas as tabelas no banco
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
