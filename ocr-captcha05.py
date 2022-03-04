#treinar modelo
import cv2
import os
import numpy as np
import pickle
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from util.helpers import resize_to_fit

#primeira etapa pegar os dados
dados = []
rotulos = []
pasta_das_imagens = "data-captcha/rotulos"

# pegando as imagens para padronizar os tamnhos
imagens = paths.list_images(pasta_das_imagens)
#print(list(imagens))
#lendo cada uma das imagens dentro das pastas
for arquivo in imagens:
    rotulo = arquivo.split(os.path.sep)[-2]
    imagem = cv2.imread(arquivo)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    #pondo o tamanho padrão 20 x 20
    imagem = resize_to_fit(imagem, 20, 20)

    #pondo 3 dimenções na imagem
    # imagem tem [ valor0, valor1 ] o axis=2 significa [ valor0, valor1, valor2]
    imagem = np.expand_dims(imagem, axis=2)

    #adicionando a lista de dados
    dados.append(imagem)
    rotulos.append(rotulo)

# criando a I.A
# normalizar a imagem em 0 e 1 , 255 = 1
dados = np.array(dados, dtype="float") / 255
rotulos = np.array(rotulos)

# separar em 3 partes [ treinamento, validação, teste ]
(x_treino, x_teste, y_treino, y_teste) = train_test_split(dados, rotulos, test_size=0.20, random_state=0)

#aplicando o LabelBinarizer <- dando nome ao rótulo
lb = LabelBinarizer().fit(y_treino)
y_treino = lb.transform(y_treino)
y_teste = lb.transform(y_teste)

# salvar o labelbinarizer em um arquivo com o pickle
with open('rotulos_modelo.dat', 'wb') as arquivo_pickle:
    pickle.dump(lb, arquivo_pickle)

# criando e treinando a IA
modelo = Sequential()

# criar as camadas da rede neural
modelo.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# criar a 2ª camada
modelo.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# mais uma camada
modelo.add(Flatten())
modelo.add(Dense(500, activation="relu"))

# camada de saída
modelo.add(Dense(26, activation="softmax"))

# compilar todas as camadas
modelo.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# treinando a rede
modelo.fit(x_treino, y_treino, validation_data=(x_teste, y_teste), batch_size=26, epochs=10, verbose=1)

# salvando o modelo
modelo.save("modelo_quebra_cap_treinado.hdf5")