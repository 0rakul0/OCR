# solucionando cap
import os

from keras.models import load_model
from util.helpers import resize_to_fit
from imutils import paths
import numpy as np
import cv2
import pickle

# processos
from ocr_captcha03 import tratar_imagens


# passos importar o modelo e importar tradutor
# modelo treinado
# rotulos_modelo

def quebra_cap():
    # tradutor
    with open("rotulos_modelo.dat", "rb") as arquivo_tradutor:
        lb = pickle.load(arquivo_tradutor)

    # modelo
    modelo = load_model("modelo_quebra_cap_treinado.hdf5")

    # usando o modelo >> ler todos os arquivos da pasta cap_resolver
    # processo ->> tratar >> identificar >> pegar as letras para o modelo >> transformar em texto
    # tratar
    tratar_imagens("data-captcha/cap_resolver/", pasta_destino="data-captcha/cap_resolver/")
    # identificar
    arquivos = list(paths.list_images("data-captcha/cap_resolver/"))
    for arquivo in arquivos:
        imagem = cv2.imread(arquivo)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        _, nova_imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV)
        # pegando o contorno da letra
        contornos, _ = cv2.findContours(nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # contorno das letras
        area_letras = []
        for contorno in contornos:
            (x, y, w, h) = cv2.boundingRect(contorno)
            area = cv2.contourArea(contorno)
            if area > 150:
                area_letras.append((x, y, w, h))

        # pondo o texto de saida em ordem
        area_letras = sorted(area_letras, key=lambda x: x[0])

        # desenhando os contornos e separando
        imagem_final = cv2.merge([imagem] * 3)  # simula o RGB

        previsao = []
        i = 0
        for retangulo in area_letras:
            x, y, w, h = retangulo
            imagem_letra = imagem[y:y + h + 1, x:x + w + 1]

            # da a letra para o modelo
            imagem_letra = resize_to_fit(imagem_letra, 20, 20)

            # pondo 4 dimensões
            imagem_letra = np.expand_dims(imagem_letra, axis=2)
            imagem_letra = np.expand_dims(imagem_letra, axis=0)

            # jogando a letra no modelo
            letra_prevista = modelo.predict(imagem_letra)
            letra_prevista = lb.inverse_transform(letra_prevista)[0]
            previsao.append(letra_prevista)

        texto_previsao = "".join(previsao)
        return texto_previsao


if __name__ == "__main__":
    quebra_cap()