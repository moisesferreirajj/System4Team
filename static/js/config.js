document.addEventListener("DOMContentLoaded", function() {
    const toggleButton = document.getElementById("toggle-theme");
    const themeIcon = document.getElementById("theme-icon");

    const currentTheme = localStorage.getItem("theme") || "dark";
    document.body.className = currentTheme; // Aplica o tema

    // Atualiza o ícone de acordo com o tema
    themeIcon.innerText = currentTheme === "dark" ? "🌙" : "☀️";

    toggleButton.addEventListener("click", function() {
        const newTheme = document.body.className === "dark" ? "light" : "dark";
        document.body.className = newTheme;
        localStorage.setItem("theme", newTheme); // Armazena o tema no localStorage
        
        // Atualiza o ícone
        themeIcon.innerText = newTheme === "dark" ? "🌙" : "☀️";
    });
});

// Função para buscar os dados do painel
        async function fetchDadosPainel() {
            const response = await fetch('/dados_painel');
            const data = await response.json();

            // Atualizando o HTML com os dados
            document.getElementById('vendasValor').innerText = `$ ${data.vendas}`;
            document.getElementById('pedidosValor').innerText = data.pedidos;
            document.getElementById('inscricoesValor').innerText = data.inscricoes;
            document.getElementById('receitaValor').innerText = `$ ${data.receita}`;

            // Criar o gráfico
            const ctx = document.getElementById('lucroChart').getContext('2d');
            const lucroChart = new Chart(ctx, {
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
        }

        // Chama a função ao carregar a página
        window.onload = fetchDadosPainel;