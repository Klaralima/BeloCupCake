# Roteiro de demonstração e evidências — BeloCupCake

## Identificação

Projeto acadêmico de Engenharia de Software: aplicação web responsiva para compra e entrega de cupcakes.

- Aplicação: https://screenshot-soul-studio-36.lovable.app
- API e documentação interativa: https://belocupcake-api.duckdns.org/docs
- Backend: https://github.com/Klaralima/BeloCupCake
- Frontend: https://github.com/Klaralima/pixel-perfect-replica
- Hospedagem: Lovable (frontend) e VPS Hostinger (FastAPI e MySQL).

O DuckDNS fornece o nome de acesso à API. Não hospeda o código nem o banco.

## Contas de demonstração

| Perfil | E-mail |
| --- | --- |
| Administrador | admin.teste@example.com |
| Entregador | entregador.teste@example.com |
| Cliente | fulano@example.com |

As senhas são fornecidas pela responsável em canal privado. O cadastro público também permite criar um novo cliente. Não utilizar dados pessoais reais nos testes.

## Preparação

1. Entrar como administrador e conferir a existência de um produto ativo com estoque positivo.
2. Conferir uma região com taxa e prazo e um bairro vinculado a ela.
3. Usar janelas separadas para demonstrar os três perfis, ou sair antes de trocar de conta. Recarregar a página encerra a sessão em memória.

## Fluxo de apresentação

| Etapa | Ação | Resultado esperado |
| --- | --- | --- |
| 1 | Cadastrar um cliente e entrar | Cadastro confirmado e acesso ao catálogo |
| 2 | Abrir um produto e adicionar ao carrinho | Produto e quantidade aparecem no carrinho |
| 3 | Selecionar bairro e preencher endereço | Taxa, prazo e total estimado são apresentados |
| 4 | Confirmar o pedido | Pedido registrado em `RECEBIDO`, carrinho limpo e histórico disponível |
| 5 | Entrar como administrador e consultar pedidos | Pedido do cliente aparece para preparo |
| 6 | Iniciar preparo e marcar pronto | Estado passa por `EM_PREPARO` e `PRONTO` |
| 7 | Entrar como entregador e escolher entrega disponível | Aceite registra o responsável e muda o estado para `ATRIBUIDA` |
| 8 | Consultar detalhes e iniciar rota | Endereço disponível e estado `EM_ROTA` |
| 9 | Confirmar entrega | Estado `ENTREGUE` |
| 10 | Consultar o histórico do cliente | Conclusão refletida no pedido após atualizar a consulta |

Pagamento é presencial e não há transação financeira no aplicativo. A estimativa de entrega não representa rastreamento em tempo real.

## Verificações complementares

- Outro cliente não visualiza o pedido do primeiro.
- Cliente não consegue utilizar operações de administrador ou entregador.
- Produto inativo ou sem estoque não aparece no catálogo público.
- Não é permitido pular etapas do preparo e da entrega.
- Um pedido em `RECEBIDO` pode ser cancelado pelo administrador, restituindo o estoque.
- Uma entrega aceita deixa de estar disponível para outro entregador.
- Uma URL de imagem inválida exibe a imagem padrão.

## Registro de validação

Em 08/11/2026, a responsável informou que testou com sucesso o fluxo publicado desde o cadastro e a compra até o aceite e a entrega. Esse registro é uma confirmação manual da responsável, não um relatório automatizado de navegador.

As verificações locais realizadas durante o desenvolvimento registraram 7 testes do backend e 8 do frontend aprovados, além da verificação TypeScript e build. A suíte não comprova todos os cenários complementares acima; eles constituem um roteiro de verificação adicional.

## Evidências para anexar à entrega

Capturar as telas abaixo durante uma demonstração. As imagens ainda precisam ser produzidas pela responsável e não estão anexadas a este documento.

1. Catálogo com produtos.
2. Carrinho com taxa e total estimado.
3. Pedido registrado no histórico do cliente.
4. Pedido em preparo na área administrativa.
5. Entrega aceita na área do entregador.
6. Pedido entregue no histórico do cliente.

Não incluir senhas, tokens, arquivos `.env` nem dados pessoais reais nas capturas.

## Texto de apresentação

O BeloCupCake é uma aplicação web responsiva desenvolvida para demonstrar o processo de compra e entrega de cupcakes. Possui perfis de cliente, administrador e entregador, com autenticação e controle de acesso. O cliente consulta produtos e faz pedidos; o administrador gerencia o catálogo e o preparo; o entregador escolhe uma entrega disponível e registra sua conclusão. O frontend utiliza React e TypeScript e está publicado no Lovable. A API foi desenvolvida com Python e FastAPI, com persistência em MySQL, ambos hospedados em uma VPS Hostinger. O acesso à API utiliza HTTPS e um subdomínio DuckDNS. O pagamento é presencial, sem integração financeira.
