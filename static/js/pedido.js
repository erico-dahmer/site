// Pega os elementos da página
const form = document.getElementById("form-pedido");
const campoQuantidade = document.getElementById("quantidade");
const campoTotal = document.getElementById("total");

// Pega o preço que o HTML guardou em data-preco
const preco = parseFloat(form.dataset.preco);

// Recalcula o total sempre que a quantidade muda
function atualizarTotal() {
    const quantidade = parseInt(campoQuantidade.value) || 0;
    const total = quantidade * preco;
    campoTotal.textContent = total.toFixed(2).replace(".", ",");
}

campoQuantidade.addEventListener("input", atualizarTotal);

// Calcula já na abertura da página
atualizarTotal();