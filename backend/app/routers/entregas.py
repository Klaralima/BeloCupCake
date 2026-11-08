from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dependencies import exigir_perfis, obter_usuario_atual
from app.models.usuario import Usuario
from app.schemas.pedido import PedidoDetalheResposta
from app.services.pedido import buscar_pedido_entregador
from app.schemas.entrega import EntregaDisponivelResposta, EntregaAceitaResposta, EntregaIniciadaResposta, EntregaConcluidaResposta, MinhaEntregaResposta
from app.services.entrega import listar_entregas_disponiveis, aceitar_entrega, iniciar_entrega, concluir_entrega, listar_minhas_entregas


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

@router.post(
    "/{pedido_id}/concluir",
    response_model=EntregaConcluidaResposta,
    status_code=200,
)
def concluir_entrega_do_pedido(
    pedido_id: int,
    sessao: Session = Depends(obter_sessao),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return concluir_entrega(
        sessao=sessao,
        pedido_id=pedido_id,
        entregador_id=usuario_atual.id,
    )

@router.get(
    "/minhas",
    response_model=list[MinhaEntregaResposta],
)
def consultar_minhas_entregas(
    sessao: Session = Depends(obter_sessao),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    status: Literal["ATRIBUIDA", "EM_ROTA", "ENTREGUE"] | None = Query(
        default=None,
    ),
    limite: int = Query(default=20, ge=1, le=100),
    deslocamento: int = Query(default=0, ge=0),
):
    return listar_minhas_entregas(
        sessao=sessao,
        entregador_id=usuario_atual.id,
        status=status,
        limite=limite,
        deslocamento=deslocamento,
    )


@router.get("/{pedido_id}", response_model=PedidoDetalheResposta)
def consultar_detalhes_entrega(
    pedido_id: Annotated[int, Path(ge=1)],
    sessao: Session = Depends(obter_sessao),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    pedido = buscar_pedido_entregador(sessao, pedido_id, usuario_atual.id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Entrega não encontrada para sua conta.")
    return pedido
