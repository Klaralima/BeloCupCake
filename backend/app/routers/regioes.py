from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dependencies import exigir_perfis
from app.schemas.regiao_entrega import (
    RegiaoEntregaCriar,
    RegiaoEntregaResposta,
)
from app.services.regiao_entrega import cadastrar_regiao


router = APIRouter(
    prefix="/admin/regioes",
    tags=["Regiões de entrega"],
    dependencies=[Depends(exigir_perfis("ADMINISTRADOR"))],
)


@router.post(
    "",
    response_model=RegiaoEntregaResposta,
    status_code=status.HTTP_201_CREATED,
)
def criar_regiao(
    dados: RegiaoEntregaCriar,
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    return cadastrar_regiao(sessao, dados)