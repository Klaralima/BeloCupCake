from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.schemas.autenticacao import LoginEntrada, TokenResposta
from app.services.autenticacao import (
    TOKEN_DURACAO_SEGUNDOS,
    CredenciaisInvalidasError,
    autenticar_usuario,
    criar_token_acesso,
)


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResposta)
def realizar_login(
    dados: LoginEntrada,
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    try:
        usuario = autenticar_usuario(
            sessao,
            str(dados.email),
            dados.senha,
        )
    except CredenciaisInvalidasError:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    return TokenResposta(
        access_token=criar_token_acesso(usuario.id),
        expires_in=TOKEN_DURACAO_SEGUNDOS,
    )