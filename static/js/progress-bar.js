function ProgressMeta() {
    const lucrosProdutos = produtos.map(produto => parseFloat(produto.lucro)); 
    let lucroAtual = lucrosProdutos.reduce((acc, current)=> acc + current, 0);
    var bar = document.getElementById('ProgressBar');
    const Meta = 100000;
    let width = (lucroAtual/meta)*100;

    // Garante que a barra não ultrapasse 100%
    if (width > 100){
        width=100;
    }
    
    const intervalo = setInterval(() => {
        if (width >= meta){
            clearInterval(intervalo);
        } else {
            width++;
            bar.style.width = width + '%'
        }
    }, 100);
};