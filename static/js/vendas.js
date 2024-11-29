async function fetchDadosPainel() {
    try {
        const response = await fetch('/json/dados-vendas');
        const data = await response.json();

        // Função para formatar números como moeda
        const formatarMoeda = (valor) => {
            return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
        };

        // Extrair os dados dos produtos mais vendidos (lucro e nome)
        const produtos = data.produtos_mais_vendidos;
        const nomesProdutos = produtos.map(produto => produto.nome);  // Nomes dos produtos
        const lucrosProdutos = produtos.map(produto => parseFloat(produto.lucro));  // Lucros dos produtos

        // Criar gráfico com produtos mais vendidos como labels e lucros como dados
        const ctx = document.getElementById('lucroChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',  // Usando 'bar' para exibir barras para cada produto
            data: {
                labels: nomesProdutos,  // Usando os nomes dos produtos como labels
                datasets: [
                    {
                        label: 'Lucro por Produto',
                        data: lucrosProdutos,  // Dados de lucro para cada produto
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',  // Cor de fundo azul
                        borderColor: 'rgba(54, 162, 235, 1)',  // Cor da borda azul
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatarMoeda(value);  // Formatando o eixo Y para moeda
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error("Erro ao carregar dados:", error);
    }
}

async function fetchPedidos() {
    try {
        const response = await fetch('/json/listagem-pedidos');
        const data = await response.json();

        if (!data.pedidos) {
            throw new Error("Dados de pedidos não encontrados.");
        }

        const pedidosLista = document.getElementById('PedidosLista');
        pedidosLista.innerHTML = '';

        data.pedidos.forEach(pedido => {
            const listItem = document.createElement('li');
            const pedidoInfo = `Venda #${pedido.id_venda} - ${pedido.cliente_nome} | ${pedido.produto_nome} (${pedido.quantidade}) - Data: ${pedido.data_pedido} <br>`;
            
            const statusSpan = document.createElement('span');
            if (pedido.finalizado) {
                statusSpan.classList.add('badge', 'bg-success');
                statusSpan.textContent = 'Finalizado';
            } else {
                statusSpan.classList.add('badge', 'bg-danger');
                statusSpan.textContent = 'Não Finalizado';
            }

            listItem.innerHTML = pedidoInfo + ' ' + statusSpan.outerHTML;
            pedidosLista.appendChild(listItem);
        });
    } catch (error) {
        console.error("Erro ao carregar os pedidos:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    fetchDadosPainel();
    fetchPedidos();
});
