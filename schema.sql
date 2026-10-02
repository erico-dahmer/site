CREATE TABLE IF NOT EXISTS produtos (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           TEXT    NOT NULL,
    descricao      TEXT    NOT NULL,
    custo_producao REAL    NOT NULL CHECK (custo_producao >= 0),
    valor_venda    REAL    NOT NULL CHECK (valor_venda >= 0),
    estoque        INTEGER NOT NULL CHECK (estoque >= 0),
    imagem         TEXT
);

CREATE TABLE IF NOT EXISTS pedidos (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id    INTEGER NOT NULL,
    cliente_nome  TEXT    NOT NULL,
    cliente_email TEXT    NOT NULL,
    quantidade    INTEGER NOT NULL CHECK (quantidade > 0),
    valor_total   REAL    NOT NULL,
    data_pedido   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
);