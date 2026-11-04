from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Entrega, Pedido


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