from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.schemas.bairro import BairroDisponivelResposta
from app.services.bairro import listar_bairros_disponiveis


router = APIRouter(
    prefix="/bairros",
    tags=["Bairros atendidos"],
)


@router.get("", response_model=list[BairroDisponivelResposta])
def consultar_bairros_atendidos(
    sessao: Annotated[Session, Depends(obter_sessao)],
    limite: Annotated[int, Query(ge=1, le=200)] = 100,
    deslocamento: Annotated[int, Query(ge=0)] = 0,
):
    return listar_bairros_disponiveis(
        sessao=sessao,
        limite=limite,
        deslocamento=deslocamento,
    )