document.addEventListener("DOMContentLoaded", function() {
  const input = document.getElementById("fileInpu");
  if (input) {
    input.addEventListener("change", function() {
      console.log("Arquivo selecionado!");
    });
  }
});


    function reconhecer() {
      fetch('http://127.0.0.1:5000/reconhecer')   // <<-- porta do BACKEND
        .then(r => r.json())
        .then(data => alert(data.status || 'OK'))
        .catch(err => alert('Erro: ' + err));
    }

