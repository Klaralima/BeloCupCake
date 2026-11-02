from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(max_length=254)
    senha: str = Field(min_length=1, max_length=128)


class TokenResposta(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int