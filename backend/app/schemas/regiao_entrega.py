from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class RegiaoEntregaCriar(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    nome: str = Field(min_length=1, max_length=100)

    taxa: Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
        allow_inf_nan=False,
    )

    prazo_minutos: int = Field(
        gt=0,
        le=2147483647,
        strict=True,
    )


class RegiaoEntregaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    taxa: Decimal
    prazo_minutos: int
    ativo: bool