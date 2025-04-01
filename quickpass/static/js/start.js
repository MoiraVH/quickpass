// Animación de entrada en el viewport
document.addEventListener("DOMContentLoaded", () => {
    const fadeElements = document.querySelectorAll('.fade-in'); // Todos los elementos con la clase fade-in

    const options = {
        root: null, // Observamos desde el viewport
        rootMargin: '0px', // Sin margen extra
        threshold: 0.1 // Se activa cuando el 10% del elemento es visible
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-visible'); // Agrega la clase de animación
                observer.unobserve(entry.target); // Deja de observar el elemento
            }
        });
    }, options);

    fadeElements.forEach(element => {
        observer.observe(element); // Comienza a observar cada elemento
    });
});

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded'), function() {
    // Mobile navigation toggle
    const mobileNavToggle = document.createElement('div');
    mobileNavToggle.className = 'mobile-nav-toggle';
    mobileNavToggle.innerHTML = '<i class="fas fa-bars"></i>';
    document.querySelector('.top-nav .container').appendChild(mobileNavToggle);
    
    mobileNavToggle.addEventListener('click', function() {
        document.querySelector('.nav-links').classList.toggle('active');
    });
    
    // Add responsive navigation class and modify styles for mobile view
    const mediaQuery = window.matchMedia('(max-width: 768px)');
    
    function handleMobileNav(e) {
        if (e.matches) {
            document.querySelector('.nav-links').style.display = 'none';
            document.querySelector('.nav-links').classList.add('mobile');
        } else {
            document.querySelector('.nav-links').style.display = 'block';
            document.querySelector('.nav-links').classList.remove('mobile');
            document.querySelector('.nav-links').classList.remove('active');
        }
    }
    
    mediaQuery.addListener(handleMobileNav);
    handleMobileNav(mediaQuery);
    
    // Slider functionality for projects section
    const projectSlider = {
        currentSlide: 1,
        totalSlides: 4,
        container: document.querySelector('.projects'),
        updateCounter: function() {
            this.container.querySelector('.counter .number:first-child').textContent = 
                String(this.currentSlide).padStart(2, '0');
        },
        next: function() {
            this.currentSlide = this.currentSlide === this.totalSlides ? 1 : this.currentSlide + 1;
            this.updateCounter();
            // Here you would add code to actually change the slide content
        },
        prev: function() {
            this.currentSlide = this.currentSlide === 1 ? this.totalSlides : this.currentSlide - 1;
            this.updateCounter();
            // Here you would add code to actually change the slide content
        },
        init: function() {
            const that = this;
            this.container.querySelector('.arrow.right').addEventListener('click', function() {
                that.next();
            });
            this.container.querySelector('.arrow.left').addEventListener('click', function() {
                that.prev();
            });
        }
    };
    
    // Slider functionality for value creation section
    const valueSlider = {
        currentSlide: 1,
        totalSlides: 4,
        container: document.querySelector('.value-creation'),
        updateCounter: function() {
            this.container.querySelector('.counter .number:first-child').textContent = 
                String(this.currentSlide).padStart(2, '0');
        },
        next: function() {
            this.currentSlide = this.currentSlide === this.totalSlides ? 1 : this.currentSlide + 1;
            this.updateCounter();
            // Here you would add code to actually change the slide content
        },
        prev: function() {
            this.currentSlide = this.currentSlide === 1 ? this.totalSlides : this.currentSlide - 1;
            this.updateCounter();
            // Here you would add code to actually change the slide content
        },
        init: function() {
            const that = this;
            this.container.querySelector('.arrow.right').addEventListener('click', function() {
                that.next();
            });
            this.container.querySelector('.arrow.left').addEventListener('click', function() {
                that.prev();
            });
        }
    };
    
    // Initialize sliders
    projectSlider.init();
    valueSlider.init();
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Adjust for fixed header
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Sticky navigation
    const navbar = document.querySelector('.top-nav');
    const navbarOffset = navbar.offsetTop;
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > navbarOffset) {
            navbar.classList.add('sticky');
        } else {
            navbar.classList.remove('sticky');
        }
    });
    
    // Animation on scroll
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    function checkIfInView() {
        const windowHeight = window.innerHeight;
        const windowTopPosition = window.pageYOffset;
        const windowBottomPosition = windowTopPosition + windowHeight;
        
        animateElements.forEach(element => {
            const elementHeight = element.offsetHeight;
            const elementTopPosition = element.offsetTop;
            const elementBottomPosition = elementTopPosition + elementHeight;
            
            // Check if element is in view
            if (
                (elementBottomPosition >= windowTopPosition) &&
                (elementTopPosition <= windowBottomPosition)
            ) {
                element.classList.add('visible');
            }
        });
    }
    
    // Add animate-on-scroll class to sections
    document.querySelectorAll('section').forEach(section => {
        section.classList.add('animate-on-scroll');
    });
    
    window.addEventListener('scroll', checkIfInView);
    window.addEventListener('resize', check);
}