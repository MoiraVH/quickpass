document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todas las tarjetas de casetas
    const casetaCards = document.querySelectorAll('.caseta-card');
    
    // Agregar evento de clic a cada tarjeta
    casetaCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Evitar que se active si se hizo clic en el botón (el formulario se encargará)
            if (e.target.tagName !== 'BUTTON') {
                // Obtener el ID de la caseta desde el atributo data
                const casetaId = this.getAttribute('data-caseta-id');
                
                // Resaltar la tarjeta seleccionada y quitar resaltado de las demás
                casetaCards.forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                
                // Opcional: Autoenviar el formulario al hacer clic en la tarjeta
                // const form = this.querySelector('form');
                // if (form) form.submit();
            }
        });
    });
    
    // Añadir estilo para tarjetas seleccionadas
    const style = document.createElement('style');
    style.textContent = `
        .caseta-card.selected {
            border: 2px solid #4f46e5;
            background-color: #f9f9ff;
        }
    `;
    document.head.appendChild(style);
    
    // Filtrar casetas por estado (si implementamos un filtro)
    const filterButtons = document.querySelectorAll('.filter-btn');
    if (filterButtons.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                const filter = this.getAttribute('data-filter');
                
                // Activar botón seleccionado
                filterButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                // Mostrar/ocultar casetas según el filtro
                casetaCards.forEach(card => {
                    if (filter === 'all') {
                        card.style.display = 'block';
                    } else {
                        const status = card.querySelector('.caseta-status').classList[1];
                        card.style.display = (status === filter) ? 'block' : 'none';
                    }
                });
            });
        });
    }
});