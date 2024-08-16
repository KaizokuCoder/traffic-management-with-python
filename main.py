import os
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def main():
  """ Faz o main 👆 """

  ### ROTATÓRIA ###

  # Entradas da rotatória (carro/min)
  a1, a2, a3, a4 = 0, 0, 0, 0

  # Saídas da rotatória (carro/min)
  b1, b2, b3, b4 = 0, 0, 0, 0

  # Trechos da rotatória
  x1, x2, x3, x4 = 0, 0, 0, 0

  # Capacidade de cada trecho
  CAPACITY = 0

  ### SEMÁFORO ###

  # Ver se precisa ou não de semáforo

  # Abrir imagem com matplotlib
  img = Image.open('images/image.png')

  imgplot = plt.imshow(img)
  plt.show()

#   total de entradas = total de saídas
#   total de entradas no nó = total de saídas do nó

if (__name__ == "__main__"):
  main()
