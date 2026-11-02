from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.models.usuario import Usuario
from app.services.autenticacao import JWT_ALGORITHM, JWT_SECRET_KEY


bearer = HTTPBearer(auto_error=False)


def obter_usuario_atual(
    credenciais: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer),
    ],
    sessao: Annotated[Session, Depends(obter_sessao)],
) -> Usuario:
    erro_autenticacao = HTTPException(
        status_code=401,
        detail="Não foi possível autenticar. Faça login novamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credenciais is None:
        raise erro_autenticacao

    try:
        dados_token = jwt.decode(
            credenciais.credentials,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["sub", "exp", "iat"]},
        )

        usuario_id = int(dados_token["sub"])

        if not 1 <= usuario_id <= 18446744073709551615:
            raise ValueError("Identificador fora do intervalo permitido.")

    except (InvalidTokenError, ValueError, TypeError):
        raise erro_autenticacao from None

    usuario = sessao.get(Usuario, usuario_id)

    if usuario is None or not usuario.ativo:
        raise erro_autenticacao

    return usuario

def exigir_perfis(*perfis_permitidos: str):
    def verificar_perfil(
        usuario: Annotated[Usuario, Depends(obter_usuario_atual)],
    ) -> Usuario:
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=403,
                detail="Seu perfil não tem permissão para esta operação.",
            )

        return usuario

    return verificar_perfil