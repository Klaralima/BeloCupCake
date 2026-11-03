from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.bairro import Bairro
from app.models.regiao_entrega import RegiaoEntrega
from app.schemas.bairro import BairroCriar


class RegiaoNaoEncontradaError(Exception):
    pass


class RegiaoInativaError(Exception):
    pass


class BairroJaCadastradoError(Exception):
    pass


def cadastrar_bairro(sessao: Session, dados: BairroCriar) -> Bairro:
    regiao = sessao.scalar(
        select(RegiaoEntrega)
        .where(RegiaoEntrega.id == dados.regiao_entrega_id)
        .with_for_update()
    )

    if regiao is None:
        raise RegiaoNaoEncontradaError()

    if not regiao.ativo:
        raise RegiaoInativaError()

    bairro = Bairro(
        regiao_entrega_id=regiao.id,
        nome=dados.nome,
        cidade=dados.cidade,
        uf=dados.uf,
        ativo=True,
    )

    sessao.add(bairro)

    try:
        sessao.commit()
    except IntegrityError as erro:
        sessao.rollback()

        if erro.orig.args and erro.orig.args[0] == 1062:
            raise BairroJaCadastradoError() from erro

        raise
    except SQLAlchemyError:
        sessao.rollback()
        raise

    sessao.refresh(bairro)
    return bairro

def listar_bairros_disponiveis(
    sessao: Session,
    limite: int,
    deslocamento: int,
):
    consulta = (
        select(
            Bairro.id,
            Bairro.nome,
            Bairro.cidade,
            Bairro.uf,
            RegiaoEntrega.taxa.label("taxa_entrega"),
            RegiaoEntrega.prazo_minutos,
        )
        .join(
            RegiaoEntrega,
            RegiaoEntrega.id == Bairro.regiao_entrega_id,
        )
        .where(
            Bairro.ativo.is_(True),
            RegiaoEntrega.ativo.is_(True),
        )
        .order_by(Bairro.cidade, Bairro.nome, Bairro.id)
        .offset(deslocamento)
        .limit(limite)
    )

    return sessao.execute(consulta).mappings().all()