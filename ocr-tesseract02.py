import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#caminho da imagem
#imagem = cv2.imread("img/imgem.png")
imagem = cv2.imread("data-captcha/ok/telanova0.png")

#tratando a imagem
imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

config_tesseract = '--tessdata-dir tessdata'
#conversão imagem >> texto
texto = pytesseract.image_to_string(imagem, lang="por", config=config_tesseract)

# shape da imagem
hImg, wImg, _ = imagem.shape
box = pytesseract.image_to_boxes(imagem)

#identificando letras
for b in box.splitlines():
    b = b.split(' ')
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    #seleciona o caractere da imagem
    cv2.rectangle(imagem, (x, hImg-y), (w, hImg-h), (0, 0, 255), 2)
    #poem uma legenda na letra identificada
    cv2.putText(imagem, b[0], (x, hImg-y+30), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
    #saida de dados
    print(b)

#o imagem_to_data identifica um bloco de caracteres
#box = pytesseract.image_to_data(imagem)
#identificando palavras
#for x, b in enumerate(box.splitlines()):
#    if x != 0:
#        b = b.split()
#        if len(b) == 12:
            #print(b)
#            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            #seleciona a palavra da imagem
#            cv2.rectangle(imagem, (x, y), (w+x, h+y), (0, 0, 255), 2)
            #poem uma legenda na palavra identificada
#            cv2.putText(imagem, b[11], (x+30, y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
            #saida de dados
#            print(b[11])

#mostrando a imagem
cv2.imshow("imagem", imagem) #lembrando que o canal está no BGR
cv2.waitKey(0)
