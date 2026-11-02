from pydantic import BaseModel, ConfigDict, Field, field_validator


class BairroCriar(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    regiao_entrega_id: int = Field(
        ge=1,
        le=18446744073709551615,
        strict=True,
    )
    nome: str = Field(min_length=1, max_length=100)
    cidade: str = Field(min_length=1, max_length=100)
    uf: str = Field(pattern=r"^[A-Z]{2}$")

    @field_validator("uf", mode="before")
    @classmethod
    def normalizar_uf(cls, valor):
        if isinstance(valor, str):
            return valor.strip().upper()
        return valor


class BairroResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    regiao_entrega_id: int
    nome: str
    cidade: str
    uf: str
    ativo: bool