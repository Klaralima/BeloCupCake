import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.services.usuario import password_hash


load_dotenv(
    Path(__file__).resolve().parents[2] / ".env",
    interpolate=False,
)

JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_ALGORITHM = "HS256"
TOKEN_DURACAO_SEGUNDOS = 30 * 60

if len(JWT_SECRET_KEY.encode("utf-8")) < 32:
    raise ValueError("Configure uma chave JWT com pelo menos 32 bytes.")

HASH_FICTICIO = password_hash.hash("senha-ficticia-para-verificacao")


class CredenciaisInvalidasError(Exception):
    pass


def autenticar_usuario(
    sessao: Session,
    email: str,
    senha: str,
) -> Usuario:
    usuario = sessao.scalar(
        select(Usuario).where(Usuario.email == email)
    )

    hash_armazenado = (
        usuario.senha_hash if usuario is not None else HASH_FICTICIO
    )
    senha_valida = password_hash.verify(senha, hash_armazenado)

    if usuario is None or not senha_valida or not usuario.ativo:
        raise CredenciaisInvalidasError()

    return usuario


def criar_token_acesso(usuario_id: int) -> str:
    agora = datetime.now(timezone.utc)

    dados_token = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(seconds=TOKEN_DURACAO_SEGUNDOS),
    }

    return jwt.encode(
        dados_token,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )