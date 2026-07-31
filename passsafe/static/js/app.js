document.addEventListener('click', function (event) {
  if (event.target.matches('.copy-button')) {
    const password = event.target.dataset.password;
    if (!password) return;
    navigator.clipboard.writeText(password).then(() => {
      alert('Contraseña copiada al portapapeles');
    });
    return;
  }

  if (event.target.matches('.toggle-password')) {
    const card = event.target.closest('.credential-card');
    if (!card) return;
    const input = card.querySelector('.password-field');
    if (!input) return;
    const isHidden = input.type === 'password';
    input.type = isHidden ? 'text' : 'password';
    event.target.textContent = isHidden ? 'Ocultar' : 'Ver';
  }
});
