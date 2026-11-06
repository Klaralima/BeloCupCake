from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime, timezone

from app.models import Entrega, Pedido
from app.models.usuario import Usuario
from app.schemas.entrega import EntregaAceitaResposta


def listar_entregas_disponiveis(
    sessao: Session,
    limite: int,
    deslocamento: int,
):
    consulta = (
        select(
            Pedido.id.label("pedido_id"),
            Pedido.bairro_nome,
            Pedido.cidade,
            Pedido.uf,
            Pedido.previsao_entrega,
        )
        .outerjoin(
            Entrega,
            Entrega.pedido_id == Pedido.id,
        )
        .where(
            Pedido.status == "PRONTO",
            Entrega.id.is_(None),
        )
        .order_by(Pedido.criado_em, Pedido.id)
        .offset(deslocamento)
        .limit(limite)
    )

    return sessao.execute(consulta).mappings().all()


def aceitar_entrega(
    sessao: Session,
    pedido_id: int,
    entregador_id: int,
) -> EntregaAceitaResposta:
    try:
        consulta = (
            select(Pedido)
            .where(Pedido.id == pedido_id)
            .with_for_update()
        )
        pedido = sessao.scalar(consulta)

        if pedido is None:
            raise HTTPException(
                status_code=404,
                detail="Pedido não encontrado.",
            )

        if pedido.status != "PRONTO":
            raise HTTPException(
                status_code=409,
                detail="O pedido não está disponível para aceite.",
            )

        aceita_em = datetime.now(timezone.utc).replace(
            tzinfo=None,
            microsecond=0,
        )
        entrega = Entrega(
            pedido_id=pedido.id,
            entregador_id=entregador_id,
            aceita_em=aceita_em,
        )
        sessao.add(entrega)
        pedido.status = "ATRIBUIDA"

        resposta = EntregaAceitaResposta(
            pedido_id=pedido.id,
            entregador_id=entregador_id,
            status=pedido.status,
            aceita_em=aceita_em,
        )
        sessao.commit()
        return resposta

    except HTTPException:
        sessao.rollback()
        raise

    except IntegrityError as erro:
        sessao.rollback()
        # No MySQL, 1062 indica violação de uma chave única.
        if erro.orig.args and erro.orig.args[0] == 1062:
            raise HTTPException(
                status_code=409,
                detail="Este pedido já possui uma entrega.",
            ) from erro
        raise

    except SQLAlchemyError:
        sessao.rollback()
        raise