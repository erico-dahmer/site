import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from database import get_connection, init_db

app = Flask(__name__)
app.secret_key = "troque-esta-chave-depois"

UPLOAD_DIR = os.path.join(app.static_folder, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

EXTENSOES_OK = {"png", "jpg", "jpeg", "webp", "gif"}
MAX_PRODUTOS = 3


def extensao_valida(nome_arquivo):
    return "." in nome_arquivo and nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_OK


@app.route("/")
def catalogo():
    with get_connection() as conn:
        produtos = conn.execute("SELECT * FROM produtos ORDER BY id").fetchall()
    return render_template("catalogo.html", produtos=produtos)


@app.route("/admin")
def admin():
    with get_connection() as conn:
        produtos = conn.execute("SELECT * FROM produtos ORDER BY id").fetchall()
    return render_template("admin.html", produtos=produtos, max_produtos=MAX_PRODUTOS)


@app.route("/admin/produtos", methods=["POST"])
def cadastrar_produto():
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
        if total >= MAX_PRODUTOS:
            flash(f"Limite de {MAX_PRODUTOS} produtos atingido.", "erro")
            return redirect(url_for("admin"))

        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()

        try:
            custo = float(request.form.get("custo_producao", "").replace(",", "."))
            valor = float(request.form.get("valor_venda", "").replace(",", "."))
            estoque = int(request.form.get("estoque", ""))
        except ValueError:
            flash("Custo, valor e estoque precisam ser números válidos.", "erro")
            return redirect(url_for("admin"))

        if not nome or not descricao:
            flash("Nome e descrição são obrigatórios.", "erro")
            return redirect(url_for("admin"))
        if custo < 0 or valor < 0 or estoque < 0:
            flash("Valores não podem ser negativos.", "erro")
            return redirect(url_for("admin"))

        nome_imagem = None
        arquivo = request.files.get("imagem")
        if arquivo and arquivo.filename:
            if not extensao_valida(arquivo.filename):
                flash("Imagem inválida. Use png, jpg, jpeg, webp ou gif.", "erro")
                return redirect(url_for("admin"))
            prefixo = datetime.now().strftime("%Y%m%d%H%M%S")
            nome_imagem = f"{prefixo}_{secure_filename(arquivo.filename)}"
            arquivo.save(os.path.join(UPLOAD_DIR, nome_imagem))

        conn.execute(
            """INSERT INTO produtos
               (nome, descricao, custo_producao, valor_venda, estoque, imagem)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (nome, descricao, custo, valor, estoque, nome_imagem),
        )

    flash("Produto cadastrado com sucesso!", "ok")
    return redirect(url_for("admin"))
@app.route("/pedido/<int:produto_id>", methods=["GET", "POST"])
def pedido(produto_id):
    # 1. Busca o produto no banco
    with get_connection() as conn:
        produto = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (produto_id,)
        ).fetchone()

    if produto is None:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("catalogo"))

    if produto["estoque"] <= 0:
        flash("Este produto está esgotado.", "erro")
        return redirect(url_for("catalogo"))

    # 2. Se o cliente enviou o formulário
    if request.method == "POST":
        nome = request.form.get("cliente_nome", "").strip()
        email = request.form.get("cliente_email", "").strip()

        try:
            quantidade = int(request.form.get("quantidade", ""))
        except ValueError:
            flash("A quantidade precisa ser um número inteiro.", "erro")
            return redirect(url_for("pedido", produto_id=produto_id))

        if not nome or "@" not in email:
            flash("Preencha o nome e um e-mail válido.", "erro")
            return redirect(url_for("pedido", produto_id=produto_id))
        if quantidade <= 0:
            flash("A quantidade precisa ser maior que zero.", "erro")
            return redirect(url_for("pedido", produto_id=produto_id))

        # O total é calculado AQUI, com o preço do banco (mais seguro)
        total = round(quantidade * produto["valor_venda"], 2)

        with get_connection() as conn:
            # BAIXA NO ESTOQUE: só diminui se houver quantidade suficiente
            resultado = conn.execute(
                """UPDATE produtos
                   SET estoque = estoque - ?
                   WHERE id = ? AND estoque >= ?""",
                (quantidade, produto_id, quantidade),
            )

            # rowcount == 0 significa que nenhuma linha foi alterada,
            # ou seja, não tinha estoque suficiente
            if resultado.rowcount == 0:
                flash("Estoque insuficiente para essa quantidade.", "erro")
                return redirect(url_for("pedido", produto_id=produto_id))

            # Registra o pedido
            conn.execute(
                """INSERT INTO pedidos
                   (produto_id, cliente_nome, cliente_email, quantidade, valor_total)
                   VALUES (?, ?, ?, ?, ?)""",
                (produto_id, nome, email, quantidade, total),
            )

        flash(f"Pedido realizado com sucesso! Total: R$ {total:.2f}", "ok")
        return redirect(url_for("catalogo"))

    # 3. Se só abriu a página (GET), mostra o formulário
    return render_template("pedido.html", produto=produto)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)