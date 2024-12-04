document.addEventListener('DOMContentLoaded', function() {    
    const form = document.getElementById('cad');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();  // EVITA O ENVIO PADRÃO DO FORMULÁRIO

            // ADICIONAR CLIENTE - ROUTE - POST
            const formData = new FormData(this);
            fetch('json/adicionar_cliente', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  // MOSTRA O ALERTA COM A RESPOSTA DO /JSON/ADICIONAR_CLIENTE
                    const modal = bootstrap.Modal.getInstance(document.getElementById('add'));
                    modal.hide(); // FECHA O MODAL
                    location.reload();  // RECARREGA PARA APARECER A INFO
                } else if (data.error) {
                    alert(data.error);  // MOSTRA O ERRO
                }
            })
            .catch(error => alert('Erro ao adicionar cliente: ' + error));
        });
    } else {
        console.error('Formulário com ID "cad" não encontrado.');
    }

    // EDIÇÃO DE CLIENTE
    const editForm = document.querySelector('#modal1 form');
    if (editForm) {
        const modal = new bootstrap.Modal(document.getElementById('modal1'));
        const editButton = document.querySelectorAll('.btn-edit');
        editButton.forEach(button => {
            button.addEventListener('click', function() {

                // BUSCA O CLIENTE - ROUTE - GET
                const clienteId = button.getAttribute('data-id');
                fetch(`/json/buscar-cliente/${clienteId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data) {
                            const cliente = data;
                            editForm.querySelector('input[name="nome"]').value = cliente.nome;
                            editForm.querySelector('input[name="email"]').value = cliente.email;
                            editForm.querySelector('input[name="telefone"]').value = cliente.telefone;
                            editForm.querySelector('input[name="endereco"]').value = cliente.endereco;
                            editForm.setAttribute('data-id', cliente.id);  // ID DO CLIENTE PARA SER ENVIADO VIA POST
                        } else {
                            alert('Dados do cliente não encontrados.');
                        }
                    })
                    .catch(error => alert('Erro ao carregar dados do cliente: ' + error));

                modal.show();  // MOSTRA O MODAL
            });
        });

        // AO ACEITAR A EDIÇÃO
        editForm.addEventListener('submit', function(event) {
            event.preventDefault();  // ENVIA O FORMULÁRIO
            const clienteId = editForm.getAttribute('data-id');  // PEGA O ID DO CLIENTE
            if (!clienteId) {
                alert('ID do cliente não encontrado.');  // VERIFICA SE O ID DO CLIENTE EXISTE
                return;
            }

            // EDITA O CLIENTE - ROUTE - POST
            const formData = new FormData(editForm);
            fetch(`/json/editar-cliente/${clienteId}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  // MOSTRA O ALERTA COM A RESPOSTA DO /JSON/EDITAR_CLIENTE
                    const modal = bootstrap.Modal.getInstance(document.getElementById('modal1'));
                    modal.hide();  // FECHA O MODAL
                    location.reload();  // RECARREGA PARA APARECER A INFO
                } else if (data.error) {
                    alert(data.error);  // MOSTRA O ERRO
                }
            })
            .catch(error => alert('Erro ao editar cliente: ' + error));
        });

    }
});
