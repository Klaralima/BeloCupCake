from decimal import Decimal

from sqlalchemy import (
    Boolean, CheckConstraint, Integer, Numeric, String, Text, text,
)
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Produto(Base):
    __tablename__ = "produto"

    __table_args__ = (
        CheckConstraint("preco > 0", name="chk_produto_preco"),
        CheckConstraint("estoque >= 0", name="chk_produto_estoque"),
        CheckConstraint("ativo IN (0, 1)", name="chk_produto_ativo"),
    )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), primary_key=True, autoincrement=True
    )
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    sabor: Mapped[str] = mapped_column(String(100), nullable=False)
    tamanho: Mapped[str] = mapped_column(String(30), nullable=False)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estoque: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    imagem_url: Mapped[str | None] = mapped_column(
        String(2048), nullable=True
    )
    ativo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("1")
    )