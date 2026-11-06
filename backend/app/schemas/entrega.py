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


class EntregaIniciadaResposta(BaseModel):
    pedido_id: int
    entregador_id: int
    status: str
    saida_em: datetime

class EntregaConcluidaResposta(BaseModel):
    pedido_id: int
    entregador_id: int
    status: str
    entregue_em: datetime

class MinhaEntregaResposta(BaseModel):
    pedido_id: int
    status: str
    aceita_em: datetime
    saida_em: datetime | None
    entregue_em: datetime | None