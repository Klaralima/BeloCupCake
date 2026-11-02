from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query

from app.dependencies import exigir_perfis
from app.models.usuario import Usuario
from app.database import obter_sessao
from app.schemas.produto import ProdutoResposta
from app.services.produto import listar_produtos_administracao


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