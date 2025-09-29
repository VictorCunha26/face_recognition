from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# pasta onde as fotos vão ser salvas
UPLOAD_FOLDER = "faces"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "Nenhum arquivo enviado", 400
    file = request.files["file"]
    if file.filename == "":
        return "Arquivo inválido", 400

    # salvar dentro da pasta faces
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    return f"Foto {file.filename} salva com sucesso em {UPLOAD_FOLDER}!"

@app.route("/reconhecer", methods=["POST"])
def reconhecer():
    # Aqui você pode chamar seu programa de reconhecimento
    return "Reconhecimento em andamento..."

if __name__ == "__main__":
    app.run(debug=True)
