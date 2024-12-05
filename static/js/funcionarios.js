document.addEventListener('DOMContentLoaded', function() {    
    const form = document.getElementById('cad');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();  // EVITA O ENVIO PADRÃO DO FORMULÁRIO

            // ADICIONAR funcionario - ROUTE - POST
            const formData = new FormData(this);
            fetch('json/adicionar_funcionario', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  // MOSTRA O ALERTA COM A RESPOSTA DO /JSON/ADICIONAR_FUNCIONARIO
                    const modal = bootstrap.Modal.getInstance(document.getElementById('add'));
                    modal.hide(); // FECHA O MODAL
                    location.reload();  // RECARREGA PARA APARECER A INFO
                } else if (data.error) {
                    alert(data.error);  // MOSTRA O ERRO
                }
            })
            .catch(error => alert('Erro ao adicionar funcionario: ' + error));
        });
    } else {
        console.error('Formulário com ID "cad" não encontrado.');
    }

    // EDIÇÃO DE funcionario
    const editForm = document.querySelector('#modal1 form');
    if (editForm) {
        const modal = new bootstrap.Modal(document.getElementById('modal1'));
        const editButton = document.querySelectorAll('.btn-edit');
        editButton.forEach(button => {
            button.addEventListener('click', function() {

                // BUSCA O funcionario - ROUTE - GET
                const funcionarioId = button.getAttribute('data-id');
                fetch(`/json/buscar-funcionario/${funcionarioId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data) {
                            const funcionario = data;
                            editForm.querySelector('input[name="nome"]').value = funcionario.nome;
                            editForm.querySelector('input[name="email"]').value = funcionario.email;
                            editForm.querySelector('input[name="telefone"]').value = funcionario.telefone;                            editForm.setAttribute('data-id', funcionario.id);  // ID DO FUNCIONARIO PARA SER ENVIADO VIA POST
                        } else {
                            alert('Dados do funcionario não encontrados.');
                        }
                    })
                    .catch(error => alert('Erro ao carregar dados do funcionario: ' + error));

                modal.show();  // MOSTRA O MODAL
            });
        });

        // AO ACEITAR A EDIÇÃO
        editForm.addEventListener('submit', function(event) {
            event.preventDefault();  // ENVIA O FORMULÁRIO
            const funcionarioId = editForm.getAttribute('data-id');  // PEGA O ID DO funcionario
            if (!funcionarioId) {
                alert('ID do funcionario não encontrado.');  // VERIFICA SE O ID DO funcionario EXISTE
                return;
            }

            // EDITA O funcionario - ROUTE - POST
            const formData = new FormData(editForm);
            fetch(`/json/editar-funcionario/${funcionarioId}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  // MOSTRA O ALERTA COM A RESPOSTA DO /JSON/EDITAR_funcionario
                    const modal = bootstrap.Modal.getInstance(document.getElementById('modal1'));
                    modal.hide();  // FECHA O MODAL
                    location.reload();  // RECARREGA PARA APARECER A INFO
                } else if (data.error) {
                    alert(data.error);  // MOSTRA O ERRO
                }
            })
            .catch(error => alert('Erro ao editar funcionario: ' + error));
        });

    }
});
