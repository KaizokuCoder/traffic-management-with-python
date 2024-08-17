import os
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def main():
  """
  Faz o main 👆
  """

  ### ROTATÓRIA ###

  # Entradas da rotatória (carro/min)
  Ae, Be, Ce, De = 0, 0, 0, 0

  # Saídas da rotatória (carro/min)
  As, Bs, Cs, Ds = 0, 0, 0, 0

  # Trechos da rotatória
  X1, X2, X3, X4 = 0, 0, 0, 0

  # Capacidade de cada trecho
  CAPACITY = 100

  ### SEMÁFORO ###

  # Ver se precisa ou não de semáforo

  # Abrir imagem com matplotlib
  img = Image.open('images/image.png')

  imgplot = plt.imshow(img)
  # plt.show()

  # A: X1 + Ae = As + X2 => X1 - X2 = As - Ae
  # B: X2 + Be = Bs + X3 => X2 - X3 = Bs - Be
  # C: X3 + Ce = Cs + X4 => X3 - X4 = Cs - Ce
  # D: X4 + De = Ds + X1 => X4 - X1 = Ds - De

  #[[1, -1, 0, 0, A],
  # [0, 1, -1, 0, B],
  # [0, 0, 1, -1, C],
  # [-1, 0, 0, 1, D]]

  # Juntando os resultados em uma varíavel
  A = As - Ae
  B = Bs - Be
  C = Cs - Ce
  D = Ds - De

  # Gerando a matriz de fluxo

  flux_matrix = [[1, 0, 0, -1, A + B + C    ],
                 [0, 1, 0, -1, B + C        ],
                 [0, 0, 1, -1, C            ],
                 [0, 0, 0,  0, D + A + B + C]]

  # A + B + C + D = 0
  # ou seja: As - Ae + Bs - Be + Cs - Ce + Ds - De = 0

  # X1 = A + B + C + X4
  # X2 = B + C + X4
  # X3 = C + X4
  # X4 = t -> Variável Livre
  
  # X1 + X2 + X3 + X4 <= CAPACITY
  
  print("Digite os valores das entradas (Azul), separando-os com um espaço:")
  Ae, Be, Ce, De = int(input().split())

  print("Digite os valores das saídas (Vermelho), separando-os com um espaço:")
  As, Bs, Cs, Ds = int(input().split())

  # Total de Entradas no Nó = Total de Saídas do Nó
  if (Ae + Be + Ce + De != As + Bs + Cs + Ds):
    print("O total de entradas é diferente do total de saídas")
    return

  
  


if (__name__ == "__main__"):
  main()
