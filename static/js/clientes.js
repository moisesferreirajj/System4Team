document.addEventListener("DOMContentLoaded", function() {
    const clientTableBody = document.querySelector('.clients tbody');
    const editClientForm = document.querySelector('.edit');
    const modalTitle = document.querySelector('.modal-header .title');

    // Função para carregar os dados do cliente no modal
    clientTableBody.addEventListener('click', function(event) {
        if (event.target.classList.contains('btn-edit')) {
            const clienteId = event.target.closest('tr').dataset.id;

            //ENVIA A REQUISIÇÃO PARA PEGAR O CODIGO DOS CLIENTES
            fetch(`/buscar_cliente/${clienteId}`)
                .then(response => response.json())
                .then(data => {
                    //PREENCHER CAMPOS
                    modalTitle.textContent = `Editar Cliente - ${data.nome}`;
                    editClientForm.querySelector('input[name="nome"]').value = data.nome;
                    editClientForm.querySelector('input[name="email"]').value = data.email;
                    editClientForm.querySelector('input[name="telefone"]').value = data.telefone;
                    editClientForm.querySelector('input[name="endereco"]').value = data.endereco;

                    //ATUALIZA O ATB DE ACORDO AO MODAL
                    editClientForm.action = `/editar_cliente/${data.id}`;
                })
                .catch(err => {
                    alert('Erro ao carregar os dados do cliente');
                });
        }
    });

    editClientForm.addEventListener('submit', function(event) {
        event.preventDefault();

        //DADOS DO FORMULARIO
        const nome = editClientForm.querySelector('input[name="nome"]').value;
        const email = editClientForm.querySelector('input[name="email"]').value;
        const telefone = editClientForm.querySelector('input[name="telefone"]').value;
        const endereco = editClientForm.querySelector('input[name="endereco"]').value;

        //VERIFICA CAMPO PREENCHIDO OU NAO
        if (!nome || !email || !telefone || !endereco) {
            alert('Todos os campos são obrigatórios!');
            return;
        }

        //ENVIA OS DADOS
        fetch(editClientForm.action, {
            method: 'POST',
            body: new URLSearchParams(new FormData(editClientForm)),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                //ATUALIZAR TABELA
                atualizarTabela();
                //FECHAR MODAL APÓS SALVAR
                $('#modal1').modal('hide');
            } else {
                alert(data.error || 'Erro ao atualizar o cliente. Tente novamente.');
            }
        })
        .catch(err => {
            alert('Erro ao enviar dados para o servidor');
        });
    });

    //FUNÇÃO PARA ATUALIZAR TABELA
    function atualizarTabela() {
        fetch('/clientes')
            .then(response => response.json())
            .then(clientes => {
                const rows = clientes.map(cliente => {
                    return `<tr data-id="${cliente.id}">
                        <td>${cliente.id}</td>
                        <td>${cliente.nome}</td>
                        <td>${cliente.email}</td>
                        <td>${cliente.telefone}</td>
                        <td>
                            <button class="btn-edit" data-bs-toggle="modal" data-bs-target="#modal1">Editar</button>
                            <button class="delete">Excluir</button>
                        </td>
                    </tr>`;
                }).join('');
                clientTableBody.innerHTML = rows;
            });
    }

    atualizarTabela();
});
