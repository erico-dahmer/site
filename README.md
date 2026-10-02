# Projeto Empresa Familiar

site de vendas com pedido e baixa automática de estoque, e relatórios com gráfico.

## Funcionalidades
- Cadastro de exatamente 3 produtos (código, nome, descrição, custo, valor de venda, estoque e imagem)
- Catálogo visual dos produtos (público)
- Formulário de pedido com total dinâmico (JavaScript)
- Baixa automática no estoque a cada pedido
- Relatórios com filtro de datas, agrupamento diário/semanal/mensal e gráfico comparativo
- Login do administrador (Admin e Relatórios protegidos)
- Edição de produtos e reposição de estoque

## Tecnologias
Python 3 (Flask), SQLite, HTML, CSS, JavaScript e Chart.js.

## Como rodar
1. Clone o repositório e abra a pasta no VSCode
2. Crie e ative o ambiente virtual:
   `python -m venv venv` e depois `venv\Scripts\activate`
3. Instale as bibliotecas: `pip install -r requirements.txt`
4. Crie o usuário administrador: `python criar_admin.py`
5. Inicie o sistema: `python app.py`
6. Abra `http://127.0.0.1:5000`

## Estrutura
- `app.py`: rotas do sistema
- `database.py` e `schema.sql`: banco SQLite
- `templates/`: páginas HTML
- `static/`: CSS, JavaScript e imagens
- `docs/`: escopo e documentação

## Equipe
| Nome | Papel |
|------|-------|
| (Gustavo Gomes Madruga) | Gerente de Projeto |
| (João Vítor Primaz) | Analista de Sistema |
| Érico Cattoi Dahmer | Programador |
| Henrique Malvessi Lagemann | Programador |