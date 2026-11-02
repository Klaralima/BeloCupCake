from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import exigir_perfis
from app.models.usuario import Usuario


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