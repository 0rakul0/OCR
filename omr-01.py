import cv2
import numpy as np
import utlis

# configurações inicias
path = 'img/1.jpg'
widthImg = 450
heigthImg = 450
questoes = 5
escolhas = 5
ans = [1, 2, 0, 1, 4]  # <- resposta
# imagem
img = cv2.imread(path)
webCamFeed = True
# processamento

"""
    original, cinza, blur, linhas
    """
img = cv2.resize(img, (widthImg, heigthImg))
imgContours = img.copy()
imgContornoMaior = img.copy()
imgFinal = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgLines = cv2.Canny(imgBlur, 10, 50)
imgBlank = np.zeros_like(img)

# blocos <- quadrados
contours, hierarchy = cv2.findContours(
    imgLines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

# usando os retangulos para gabaritos
rectCon = utlis.rectContour(contours)
"""geralmente o retangulo maior detectado são as questões"""
contornoMaior = utlis.getCornerPoints(rectCon[0])
pontuacao = utlis.getCornerPoints(rectCon[1])
if contornoMaior.size != 0 and pontuacao.size != 0:
    cv2.drawContours(imgContornoMaior,
                     contornoMaior, -1, (0, 200, 0), 8)
    cv2.drawContours(imgContornoMaior, pontuacao, -1, (200, 0, 0), 8)
    contornoMaior = utlis.reorder(contornoMaior)
    pontuacao = utlis.reorder(pontuacao)

    # quadrado das respostas
    pt1 = np.float32(contornoMaior)
    pt2 = np.float32(
        [[0, 0], [widthImg, 0], [0, heigthImg], [widthImg, heigthImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    marcadoPeloCandidato = cv2.warpPerspective(
        img, matrix, (widthImg, heigthImg))

    # quadrado dos pontos
    ptG1 = np.float32(pontuacao)
    ptG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
    matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
    marcaDosAcertos = cv2.warpPerspective(img, matrixG, (225, 100))

    # aplicação do gabarito resposta
    imgGabaritoGray = cv2.cvtColor(
        marcadoPeloCandidato, cv2.COLOR_BGR2GRAY)
    opcaoMarcada = cv2.threshold(
        imgGabaritoGray, 170, 255, cv2.THRESH_BINARY_INV)[1]

    # opção marcada pelo candidato
    marcado = utlis.splitBoxes(opcaoMarcada)

    # contagem dos pixel na escolha do candidato observar a saida de dados para o valor máximo
    valorPixel = np.zeros((questoes, escolhas))
    countColunas = 0
    countLinhas = 0
    for opcao in marcado:
        totalMarcadoPixel = cv2.countNonZero(opcao)
        valorPixel[countLinhas][countColunas] = totalMarcadoPixel
        countColunas += 1
        if (countColunas == escolhas):
                countLinhas += 1
                countColunas = 0
                # print(valorPixel)

        meuIndex = []
                # verificando a opção marcada verificando o numero maximo de pixel dentro da linha.
"""como são 5 questões o for varre a linha e verifica qual das colunas
             tem mais pixel e retorna o valor do indice com maior numero"""
for x in range(0, questoes):
    arr = valorPixel[x]
                # print("arr", arr)
    meuIndexValor = np.where(arr == np.amax(arr))
                # print(meuIndexValor[0]) # <- aqui mostra qual parte do array é a resposta marcada pelo participante
    meuIndex.append(meuIndexValor[0][0])
                # print(meuIndex) # saida em linha das opções marcadas

                # comparativo de acerto
    classificacao = []
for x in range(0, questoes):
    if ans[x] == meuIndex[x]:
        classificacao.append(1)
    else:
        classificacao.append(0)
                  # print(classificacao) #<- aqui mostra se acertou ou não

pontuacaoFinal = (sum(classificacao)/questoes*10)
print(pontuacaoFinal)  # numero de acertos

""" apartir daqui seria legal implementar uma saida para impressão no excel,
                     com o nome do aluno e os pontos do mesmo"""

                # mostrando o resultado na marcação em pespequitiva
copyMarcadoPeleCandidato = marcadoPeloCandidato.copy()
utlis.showAnswers(copyMarcadoPeleCandidato,
                                  meuIndex, classificacao, ans)
utlis.drawGrid(marcadoPeloCandidato)

imgDrawings = np.zeros_like(marcadoPeloCandidato)
utlis.showAnswers(imgDrawings, meuIndex,classificacao, ans)
invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
invMarcado = cv2.warpPerspective(imgDrawings, invMatrix, (widthImg, heigthImg))

                # mostrando a pontuação no display
imgResultadoGray = np.zeros_like(marcaDosAcertos, np.uint8)
cv2.putText(imgResultadoGray, str(float(pontuacaoFinal)),
                            (40, 80), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 0), 3)
invMatrixG = cv2.getPerspectiveTransform(ptG2, ptG1)
imgInvResultado = cv2.warpPerspective(
                    imgResultadoGray, invMatrixG, (widthImg, heigthImg))

                # MOSTRAR RESPOSTAS E NOTAS NA IMAGEM FINAL
imgFinal = cv2.addWeighted(imgFinal, 1, invMarcado, 1, 0)
imgFinal = cv2.addWeighted(
                    imgFinal, 1, imgInvResultado, 1, 0)

                # blocos de imagem
imageArray = ([img, imgGray, imgBlur, imgLines],
                              [imgContours, imgContornoMaior, marcadoPeloCandidato, opcaoMarcada])
cv2.imshow("final", imgFinal)

imageStacked = utlis.stackImages(imageArray, 0.4)

                # saida
cv2.imshow("original", imageStacked)
cv2.waitKey(0)