from datetime import datetime

from pydantic import BaseModel


class EntregaDisponivelResposta(BaseModel):
    pedido_id: int
    bairro_nome: str
    cidade: str
    uf: str
    previsao_entrega: datetime
    

class EntregaAceitaResposta(BaseModel):
    pedido_id: int
    entregador_id: int
    status: str
    aceita_em: datetime