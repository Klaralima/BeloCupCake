from datetime import datetime

from pydantic import BaseModel


class EntregaDisponivelResposta(BaseModel):
    pedido_id: int
    bairro_nome: str
    cidade: str
    uf: str
    previsao_entrega: datetime