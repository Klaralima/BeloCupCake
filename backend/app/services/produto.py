from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select

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

def listar_produtos_disponiveis(
    sessao: Session,
    limite: int,
    deslocamento: int,
) -> list[Produto]:
    consulta = (
        select(Produto)
        .where(
            Produto.ativo.is_(True),
            Produto.estoque > 0,
        )
        .order_by(Produto.id)
        .offset(deslocamento)
        .limit(limite)
    )

    return list(sessao.scalars(consulta).all())

def buscar_produto_disponivel(
    sessao: Session,
    produto_id: int,
) -> Produto | None:
    consulta = select(Produto).where(
        Produto.id == produto_id,
        Produto.ativo.is_(True),
        Produto.estoque > 0,
    )

    return sessao.scalar(consulta)