# Main libraries
import json
import numpy as np
import math
import matplotlib.pyplot as plt
# Our files
import escalation
import simulator
# Image processing library
from PIL import Image


# !--> Search for the comments like this one though the code


# Colors for terminal

# Hard reset
RESET = '\033[0m'

# Color-map
RED = '\033[31m'
GRAY = '\033[30m'
BLUE = '\033[34m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
DARK_GRAY = '\033[90m'
BRIGHT_YELLOW = '\033[93m'

# Reset color
COLOR_RESET = '\033[39m'

# Roundway capacity
CAPACITY = 250

def main():
  """
  Faz o main 👆
  """

  ### Example 1: Roundway Flow Management ###

  # Open image with matplotlib
  
  # !--> At this point, we will explain the idea of the roundabout flow management
  # !--> That's the whole purpose of the image below, you will see why later
  # !--> Remember to close the image to continue the program

  # !--> I put a "auto-complete" for the inputs values here
  # !--> Because I was bored of typing the same values over and over again
  # !--> You can remove the comments and type the values manually
  # !--> Also, I changed the variables names so that we fix our problem with the matrix

  print(f'Enter the input values {BLUE}(Blue){COLOR_RESET}, separating them with a space:')
  print(DARK_GRAY, end='')
  # Ea, Ec, Ee, Eg = [int(x) for x in input().split()]
  Ea, Ec, Ee, Eg =  [27, 63, 48, 82]
  print(Ea, Ec, Ee, Eg)
  print(COLOR_RESET, end='')

  print(f'\nEnter the output values {RED}(Red){COLOR_RESET}, separating them with a space:')
  print(DARK_GRAY, end='')
  # Sb, Sd, Sf, Sh = [int(x) for x in input().split()]
  Sb, Sd, Sf, Sh = [35, 52, 68, 65]
  print(Sb, Sd, Sf, Sh)
  print(COLOR_RESET, end='')
  print("\n")

  # Total number of inputs at the node = Total number of outputs at the node
  if (Ea + Ec + Ee + Eg != Sb + Sd + Sf + Sh):
    print(RED + '\nThe total number of inputs is different from the total number of outputs')
    print(COLOR_RESET, end='')
    return 1
  
  # !--> Here. From now on I changed the way we built the matrix
  # !--> Now it has 8 nodes... 😢
  # !--> We also will need a new image for representation of the roundabout

  # Equations:

  # A: X8 + Ea = X1 ==> X8 - X1 = -Ea
  # B: X1 = Sb + X2 ==> X1 - X2 = Sb
  # C: X2 + Ec = X3 ==> X2 - X3 = -Ec
  # D: X3 = Cs + X4 ==> X3 - X4 = Sd
  # E: X4 + Ee = X5 ==> X4 - X5 = -Ee
  # F: X5 = Sd + X6 ==> X5 - X6 = Sf
  # G: X6 + Eg = X7 ==> X6 - X7 = -Eg
  # H: X7 = Sf + X8 ==> X7 - X8 = Sh

  # Creating the matrix

  flow_matrix = [[-1,  0,  0,  0,  0,  0,  0,  1, -Ea],
                 [ 1, -1,  0,  0,  0,  0,  0,  0,  Sb],
                 [ 0,  1, -1,  0,  0,  0,  0,  0, -Ec],
                 [ 0,  0,  1, -1,  0,  0,  0,  0,  Sd],
                 [ 0,  0,  0,  1, -1,  0,  0,  0, -Ee],
                 [ 0,  0,  0,  0,  1, -1,  0,  0,  Sf],
                 [ 0,  0,  0,  0,  0,  1, -1,  0, -Eg],
                 [ 0,  0,  0,  0,  0,  0,  1, -1,  Sh],]
  
  # !--> Now we are using the escalation.py file to solve the matrix
  # !--> It basically show step by step the solution of the matrix
  # !--> It also prints the matrix on terminal step by step
  # !--> We will need to remove that print later, because its huge and annoying

  escalation.toLrfe(flow_matrix)

  solution_1 = flow_matrix[0][8]
  solution_2 = flow_matrix[1][8]
  solution_3 = flow_matrix[2][8]
  solution_4 = flow_matrix[3][8]
  solution_5 = flow_matrix[4][8]
  solution_6 = flow_matrix[5][8]
  solution_7 = flow_matrix[6][8]
  # solution_8 must be 0

  # !--> Some explanation about the results

  # [[ 1,  0,  0,  0,  0,  0,  0, -1, Ea                                    ],
  #  [ 0,  1,  0,  0,  0,  0,  0, -1, -Sb + Ea                              ],
  #  [ 0,  0,  1,  0,  0,  0,  0, -1, Ec - Sb + Ea                          ],
  #  [ 0,  0,  0,  1,  0,  0,  0, -1, -Sd + Ec - Sb + Ea                    ],
  #  [ 0,  0,  0,  0,  1,  0,  0, -1, Ee - Sd + Ec - Sb + Ea                ],
  #  [ 0,  0,  0,  0,  0,  1,  0, -1, -Sf + Ee - Sd + Ec - Sb + Ea          ],
  #  [ 0,  0,  0,  0,  0,  0,  1, -1, Eg - Sf + Ee - Sd + Ec - Sb + Ea      ],
  #  [ 0,  0,  0,  0,  0,  0,  0,  0, -Sh + Eg - Sf + Ee - Sd + Ec - Sb + Ea]]

  # Entries - Exits must be 0
  # In other words: Ea + Be + Ec + De - As - Sb - Cs - Sd = 0

  # X1 = Ea + X8
  # X2 = -Sb + Ea + X8
  # X3 = Ec - Sb + Ea + X8
  # X4 = -Sd + Ec - Sb + Ea + X8
  # X5 = Ee - Sd + Ec - Sb + Ea + X8
  # X6 = -Sf + Ee - Sd + Ec - Sb + Ea + X8
  # X7 = Eg - Sf + Ee - Sd + Ec - Sb + Ea + X8
  # X8 = X8

  
  # X1 + X2 + X3 + X4 + X5 + X6 + X7 + X8 <= CAPACITY (less or equal the roundway capacity)

  """
  Parte 1 - Predicting the flow
  """
  
  # Finding the lower bound

  lower_bound = min(solution_1, solution_2, solution_3, solution_4, solution_5, solution_6, solution_7)
  
  print('\033[01m' + '\nLet\'s predict the flow of cars in the roundabout' + RESET)
  print(f'Type the value of X8: ')

  print(DARK_GRAY, end='')
  X8 = float(input())
  print(COLOR_RESET, end='')

  while X8 <= (-lower_bound) and X8 >= Ea + Ec + Ee + Eg:
    print(f'Type the value of X8 {YELLOW}({-lower_bound} <= X8 <= {Ea + Ec + Ee + Eg}){COLOR_RESET}: ')
    print(DARK_GRAY, end='')
    X8 = float(input())
    print(COLOR_RESET, end='')

  # Calculating the flow of cars
  X1 = solution_1 + X8
  X2 = solution_2 + X8
  X3 = solution_3 + X8
  X4 = solution_4 + X8
  X5 = solution_5 + X8
  X6 = solution_6 + X8
  X7 = solution_7 + X8


  print(f"\nThe flow of cars are:\nX1: {DARK_GRAY}{X1}{COLOR_RESET}\nX2: {DARK_GRAY}{X2}{COLOR_RESET}\nX3: {DARK_GRAY}{X3}{COLOR_RESET}\nX4: {DARK_GRAY}{X4}{COLOR_RESET}\nX5: {DARK_GRAY}{X5}{COLOR_RESET}\nX6: {DARK_GRAY}{X6}{COLOR_RESET}\nX7: {DARK_GRAY}{X7}{COLOR_RESET}\nX8: {DARK_GRAY}{X8}{COLOR_RESET}\n")


  """
  Parte 2 - Verify if the cars flow is greater than the capacity
  """
    
  if (X1 + X2 + X3 + X4 + X5 + X6 + X7 + X8 > CAPACITY):
    print(RED + 'The flow of cars is greater than the capacity of the roundabout')
    print(BRIGHT_YELLOW + 'A traffic light is needed to control the flow!')
    print(COLOR_RESET, end='')
  else:
    print(BRIGHT_YELLOW + 'The flow of cars is less than the capacity of the roundabout')
    print(COLOR_RESET, end='')
  

  """
  Parte 3 - Simulation :)
  """

  # !--> So this is the new part of the code...
  # !--> Run and see the results!
  # !--> Give feedback later please!
  # !--> The purpose of this part is to show the theory in practice.
  # !--> Hopefuly it helps with the explanation and how it works.
  # !--> I just added the traffic light system, guess it works... kinda... 😅

  print(BLUE,"\n\n\tStart Simulation?\n\n\t(y/n): ",COLOR_RESET, end='')
  print(DARK_GRAY, end='')
  run = input()
  print(COLOR_RESET, end='')

  while run == 'y':
    print(f"\nType the roads where you want to place the first cycle of traffic lights.\nJust the entries {BLUE}(Blue){COLOR_RESET} or empty.\n: ", end="")

    print(DARK_GRAY, end='')
    traffic_lights1 = input().split()
    print(COLOR_RESET, end='')

    if traffic_lights1 == ['']:
      traffic_lights1 = []

    print(f"\nType the roads where you want to place the second cycle of traffic lights\nJust the entries {BLUE}(Blue){COLOR_RESET} or empty.\n{YELLOW}Cant be the same as before.{COLOR_RESET}\n: ", end="")

    print(DARK_GRAY, end='')
    traffic_lights2 = input().split()
    print(COLOR_RESET, end='')

    if traffic_lights2 == ['']:
      traffic_lights2 = []

    print(GREEN,"\nRunning simulation...", COLOR_RESET)
  
    values = [[Ea, Ec, Ee, Eg], [Sb, Sd, Sf, Sh]]
    simulator.run(values, CAPACITY, X8, traffic_lights1, traffic_lights2)

    print(BLUE,"\n\n\tRun again?\n\n\t(y/n): ",COLOR_RESET, end='')
    print(DARK_GRAY, end='')
    run = input()
    print(COLOR_RESET, end='')


  return 0

if (__name__ == "__main__"):
    main()
