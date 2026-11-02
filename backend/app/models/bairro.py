from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
    text,
    CHAR
)
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Bairro(Base):
    __tablename__ = "bairro"

    __table_args__ = (
        UniqueConstraint(
            "nome", "cidade", "uf",
            name="uq_bairro_localidade",
        ),
        CheckConstraint(
            "ativo IN (0, 1)",
            name="chk_bairro_ativo",
        ),
    )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    regiao_entrega_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "regiao_entrega.id",
            name="fk_bairro_regiao",
            ondelete="RESTRICT",
            onupdate="RESTRICT",
        ),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    uf: Mapped[str] = mapped_column(CHAR(2), nullable=False)

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("1"),
    )