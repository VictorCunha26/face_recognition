import threading # permite executar a verificação de rosto em paralelo, sem travar o vídeo
import cv2 # bibliotrca OpenCv para captura de video e manipulação de imagens 
import os # usado para navegar pela pasta com imagens de referencia
from deepface import DeepFace # biblioteca para reconhecimento facial 
from flask import Flask

app = Flask(__name__)

# Inicializa a webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)# 0 refere-se a camera padrão, cv2.CAP_DSHOW: backend do DirectShow no Windows (ajuda com problemas de captura em alguns sistemas).
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # tamanho largura
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)# tamanho altura

counter = 0 # conta os frames, usado para decidir quando verificar o rosto
face_match = False # variável global que indica se a verificação encontrou um rosto compatível(True) ou não (False)

# Carrega todas as imagens de referência de uma pasta
reference_images = []
reference_folder = "faces"  # Crie uma pasta chamada 'faces' e coloque imagens lá

for filename in os.listdir(reference_folder): # percorre todos os arquivos da pasta faces
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')): # Garante que apenas arquivos de imagem sejam processados (extensões suportadas)
        img_path = os.path.join(reference_folder, filename)# Constrói o caminho completo da imagem
        img = cv2.imread(img_path)#  lê a imagem com cv2.imread
        if img is not None:
            reference_images.append(img) # adiciona a  imagem a lista reference_images se ela foi carregada com sucesso.

def check_face(frame): # define uma função que será executada em uma thread (sequência de tarefas que um programa pode executar em paralelo para aumentar o desempenho) separada para verificar se o rosto na imagem da webcam bate com algum dos rostos da lista 
    global face_match
    match_found = False # variável local usada para guardar o resultado da verifição
    for ref_img in reference_images: # Itera sobre todas as imagens de referência carregadas
        try:
            result = DeepFace.verify(frame, ref_img.copy(), enforce_detection=False) # Compara a imagem do frame com a imagem de referência usando DeepFace.verify. enforce_detection=False evita erro caso o rosto não seja detectado (mas pode gerar falsos positivos).
            if result['verified']:
                match_found = True
                break
        except Exception as e:
            continue
    face_match = match_found # Atualiza a variável global com o resultado da verificação.

# Loop principal
while True:
    ret, frame = cap.read() # ret será True se a leitura for bem sucedida. Frame contém a imagem capturada

    if ret:
        if counter % 30 == 0:  # Verifica a cada 30 frames
            threading.Thread(target=check_face, args=(frame.copy(),)).start() # cria uma nova thread para executar check_face(frame) sem travar o vídeo. frame.copy() evita problemas de concorrência ao modificar a imagem.

        counter += 1

        if face_match:
            cv2.putText(frame, "Face Matched", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No Match", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


