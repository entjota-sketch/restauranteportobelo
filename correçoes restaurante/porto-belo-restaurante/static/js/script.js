// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling para enlaces de ancla
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = target.offsetTop - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Cerrar navbar móvil si está abierto
                const navbarToggler = document.querySelector('.navbar-toggler');
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            }
        });
    });

    // Establecer la fecha mínima para el campo de fecha (hoy)
    const fechaInput = document.getElementById('fecha');
    if (fechaInput) {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        fechaInput.min = `${year}-${month}-${day}`;
    }

    // Manejar mensajes flash
    const flashes = document.querySelectorAll('.alert');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.display = 'none';
        }, 5000);
    });

    // Validación de horario de reserva
    const horaInput = document.getElementById('hora');
    if (horaInput) {
        horaInput.addEventListener('change', function() {
            const hora = this.value;
            if (hora) {
                const [hours, minutes] = hora.split(':').map(Number);
                if (hours < 13 || (hours === 13 && minutes < 30) || (hours > 16 && hours < 20) || (hours === 16 && minutes > 0) || hours > 23 || (hours === 23 && minutes > 0)) {
                    alert('El horario de atención es:\nComidas 13:30h a lás 16:00h (La cocina cierra a lás 15:00h)\nCenas 20:30h a lás 23:00h (la cocina cierra a lás 22:00h)');
                    this.value = '';
                }
            }
        });
    }
});

// Navbar background change on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.backgroundColor = '#6B3E12';
    } else {
        navbar.style.backgroundColor = '#8B4513';
    }
});