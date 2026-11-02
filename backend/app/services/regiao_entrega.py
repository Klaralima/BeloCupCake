from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.regiao_entrega import RegiaoEntrega
from app.schemas.regiao_entrega import RegiaoEntregaCriar


def cadastrar_regiao(
    sessao: Session,
    dados: RegiaoEntregaCriar,
) -> RegiaoEntrega:
    regiao = RegiaoEntrega(
        nome=dados.nome,
        taxa=dados.taxa,
        prazo_minutos=dados.prazo_minutos,
        ativo=True,
    )

    sessao.add(regiao)

    try:
        sessao.commit()
    except SQLAlchemyError:
        sessao.rollback()
        raise

    sessao.refresh(regiao)
    return regiao