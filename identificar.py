import threading # permite executar a verificação de rosto em paralelo, sem travar o vídeo
import cv2 # bibliotrca OpenCv para captura de video e manipulação de imagens 
import os # usado para navegar pela pasta com imagens de referencia
from deepface import DeepFace # biblioteca para reconhecimento facial 
from flask import Flask
from database import Database
from datetime import datetime

app = Flask(__name__)

# Inicializa a webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)# 0 refere-se a camera padrão, cv2.CAP_DSHOW: backend do DirectShow no Windows (ajuda com problemas de captura em alguns sistemas).
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # tamanho largura
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)# tamanho altura

counter = 0 # conta os frames, usado para decidir quando verificar o rosto
face_match = False # variável global que indica se a verificação encontrou um rosto compatível(True) ou não (False)
nome_identificado = None
nomes_salvos = set()

# Carrega todas as imagens de referência de uma pasta
reference_images = []
reference_names = []
reference_folder = "faces"  # Crie uma pasta chamada 'faces' e coloque imagens lá

for filename in os.listdir(reference_folder): # percorre todos os arquivos da pasta faces
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')): # Garante que apenas arquivos de imagem sejam processados (extensões suportadas)
        img_path = os.path.join(reference_folder, filename)# Constrói o caminho completo da imagem
        img = cv2.imread(img_path)#  lê a imagem com cv2.imread
        if img is not None:
            reference_images.append(img) # adiciona a  imagem a lista reference_images se ela foi carregada com sucesso.
            reference_names.append(os.path.splitext(filename)[0])

def salvar_no_banco(nome):
    if nome in nomes_salvos:
        return
    
    try:
        db = Database()
        db.conectar()
        if db.is_connected():
            sql = "INSERT INTO alunos (nome_aluno, data_horario) VALUES (%s, %s)"
            data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.executar(sql, (nome, data_hora))
            print(f"[DB] {nome} salvo no banco de dados MySQl com sucesso")
            nomes_salvos.add(nome)
        db.desconectar()
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")

def check_face(frame): # define uma função que será executada em uma thread (sequência de tarefas que um programa pode executar em paralelo para aumentar o desempenho) separada para verificar se o rosto na imagem da webcam bate com algum dos rostos da lista 
    global face_match, nome_identificado
    match_found = False # variável local usada para guardar o resultado da verifição
    nome = None
    for ref_img, ref_name in zip(reference_images, reference_names): # Itera sobre todas as imagens de referência carregadas
        try:
            result = DeepFace.verify(frame, ref_img.copy(), enforce_detection=True) # Compara a imagem do frame com a imagem de referência usando DeepFace.verify. enforce_detection=False evita erro caso o rosto não seja detectado (mas pode gerar falsos positivos).
            if result['verified']:
                match_found = True
                nome = ref_name
                break
        except Exception as e:
            continue
    face_match = match_found # Atualiza a variável global com o resultado da verificação.

    if match_found:
        salvar_no_banco(nome)
        nome_identificado = nome
        face_match = True
    else:
        face_match = False
        nome_identificado = None

# Loop principal
while True:
    ret, frame = cap.read() # ret será True se a leitura for bem sucedida. Frame contém a imagem capturada

    if ret:
        if counter % 30 == 0:  # Verifica a cada 30 frames
            threading.Thread(target=check_face, args=(frame.copy(),)).start() # cria uma nova thread para executar check_face(frame) sem travar o vídeo. frame.copy() evita problemas de concorrência ao modificar a imagem.

        counter += 1

        if face_match and nome_identificado:
            texto = f"Face: {nome_identificado}"
            cor = (0, 255, 0)
        else:
            texto = "Nenhum rosto reconhecido"
            cor = (0, 0, 255)

        cv2.putText(frame, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, cor, 2)
        cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()