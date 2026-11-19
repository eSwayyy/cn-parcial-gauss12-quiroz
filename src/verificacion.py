from decimal import Decimal, localcontext
#      ^^ Recomendación directa de chatgpt para cumplir con verificar con precisión extendida c:

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
