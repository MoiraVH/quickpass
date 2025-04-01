// Código para manejar la subida de fotos
document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    const uploadBtn = document.getElementById('upload-btn');
    const photoUpload = document.getElementById('photo-upload');
    const profileImage = document.getElementById('profile-image');
    const currentPhoto = document.getElementById('current-photo');
    const removePhotoBtn = document.getElementById('remove-photo-btn');
    
    // El código existente para manejar el cambio de secciones
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Depuración - verificar que se está ejecutando el evento
            console.log('Click en menú:', this.getAttribute('data-section'));
            
            // Desactivar todos los menús y secciones
            document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
            document.querySelectorAll('.content-section').forEach(section => section.classList.remove('active'));
            
            // Activar el menú seleccionado
            this.classList.add('active');
            
            // Mostrar la sección correspondiente
            const sectionId = this.getAttribute('data-section');
            const targetSection = document.getElementById(sectionId);
            
            if (targetSection) {
                targetSection.classList.add('active');
                console.log('Sección activada:', sectionId);
            } else {
                console.error('No se encontró la sección:', sectionId);
            }
        });
    });
    
    // Actualizar contador de caracteres en el título
    const headlineInput = document.getElementById('headline');
    const charCount = document.querySelector('.char-count');
    
    if (headlineInput && charCount) {
        headlineInput.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = count + '/60';
        });
    }
    
    // Manejo de subida de foto de perfil
    if (uploadBtn && photoUpload) {
        uploadBtn.addEventListener('click', function() {
            photoUpload.click();
        });
        
        photoUpload.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                
                // Validar tamaño del archivo (máximo 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    showError('El archivo es demasiado grande. El tamaño máximo permitido es 5MB.');
                    return;
                }
                
                // Validar tipo de archivo
                const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
                if (!validTypes.includes(file.type)) {
                    showError('Formato de archivo no válido. Por favor sube JPG, PNG o GIF.');
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Mostrar la imagen cargada
                    profileImage.src = e.target.result;
                    profileImage.classList.remove('hidden');
                    currentPhoto.classList.add('hidden');
                    removePhotoBtn.classList.remove('hidden');
                    
                    // Aquí podrías implementar la subida al servidor si es necesario
                    console.log('Imagen lista para subir al servidor');
                    
                    // Actualizar las iniciales en la barra lateral también
                    updateSidebarAvatar(e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
        
        // Funcionalidad para eliminar la foto
        if (removePhotoBtn) {
            removePhotoBtn.addEventListener('click', function() {
                // Restablecer a las iniciales
                profileImage.classList.add('hidden');
                currentPhoto.classList.remove('hidden');
                removePhotoBtn.classList.add('hidden');
                photoUpload.value = ''; // Limpiar el input file
                
                // Restablecer avatar en la barra lateral
                resetSidebarAvatar();
                
                console.log('Foto de perfil eliminada');
            });
        }
    }
    
    // Función para mostrar mensajes de error
    function showError(message) {
        // Eliminar mensaje de error anterior si existe
        const existingError = document.getElementById('photo-upload-error');
        if (existingError) {
            existingError.remove();
        }
        
        // Crear nuevo mensaje de error
        const errorElement = document.createElement('p');
        errorElement.id = 'photo-upload-error';
        errorElement.textContent = message;
        
        // Insertar después del botón de subida
        uploadBtn.parentNode.insertBefore(errorElement, uploadBtn.nextSibling);
        
        // Limpiar el input file
        photoUpload.value = '';
    }
    
    // Función para actualizar el avatar en la barra lateral
    function updateSidebarAvatar(imageUrl) {
        const sidebarAvatar = document.querySelector('.sidebar .profile-avatar');
        if (sidebarAvatar) {
            // Guardar el contenido original de texto (iniciales)
            if (!sidebarAvatar.dataset.originalText) {
                sidebarAvatar.dataset.originalText = sidebarAvatar.textContent;
            }
            
            // Cambiar el estilo para mostrar la imagen
            sidebarAvatar.textContent = '';
            sidebarAvatar.style.backgroundImage = `url(${imageUrl})`;
            sidebarAvatar.style.backgroundSize = 'cover';
            sidebarAvatar.style.backgroundPosition = 'center';
        }
    }
    
    // Función para restablecer el avatar en la barra lateral
    function resetSidebarAvatar() {
        const sidebarAvatar = document.querySelector('.sidebar .profile-avatar');
        if (sidebarAvatar && sidebarAvatar.dataset.originalText) {
            // Restablecer al texto original (iniciales)
            sidebarAvatar.textContent = sidebarAvatar.dataset.originalText;
            sidebarAvatar.style.backgroundImage = '';
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    // Obtener la última sección activa desde localStorage
    const activeSection = localStorage.getItem("activeSection");
    
    // Si hay una sección almacenada, activarla
    if (activeSection) {
        document.querySelectorAll(".content-section").forEach(section => {
            section.classList.remove("active");
        });
        document.querySelectorAll(".menu-item").forEach(item => {
            item.classList.remove("active");
        });

        document.getElementById(activeSection)?.classList.add("active");
        document.querySelector(`[data-section="${activeSection}"]`)?.classList.add("active");
    }

    // Manejar el cambio de secciones y guardarlo en localStorage
    document.querySelectorAll(".menu-item").forEach(item => {
        item.addEventListener("click", function () {
            const section = this.getAttribute("data-section");

            // Remover clases activas
            document.querySelectorAll(".content-section").forEach(section => {
                section.classList.remove("active");
            });
            document.querySelectorAll(".menu-item").forEach(item => {
                item.classList.remove("active");
            });

            // Activar la nueva sección
            document.getElementById(section)?.classList.add("active");
            this.classList.add("active");

            // Guardar la sección activa en localStorage
            localStorage.setItem("activeSection", section);
        });
    });
});
