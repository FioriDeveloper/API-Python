from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.data.tabelas.Usuario import Usuario
from app.data.tabelas.Pedido import Pedido, PedidoCreate

router = APIRouter(prefix="/pedido", tags=["Pedido"])

@router.get("/")
async def home_pedido ():
    print("Função A Adicionar Pedido Type /criar_pedido")
    print("Função B")
    print("Função C")

    return {"mensage":"Essas são as funçoes"}

@router.post("/criar_pedido")
async def criar_pedido (pedido: PedidoCreate, db: Session = Depends(get_db)):
    try:
        novo_pedido = Pedido(
        id_usuario = pedido.id_usuario,
        valor_total =  pedido.valor_total,
        endereco = pedido.endereco,
        status_pedido =  pedido.status_pedido


        )
        db.add(novo_pedido)
        db.commit()
        db.refresh(novo_pedido)

        return {"mensagem":"Pedido criado "}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar pedido {str(e)}")

@router.delete("/deletar_pedido/{pedido_id}")
def deletar_pedido(pedido_id:int, db: Session =  Depends(get_db)):
    try:
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido Not Found :(")
        db.delete(pedido)
        db.commit()
        return {"mensage":"Pedido deletado :)"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar pedido {str(e)}")



