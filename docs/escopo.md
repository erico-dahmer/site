# Documento de Escopo e Requisitos

## 1. Problema
Empresa familiar com 3 produtos controla vendas e estoque no papel e não tem presença digital.

## 2. Objetivo
Entregar um sistema com banco de dados, site de vendas e relatórios gerenciais (MVP).

## 3. Requisitos funcionais
- RF01: cadastrar produtos com código, nome, descrição, custo, valor de venda, estoque e imagem
- RF02: exibir os produtos em um catálogo visual
- RF03: permitir pedido de compra com total calculado dinamicamente
- RF04: dar baixa automática no estoque a cada pedido
- RF05: gerar relatórios filtrados por data e agrupados por dia, semana ou mês
- RF06: exibir gráfico comparativo das vendas dos 3 produtos
- RF07: proteger Admin e Relatórios com login
- RF08: permitir editar produtos e repor estoque

## 4. Requisitos não funcionais
- Dados guardados em banco SQLite
- Senhas guardadas com hash
- Código versionado no Git, com commits regulares

## 5. Regras de negócio
- Pedido só é aceito se houver estoque suficiente
- Todo pedido reduz o estoque na quantidade comprada
- O total do pedido é calculado no servidor com o preço do banco

## 6. Tecnologias
Python (Flask), SQLite, HTML, CSS, JavaScript, Chart.js.

## 7. Fora do escopo (versão futura)
Pagamento online, cadastro de clientes, mais de 3 produtos, controle de entrega.