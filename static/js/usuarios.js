document.addEventListener('DOMContentLoaded', function() {    
    const editForm = document.querySelector('#editmodal form');
    if (editForm) {
        const modal = new bootstrap.Modal(document.getElementById('editmodal'));
        const editButton = document.querySelectorAll('.btn-edit');
        editButton.forEach(button => {
            button.addEventListener('click', function() {

                //BUSCA O USUARIO - Route - GET
                const usuarioId = button.getAttribute('data-id');
                fetch(`/json/buscar_usuario/${usuarioId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data) {
                            const usuario = data;
                            editForm.querySelector('input[name="username"]').value = usuario.username;
                            editForm.querySelector('input[name="email"]').value = usuario.email;
                            editForm.querySelector('input[name="cargo"]').value = usuario.cargo;
                            editForm.querySelector('input[name="funcionario"]').value = usuario.funcionario;
                            editForm.setAttribute('data-id', usuario.id);  // ID DO USUARIO PARA SER ENVIADO VIA POST
                        } else {
                            alert('Dados do usuário não encontrados.');
                        }
                    })
                    .catch(error => alert('Erro ao carregar dados do usuário: ' + error));

                modal.show();  //MOSTRA O MODAL "EDIT"
            });
        });

        // AO ACEITAR A EDIÇÃO
        editForm.addEventListener('submit', function(event) {
            event.preventDefault(); // ENVIA O FORMULARIO
            const usuarioId = editForm.getAttribute('data-id');  // PEGA O ID DO USUÁRIO
            if (!usuarioId) {
                alert('ID do usuário não encontrado.');  // VERIFICA SE O ID EXISTE
                return;
            }

            // EDITA O USUÁRIO COM O DATA-ID - Route - POST
            const formData = new FormData(editForm);
            fetch(`/json/editar_usuario/${usuarioId}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  // MOSTRA O ALERTA DO /json/editar_usuario
                    const modal = bootstrap.Modal.getInstance(document.getElementById('editmodal'));
                    modal.hide();  // FECHA O MODAL
                    location.reload();   // RECARREGA PARA APARECER A INFO
                } else if (data.error) {
                    alert(data.error);  // MOSTRA O ERRO
                }
            })
            .catch(error => alert('Erro ao editar usuário: ' + error));
        });
    }
});
