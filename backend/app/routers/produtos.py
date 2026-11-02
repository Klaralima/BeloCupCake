from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dependencies import exigir_perfis
from app.schemas.produto import (
    ProdutoAtualizar,
    ProdutoCriar,
    ProdutoResposta,
)
from app.services.produto import (
    atualizar_produto,
    buscar_produto_disponivel,
    cadastrar_produto,
    listar_produtos_disponiveis,
)


router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post(
    "",
    response_model=ProdutoResposta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(exigir_perfis("ADMINISTRADOR"))],
)
def criar_produto(
    dados: ProdutoCriar,
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    return cadastrar_produto(sessao, dados)

    
@router.get("", response_model=list[ProdutoResposta])
def listar_produtos(
    sessao: Annotated[Session, Depends(obter_sessao)],
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
    deslocamento: Annotated[int, Query(ge=0)] = 0,
):
    return listar_produtos_disponiveis(
        sessao=sessao,
        limite=limite,
        deslocamento=deslocamento,
    )

@router.get("/{produto_id}", response_model=ProdutoResposta)
def consultar_produto(
    produto_id: Annotated[
        int,
        Path(ge=1, le=18446744073709551615),
    ],
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    produto = buscar_produto_disponivel(sessao, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou indisponível.",
        )

    return produto

@router.patch(
    "/{produto_id}",
    response_model=ProdutoResposta,
    dependencies=[Depends(exigir_perfis("ADMINISTRADOR"))],
)
def editar_produto(
    produto_id: Annotated[
        int,
        Path(ge=1, le=18446744073709551615),
    ],
    dados: ProdutoAtualizar,
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    produto = atualizar_produto(sessao, produto_id, dados)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    return produto