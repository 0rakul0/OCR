#testando captchas 02
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('data-captcha/bloco/cap01.png', 0)
img2 = cv2.imread('data-captcha/bloco/cap02.png', 0)

_, escolhido1 = cv2.threshold(img1, 25, 255, cv2.THRESH_BINARY)
_, escolhido2 = cv2.threshold(img2, 25, 255, cv2.THRESH_BINARY)


cv2.imshow('escolhido1', escolhido1)
cv2.imshow('escolhido2', escolhido2)


cv2.waitKey(0)
cv2.destroyWindow()
