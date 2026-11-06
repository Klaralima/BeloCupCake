from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dependencies import exigir_perfis, obter_usuario_atual
from app.models.usuario import Usuario
from app.schemas.entrega import EntregaDisponivelResposta, EntregaAceitaResposta, EntregaIniciadaResposta
from app.services.entrega import listar_entregas_disponiveis, aceitar_entrega, iniciar_entrega


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

@router.post(
    "/{pedido_id}/aceitar",
    response_model=EntregaAceitaResposta,
    status_code=201,
)
def aceitar_entrega_do_pedido(
    pedido_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return aceitar_entrega(
        sessao=sessao,
        pedido_id=pedido_id,
        entregador_id=usuario_atual.id,
    )

@router.post(
    "/{pedido_id}/iniciar",
    response_model=EntregaIniciadaResposta,
    status_code=200,
)
def iniciar_entrega_do_pedido(
    pedido_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return iniciar_entrega(
        sessao=sessao,
        pedido_id=pedido_id,
        entregador_id=usuario_atual.id,
    )