# Main libraries
import json
import numpy as np
import matplotlib.pyplot as plt
# Our files
import escalation
import simulator
# Image processing library
from PIL import Image

# !--> Search for the comments like this one though the code

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
CAPACITY = 50

def main():
  """
  Faz o main 👆
  """

  ### Example 1: Roundway Flow Management ###

  # Open image with matplotlib
  
  # !--> On this part we will explain the idea of the roundabout flow management
  # !--> That's the whole purpose of the image below, you will see why later
  # !--> Remember to close the image to continue the program

  img = Image.open('images/image_wo_color.png')

  imgplot = plt.imshow(img)
  plt.show()
  
  # !--> I put a "auto-complete" for the inputs values
  # !--> I was bored of typing the same values over and over again
  # !--> You can remove the comments and type the values manually

  print(f'Enter the input values {BLUE}(Blue){COLOR_RESET}, separating them with a space:')
  print(DARK_GRAY, end='')
  # Ae, Be, Ce, De = [int(x) for x in input().split()]
  Ae, Be, Ce, De =  [10, 20, 25, 15]
  print(Ae, Be, Ce, De)
  print(COLOR_RESET, end='')

  print(f'\nEnter the output values {RED}(Red){COLOR_RESET}, separating them with a space:')
  print(DARK_GRAY, end='')
  # As, Bs, Cs, Ds = [int(x) for x in input().split()]
  As, Bs, Cs, Ds = [19, 11, 30, 10]
  print(As, Bs, Cs, Ds)
  print(COLOR_RESET, end='')
  print("\n")

  # Total number of inputs at the node = Total number of outputs at the node
  if (Ae + Be + Ce + De != As + Bs + Cs + Ds):
    print(RED + '\nThe total number of inputs is different from the total number of outputs')
    print(COLOR_RESET, end='')
    return 1

  # A: X1 + Ae = As + X2 => X1 - X2 = As - Ae
  # B: X2 + Be = Bs + X3 => X2 - X3 = Bs - Be
  # C: X3 + Ce = Cs + X4 => X3 - X4 = Cs - Ce
  # D: X4 + De = Ds + X1 => X4 - X1 = Ds - De

  # Storing the results in a variable
  A = As - Ae
  B = Bs - Be
  C = Cs - Ce
  D = Ds - De

  # Creating the matrix

  flow_matrix = [[1, -1, 0, 0, A],
                 [0, 1, -1, 0, B],
                 [0, 0, 1, -1, C],
                 [-1, 0, 0, 1, D]]
  
  # !--> Now we are using the escalation.py file to solve the matrix
  # !--> It basically show step by step the solution of the matrix
  # !--> It also prints the matrix on terminal, but we can change later if you all didnt like

  escalation.toLrfe(flow_matrix)

  solution_1 = flow_matrix[0][4]
  solution_2 = flow_matrix[1][4]
  solution_3 = flow_matrix[2][4]
  # solution_4 must be 0

  # [[1, -1, 0, 0, A + B + C    ],
  #  [0, 1, -1, 0, B + C        ],
  #  [0, 0, 1, -1, C            ],
  #  [0, 0, 0,  1, D + A + B + C]]

  # A + B + C + D must be 0
  # ou seja: As - Ae + Bs - Be + Cs - Ce + Ds - De = 0

  # X1 = A + B + C + X4
  # X2 = B + C + X4
  # X3 = C + X4
  # X4 = X4 -> Free variable
  
  # X1 + X2 + X3 + X4 <= CAPACITY (less or equal the roundway capacity)

  """
  Parte 1 - Predicting the flow
  """
  
  # Finding the lower bound

  lower_bound = 0

  if (solution_3 < solution_2 and solution_3 < solution_1):
    lower_bound = solution_3
  elif (solution_2 < solution_1):
    lower_bound = solution_2
  else:
    lower_bound = solution_1

  
  print('\033[01m' + '\nLet\'s predict the flow of cars in the roundabout' + RESET)
  print(f'Type the value of X4: ')

  print(DARK_GRAY, end='')
  X4 = int(input())
  print(COLOR_RESET, end='')

  while X4 < lower_bound:
    print(f'Type the value of X4 {YELLOW}(greater than {lower_bound}){COLOR_RESET}: ')
    print(DARK_GRAY, end='')
    X4 = int(input())
    print(COLOR_RESET, end='')

  # Calculating the flow of cars
  X1 = solution_1 + X4
  X2 = solution_2 + X4
  X3 = solution_3 + X4

  print(f"\nThe flow of cars are: X1: {DARK_GRAY}{X1}{COLOR_RESET} X2: {DARK_GRAY}{X2}{COLOR_RESET} X3: {DARK_GRAY}{X3}{COLOR_RESET} X4: {DARK_GRAY}{X4}{COLOR_RESET}\n")


  """
  Parte 2 - Verify if the cars flow is greater than the capacity
  """
    
  if (X1 + X2 + X3 + X4 > CAPACITY):
    print(RED + 'The flow of cars is greater than the capacity of the roundabout')
    print(BRIGHT_YELLOW + 'A traffic light is needed to control the flow!')
    print(COLOR_RESET, end='')
  else:
    print(BRIGHT_YELLOW + 'The flow of cars is less than the capacity of the roundabout')
    print(COLOR_RESET, end='')
  

  """
  Parte 3 - Simulation :)
  """

  # !--> So this is kind of a surprise, hehehe.
  # !--> Run and see the results!
  # !--> Give feedback later please!
  # !--> I will also add more features later, like adding a traffic light to control the flow.

  print(BLUE,"\n\n\tStart Simulation?\n\n\t(y/n): ",COLOR_RESET, end='')
  print(DARK_GRAY, end='')
  start = input()
  print(COLOR_RESET, end='')

  if start == 'y':
    values = [[Ae, Be, Ce, De], [As, Bs, Cs, Ds], [X1, X2, X3, X4]]
    simulator.run(values, CAPACITY)

  return 0

if (__name__ == "__main__"):
    main()
