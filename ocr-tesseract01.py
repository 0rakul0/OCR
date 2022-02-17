import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

#caminho da imagem
imagem = cv2.imread("img/imgem.png")
imagem_dois = cv2.imread("img/sem_sofrencia.png")

#mostrando a imagem
cv2.imshow("imagem",imagem_dois) #lembrando que o canal está no BGR

#comando para conveter o canal para de BGR para RGB
imagem = cv2.cvtColor(imagem_dois, cv2.COLOR_BGR2RGB)
cv2.waitKey(0)

config_tesseract = '--tessdata-dir tessdata'
#conversão imagem >> texto
texto = pytesseract.image_to_string(imagem, lang="por", config=config_tesseract)

#saida de informação
print(texto)