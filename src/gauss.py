# Contadores globales (se reinician en cada corrida)
cont = {}


def reiniciar():
    cont.update(muldiv_pasos=[], addsub_pasos=[], muldiv_sust=0, addsub_sust=0,
                comparaciones=0, intercambios=0, mult_max=0.0, a_max=0.0)


def eliminar_columna(A, B, i):
    n = len(A)
    md = ad = 0
    for j in range(i + 1, n):
        m = A[j][i] / A[i][i]; md += 1          # multiplicador: una vez por fila
        cont["mult_max"] = max(cont["mult_max"], abs(m))
        A[j][i] = 0.0                           # ya se sabe que queda en cero
        for k in range(i + 1, n):               # desde i+1, no desde i
            A[j][k] = A[j][k] - m * A[i][k]; md += 1; ad += 1
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
    A = [f[:] for f in A]; B = B[:]
    reiniciar()
    cont["a_max"] = max(abs(v) for f in A for v in f)
    a_max0 = cont["a_max"]
    for i in range(len(A) - 1):
        if pivoteo:
            idx = i
            for j in range(i + 1, len(A)):
                cont["comparaciones"] += 1
                if abs(A[j][i]) > abs(A[idx][i]):
                    idx = j
            if idx != i:
                A[i], A[idx] = A[idx], A[i]
                B[i], B[idx] = B[idx], B[i]
                cont["intercambios"] += 1
        eliminar_columna(A, B, i)
    x = sustitucion_regresiva(A, B)
    crecimiento = cont["a_max"] / a_max0
    return x, crecimiento