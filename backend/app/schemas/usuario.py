from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class UsuarioCriar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1, max_length=150)
    email: EmailStr = Field(max_length=254)
    telefone: str = Field(min_length=1, max_length=20)
    senha: str = Field(min_length=8, max_length=128)

    @field_validator("nome", "telefone", mode="before")
    @classmethod
    def remover_espacos_externos(cls, valor):
        if isinstance(valor, str):
            return valor.strip()
        return valor


class UsuarioResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    telefone: str
    perfil: str
    ativo: bool