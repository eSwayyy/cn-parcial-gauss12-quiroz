import numpy as np
from decimal import Decimal, localcontext

def calcular_residuo(A, B, x):
    residuo = []

    with localcontext() as ctx:
        ctx.prec = 50 # configurar temporalmente la precision de las operaciones a 50 decimales 

        for i in range(len(A)):
            suma = Decimal(0)

            for j in range(len(A[i])):
                a = Decimal(str(A[i][j]))
                valor_x = Decimal(str(x[j]))

                suma += a * valor_x

            b = Decimal(str(B[i]))
            residuo.append(b - suma)
    return residuo

def norma_infinito(vector):
    mayor = 0
    for valor in vector:
        if abs(valor) > mayor:
            mayor = abs(valor)
    return mayor

def error_relativo(x, x_ref):
    numerador = 0
    denominador = 0
    for i in range(len(x)):
        diferencia = abs(x[i] - x_ref[i])
        if diferencia > numerador:
            numerador = diferencia

        if abs(x_ref[i]) > denominador:
            denominador = abs(x_ref[i])
    return numerador/denominador

def calcular_dx(L, U, permutacion, residuo):
    n = len(residuo)

    r = [0] * n

    for i in range(n):
        r[i] = float(residuo[permutacion[i]])

    y = [0] * n

    for i in range(n):
        suma = r[i]

        for j in range(i):
            suma -= L[i][j] * y[j]

        y[i] = suma / L[i][i]

    dx = [0] * n

    for i in range(n - 1, -1, -1):
        suma = y[i]

        for j in range(i + 1, n):
            suma -= U[i][j] * dx[j]

        dx[i] = suma / U[i][i]

    return dx

def correccion_iterativa(A, B, x, L, U, permutacion):
    residuo_antes = calcular_residuo(A, B, x)

    dx = calcular_dx(L, U, permutacion, residuo_antes)

    x_nuevo = []

    for i in range(len(x)):
        x_nuevo.append(x[i] + dx[i])

    residuo_despues = calcular_residuo(A, B, x_nuevo)

    return x_nuevo, residuo_antes, residuo_despues