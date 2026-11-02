from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.dependencies import exigir_perfis
from app.schemas.bairro import BairroCriar, BairroResposta
from app.services.bairro import (
    BairroJaCadastradoError,
    RegiaoInativaError,
    RegiaoNaoEncontradaError,
    cadastrar_bairro,
)


router = APIRouter(
    prefix="/admin/bairros",
    tags=["Bairros"],
    dependencies=[Depends(exigir_perfis("ADMINISTRADOR"))],
)


@router.post(
    "",
    response_model=BairroResposta,
    status_code=status.HTTP_201_CREATED,
)
def criar_bairro(
    dados: BairroCriar,
    sessao: Annotated[Session, Depends(obter_sessao)],
):
    try:
        return cadastrar_bairro(sessao, dados)
    except RegiaoNaoEncontradaError:
        raise HTTPException(
            status_code=404,
            detail="Região de entrega não encontrada.",
        ) from None
    except RegiaoInativaError:
        raise HTTPException(
            status_code=409,
            detail="Não é possível cadastrar um bairro em uma região inativa.",
        ) from None
    except BairroJaCadastradoError:
        raise HTTPException(
            status_code=409,
            detail="Bairro já cadastrado nessa cidade e UF.",
        ) from None