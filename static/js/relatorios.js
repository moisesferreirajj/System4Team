document.querySelectorAll('[data-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el, {
        title: el.getAttribute('data-bs-original-title')
    });
});
