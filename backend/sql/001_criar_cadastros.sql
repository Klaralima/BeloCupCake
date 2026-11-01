USE belocupcake_dev;

CREATE TABLE usuario (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    perfil ENUM('CLIENTE', 'ADMINISTRADOR', 'ENTREGADOR')
        NOT NULL DEFAULT 'CLIENTE',
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_usuario_email UNIQUE (email),
    CONSTRAINT chk_usuario_ativo CHECK (ativo IN (0, 1))
) ENGINE=InnoDB;

CREATE TABLE regiao_entrega (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    taxa DECIMAL(10, 2) NOT NULL,
    prazo_minutos INT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_regiao_taxa CHECK (taxa >= 0),
    CONSTRAINT chk_regiao_prazo CHECK (prazo_minutos > 0),
    CONSTRAINT chk_regiao_ativo CHECK (ativo IN (0, 1))
) ENGINE=InnoDB;

CREATE TABLE bairro (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    regiao_entrega_id BIGINT UNSIGNED NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_bairro_localidade UNIQUE (nome, cidade, uf),

    CONSTRAINT fk_bairro_regiao
        FOREIGN KEY (regiao_entrega_id)
        REFERENCES regiao_entrega (id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_bairro_ativo CHECK (ativo IN (0, 1))
) ENGINE=InnoDB;