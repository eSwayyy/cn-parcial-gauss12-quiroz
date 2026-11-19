import csv
import gauss
import conteo
import estabilidad
import numpy as np

def leer_archivos(ruta, matriz=False):
    with open(ruta, newline="") as archivo:
        datos = [
            [float(valor) for valor in fila]
            for fila in csv.reader(archivo)
        ]

    if matriz:
        return datos

    return [valor for fila in datos for valor in fila]


if __name__ == "__main__":
    rutas = ("datos/matriz_a.csv", "datos/vector_b.csv")

    A = leer_archivos(rutas[0], True)
    B = leer_archivos(rutas[1])
    x_ref = np.linalg.solve(
        np.array(A, dtype=float),
        np.array(B, dtype=float)
    )

    for metodo in ("ninguno", "parcial", "escalado"):
        x, crecimiento, traza, cont = gauss.gauss(A, B, metodo)
        error = estabilidad.error_relativo(x, x_ref)

        print(f"Maximo multiplicador: {cont['mult_max']:.6e}")
        print(f"Factor de crecimiento: {crecimiento:.6e}")
        print(f"Error relativo: {error:.6e}")

        print(f"\n{'=' * 40}")
        print(f"Método: {metodo}")
        print(f"{'=' * 40}")

        print("\nSolución:")
        for i, valor in enumerate(x):
            print(f"x{i+1} = {valor:.12g}")

        print(f"\nFactor de crecimiento: {crecimiento:.6e}")
        print(f"Pasos de eliminación: {len(traza)}")

        conteo.mostrar_conteo(cont)
