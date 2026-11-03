from copy import deepcopy

from pydantic import ValidationError

from app.schemas.pedido import PedidoCriar


pedido_base = {
    "bairro_id": 1,
    "logradouro": "Rua de Demonstração",
    "numero": "100",
    "complemento": "",
    "cep": "58000000",
    "itens": [
        {"produto_id": 1, "quantidade": 2},
    ],
}


def verificar(nome, dados, deve_aceitar):
    try:
        PedidoCriar.model_validate(dados)
        aceitou = True
    except ValidationError:
        aceitou = False

    assert aceitou == deve_aceitar, f"Resultado inesperado: {nome}"
    print(f"OK: {nome}")


verificar("pedido válido", pedido_base, True)

caso = deepcopy(pedido_base)
caso["itens"] = []
verificar("rejeita carrinho vazio", caso, False)

caso = deepcopy(pedido_base)
caso["itens"].append({"produto_id": 1, "quantidade": 1})
verificar("rejeita produto repetido", caso, False)

caso = deepcopy(pedido_base)
caso["itens"][0]["quantidade"] = 0
verificar("rejeita quantidade zero", caso, False)

caso = deepcopy(pedido_base)
caso["itens"][0]["preco_unitario"] = "0.01"
verificar("rejeita preço enviado pelo cliente", caso, False)

caso = deepcopy(pedido_base)
caso["cliente_id"] = 99
verificar("rejeita identidade enviada no JSON", caso, False)

caso = deepcopy(pedido_base)
caso["cep"] = "58000-000"
verificar("rejeita CEP com formato incorreto", caso, False)

print("Todas as verificações passaram.")