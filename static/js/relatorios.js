// Só desenha o gráfico se existir o <canvas> (ou seja, se houver vendas)
const canvas = document.getElementById("grafico");

if (canvas) {
    const cores = ["#2450c8", "#e07a3f", "#2a9d5c"];

    // Dá uma cor para cada produto
    const datasets = dadosGrafico.datasets.map((d, i) => ({
        label: d.label,
        data: d.data,
        backgroundColor: cores[i % cores.length],
    }));

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: dadosGrafico.labels,
            datasets: datasets,
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 },
                    title: { display: true, text: "Unidades vendidas" },
                },
            },
        },
    });
}