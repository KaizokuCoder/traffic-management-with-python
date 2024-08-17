# Bibliotecas utilizadas
import json
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

# Hard reset
RESET = '\033[0m'

# Color-map
RED = '\033[31m'
GRAY = '\033[30m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
DARK_GRAY = '\033[90m'
BRIGHT_YELLOW = '\033[93m'

# Reset color
COLOR_RESET = '\033[39m'

# Roundway capacity
CAPACITY = 25

def main():
  """
  Faz o main 👆
  """

  ### Example 1: Roundway Flow Management ###

  # Roundway entries (car/min)
  Ae, Be, Ce, De = 0, 0, 0, 0

  # Roundway exits (car/min)
  As, Bs, Cs, Ds = 0, 0, 0, 0

  # Roundway bits (car/min)
  X1, X2, X3, X4 = 0, 0, 0, 0

  # Open image with matplotlib
  # img = Image.open('images/image_wo_color.png')

  # imgplot = plt.imshow(img)
  # plt.show()
  
  print(f'Enter the input values {BLUE}(Blue){COLOR_RESET}, separating them with a space:')
  print(DARK_GRAY, end='')
  Ae, Be, Ce, De = [int(x) if (int(x) < 0) else -1 for x in input().split()]
  print(COLOR_RESET, end='')

  print(f'\nEnter the output values {RED}(Red){COLOR_RESET}, separating them with a space:')
  print(DARK_GRAY, end='')
  As, Bs, Cs, Ds = [int(x) if (int(x) < 0) else -1 for x in input().split()]
  print(COLOR_RESET, end='')

  # A: X1 + Ae = As + X2 => X1 - X2 = As - Ae
  # B: X2 + Be = Bs + X3 => X2 - X3 = Bs - Be
  # C: X3 + Ce = Cs + X4 => X3 - X4 = Cs - Ce
  # D: X4 + De = Ds + X1 => X4 - X1 = Ds - De

  # Storing the results in a variable
  A = As - Ae
  B = Bs - Be
  C = Cs - Ce
  D = Ds - De

  #[[1, -1, 0, 0, A],
  # [0, 1, -1, 0, B],
  # [0, 0, 1, -1, C],
  # [-1, 0, 0, 1, D]]

  # Creating the matrix

  flow_matrix = [[1, 0, 0, -1, A + B + C    ],
                 [0, 1, 0, -1, B + C        ],
                 [0, 0, 1, -1, C            ],
                 [0, 0, 0,  0, D + A + B + C]]

  # A + B + C + D = 0
  # ou seja: As - Ae + Bs - Be + Cs - Ce + Ds - De = 0

  # X1 = A + B + C + X4
  # X2 = B + C + X4
  # X3 = C + X4
  # X4 = t -> Free variable
  
  # X1 + X2 + X3 + X4 <= CAPACITY

  # Total number of inputs at the node = Total number of outputs at the node
  if (Ae + Be + Ce + De != As + Bs + Cs + Ds):
    print(RED + '\nThe total number of inputs is different from the total number of outputs')
    print(COLOR_RESET, end='')
    return

  """
  Parte 1 - Predicting the flow
  """

  lower_bound = 0

  if (C < B + C and C < A + B + C):
    lower_bound = C
  elif (B + C < A + B + C):
    lower_bound = B + C
  else:
    lower_bound = A + B + C

  
  print('\033[01m' + '\nLet\'s predict the flow of cars in the roundabout' + RESET)
  print('Type the value of X4: ')

  print(DARK_GRAY, end='')
  X4 = int(input())
  print(COLOR_RESET, end='')

  while X4 < lower_bound:
    print(f'Type the value of X4 {YELLOW}(greater than {lower_bound}){COLOR_RESET}: ')
    print(DARK_GRAY, end='')
    X4 = int(input())
    print(COLOR_RESET, end='')

  # Calculando o fluxo de carros
  X1 = A + B + C + X4
  X2 = B + C + X4
  X3 = C + X4

  print(f"\nThe flow of cars are: X1: {DARK_GRAY}{X1}{COLOR_RESET} X2: {DARK_GRAY}{X2}{COLOR_RESET} X3: {DARK_GRAY}{X3}{COLOR_RESET} X4: {DARK_GRAY}{X4}{COLOR_RESET}\n")


  """
  Parte 2 - Verify if the cars flow is greater than the capacity
  """
  
  if (X1 + X2 + X3 + X4 > CAPACITY):
    print(RED + 'The flow of cars is greater than the capacity of the roundabout')
    print(BRIGHT_YELLOW + 'A traffic light is needed to control the flow!')
    print(COLOR_RESET, end='')
    

  return 0

if (__name__ == "__main__"):
  main()
