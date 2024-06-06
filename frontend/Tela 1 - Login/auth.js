document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('login-form').addEventListener('submit', async function(event) {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const senha = document.getElementById('password').value; // Altere a variável para 'senha'

      try {
          const response = await fetch('http://127.0.0.1:5000/login', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ email, senha }) // Envie 'senha' ao invés de 'password'
          });

          if (response.ok) {
              const data = await response.json();
              localStorage.setItem('access_token', data.access_token);
              localStorage.setItem('refresh_token', data.access_token);
              window.location.href = '../Tela 2 - Inicio/tela2.html';
          } else {
              alert('Login failed. Please check your credentials.');
          }
      } catch (error) {
          console.error('Error:', error);
      }
  });

  async function getAccessToken() {
      const refresh_token = localStorage.getItem('refresh_token');

      try {
          const response = await fetch('http://127.0.0.1:5000/refresh', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${refresh_token}`
              }
          });

          if (response.ok) {
              const data = await response.json();
              localStorage.setItem('access_token', data.access_token);
              return data.access_token;
          } else {
              alert('Session expired. Please log in again.');
              window.location.href = '../Tela 1 - Login/tela1.html';
          }
      } catch (error) {
          console.error('Error:', error);
      }
  }
  setInterval(getAccessToken, 600000);
});
