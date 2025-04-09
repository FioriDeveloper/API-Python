from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from decimal import Decimal
from sqlalchemy.orm import Session
from app.data.tabelas.Pagamento import PagamentoCreate, Pagamento
from app.data.tabelas.Pedido import Pedido, PedidoCreate


router = APIRouter()

@router.get("/obter_pagamento_por_id/{id}", response_model=PagamentoCreate)
async def obter_pagamento_por_id(
    id: int,
    db: Session = Depends(get_db)):
    try:
        # Buscar pagamento pelo ID
        pagamento = db.query(Pagamento).filter(Pagamento.id == id).first()

        if not pagamento:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")

        # Retornar os dados do pagamento encontrado
        return PagamentoCreate(
            id_pedido = pagamento.id_pedido,
            id_usuario = pagamento.id_usuario,
            valor = pagamento.valor,
            metodo_pagamento = pagamento.metodo_pagamento,
            criado_em = pagamento.criado_em
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter pagamento: {str(e)}")

        

@router.post("/adicionar_novo_pagamento")
async def adicionar_novo_pagamento(
    pagamento_create: PagamentoCreate, 
    db: Session = Depends(get_db)
):
    try:
        # Verificar se o pedido existe
        pedido = db.query(Pedido).filter(Pedido.id == pagamento_create.id_pedido).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        # Criar pagamento
        novo_pagamento = Pagamento(
            id_pedido=pagamento_create.id_pedido,
            id_usuario=pagamento_create.id_usuario,
            valor=Decimal(pagamento_create.valor),
            metodo_pagamento=pagamento_create.metodo_pagamento,
            criado_em=datetime.now()
        )

        db.add(novo_pagamento)
        db.commit()
        db.refresh(novo_pagamento)

        return {
            "id": novo_pagamento.id,
            "id_pedido": novo_pagamento.id_pedido,
            "id_usuario": novo_pagamento.id_usuario,
            "valor": novo_pagamento.valor,
            "metodo_pagamento": novo_pagamento.metodo_pagamento,
            "criado_em": novo_pagamento.criado_em
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar pagamento: {str(e)}")
