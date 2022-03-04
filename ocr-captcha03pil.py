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
        _, img_tratada = cv2.threshold(img_cinza, 155, 255, cv2.THRESH_TRUNC or cv2.THRESH_OTSU)
        nome_arquivo = os.path.basename(arquivo)
        cv2.imwrite(f'{pasta_destino}/{nome_arquivo}', img_tratada)

    # segundo tratamento
    arquivos = glob.glob(f"{pasta_destino}/*")
    for arquivo in arquivos:
        im = Image.open(arquivo)
        im = im.convert("P")
        im2 = Image.new("P", im.size, 255)
        temp = {}
        for x in range(im.size[1]):
            for y in range(im.size[0]):
                pix = im.getpixel((y, x))
                temp[pix] = pix
                if pix > 115:
                    im2.putpixel((y, x), 0)
        im2.save(f'{pasta_destino}/{nome_arquivo}')

    # terceiro tratamento
    arquivos = glob.glob(f"{pasta_destino}/*")
    for arquivo in arquivos:
        img = cv2.imread(arquivo)
        img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img_tratada = cv2.threshold(img_cinza, 30, 255, cv2.THRESH_BINARY or cv2.THRESH_OTSU)
        nome_arquivo = os.path.basename(arquivo)
        cv2.imwrite(f'{pasta_destino}/{nome_arquivo}', img_tratada)

if __name__ == "__main__":
    tratar_imagens('data-captcha/bloco')