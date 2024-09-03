import networkx as nx
import matplotlib.pyplot as plt
import re
# Peso de operadores
# ^ Derecha - Izquierda
# / * Izquierda - Derecha
# - + Izquierda - Derecha

def leerExpresion(expresion):
    expresion = expresion.replace(" ", "")
    regex = r'(\d+|[a-zA-Z][a-zA-Z0-9]*)([\-\+\/\*\^](\d+|[a-zA-Z][a-zA-Z0-9]*))*'
    if not re.fullmatch(regex, expresion):
        raise ValueError('La expresión no coincide')
    print(f'Se analiza la expresión {expresion}')
    operando = ''
    operandos = []
    operadores = []
    grafo = nx.Graph()
    for elemento in expresion:
        if elemento not in ['-', '+', '/', '*', '^']:
            operando += elemento
        else:
            operandos.append(operando)
            grafo.add_node(operando)

            operando = ''
        if elemento in ['-', '+', '/', '*', '^']:
            operadores.append(elemento)
            grafo.add_node(elemento)
    print(operandos)
    print(operadores)
    return grafo


testExpression = '51*42/56+38/23*62-56*94'

plt.figure(figsize=(12, 6))
nx.draw(leerExpresion(testExpression), with_labels=True)
plt.show()
