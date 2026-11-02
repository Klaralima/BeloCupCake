from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dependencies import exigir_perfis
from app.schemas.produto import ProdutoCriar, ProdutoResposta
from app.services.produto import cadastrar_produto


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