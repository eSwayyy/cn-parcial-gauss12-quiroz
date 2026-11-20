import csv
import gauss
import conteo
import verificacion
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

    archivo_solucion = open("resultados/solucion.csv", "w", newline="", encoding="utf-8")
    archivo_traza = open("resultados/traza_eliminacion.txt", "w", encoding="utf-8")
    archivo_residuo = open("resultados/residuo.txt", "w", encoding="utf-8")
    with open("resultados/conteo_flops.md", "w", encoding="utf-8") as archivo:
        archivo.write("# Conteo de operaciones\n")

    escritor = csv.writer(archivo_solucion)
    escritor.writerow(["metodo", "incognita", "valor"])

    for metodo in ("ninguno", "parcial", "escalado"):
        x, crecimiento, traza, cont, L, U, permutacion = gauss.gauss(A, B, metodo)
        x_refinado, r_antes, r_despues = verificacion.correccion_iterativa(A, B, x, L, U, permutacion)

        for i in range(len(x)):
            escritor.writerow([metodo, f"x{i+1}", format(x[i], ".17g")])

        archivo_traza.write(f"\nMETODO: {metodo}\n")
        for i in range(len(traza)):
            archivo_traza.write(f"\nPaso {i+1}\n")

            for fila in traza[i]:
                for valor in fila:
                    archivo_traza.write(f"{valor:.12e} ")
                archivo_traza.write("\n")
        conteo.mostrar_conteo(cont, metodo)

        archivo_residuo.write(f"\nMETODO: {metodo}\n")

        archivo_residuo.write("\nResiduo antes del refinamiento:\n")

        for i in range(len(r_antes)):
            archivo_residuo.write(f"r{i+1} = {r_antes[i]}\n")

        archivo_residuo.write(
            f"Norma infinito antes: {verificacion.norma_infinito(r_antes)}\n"
        )

        archivo_residuo.write("\nResiduo despues del refinamiento:\n")

        for i in range(len(r_despues)):
            archivo_residuo.write(f"r{i+1} = {r_despues[i]}\n")

        archivo_residuo.write(
            f"Norma infinito despues: {verificacion.norma_infinito(r_despues)}\n"
        )
    archivo_solucion.close()
    archivo_traza.close()
    archivo_residuo.close()