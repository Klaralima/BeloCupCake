from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCriar


password_hash = PasswordHash.recommended()


class EmailJaCadastradoError(Exception):
    pass


def cadastrar_cliente(sessao: Session, dados: UsuarioCriar) -> Usuario:
    existente = sessao.scalar(
        select(Usuario.id).where(Usuario.email == str(dados.email))
    )

    if existente is not None:
        raise EmailJaCadastradoError()

    usuario = Usuario(
        nome=dados.nome,
        email=str(dados.email),
        telefone=dados.telefone,
        senha_hash=password_hash.hash(dados.senha),
        perfil="CLIENTE",
        ativo=True,
    )

    sessao.add(usuario)

    try:
        sessao.commit()
    except IntegrityError as erro:
        sessao.rollback()

        if erro.orig.args and erro.orig.args[0] == 1062:
            raise EmailJaCadastradoError() from erro

        raise

    sessao.refresh(usuario)
    return usuario