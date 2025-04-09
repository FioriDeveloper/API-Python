
from fastapi import  APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from app.data.tabelas.Usuario import Usuario, UsuarioCreate
from sqlalchemy.orm import Session
from app.database import get_db
from app.router.rotas_produto import router

router = APIRouter(prefix="/usuario", tags=["Usuarios"])
class UsuarioResponse(BaseModel):
    id: int
    nome : str
    email : str

    class Config:
        from_attributes = True


@router.post("/criar_usuario", response_model= UsuarioCreate)
async def criar_usuario(usuario: UsuarioCreate,db: Session = Depends(get_db)):
    try:
    # Criando o novo usuário
        criando_novo_usuario = Usuario(
            nome= usuario.nome,
            email= usuario.email,
            senha= usuario.senha,  # deve ser armazenada de forma segura (criptografada)
            endereco= usuario.endereco
        )
        def user_mensagem():
              print("Usuário criado")
        db.add(criando_novo_usuario)# Adicionando o novo usuário à sessão

        # Efetivando a transação (salvando no banco)
        db.commit()

        # Atualizando o objeto para refletir as modificações (como o ID atribuído pelo banco)
        db.refresh(criando_novo_usuario)

        return criando_novo_usuario, user_mensagem()  # Retornando o usuário recém-criado
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

@router.delete("/deletar_usuario/{usuario_id}")
def deletar_usuario(usuario_id:int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")

        db.delete(usuario)

        # Efetivando a transação
        db.commit()

        return {"Usuario deletado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code= 500, detail=f"Erro ao deletar user {str(e)}")