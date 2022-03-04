#testando captchas 02
import cv2
import os
import glob
from PIL import Image
from matplotlib import pyplot as plt

def tratar_imagens(pasta_origem, pasta_destino='data-captcha/ok'):
    # primeiro tratamento
    arquivos = glob.glob(f"{pasta_origem}/*")
    for arquivo in arquivos:
        img = cv2.imread(arquivo)
        img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img_tratada = cv2.threshold(img_cinza, 150, 255, cv2.THRESH_TRUNC or cv2.THRESH_OTSU)
        nome_arquivo = os.path.basename(arquivo)
        cv2.imwrite(f'{pasta_destino}/{nome_arquivo}', img_tratada)

    # segundo tratamento
    arquivos = glob.glob(f"{pasta_destino}/*")
    for arquivo in arquivos:
        img = cv2.imread(arquivo)
        img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img_tratada = cv2.threshold(img_cinza, 25, 255, cv2.THRESH_BINARY or cv2.THRESH_OTSU)
        nome_arquivo = os.path.basename(arquivo)
        cv2.imwrite(f'{pasta_destino}/{nome_arquivo}', img_tratada)


if __name__ == "__main__":
    tratar_imagens('data-captcha/bloco')