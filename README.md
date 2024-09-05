## Árboles de Expresión
El proyecto consiste en un solo archivo, este contiene la clase `Node`, que es la estructura básica del árbol.

La función `get_precedence` es una función auxiliar que permite identificar el peso de los operadores.

La función `construct_expression_tree` tiene una subfunción `apply_operator` y esta es una función que construye la estructura del árbol a partir de una expresión. Va recorriéndola, juntando los caracteres que forman un operando y aplicando los operadores en la ubicación del árbol que le corresponde.

La función `print_tree` recibe el nodo raíz, la identación y la dirección del último nodo imprimido, pero estos dos últimos son opcionales y solo se usan durante la ejecución recursiva. Al invocarla usando un nodo raíz, te imprime, usando una representación gráfica, la estructura del árbol.

Para ejecutarlo se usa `python main.py` y te pedirá ingresar una expresión infija, puede o no tener paréntesis.

### Notas
- No admite variables, solo números enteros
- No esta bien testeado