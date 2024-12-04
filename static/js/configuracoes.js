document.addEventListener('DOMContentLoaded', function() {
    const alterarImagemBtn = document.getElementById('alterar_imagem_btn');
    const uploadImagemForm = document.getElementById('upload_imagem_form');
    const imagemInput = document.getElementById('imagem_input');

    if (alterarImagemBtn && uploadImagemForm && imagemInput) {
        alterarImagemBtn.addEventListener('click', function() {
            if (uploadImagemForm.style.display === 'block') {
                //SE O USUARIO ESTIVER VISIVEL E O USUARIO CLICAR NOVAMENTE NO ALTERAR IMAGEM, RECOLHA ELE
                uploadImagemForm.style.display = 'none';
            } else {
                //SE ESTIVER OCULTO EXIBA ELE
                uploadImagemForm.style.display = 'block';
            }
        });

        //EVENTO PARA ENVIAR A IMAGEM DIRETAMENTE APÓS SELECIONAR ELA
        imagemInput.addEventListener('change', function() {
            if (imagemInput.files && imagemInput.files[0]) {
                uploadImagemForm.submit(); //ENVIA O FORMULÁRIO APÓS SELECIONAR IMAGEM
            }
        });
    }
});
