from sqlalchemy.orm import Session
from app.data.tabelas.Produto import Produto, ProdutoCreate
from fastapi import Depends, HTTPException, APIRouter
from app.database import get_db

router = APIRouter()


@router.post("/adicionar_novo_produto/", response_model=ProdutoCreate)
async def criar_produto(
        #aqui colocamos os parâmetros que queremos quando a função for executada 
        produto: ProdutoCreate,
        db: Session = Depends(get_db) 
 
):
    try:
        novo_produto = Produto(
            nome=produto.nome, descricao=produto.descricao , categoria=produto.categoria, qnt_estoque= produto.qnt_estoque, preco=produto.preco
            #aqui são parâmetros para que a variavel (novo produto) leve a informação até a classe Produto que esta em modelo.py
        )    
        db.add(novo_produto) #executa a função e add novo produto..
        db.commit() #salva as alterações 
        db.refresh(novo_produto) #atualiza os dados do novo (novo produto) 
        return novo_produto
    except Exception as e:
        db.rollback() #se der erro, desfaz a transação para evitar inconsistências
        raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {str(e)}")


@router.put("/atualizar_produto/{id}", response_model=ProdutoCreate)
async def atualizar_produto(
    id: int,
    produto: ProdutoCreate,
    db: Session = Depends(get_db)):
    try:
        # buscar produto existente pelo ID
        produto_existente = db.query(Produto).filter(Produto.id == id).first()

        if not produto_existente:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        # atualizar os dados do produto com os dados fornecidos
        produto_existente.nome = produto.nome
        produto_existente.descricao = produto.descricao
        produto_existente.categoria = produto.categoria
        produto_existente.preco = produto.preco
        produto_existente.qnt_estoque = produto.qnt_estoque

        # commit para salvar as mudanças no banco de dados
        db.commit()
        db.refresh(produto_existente) # atualiza os dados do produto

        return produto_existente
        

    except Exception as e:
        db.rollback() # Desfaz qualquer alteração se ocorrer erro
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto: {str(e)}")


@router.delete("/deletar_produto/{id}")
async def deletar_produto(
    id: int,
    db: Session = Depends(get_db)):
    try:
        #buscar o produto existente pelo ID
        produto_existente = db.query(Produto).filter(Produto.id == id).first()

        if not produto_existente:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        # deletar o produto
        db.delete(produto_existente)

        # commit para salvar as mudanças no banco de dados
        db.commit()

        return{"message": f"Produto com ID {id} foi deletado com sucesso!"}

    except Exception as e:
        db.rollback() # Desfaz qualquer alteração se ocorrer erro
        raise HTTPException(status_code=500, detail=f"Erro ao deletar produto: {str(e)}")


@router.get("/pegar_produto_por_id/{id}", response_model=ProdutoCreate)
async def pegar_produto_por_id(
    id: int,
    db: Session = Depends(get_db)):
    try:
        # buscar produto pelo id
        produto = db.query(Produto).filter(Produto.id == id).first()

        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        return produto
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")


@router.get("/pegar_produtos/", response_model=list[ProdutoCreate])
async def pegar_produtos(db: Session = Depends(get_db)):
    try:
        # Buscar todos os produtos
        produtos = db.query(Produto).all()

        return produtos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produtos: {str(e)}")


        