# Contadores globales (se reinician en cada corrida)
cont = {}

def reiniciar():
    cont.update(muldiv_pasos=[], addsub_pasos=[], muldiv_sust=0, addsub_sust=0,
                comparaciones=0, intercambios=0, mult_max=0, a_max=0)


def eliminar_columna(A, B, i):
    n = len(A)
    md = ad = 0
    for j in range(i + 1, n):
        m = A[j][i] / A[i][i]
        md += 1
        cont["mult_max"] = max(cont["mult_max"], abs(m))
        A[j][i] = 0.0
        for k in range(i + 1, n):
            A[j][k] = A[j][k] - m * A[i][k]
            md += 1
            ad += 1
            cont["a_max"] = max(cont["a_max"], abs(A[j][k]))
        B[j] = B[j] - m * B[i]; md += 1; ad += 1
    cont["muldiv_pasos"].append(md)
    cont["addsub_pasos"].append(ad)


def sustitucion_regresiva(A, B):
    n = len(A)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        t = B[i]
        for k in range(i + 1, n):
            t = t - A[i][k] * x[k]
            cont["muldiv_sust"] += 1; cont["addsub_sust"] += 1
        x[i] = t / A[i][i]; cont["muldiv_sust"] += 1
    return x


def gauss(A, B, pivoteo):
    """pivoteo=False: sin pivoteo. pivoteo=True: parcial (tu versión)."""
    traza = []
    A = [f[:] for f in A]; B = B[:]
    escalas = [
    max(abs(valor) for valor in fila)
    for fila in A
    ]
    reiniciar()
    cont["a_max"] = max(abs(v) for f in A for v in f)
    a_max0 = cont["a_max"]
    for i in range(len(A) - 1):
        idx = i

        if pivoteo=="parcial":
            for j in range(i + 1, len(A)):
                cont["comparaciones"] += 1
                if abs(A[j][i]) > abs(A[idx][i]):
                    idx = j
        if pivoteo=="escalado":
            for j in range(i + 1, len(A)):
                cont["comparaciones"] += 1
                ratio_j = abs(A[j][i]) / escalas[j]
                ratio_idx = abs(A[idx][i]) / escalas[idx]
                if ratio_j > ratio_idx:
                    idx = j
        if idx != i:
            A[i], A[idx] = A[idx], A[i]
            B[i], B[idx] = B[idx], B[i]
            escalas[i], escalas[idx] = escalas[idx], escalas[i]
            cont["intercambios"] += 1
        eliminar_columna(A, B, i)
        matriz = []
        for fila in A: matriz.append(fila[:])
        traza.append(matriz)
    x = sustitucion_regresiva(A, B)
    crecimiento = cont["a_max"] / a_max0
    return x, crecimiento, traza, cont.copy()