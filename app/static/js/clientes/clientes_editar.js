// Cerrar mensajes flash
document.querySelectorAll('.close-flash').forEach(button => {
  button.addEventListener('click', (e) => {
    const alertBox = e.target.closest('.alert');
    if (alertBox) {
      alertBox.style.display = 'none';
    }
  });
});

// Validación del formulario de edición
document.getElementById('editarClienteForm')?.addEventListener('submit', function (e) {
  const nombreInput = document.getElementById('nombre');
  const nombre = nombreInput.value.trim();

  // Resetear posibles errores previos
  nombreInput.classList.remove('input-error');

  if (!nombre) {
    e.preventDefault();
    nombreInput.focus();
    nombreInput.classList.add('input-error');
    Swal.fire({
      icon: 'error',
      title: 'Campo requerido',
      text: 'El nombre es obligatorio'
    });
    return;
  }

  if (nombre.length < 3 || nombre.length > 100) {
    e.preventDefault();
    nombreInput.focus();
    nombreInput.classList.add('input-error');
    Swal.fire({
      icon: 'error',
      title: 'Longitud inválida',
      text: 'El nombre debe tener entre 3 y 100 caracteres'
    });
    return;
  }
});
