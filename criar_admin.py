import sqlite3
from getpass import getpass

from werkzeug.security import generate_password_hash

from database import get_connection, init_db

init_db()  # garante que a tabela usuarios existe

usuario = input("Nome de usuário do admin: ").strip()
senha = getpass("Senha (não aparece enquanto você digita): ")

if not usuario or len(senha) < 4:
    print("Usuário vazio ou senha muito curta (mínimo 4 caracteres).")
else:
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)",
                (usuario, generate_password_hash(senha)),
            )
        print("Administrador criado com sucesso!")
    except sqlite3.IntegrityError:
        print("Esse usuário já existe.")