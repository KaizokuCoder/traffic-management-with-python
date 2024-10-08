# Importing our files
import escalation
import simulator

# Importing libraries
import json


# !--> Search for the comments like this one though the code


# Colors for terminal

# Hard reset
RESET = '\033[0m'
print(RESET)

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
CAPACITY = 720

def menu(f, error = ''):
  # Initializing Input and Output values
  Ea, Ec, Ee, Eg = 1, 0, 0, 0
  Sb, Sd, Sf, Sh = 0, 0, 0, 0

  # Message for the user
  msg = """Select an option:
  1 - Input the values
  2 - Grab from file
"""

  # Checking if there was an error
  if (error != ''):
    msg = RED + '\n' + error + '\n\n' + COLOR_RESET + msg

  # Printing the message and getting user input
  print(msg)
  try:
    op = int(input())

    print('\n')

    # Using user input for the values
    if op == 1:
      print(f'Enter the input values {BLUE}(Blue){COLOR_RESET}, separating them with a space:')
      print(DARK_GRAY, end='')
      Ea, Ec, Ee, Eg = [int(x) for x in input().split()]
      print(COLOR_RESET, end='')

      print(f'\nEnter the output values {RED}(Red){COLOR_RESET} in %, separating them with a space:')
      print(DARK_GRAY, end='')
      Sb, Sd, Sf, Sh = [int(x) for x in input().split()]
      print(COLOR_RESET, end='')

    # Using JSON file for the values
    elif op == 2:
      # Getting JSON data
      data = json.load(f)

      # Using JSON data
      Ea, Ec, Ee, Eg = data[0]
      Sb, Sd, Sf, Sh = data[1]

    # Invalid option
    else:
      return menu(f, 'Invalid option!')

  except:
    return menu(f, 'Invalid option!')

  return Ea, Sb, Ec, Sd, Ee, Sf, Eg, Sh

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

  # Opening the JSON file
  f = open('data.json')

  # Getting the values for the inputs and outputs of the roundabout
  Ea, Sb, Ec, Sd, Ee, Sf, Eg, Sh = menu(f)

  # # Checking for an error
  # while (Ea + Ec + Ee + Eg != Sb + Sd + Sf + Sh):
  #   Ea, Sb, Ec, Sd, Ee, Sf, Eg, Sh = menu(f, 'The total number of inputs is different from the total number of outputs!')

  print("\n")

  print(f'Current values for the inputs {BLUE}(Blue){COLOR_RESET}')
  print(DARK_GRAY, end='')
  # # Ea, Ec, Ee, Eg = [int(x) for x in input().split()]
  # # Using JSON data
  # Ea, Ec, Ee, Eg = data[0]
  print(Ea, Ec, Ee, Eg)
  print(COLOR_RESET, end='')

  print(f'\nCurrent values for the outputs {RED}(Red){COLOR_RESET}')
  print(DARK_GRAY, end='')
  # # Sb, Sd, Sf, Sh = [int(x) for x in input().split()]
  # # Using JSON data
  # Sb, Sd, Sf, Sh = data[1]
  print(Sb, Sd, Sf, Sh)
  print(COLOR_RESET, end='')
  print("\n")

  # Total number of inputs at the node = Total number of outputs at the node
  # if (Ea + Ec + Ee + Eg != Sb + Sd + Sf + Sh):
  #   print(RED + '\nThe total number of inputs is different from the total number of outputs')
  #   print(COLOR_RESET, end='')
  #   return 1
  
  # !--> Here. We will create the matrix for the roundabout
  # !--> Now it has 8 nodes... 😢

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

  entries_sum = Ea + Ec + Ee + Eg
  Sb_value, Sd_value, Sf_value, Sh_value = round(Sb*(entries_sum/100),2), round(Sd*(entries_sum/100),2), round(Sf*(entries_sum/100),2), round(Sh*(entries_sum/100), 2)

  flow_matrix = [[-1,  0,  0,  0,  0,  0,  0,  1, -Ea],
                 [ 1, -1,  0,  0,  0,  0,  0,  0,  Sb_value],
                 [ 0,  1, -1,  0,  0,  0,  0,  0, -Ec],
                 [ 0,  0,  1, -1,  0,  0,  0,  0,  Sd_value],
                 [ 0,  0,  0,  1, -1,  0,  0,  0, -Ee],
                 [ 0,  0,  0,  0,  1, -1,  0,  0,  Sf_value],
                 [ 0,  0,  0,  0,  0,  1, -1,  0, -Eg],
                 [ 0,  0,  0,  0,  0,  0,  1, -1,  Sh_value],]
  
  # !--> Now we are using the escalation.py file to solve the matrix
  # !--> It basically show step by step the solution of the matrix
  # !--> It also prints the matrix on terminal step by step
  # !--> We will need to remove that print later, because its huge and annoying

  escalation.toLrfe(flow_matrix)

  solution_1 = round(flow_matrix[0][8], 2)
  solution_2 = round(flow_matrix[1][8], 2)
  solution_3 = round(flow_matrix[2][8], 2)
  solution_4 = round(flow_matrix[3][8], 2)
  solution_5 = round(flow_matrix[4][8], 2)
  solution_6 = round(flow_matrix[5][8], 2)
  solution_7 = round(flow_matrix[6][8], 2)
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
  print('Type the value of X8: ')

  print(DARK_GRAY, end='')
  X8 = float(input())
  print(COLOR_RESET, end='')

  while X8 < (-lower_bound) or X8 > (Ea + Ec + Ee + Eg):
    print(f'Type the value of X8 {YELLOW}({-lower_bound:.2f} <= X8 <= {Ea + Ec + Ee + Eg}){COLOR_RESET}: ')
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
    # print(f"\nType the roads where you want to place the first cycle of traffic lights.\nJust the entries {BLUE}(Blue){COLOR_RESET} or empty.\n: ", end="")

    # print(DARK_GRAY, end='')
    # traffic_lights1 = input().split()
    # print(COLOR_RESET, end='')

    # if traffic_lights1 == ['']:
    #   traffic_lights1 = []

    # print(f"\nType the roads where you want to place the second cycle of traffic lights\nJust the entries {BLUE}(Blue){COLOR_RESET} or empty.\n{YELLOW}Can't be the same as before.{COLOR_RESET}\n: ", end="")

    # print(DARK_GRAY, end='')
    # traffic_lights2 = input().split()
    # print(COLOR_RESET, end='')
    
    # if traffic_lights2 == ['']:
    #   traffic_lights2 = []

    print(GREEN,"\nRunning simulation...", COLOR_RESET)
  
    values = [[Ea, Ec, Ee, Eg], [Sb, Sd, Sf, Sh]]
    simulator.run(values, CAPACITY, X8)

    print(BLUE,"\n\n\tRun again?\n\n\t(y/n): ",COLOR_RESET, end='')
    print(DARK_GRAY, end='')
    run = input()
    print(COLOR_RESET, end='')

  return 0

if (__name__ == "__main__"):
    main()
