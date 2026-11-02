from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.schemas.usuario import UsuarioCriar, UsuarioResposta
from app.services.usuario import (
    EmailJaCadastradoError,
    cadastrar_cliente,
)


router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post(
    "",
    response_model=UsuarioResposta,
    status_code=status.HTTP_201_CREATED,
)
def criar_usuario(
    dados: UsuarioCriar,
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    try:
        return cadastrar_cliente(sessao, dados)
    except EmailJaCadastradoError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        ) from None