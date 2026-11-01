USE belocupcake_dev;

CREATE TABLE produto (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT NOT NULL,
    sabor VARCHAR(100) NOT NULL,
    tamanho VARCHAR(30) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL DEFAULT 0,
    imagem_url VARCHAR(2048),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_produto_preco CHECK (preco > 0),
    CONSTRAINT chk_produto_estoque CHECK (estoque >= 0),
    CONSTRAINT chk_produto_ativo CHECK (ativo IN (0, 1))
) ENGINE=InnoDB;

CREATE TABLE pedido (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    cliente_id BIGINT UNSIGNED NOT NULL,
    bairro_id BIGINT UNSIGNED NOT NULL,

    logradouro VARCHAR(200) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    complemento VARCHAR(150),
    cep CHAR(8) NOT NULL,
    bairro_nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,

    status ENUM(
        'RECEBIDO',
        'EM_PREPARO',
        'PRONTO',
        'ATRIBUIDA',
        'EM_ROTA',
        'ENTREGUE',
        'CANCELADO'
    ) NOT NULL DEFAULT 'RECEBIDO',

    subtotal DECIMAL(10, 2) NOT NULL,
    taxa_entrega DECIMAL(10, 2) NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    previsao_entrega DATETIME NOT NULL,

    CONSTRAINT fk_pedido_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES usuario (id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT fk_pedido_bairro
        FOREIGN KEY (bairro_id)
        REFERENCES bairro (id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_pedido_subtotal CHECK (subtotal > 0),
    CONSTRAINT chk_pedido_taxa CHECK (taxa_entrega >= 0),
    CONSTRAINT chk_pedido_total
        CHECK (valor_total = subtotal + taxa_entrega),
    CONSTRAINT chk_pedido_previsao
        CHECK (previsao_entrega >= criado_em),

    INDEX idx_pedido_cliente_data (cliente_id, criado_em),
    INDEX idx_pedido_status_data (status, criado_em)
) ENGINE=InnoDB;

CREATE TABLE item_pedido (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    pedido_id BIGINT UNSIGNED NOT NULL,
    produto_id BIGINT UNSIGNED NOT NULL,
    nome_produto VARCHAR(150) NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,

    CONSTRAINT fk_item_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedido (id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT fk_item_produto
        FOREIGN KEY (produto_id)
        REFERENCES produto (id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT uq_item_pedido_produto UNIQUE (pedido_id, produto_id),
    CONSTRAINT chk_item_quantidade CHECK (quantidade > 0),
    CONSTRAINT chk_item_preco CHECK (preco_unitario > 0)
) ENGINE=InnoDB;