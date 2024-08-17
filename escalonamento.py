def prettyFloat(f):
  """ prettyFloat(f) -> float """
  return "%0.2f" % f


def printMatrix( matrix ):
  for i in range(len(matrix)):
    print(map(prettyFloat, matrix[i]))

  print("\n")


def multiplyBy(line, n):
  arr = []
  for i in range(len(line)):
    arr.append(float(line[i]) * n)

  return arr


def divideBy(line, n):
  arr = []

  for i in range(len(line)):
    arr.append(float(line[i]) / n)

  return arr


def makeOne( matrix, n ):
  # make first number = 1

  print("dividindo linha:")
  print(matrix[n])
  print("por %s" % matrix[n][n])

  matrix[n] = divideBy(matrix[n], matrix[n][n])
  print(matrix[n])
  print("A matrix atualmente:")
  printMatrix(matrix)

  return matrix
  

def zero( matrix, n):
  print("zerando os elementos abaixo do 1 da linha: %s" % n)

  for i in range(n, len(matrix)):
    z = i + 1
    if (z == len(matrix)):
      break
    
    print("i, z = %s, %s " % (i, z))

    print("multiplicando linha %s por %s" %(n, matrix[z][n]))
    x = multiplyBy(matrix[n], matrix[z][n])
        
    print("subtraindo linha %s por %s" %(matrix[z], x))
    matrix[z] = [a-b for a,b in zip (matrix[z], x)]

    print(Matrix(matrix))

  return matrix


def toLrfe( matrix ):
  lineCount = len(matrix) 
  columnCount = len(matrix[1])
  printMatrix(mtx)

  for i in range(lineCount):
    matrix = makeOne(matrix, i)
    matrix = zero( matrix, i)
  
  print("\n")

  printMatrix(matrix)