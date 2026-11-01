USE belocupcake_dev;

CREATE TABLE entrega (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    pedido_id BIGINT UNSIGNED NOT NULL,
    entregador_id BIGINT UNSIGNED NOT NULL,

    aceita_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    saida_em DATETIME,
    entregue_em DATETIME,

    CONSTRAINT uq_entrega_pedido UNIQUE (pedido_id),

    CONSTRAINT fk_entrega_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedido (id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT fk_entrega_entregador
        FOREIGN KEY (entregador_id)
        REFERENCES usuario (id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_entrega_saida
        CHECK (
            saida_em IS NULL
            OR saida_em >= aceita_em
        ),

    CONSTRAINT chk_entrega_conclusao
        CHECK (
            entregue_em IS NULL
            OR (
                saida_em IS NOT NULL
                AND entregue_em >= saida_em
            )
        ),

    INDEX idx_entrega_entregador_aceite (entregador_id, aceita_em)
) ENGINE=InnoDB;