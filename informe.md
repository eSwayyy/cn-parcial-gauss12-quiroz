## Identificación

* **Autor**: Alonso Vergara\
* **Asignatura**: Computación numérica (INF-321)\
* Universidad católica del Maule
* **Fecha de entrega**: Sábado, 21 de noviembre, 01:00
* [**Link del repositorio**](https://github.com/eSwayyy/laboratorio2-la-raiz-que-se-esconde)

## Planteamiento
El problema se presenta como una resolución de un sistema de 12 ecuaciones lineales:
$$
Ax = b
$$
Donde $A$ es una matriz densa de 12x12 y $b$ es el vector de términos independientes.

Además, las filas presentann magnitudes muy diferentes, que van $10^{-8}...10^5$, por lo que sus coeficientes no están en una escala uniforme.

Este sistema es costoso de resolver ya que, al ser una matriz densa, no se pueden omitir operaciones aprovechando elementos nulos, las diferencias de escala, el pivote inicial pequeño y la casi dependencia lineal de la fila 7 hacen que se presenten dificultades a la hora de querer obtener una solución precisa.

## Estrategia de eliminación
Se realizaron 11 pasos, eliminando los elementos bajo la diagonal columna por columna, desde la primera hasta la undecima, actualizando solo los elementos necesarios de cada fila, sin recorrer columnas previamente eliminadas. Cada multiplicador $m_{ij}$ se calcula una sola vez y se utiliza para actualizar toda la fila correspondiente.

## Conteo de operaciones
Tomando en cuenta que cada operación aritmética elemental cuenta como un flop:

### Método: escalado

| Paso | Mult/Div | Sumas/Restas | Total |
|---|---:|---:|---:|
| 1 | 143 | 132 | 275 |
| 2 | 120 | 110 | 230 |
| 3 | 99 | 90 | 189 |
| 4 | 80 | 72 | 152 |
| 5 | 63 | 56 | 119 |
| 6 | 48 | 42 | 90 |
| 7 | 35 | 30 | 65 |
| 8 | 24 | 20 | 44 |
| 9 | 15 | 12 | 27 |
| 10 | 8 | 6 | 14 |
| 11 | 3 | 2 | 5 |

- Multiplicaciones/divisiones: 716
- Sumas/restas: 638
- Total flops: 1354
- Comparaciones: 66
- Intercambios: 8

Comparacion:
$$
T_{flops}\in 1486 \pm 10\% \approx (1337.4, 1634.6)
$$

## Análisis de mantisa y pivoteo
Se realizaron ejecuciones del algoritmo sin pivote, con pivoteo parcial y con pivoteo parcial escalado, obteniendo:
| Indicador | Sin pivoteo | Pivoteo parcial | Pivoteo Escalado |
|---|---|---|---|
| Multiplicador máximo | 2.752593e+13 | 6.198819e-01 | 2.465558e+09
| Factor de crecimiento | 2.641224e+03 | 1.000000e+00 | 1.783202e+00
| Error relativo | 2.077712e-10 | 2.972444e-13 | 1.903612e-14

Se puede observar que el multiplicador máximo se encuentra cuando no se aplica pivoteo, esto porque el primer pivote $a_{11}=1.3407\times10^{-8}$ es demasiado pequeño en comparación a los demás elementos.

Como se trabaja con números de doble precisión, se dispone de 53 bits de mantisa. Para estimar la diferencia de magnitud asociada al multiplicador máximo sin pivoteo, se calcula:

$$
\log_2(2.752593\times10^{13})\approx44.6\text{ bits}
$$

Esto indica una diferencia de aproximadamente 45 posiciones binarias, lo que puede provocar una pérdida importante de precisión durante las operaciones. Sin embargo, no significa que se hayan perdido exactamente 45 bits en la solución final.

Finalmente, al comparar los errores relativos obtenidos respecto a la solución de NumPy, se observa que el pivoteo parcial escalado presenta el menor error, por lo que fue el método que entregó los resultados más precisos en esta ejecución.

## Condicionamiento

Utilizaremos el número de condición proporcionado por la pauta  $\kappa_2(A)\approx 3.08\times10^{13}$, y la precisión de máquina $\varepsilon\approx2.22\times10^{-16}$.

Con esos valores, la pauta especifica la siguiente cota:

$$
\kappa_2(A)\cdot\varepsilon
=(3.08\times10^{13})(2.22\times10^{-16})
\approx6.84\times10^{-3}
$$

Para estimar cuántos dígitos significativos se pueden garantizar, calculamos:

$$
-\log_{10}(6.84\times10^{-3})\approx2.16
$$

Por lo que no permite garantizar más de aproximadamente 2 dígitos significativos correctos.

Sin embargo, esta cota resulta pesimista para el sistema, ya que considera una amplificación del error en el peor caso posible. En las ejecuciones realizadas se obtuvieron errores relativos menores, especialmente utilizando pivoteo parcial escalado.

## Resultados

Ya que no se pedía directamente programar los dígitos significativos, utilizaremos el error relativo individual, calculado con la solución de referencia por un asistente de IA.

$$
e_i=\left|\frac{x_i-x_i^{ref}}{x_i^{ref}}\right|
$$

La cantidad de dígitos significativos correctos se determina mediante:

$$
d_i=\max\left(0,\left\lfloor-\log_{10}(2e_i)\right\rfloor+1\right)
$$
Esto nos entrega los siguientes resultados:

### Metodo: Parcial escalado
| Incógnita | Valor obtenido  | Dígitos significativos correctos |
|--|--|--|
|$x_{1}$| 0.73849156269994642       | 13|
|$x_{2}$| -1.2059374167993291       | 12|
|$x_{3}$| 0.0043871952003642833     | 10|
|$x_{4}$| -0.091726453800233448     | 12|
|$x_{5}$| 2.8461093724996567        | 13|
|$x_{6}$| -0.0062815408994638128    | 10|
|$x_{7}$|1.4738205916004574         | 13|
|$x_{8}$|-0.038492716399937434      | 12|
|$x_{9}$|0.91526480369982921        | 13|
|$x_{10}$|-2.607139485200364        | 13|
|$x_{11}$|0.051873629399935429      | 12|
|$x_{12}$| -1.0849371625003397      | 13|

Observamos que los dígitos significativos corresctos se encuentran entre 10 y 13, demostrando así que a pesar de que la matríz se encontrara mal condicionada, el pivoteo escalado permitió obtener una solución con una precisión mucho mayor a la estimada mediante la cota del condicionamiento.

## Verificación
Para verificar la solución obtenida mediante pivoteo parcial escalado, se calculó el residuo utilizando precisión extendida con la librería Decimal, mediante la siguiente ecuación:

$$
r=b-Ax
$$

Posteriormente, se calculó la norma infinito del residuo:

$$
|r|_\infty=\max_i|r_i|
$$

El valor obtenido fue:

$$
|r|_\infty=4.26480233174\times10^{-10}
$$

Además, se realizó una pasada de refinamiento iterativo, resolviendo el sistema $A\Delta x=r$ y actualizando la solución:

$$
x_{\text{nuevo}}=x+\Delta x
$$

Después del refinamiento, se obtuvo:

$$
|r_{\text{nuevo}}|_\infty=5.0148654606\times10^{-11}
$$

Se observa que el refinamiento iterativo redujo la norma infinito del residuo aproximadamente 8.5 veces, lo que indica una mejora en la precisión con la que la solución satisface el sistema original.

Finalmente, se comparó la solución obtenida con la función numpy.linalg.solve, utilizada únicamente como control independiente. El error relativo respecto a esta solución fue aproximadamente:

$$
e_{\text{relativo}}=1.903612\times10^{-14}
$$

## Conclusiones

Se optó por utilizar la eliminación gaussiana con pivoteo parcial escalado, ya que fue el método que obtuvo el menor error relativo, de $1.903612\times10^{-14}$, con un total de 1354 flops, 66 comparaciones y 8 intercambios de filas.

Si bien el pivoteo requiere algunas operaciones adicionales, la diferencia en el costo es pequeña en comparación con la mejora en la precisión. Además, al aplicar el refinamiento iterativo, la norma infinito del residuo disminuyó de $4.26480233174\times10^{-10}$ a $5.0148654606\times10^{-11}$, por lo que la solución logró satisfacer el sistema con un residuo menor.

En caso de trabajar con una matriz de 1000×1000, seguiría utilizando pivoteo para evitar errores numéricos, pero buscaría optimizar las operaciones y reutilizar los multiplicadores calculados. Esto sería importante porque, a medida que aumenta el tamaño de la matriz, también aumenta considerablemente la cantidad de operaciones necesarias para resolver el sistema.

## Reproducibilidad

Para ejecutar el programa se utilizó Python y la librería NumPy, con las siguientes versiones:

- **Python:** 3.14.3
- **NumPy:** 2.5.4

Las dependencias necesarias se encuentran en el archivo `requirements.txt`.

Para reproducir los resultados, se deben instalar las dependencias y ejecutar el siguiente comando desde la carpeta principal del proyecto:

```bash
pip install -r requirements.txt
python src/main.py
```

Al ejecutar el programa, se generan automáticamente los archivos de la carpeta `resultados/`, que contienen las soluciones, la traza de eliminación, el conteo de operaciones y los residuos calculados.