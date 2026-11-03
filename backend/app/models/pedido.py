from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    text,
)
from sqlalchemy.dialects.mysql import BIGINT, ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Pedido(Base):
    __tablename__ = "pedido"

    __table_args__ = (
        CheckConstraint(
            "subtotal > 0",
            name="chk_pedido_subtotal",
        ),
        CheckConstraint(
            "taxa_entrega >= 0",
            name="chk_pedido_taxa",
        ),
        CheckConstraint(
            "valor_total = subtotal + taxa_entrega",
            name="chk_pedido_total",
        ),
        CheckConstraint(
            "previsao_entrega >= criado_em",
            name="chk_pedido_previsao",
        ),
        Index("idx_pedido_cliente_data", "cliente_id", "criado_em"),
        Index("idx_pedido_status_data", "status", "criado_em"),
    )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    cliente_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "usuario.id",
            name="fk_pedido_cliente",
            ondelete="RESTRICT",
            onupdate="RESTRICT",
        ),
        nullable=False,
    )

    bairro_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "bairro.id",
            name="fk_pedido_bairro",
            ondelete="RESTRICT",
            onupdate="RESTRICT",
        ),
        nullable=False,
    )

    logradouro: Mapped[str] = mapped_column(String(200), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    complemento: Mapped[str | None] = mapped_column(String(150))
    cep: Mapped[str] = mapped_column(CHAR(8), nullable=False)
    bairro_nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    uf: Mapped[str] = mapped_column(CHAR(2), nullable=False)

    status: Mapped[str] = mapped_column(
        ENUM(
            "RECEBIDO",
            "EM_PREPARO",
            "PRONTO",
            "ATRIBUIDA",
            "EM_ROTA",
            "ENTREGUE",
            "CANCELADO",
        ),
        nullable=False,
        server_default=text("'RECEBIDO'"),
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    taxa_entrega: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    valor_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    previsao_entrega: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )