## Árboles de Expresión
El proyecto consiste en un solo archivo, este contiene la clase `Node`, que es la estructura básica del árbol.
***
La función `get_precedence` es una función auxiliar que permite identificar el peso de los operadores y poder  evaluarlos en el órden correcto.
***
La función `construct_expression_tree` tiene una subfunción `apply_operator` y esta es una función que construye la estructura del árbol a partir de una expresión. Va recorriéndola, juntando los operandos y reconociendo operadores, cuando se encuentra listo para evaluarlos, manda a llamar a la función `apply_operator` para tomar dos operandos y un operador y formar una rama.
Devuelve el nodo raíz, junto con dos nodos al lado izquierdo y derecho.
***
Se hace uso de la librería `NetworkX` para generar un grafo y poder mostrarlo usando la librería `Matplotlib`.
Para lograrlo se hace uso de dos funciones, una para construir el grafo (`buildGraph`) y otra para calcular la jerarquía de posiciones (`hierarchy_pos`).
***
En la función principal se pide por consola una expresión que puede contener números o variables, además de parentesis, por ejemplo:
- $(a+b*c)+((d*e+f)*g)$
- $5*4+3*2-1$

### Requisitos
Para ejecutar el programa se debe tener instalado:
- `Python 3.x`
- `pip 20.x` en adelante
- Librería `NetworkX`
- Librería `Matplotlib`

Para ejecutar, se debe ingresar a la carpeta donde esta instalado y usar el interprete de python con el comando
`py ./main.py`