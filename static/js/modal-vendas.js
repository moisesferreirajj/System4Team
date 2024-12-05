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
            modalAdicionarPedido.show(); //EXIBE O MODAL

            //REMOVE O BACKDROP
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
        });
    }

    //FECHA O MODAL APÓS CLICAR NO BOTÃO DE CANCELAR
    const btnFechar = document.querySelector('.btn-close');
    if (btnFechar) {
        btnFechar.addEventListener('click', () => {
            modalAdicionarPedido.hide(); //ESCONDE O MODAL

            //REMOVE O BACKDROP CASO O BOOSTRAP FORÇAR ELE
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const modalAdicionarPedidoElement = document.getElementById('adicionarPedidoModal');
    const modalAdicionarPedido = new bootstrap.Modal(modalAdicionarPedidoElement);

    //REMOVER BACKDROP E ABRIR MODAL A SEGUIR
    modalAdicionarPedidoElement.addEventListener('show.bs.modal', () => {
        setTimeout(removerBackdrop, 10); //ESPERE 10MS PARA FECHAR O BACKDROP
    });

    const formAdicionarPedido = document.querySelector('.adicionarpedido');
    if (formAdicionarPedido) {
        formAdicionarPedido.addEventListener('submit', async (event) => {
            event.preventDefault(); //IMPEDE VINDA DE INFORMAÇÕES DE FORA, NAO ACEITA FORM PADRAO

            const formData = new FormData(formAdicionarPedido);

            try {
                const response = await fetch(formAdicionarPedido.action, {
                    method: 'POST',
                    body: formData,
                });

                if (!response.ok) {
                    throw new Error('Erro ao adicionar o pedido');
                }

                const data = await response.json();
                alert(data.message || 'Pedido adicionado com sucesso!');

                //FECHA O MODAL E REMOVE O BACKDROP
                modalAdicionarPedido.hide();
                removerBackdrop();

                setTimeout(() => {
                    location.reload(); //RECARREGAR PAGINA APÓS O ENVIO
                }, 500);
            } catch (error) {
                alert('Ocorreu um erro ao processar o pedido. Por favor, tente novamente.');
                console.error(error);
            }
        });
    }

    function removerBackdrop() {
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.remove();
        }
    }
});
