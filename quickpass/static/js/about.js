// Función para manejar el menú móvil
document.addEventListener('DOMContentLoaded'), function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainMenu = document.querySelector('.main-menu');
    
    if (mobileMenuToggle && mainMenu) {
        let isMenuOpen = false;
        
        mobileMenuToggle.addEventListener('click', function() {
            isMenuOpen = !isMenuOpen;
            
            if (isMenuOpen) {
                mainMenu.style.display = 'flex';
                mainMenu.style.flexDirection = 'column';
                mainMenu.style.position = 'absolute';
                mainMenu.style.top = '100%';
                mainMenu.style.left = '0';
                mainMenu.style.right = '0';
                mainMenu.style.backgroundColor = '#fff';
                mainMenu.style.padding = '20px';
                mainMenu.style.boxShadow = '0 5px 10px rgba(0, 0, 0, 0.1)';
            } else {
                mainMenu.style.display = 'none';
            }
        });
        
        // Cerrar menú al hacer clic fuera
        document.addEventListener('click', function(event) {
            if (isMenuOpen && !event.target.closest('.main-menu') && !event.target.closest('.mobile-menu-toggle')) {
                mainMenu.style.display = 'none';
                isMenuOpen = false;
            }
        });
    }
    
    // Funcionalidad de búsqueda
    const searchIcon = document.querySelector('.search-icon');
    
    if (searchIcon) {
        searchIcon.addEventListener('click', function() {
            const searchForm = document.createElement('div');
            searchForm.className = 'search-form';
            searchForm.innerHTML = `
                <div class="search-overlay">
                    <div class="search-container">
                        <input type="text" placeholder="Buscar...">
                        <button>Buscar</button>
                        <span class="close-search">&times;</span>
                    </div>
                </div>
            `;
            
            document.body.appendChild(searchForm);
            
            // Estilos para el overlay de búsqueda
            const searchOverlay = document.querySelector('.search-overlay');
            searchOverlay.style.position = 'fixed';
            searchOverlay.style.top = '0';
            searchOverlay.style.left = '0';
            searchOverlay.style.width = '100%';
            searchOverlay.style.height = '100%';
            searchOverlay.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            searchOverlay.style.zIndex = '1000';
            searchOverlay.style.display = 'flex';
            searchOverlay.style.justifyContent = 'center';
            searchOverlay.style.alignItems = 'center';
            
            // Estilos para el contenedor de búsqueda
            const searchContainer = document.querySelector('.search-container');
            searchContainer.style.width = '80%';
            searchContainer.style.maxWidth = '600px';
            searchContainer.style.display = 'flex';
            searchContainer.style.position = 'relative';
            
            // Estilos para el input
            const searchInput = searchContainer.querySelector('input');
            searchInput.style.flex = '1';
            searchInput.style.padding = '15px';
            searchInput.style.fontSize = '16px';
            searchInput.style.border = 'none';
            searchInput.style.borderRadius = '4px 0 0 4px';
            
            // Estilos para el botón
            const searchButton = searchContainer.querySelector('button');
            searchButton.style.padding = '15px 20px';
            searchButton.style.backgroundColor = '#00a3e0';
            searchButton.style.color = '#fff';
            searchButton.style.border = 'none';
            searchButton.style.borderRadius = '0 4px 4px 0';
            searchButton.style.cursor = 'pointer';
            
            // Estilos para el botón de cerrar
            const closeButton = document.querySelector('.close-search');
            closeButton.style.position = 'absolute';
            closeButton.style.top = '-40px';
            closeButton.style.right = '0';
            closeButton.style.color = '#fff';
            closeButton.style.fontSize = '30px';
            closeButton.style.cursor = 'pointer';
            
            // Función para cerrar la búsqueda
            const closeSearch = () => {
                document.body.removeChild(searchForm);
            };
            
            closeButton.addEventListener('click', closeSearch);
            
            // Cerrar al hacer clic en el overlay
            searchOverlay.addEventListener('click', function(event) {
                if (event.target === searchOverlay) {
                    closeSearch();
                }
            });
            
            // Cerrar al presionar ESC
            document.addEventListener('keydown', function(event) {
                if (event.key === 'Escape') {
                    closeSearch();
                }
            });
            
            // Enfocar el input automáticamente
            searchInput.focus();
        });
    }
    
    // Validación del formulario de contacto
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Validar campos requeridos
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();
            const privacy = document.getElementById('privacy').checked;
            const terms = document.getElementById('terms').checked;
            
            let valid = true;
            
            // Validar nombre
            if (!name) {
                valid = false;
                showError('name', 'Por favor, introduce tu nombre');
            } else {
                removeError('name');
            }
            
            // Validar email
            if (!email) {
                valid = false;
                showError('email', 'Por favor, introduce tu correo electrónico');
            } else if (!isValidEmail(email)) {
                valid = false;
                showError('email', 'Por favor, introduce un correo electrónico válido');
            } else {
                removeError('email');
            }
            
            // Validar mensaje
            if (!message) {
                valid = false;
                showError('message', 'Por favor, introduce tu mensaje');
            } else {
                removeError('message');
            }
            
            // Validar términos y privacidad
            if (!privacy) {
                valid = false;
                showCheckboxError('privacy', 'Debes aceptar la recepción de información');
            } else {
                removeCheckboxError('privacy');
            }
            
            if (!terms) {
                valid = false;
                showCheckboxError('terms', 'Debes aceptar los términos de privacidad');
            } else {
                removeCheckboxError('terms');
            }
            
            // Si todo es válido, enviar el formulario
            if (valid) {
                // Aquí iría el código para enviar el formulario
                alert('Formulario enviado correctamente');
                contactForm.reset();
            }
        });
    }
    
    // Funciones auxiliares para la validación
    function showError(inputId, message) {
        const input = document.getElementById(inputId);
        const errorMessage = document.createElement('span');
        errorMessage.className = 'error-message';
        errorMessage.textContent = message;
        errorMessage.style.color = 'red';
        errorMessage.style.fontSize = '12px';
        errorMessage.style.display = 'block';
        errorMessage.style.marginTop = '5px';
        
        // Eliminar mensaje de error anterior si existe
        removeError(inputId);
        
        input.style.border = '1px solid red';
        input.parentElement.appendChild(errorMessage);
    }
    
    function removeError(inputId) {
        const input = document.
    }

}