from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dependencies import exigir_perfis
from app.schemas.entrega import EntregaDisponivelResposta
from app.services.entrega import listar_entregas_disponiveis


router = APIRouter(
    prefix="/entregas",
    tags=["Entregas"],
    dependencies=[Depends(exigir_perfis("ENTREGADOR"))],
)


@router.get(
    "/disponiveis",
    response_model=list[EntregaDisponivelResposta],
)
def consultar_entregas_disponiveis(
    sessao: Annotated[Session, Depends(obter_sessao)],
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
    deslocamento: Annotated[int, Query(ge=0)] = 0,
):
    return listar_entregas_disponiveis(
        sessao=sessao,
        limite=limite,
        deslocamento=deslocamento,
    )