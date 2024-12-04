async function fetchDadosPainel() {
    try {
        const response = await fetch('/json/dados-painel');
        const data = await response.json();

        // Atualizar valores principais no dashboard
        document.getElementById('vendasValor').innerText = `R$${data.vendas}`;
        document.getElementById('pedidosValor').innerText = data.pedidos;
        document.getElementById('clientesValor').innerText = data.clientes;
        document.getElementById('receitaValor').innerText = `R$${data.receita}`;

        // Extração dos meses e valores de vendas
        const labels = data.vendas_mensais.map(venda => venda.mes);
        const vendasData = data.vendas_mensais.map(venda => parseFloat(venda.total));

        // Extração dos dados de vendas não finalizadas
        const naoFinalizadasData = data.vendas_nao_finalizadas 
            ? data.vendas_nao_finalizadas.map(venda => parseFloat(venda.total))
            : Array(vendasData.length).fill(0); // Preencher com 0 se não existir

        const ctx = document.getElementById('lucroChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels, // Labels dos meses
                datasets: [
                    {
                        label: 'Vendas Finalizadas',
                        data: vendasData,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        fill: false,
                    },
                    {
                        label: 'Vendas Não Finalizadas',
                        data: naoFinalizadasData,
                        borderColor: 'rgba(255, 99, 132, 1)',
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