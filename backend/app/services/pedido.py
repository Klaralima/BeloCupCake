from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Bairro, ItemPedido, Pedido, Produto, RegiaoEntrega
from app.schemas.pedido import (
    ItemPedidoResposta,
    PedidoCriar,
    PedidoDetalheResposta,
    PedidoResumoResposta,
)


class PedidoInvalidoError(Exception):
    pass


def criar_pedido(
    sessao: Session,
    cliente_id: int,
    dados: PedidoCriar,
) -> PedidoResumoResposta:
    try:
        destino = sessao.execute(
            select(Bairro, RegiaoEntrega)
            .join(
                RegiaoEntrega,
                RegiaoEntrega.id == Bairro.regiao_entrega_id,
            )
            .where(Bairro.id == dados.bairro_id)
            .with_for_update()
        ).one_or_none()

        if destino is None:
            raise PedidoInvalidoError("Bairro não atendido.")

        bairro, regiao = destino

        if not bairro.ativo or not regiao.ativo:
            raise PedidoInvalidoError(
                "Entrega indisponível para esse bairro."
            )

        produtos_selecionados = []
        subtotal = Decimal("0.00")

        for item in sorted(dados.itens, key=lambda item: item.produto_id):
            produto = sessao.scalar(
                select(Produto)
                .where(Produto.id == item.produto_id)
                .with_for_update()
            )

            if produto is None or not produto.ativo:
                raise PedidoInvalidoError(
                    f"Produto {item.produto_id} indisponível."
                )

            if produto.estoque < item.quantidade:
                raise PedidoInvalidoError(
                    f"Estoque insuficiente para {produto.nome}."
                )

            subtotal += produto.preco * item.quantidade
            produtos_selecionados.append((produto, item.quantidade))

        total = subtotal + regiao.taxa

        if total > Decimal("99999999.99"):
            raise PedidoInvalidoError(
                "O valor do pedido excede o limite permitido."
            )

        agora = datetime.now(timezone.utc).replace(
            tzinfo=None,
            microsecond=0,
        )

        pedido = Pedido(
            cliente_id=cliente_id,
            bairro_id=bairro.id,
            logradouro=dados.logradouro,
            numero=dados.numero,
            complemento=dados.complemento,
            cep=dados.cep,
            bairro_nome=bairro.nome,
            cidade=bairro.cidade,
            uf=bairro.uf,
            status="RECEBIDO",
            subtotal=subtotal,
            taxa_entrega=regiao.taxa,
            valor_total=total,
            criado_em=agora,
            previsao_entrega=agora + timedelta(
                minutes=regiao.prazo_minutos
            ),
        )

        sessao.add(pedido)
        sessao.flush()

        for produto, quantidade in produtos_selecionados:
            sessao.add(
                ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=produto.id,
                    nome_produto=produto.nome,
                    quantidade=quantidade,
                    preco_unitario=produto.preco,
                )
            )

            produto.estoque -= quantidade

        sessao.flush()

        resposta = PedidoResumoResposta.model_validate(pedido)
        sessao.commit()

        return resposta

    except Exception:
        sessao.rollback()
        raise

def listar_pedidos_cliente(
    sessao: Session,
    cliente_id: int,
    limite: int,
    deslocamento: int,
) -> list[Pedido]:
    consulta = (
        select(Pedido)
        .where(Pedido.cliente_id == cliente_id)
        .order_by(Pedido.criado_em.desc(), Pedido.id.desc())
        .offset(deslocamento)
        .limit(limite)
    )

    return list(sessao.scalars(consulta).all())

def buscar_pedido_cliente(
    sessao: Session,
    pedido_id: int,
    cliente_id: int,
) -> PedidoDetalheResposta | None:
    pedido = sessao.scalar(
        select(Pedido).where(
            Pedido.id == pedido_id,
            Pedido.cliente_id == cliente_id,
        )
    )

    if pedido is None:
        return None

    itens = sessao.scalars(
        select(ItemPedido)
        .where(ItemPedido.pedido_id == pedido.id)
        .order_by(ItemPedido.id)
    ).all()

    resumo = PedidoResumoResposta.model_validate(pedido)

    return PedidoDetalheResposta(
        **resumo.model_dump(),
        bairro_id=pedido.bairro_id,
        logradouro=pedido.logradouro,
        numero=pedido.numero,
        complemento=pedido.complemento,
        cep=pedido.cep,
        bairro_nome=pedido.bairro_nome,
        cidade=pedido.cidade,
        uf=pedido.uf,
        itens=[
            ItemPedidoResposta.model_validate(item)
            for item in itens
        ],
    )