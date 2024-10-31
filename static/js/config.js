async function fetchDadosPainel() {
    try {
        const response = await fetch('/dados_painel');
        const data = await response.json();

        document.getElementById('vendasValor').innerText = `R$${data.vendas}`;
        document.getElementById('pedidosValor').innerText = data.pedidos;
        document.getElementById('clientesValor').innerText = data.clientes;
        document.getElementById('receitaValor').innerText = `R$${data.receita}`;

        const ctx = document.getElementById('lucroChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho'],
                datasets: [
                    {
                        label: 'Vendas',
                        data: data.vendas_mensais,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        fill: false,
                    },
                    {
                        label: 'Despesas',
                        data: data.despesas_mensais,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        fill: false,
                    },
                    {
                        label: 'Lucro',
                        data: data.vendas_mensais.map((venda, index) => venda - data.despesas_mensais[index]),
                        borderColor: 'rgba(54, 162, 235, 1)',
                        fill: false,
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error("Erro ao carregar dados:", error);
    }
}
document.addEventListener("DOMContentLoaded", fetchDadosPainel);