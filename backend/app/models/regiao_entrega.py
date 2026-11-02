from decimal import Decimal

from sqlalchemy import (
    Boolean, CheckConstraint, Integer, Numeric, String, text,
)
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RegiaoEntrega(Base):
    __tablename__ = "regiao_entrega"

    __table_args__ = (
        CheckConstraint("taxa >= 0", name="chk_regiao_taxa"),
        CheckConstraint("prazo_minutos > 0", name="chk_regiao_prazo"),
        CheckConstraint("ativo IN (0, 1)", name="chk_regiao_ativo"),
    )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    taxa: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    prazo_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("1"),
    )