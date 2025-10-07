document.getElementById("upload").addEventListener("change", function(){
    let file = this.files[0];
    let formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => alert(data))
    .catch(err => console.error(err));
});

    function reconhecer() {
      fetch('http://127.0.0.1:5000/reconhecer')   // <<-- porta do BACKEND
        .then(r => r.json())
        .then(data => alert(data.status || 'OK'))
        .catch(err => alert('Erro: ' + err));
    }

