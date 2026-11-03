from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ItemPedido(Base):
    __tablename__ = "item_pedido"

    __table_args__ = (
        UniqueConstraint(
            "pedido_id",
            "produto_id",
            name="uq_item_pedido_produto",
        ),
        CheckConstraint(
            "quantidade > 0",
            name="chk_item_quantidade",
        ),
        CheckConstraint(
            "preco_unitario > 0",
            name="chk_item_preco",
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
            name="fk_item_pedido",
            ondelete="RESTRICT",
            onupdate="RESTRICT",
        ),
        nullable=False,
    )

    produto_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "produto.id",
            name="fk_item_produto",
            ondelete="RESTRICT",
            onupdate="RESTRICT",
        ),
        nullable=False,
    )

    nome_produto: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    quantidade: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    preco_unitario: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )