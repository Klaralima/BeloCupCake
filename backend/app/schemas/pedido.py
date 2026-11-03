from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class ItemPedidoCriar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    produto_id: int = Field(
        ge=1,
        le=18446744073709551615,
        strict=True,
    )

    quantidade: int = Field(
        ge=1,
        le=2147483647,
        strict=True,
    )


class PedidoCriar(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    bairro_id: int = Field(
        ge=1,
        le=18446744073709551615,
        strict=True,
    )

    logradouro: str = Field(min_length=1, max_length=200)
    numero: str = Field(min_length=1, max_length=20)
    complemento: str | None = Field(default=None, max_length=150)
    cep: str = Field(pattern=r"^[0-9]{8}$")

    itens: list[ItemPedidoCriar] = Field(min_length=1)

    @field_validator("complemento")
    @classmethod
    def normalizar_complemento(cls, valor):
        if valor == "":
            return None
        return valor

    @model_validator(mode="after")
    def validar_produtos_sem_repeticao(self) -> Self:
        ids = [item.produto_id for item in self.itens]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "Cada produto deve aparecer apenas uma vez. "
                "Ajuste a quantidade do item."
            )

        return self