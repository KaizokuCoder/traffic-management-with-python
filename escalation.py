from tabulate import tabulate

def prettyFloat(f):
    formatted = "%0.2f" % f
    if formatted == "-0.00":
        return "0.00"
    return formatted

def printMatrix(matrix):
    # Convert all elements to pretty float format
    formatted_matrix = [[prettyFloat(item) for item in row] for row in matrix]
    # Print the matrix using tabulate
    print(tabulate(formatted_matrix, tablefmt="grid"))

def multiplyBy(line, n):
    return [float(item) * n for item in line]


def divideBy(line, n):
    if n == 0:
        return line
    arr = []
    for i in range(len(line)):
        arr.append(float(line[i]) / n)
    return arr


def makeOne( matrix, n ):
    # make first number = 1
    print ("dividindo linha:")
    print (matrix[n])
    print ("por %s" % matrix[n][n])
    matrix[n] = divideBy(matrix[n], matrix[n][n])
    print (matrix[n])
    print ("A matrix atualmente:")
    printMatrix(matrix)
    return matrix


def zero( matrix, n):
    print ("zerando os elementos abaixo do 1 da linha: %s" % (n+1))
    for i in range(n, len(matrix)):
        z = i + 1
        if (z == len(matrix)):
            break

        print ("i, z = %s, %s " % (i, z))

        print ("multiplicando linha %s por %s" %(n+1, matrix[z][n]))
        x = multiplyBy(matrix[n], matrix[z][n])

        print ("subtraindo linha %s por %s" %(matrix[z], x))
        matrix[z] = [a-b for a,b in zip (matrix[z], x)]

        printMatrix(matrix)
    return matrix


def toLrfe( matrix ):
    lineCount = len(matrix) 
    printMatrix(matrix)

    for i in range(lineCount):
        matrix = makeOne(matrix, i)
        matrix = zero( matrix, i)

    print ("\n")

    printMatrix(matrix)


if __name__ == "__main__":
    mtx = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]

    toLrfe(mtx)
