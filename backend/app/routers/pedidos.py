from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dependencies import exigir_perfis
from app.models.usuario import Usuario
from app.schemas.pedido import PedidoCriar, PedidoResumoResposta
from app.services.pedido import (
    PedidoInvalidoError,
    criar_pedido,
    listar_pedidos_cliente,
)


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post(
    "",
    response_model=PedidoResumoResposta,
    status_code=status.HTTP_201_CREATED,
)
def finalizar_pedido(
    dados: PedidoCriar,
    usuario: Annotated[
        Usuario,
        Depends(exigir_perfis("CLIENTE")),
    ],
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    try:
        return criar_pedido(
            sessao=sessao,
            cliente_id=usuario.id,
            dados=dados,
        )
    except PedidoInvalidoError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro),
        ) from None

@router.get("", response_model=list[PedidoResumoResposta])
def consultar_meus_pedidos(
    usuario: Annotated[
        Usuario,
        Depends(exigir_perfis("CLIENTE")),
    ],
    sessao: Annotated[Session, Depends(obter_sessao)],
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
    deslocamento: Annotated[int, Query(ge=0)] = 0,
):
    return listar_pedidos_cliente(
        sessao=sessao,
        cliente_id=usuario.id,
        limite=limite,
        deslocamento=deslocamento,
    )