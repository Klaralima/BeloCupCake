from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.dependencies import exigir_perfis
from app.models.usuario import Usuario
from app.database import obter_sessao
from app.schemas.produto import ProdutoResposta
from app.services.produto import listar_produtos_administracao
from app.schemas.pedido import (
    PedidoDetalheResposta,
    PedidoResumoResposta,
    PedidoStatusAtualizar,
    StatusPedido,
)
from app.services.pedido import (
    PedidoNaoEncontradoError,
    TransicaoPedidoInvalidaError,
    atualizar_status_preparo,
    buscar_pedido_administracao,
    listar_pedidos_administracao,
    CancelamentoPedidoInvalidoError,
    cancelar_pedido,    
)


router = APIRouter(
    prefix="/admin",
    tags=["Administração"],
)


@router.get("/verificar-acesso")
def verificar_acesso_administrativo(
    usuario: Annotated[
        Usuario,
        Depends(exigir_perfis("ADMINISTRADOR")),
    ],
):
    return {
        "mensagem": "Acesso administrativo autorizado.",
        "usuario_id": usuario.id,
        "perfil": usuario.perfil,
    }

@router.get(
    "/produtos",
    response_model=list[ProdutoResposta],
    dependencies=[Depends(exigir_perfis("ADMINISTRADOR"))],
)
def listar_produtos_admin(
    sessao: Annotated[Session, Depends(obter_sessao)],
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
    deslocamento: Annotated[int, Query(ge=0)] = 0,
):
    return listar_produtos_administracao(
        sessao=sessao,
        limite=limite,
        deslocamento=deslocamento,
    )

@router.get(
    "/pedidos",
    response_model=list[PedidoResumoResposta],
    dependencies=[Depends(exigir_perfis("ADMINISTRADOR"))],
)
def consultar_pedidos_admin(
    sessao: Annotated[Session, Depends(obter_sessao)],
    status_pedido: Annotated[
        StatusPedido | None,
        Query(alias="status"),
    ] = None,
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
    deslocamento: Annotated[int, Query(ge=0)] = 0,
):
    return listar_pedidos_administracao(
        sessao=sessao,
        status_pedido=status_pedido,
        limite=limite,
        deslocamento=deslocamento,
    )

@router.get(
    "/pedidos/{pedido_id}",
    response_model=PedidoDetalheResposta,
    dependencies=[Depends(exigir_perfis("ADMINISTRADOR"))],
)
def consultar_pedido_admin(
    pedido_id: Annotated[
        int,
        Path(ge=1, le=18446744073709551615),
    ],
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    pedido = buscar_pedido_administracao(
        sessao=sessao,
        pedido_id=pedido_id,
    )

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado.",
        )

    return pedido

@router.patch(
    "/pedidos/{pedido_id}/status",
    response_model=PedidoResumoResposta,
    dependencies=[Depends(exigir_perfis("ADMINISTRADOR"))],
)
def alterar_status_preparo(
    pedido_id: Annotated[
        int,
        Path(ge=1, le=18446744073709551615),
    ],
    dados: PedidoStatusAtualizar,
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    try:
        return atualizar_status_preparo(
            sessao=sessao,
            pedido_id=pedido_id,
            novo_status=dados.status,
        )

    except PedidoNaoEncontradoError:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado.",
        ) from None

    except TransicaoPedidoInvalidaError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro),
        ) from None

@router.post(
    "/pedidos/{pedido_id}/cancelar",
    response_model=PedidoResumoResposta,
    dependencies=[Depends(exigir_perfis("ADMINISTRADOR"))],
)
def cancelar_pedido_admin(
    pedido_id: Annotated[
        int,
        Path(ge=1, le=18446744073709551615),
    ],
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    try:
        return cancelar_pedido(
            sessao=sessao,
            pedido_id=pedido_id,
        )

    except PedidoNaoEncontradoError:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado.",
        ) from None

    except CancelamentoPedidoInvalidoError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro),
        ) from None