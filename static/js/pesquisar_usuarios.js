document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.querySelector('.search');
    const searchInput = document.querySelector('.input');
    const tabelaUsuarios = document.querySelector('#tabela-usuarios');  // Referência para o corpo da tabela

    // Função para atualizar a tabela com os resultados da pesquisa
    function updateTable(users) {
        // Limpa o corpo da tabela
        tabelaUsuarios.innerHTML = '';

        if (users.length === 0) {
            tabelaUsuarios.innerHTML = '<tr><td colspan="5">Nenhum usuário encontrado.</td></tr>';
            return;
        }

        // Preenche a tabela com os novos usuários
        users.forEach(user => {
            const tr = document.createElement('tr');
            tr.classList.add('fields');
            tr.innerHTML = `
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${user.cargo}</td>
                <td>${user.funcionario ? user.funcionario : 'N/A'}</td>
                <td class="actions">
                    <button class="btn-edit" type="button" data-bs-toggle="modal" data-bs-target="#editmodal" data-id="${user.id}">Editar</button>
                </td>
            `;
            tabelaUsuarios.appendChild(tr);
        });
    }

    // Função para pesquisar usuários
    function searchUsers(query) {
        // Se a consulta estiver vazia, carrega todos os usuários
        if (!query) {
            // Chame a rota para carregar todos os usuários, ou use um array de todos os usuários caso você já tenha esses dados no frontend
            fetch('/json/listar_usuarios')
                .then(response => response.json())
                .then(data => {
                    updateTable(data);
                })
                .catch(error => {
                    console.error('Erro ao carregar todos os usuários:', error);
                    updateTable([]);  // Limpa a tabela em caso de erro
                });
        } else {
            fetch(`/json/pesquisar_usuario?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error || data.message) {
                        updateTable([]);  // Se não encontrar, mostra uma mensagem vazia
                    } else {
                        updateTable(data);  // Atualiza a tabela com os resultados encontrados
                    }
                })
                .catch(error => {
                    console.error('Erro na busca:', error);
                    updateTable([]);  // Limpa a tabela em caso de erro
                });
        }
    }

    // Evento de digitação para disparar a pesquisa
    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();
        if (query.length >= 3) {  // Inicia a pesquisa depois de 3 caracteres
            searchUsers(query);
        } else {
            // Se a pesquisa for muito curta, recarrega a tabela original
            searchUsers('');
        }
    });

    // Evento de clique no botão de pesquisa
    searchButton.addEventListener('click', function() {
        const query = searchInput.value.trim();
        if (query.length >= 3) {
            searchUsers(query);
        } else {
            searchUsers('');  // Recarrega a tabela original se a pesquisa estiver vazia
        }
    });
});
