#separando as letras
import cv2
import os
import glob

arquivos = glob.glob('data-captcha/ok/*')
for arquivo in arquivos:
    imagem = cv2.imread(arquivo)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    _, nova_imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV)
    #pegando o contorno da letra
    contornos, _ = cv2.findContours(nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #contorno das letras
    area_letras = []
    for contorno in contornos:
        (x, y, w, h) = cv2.boundingRect(contorno)
        area = cv2.contourArea(contorno)
        if area > 50:
            area_letras.append((x, y, w, h))

    # limite de letras reconhecidas === 5
    if len(area_letras) != 5:
        continue
    #desenhando os contornos e separando
    imagem_final = cv2.merge([imagem] * 3) #simula o RGB
    i = 0
    for retangulo in area_letras:
        x, y, w, h = retangulo
        imagem_letra = imagem[y:y+h+1, x:x+w+1]

        i += 1
        nome_arquivo = os.path.basename(arquivo).replace(".png", f"letra{i}.png")
        cv2.imwrite(f'data-captcha/alfabeto/{nome_arquivo}', imagem_letra)
        cv2.rectangle(imagem_final, (x-2, y-2), (x+w+2, y+h+2), (200, 52, 255), 2)
    #jogando a imagem no identificado
    nome_arquivo = os.path.basename(arquivo)
    cv2.imwrite(f"data-captcha/identificado/{nome_arquivo}", imagem_final)