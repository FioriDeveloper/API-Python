from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.data.tabelas.ItemCarrinho import  ItemCarrinho, ItemCarrinhoCreate
from app.data.tabelas.Carrinho import Carrinho, CarrinhoCreate
from sqlalchemy.orm import Session


router = APIRouter(prefix="/carrinho", tags=["Carrinho"])

@router.get("/consultar_carrinho_por_userId")
async def pegar_carrinho_por_userId(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    try:
        # consultando o carrinho do usuario
        carrinho = db.query(Carrinho).filter(Carrinho.id_usuario == id_usuario).first()

        if not carrinho:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado para este usuário")

        # calculando o valor total do carrinho, somando o valor dos itens
        valor_total = sum(item.preco * item.quantidade for item in carrinho.itens)

        return {
            "id": carrinho.id,
            "id_usuario": carrinho.id_usuario,
            "valor_total": valor_total,
            "itens": [
                {
                "id_produto": item.id_produto,
                "quantidade": item.quantidade,
                "preco": item.preco,
                "total_item": item.preco * item.quantidade
                }
                for item in carrinho.itens
            ]
        }


    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao pegar carrinho do usuário: {str(e)}")


@router.post("/salvar_novo_carrinho")
async def salvar_novo_carrinho(
    carrinho_create: CarrinhoCreate, # Dados do carrinho
    itens_create: list[ItemCarrinhoCreate], # itens do carrinho
    db: Session = Depends(get_db)):
    try:
        # criando o carrinho
        carrinho = Carrinho(
            id_usuario = carrinho_create.id_usuario,
            valor_total = carrinho_create.valor_total
        )
        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)

        # Adicionando os itens no carrinho
        for item in itens_create:
            item_carrinho = ItemCarrinho(
                id_carrinho = carrinho.id,
                id_usuario = item.id_usuario,
                id_produto = item.id_produto,
                quantidade = item.quantidade,
                preco = item.preco

            )
            db.add(item_carrinho)
        
        db.commit()

        # Calculando o valor total do carrinho após salvar os itens
        valor_total_calculado = sum(
            item.preco * item.quantidade for item in itens_create
        )

        # Atualizando o valor total do carrinho no banco
        carrinho.valor_total = Decimal(valor_total_calculado)
        db.commit()

        # retorna o carrinho
        return {
            "id": carrinho.id,
            "id_usuario": carrinho.id_usuario,
            "valor_total": carrinho.valor_total,
            "itens": [
                {
                    "id_produto": item.id_produto,
                    "quantidade": item.quantidade,
                    "preco": item.preco,
                    "total_item": item.preco * item.quantidade
                }
                for item in itens_create
            ]
        }



    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar novo carrinho: {str(e)}")

@router.put("/atualizar_carrinho")
async def atualizar_carrinho(

    carrinho_update: CarrinhoCreate,  # Dados do carrinho a serem atualizados
    db: Session = Depends(get_db)
):
    try:
        # Atualizando o carrinho (id_usuario, valor_total)
        carrinho = db.query(Carrinho).filter(Carrinho.id == carrinho_update.id_usuario).first()

        if not carrinho:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")

        carrinho.id_usuario = carrinho_update.id_usuario
        carrinho.valor_total = carrinho_update.valor_total
        db.commit()
        db.refresh(carrinho)

        return {
            "id": carrinho.id,
            "id_usuario": carrinho.id_usuario,
            "valor_total": carrinho.valor_total,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar carrinho: {str(e)}")



@router.put("/atualizar_item_carrinho")
async def atualizar_item_carrinho(
    item_update: ItemCarrinhoCreate,  # Dados do item a ser atualizado
    db: Session = Depends(get_db)
):
    try:
        # Encontrar o item no carrinho
        item_carrinho = db.query(ItemCarrinho).filter(
            ItemCarrinho.id_carrinho == item_update.id_carrinho,
            ItemCarrinho.id_produto == item_update.id_produto
        ).first()

        if not item_carrinho:
            raise HTTPException(status_code=404, detail="Item não encontrado")

        # Atualizando o item
        item_carrinho.quantidade = item_update.quantidade
        item_carrinho.preco = item_update.preco
        db.commit()

        # Recalcular o valor total do carrinho
        carrinho = db.query(Carrinho).filter(Carrinho.id == item_carrinho.id_carrinho).first()
        valor_total_calculado = sum(
            item.preco * item.quantidade for item in carrinho.itens
        )
        carrinho.valor_total = Decimal(valor_total_calculado)
        db.commit()

        return {
            "id_produto": item_carrinho.id_produto,
            "quantidade": item_carrinho.quantidade,
            "preco": item_carrinho.preco,
            "total_item": item_carrinho.preco * item_carrinho.quantidade
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar item do carrinho: {str(e)}")