from sqlalchemy import Boolean, CheckConstraint, String, text
from sqlalchemy.dialects.mysql import BIGINT, ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    __table_args__ = (
        CheckConstraint(
            "ativo IN (0, 1)",
            name="chk_usuario_ativo",
        ),
    )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(254),
        nullable=False,
        unique=True,
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    perfil: Mapped[str] = mapped_column(
        ENUM("CLIENTE", "ADMINISTRADOR", "ENTREGADOR"),
        nullable=False,
        server_default=text("'CLIENTE'"),
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("1"),
    )