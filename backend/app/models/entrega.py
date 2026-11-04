from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Entrega(Base):
    __tablename__ = "entrega"

    __table_args__ = (
        UniqueConstraint("pedido_id", name="uq_entrega_pedido"),
        CheckConstraint(
            "saida_em IS NULL OR saida_em >= aceita_em",
            name="chk_entrega_saida",
        ),
        CheckConstraint(
            "entregue_em IS NULL OR "
            "(saida_em IS NOT NULL AND entregue_em >= saida_em)",
            name="chk_entrega_conclusao",
        ),
        Index(
            "idx_entrega_entregador_aceite",
            "entregador_id",
            "aceita_em",
        ),
    )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    pedido_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "pedido.id",
            name="fk_entrega_pedido",
            ondelete="RESTRICT",
            onupdate="RESTRICT",
        ),
        nullable=False,
    )

    entregador_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "usuario.id",
            name="fk_entrega_entregador",
            ondelete="RESTRICT",
            onupdate="RESTRICT",
        ),
        nullable=False,
    )

    aceita_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    saida_em: Mapped[datetime | None] = mapped_column(DateTime)
    entregue_em: Mapped[datetime | None] = mapped_column(DateTime)