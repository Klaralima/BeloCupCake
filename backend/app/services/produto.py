from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto import ProdutoCriar


def cadastrar_produto(sessao: Session, dados: ProdutoCriar) -> Produto:
    produto = Produto(
        nome=dados.nome,
        descricao=dados.descricao,
        sabor=dados.sabor,
        tamanho=dados.tamanho,
        preco=dados.preco,
        estoque=dados.estoque,
        imagem_url=(
            str(dados.imagem_url)
            if dados.imagem_url is not None
            else None
        ),
        ativo=True,
    )

    sessao.add(produto)

    try:
        sessao.commit()
    except SQLAlchemyError:
        sessao.rollback()
        raise

    sessao.refresh(produto)
    return produto