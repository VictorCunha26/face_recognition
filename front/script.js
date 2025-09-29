  document.getElementById('fileInput').addEventListener('change', function() {
      if (this.files.length > 0) {
        console.log("Arquivo selecionado:", this.files[0].name);
      }
    });

    function reconhecer() {
    fetch('/reconhecer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({}) // envie dados se necessário
    })
    .then(response => response.json())
    .then(data => {
      alert(data.mensagem); // ou console.log(data), dependendo do que quer fazer
    })
    .catch(error => {
      console.error('Erro:', error);
    });
  }

