from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProdutoCriar(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    nome: str = Field(min_length=1, max_length=150)
    descricao: str = Field(min_length=1, max_length=5000)
    sabor: str = Field(min_length=1, max_length=100)
    tamanho: str = Field(min_length=1, max_length=30)

    preco: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
        allow_inf_nan=False,
    )

    estoque: int = Field(
        default=0,
        ge=0,
        le=2147483647,
        strict=True,
    )

    imagem_url: HttpUrl | None = Field(default=None, max_length=2048)


class ProdutoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str
    sabor: str
    tamanho: str
    preco: Decimal
    estoque: int
    imagem_url: str | None
    ativo: bool