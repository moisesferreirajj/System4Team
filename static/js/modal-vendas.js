document.addEventListener('DOMContentLoaded', () => {
    const modalAdicionarPedido = document.querySelector('#adicionarPedidoModal');

    modalAdicionarPedido.addEventListener('show.bs.modal', () => {
        fetch('/json/pedidos-info')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar dados');
                }
                return response.json();
            })
            .then(data => {
                preencherSelect('cliente', data.clientes);
                preencherSelect('produto', data.produtos);
                preencherSelect('funcionario', data.funcionarios);
                preencherSelect('empresa', data.empresas);
            })
            .catch(error => console.error(error));
    });

    function preencherSelect(selectId, options) {
        const select = document.getElementById(selectId);
        select.innerHTML = ''; // Limpa opções anteriores
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.hidden = true;
        defaultOption.selected = true;
        select.appendChild(defaultOption);

        options.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option.id;
            opt.textContent = option.nome;
            select.appendChild(opt);
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const modalAdicionarPedido = new bootstrap.Modal(document.getElementById('adicionarPedidoModal'));

    const btnAdicionar = document.querySelector('#btnAdicionar');
    if (btnAdicionar) {
        btnAdicionar.addEventListener('click', () => {
            modalAdicionarPedido.show(); // Exibe o modal

            // Remove o backdrop manualmente
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
        });
    }

    // Fechar o modal ao clicar no botão de fechar
    const btnFechar = document.querySelector('.btn-close');
    if (btnFechar) {
        btnFechar.addEventListener('click', () => {
            modalAdicionarPedido.hide(); // Esconde o modal

            // Também remove o backdrop, se houver
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
        });
    }
});
