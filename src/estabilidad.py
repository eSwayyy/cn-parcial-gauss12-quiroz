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