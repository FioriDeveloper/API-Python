from app.database import SessionLocal
from app.router.userfuncao import criar_usuario

# Criando uma sessão manualmente
db = SessionLocal()

# Chamando a função
novo_usuario = criar_usuario(db, "João Silva", "joao@email.com", "senha123","teste")

print(novo_usuario)
db.close()  # Fechando a conexão após o uso
