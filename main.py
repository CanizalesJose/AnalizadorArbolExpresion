import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox

# Crear clase para estructurar el árbol
class Node:
    def __init__(self, value):
        # Cada nodo tiene un valor y otro nodo a la izquierda y derecha
        self.value = value
        self.left = None
        self.right = None

# Función para comprobar el peso de un operador
def get_precedence(op):
    precedences = {'-': 1, '+': 1, '/': 2, '*': 2, '^': 3}
    return precedences.get(op)

# Función para comprobar si un valor es variable o número
def is_variable_or_number(char):
    return char.isdigit() or char.isalpha()

# Función que construye el árbol
def construct_expression_tree(expression):
    # Función interna para usar solo dentro de esta operación
    def apply_operator(operators, values):
        # Saca un operador de la lista de operadores
        operator = operators.pop()
        # Saca dos operandos de la lista de operandos
        right = values.pop()
        left = values.pop()
        # Crea una rama con el operador como raíz
        node = Node(operator)
        node.left = left
        node.right = right
        # Se agrega a la lista de operandos, reemplazando a los dos valores usados
        values.append(node)
    
    # Se crean las listas de operadores y operandos, así como el conteo para el ciclo
    operators = []
    values = []
    i = 0
    # Recorre cada elemento de la expresión, ignorando los espacios
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        # Si encuentra un parentesis inicia la evaluación de una subexpresión
        if expression[i] == '(':
            operators.append(expression[i])
        elif is_variable_or_number(expression[i]):
            # Si encuentra un operando lo agrega a una lista interna
            token = []
            while i < len(expression) and is_variable_or_number(expression[i]):
                token.append(expression[i])
                i += 1
            values.append(Node(''.join(token)))
            continue
        # Al cerrar el parentesis y la subexpresión se comienzan a evaluar los operadores usando la función interna
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()
        # Si encuentra un operador se comprueba la precedencia comparandolo con los operadores anteriores
        else:
            while (operators and operators[-1] != '(' and get_precedence(operators[-1]) >= get_precedence(expression[i])):
                apply_operator(operators, values)
            operators.append(expression[i])
        
        i += 1
    # Después de recorrer la expresión, se aplican los operadores restantes
    while operators:
        apply_operator(operators, values)
    
    # En la lista, el último valor será la raíz, por lo que se regresa y a partir de ella se puede recorrer el árbol entero
    return values[0]

# Función para construir un grafo usando NetworkX
def buildGraph(graph, node, node_id_map):
    if node is not None:
        # Se crea un identificador para cada nodo y evitar que se tome como repetido
        node_id = id(node)
        node_id_map[node_id] = node.value
        # Si hay un nodo izquierdo, se agrega una conexión y se continúa recursivamente
        if node.left is not None:
            left_id = id(node.left)
            graph.add_edge(node_id, left_id)
            buildGraph(graph, node.left, node_id_map)
        
        # Si hay un nodo derecho, se agrega una conexión y se continúa recursivamente
        if node.right is not None:
            right_id = id(node.right)
            graph.add_edge(node_id, right_id)
            buildGraph(graph, node.right, node_id_map)

def hierarchy_pos(graph, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=None):
    if pos is None:
        pos = {}
    if parsed is None:
        parsed = set()
        
    if root not in parsed:
        parsed.add(root)
        neighbors = list(graph.neighbors(root))
        if parent is not None:
            neighbors.remove(parent)
        if len(neighbors) != 0:
            dx = width / 2
            nextx = xcenter - width / 2 - dx / 2
            for neighbor in neighbors:
                nextx += dx
                pos = hierarchy_pos(graph, neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
        pos[root] = (xcenter, vert_loc)
    return pos

def notacionPolaca(nodo):
    if nodo is None:
        return ""
    result = str(nodo.value)
    left = notacionPolaca(nodo.left)
    right = notacionPolaca(nodo.right)
    return result + (f" {left}" if left else "") + (f" {right}" if right else "")

def inorder(nodo):
    if nodo is None:
        return ""
    left = inorder(nodo.left)
    result = str(nodo.value)
    right = inorder(nodo.right)
    return (f"{left} " if left else "") + result + (f" {right}" if right else "")

def posorder(nodo):
    if nodo is None:
        return ""
    left = posorder(nodo.left)
    right = posorder(nodo.right)
    result = str(nodo.value)
    return (f"{left} " if left else "") + (f"{right} " if right else "") + result

# Función principal
if __name__ == "__main__":
    # (a+b*c)+((d*e+f)*g)
    # 5*4+3*2-1
    tknroot = tk.Tk()
    tknroot.withdraw()
    # Ingresar expresión desde dialogo de texto
    expression = simpledialog.askstring(title='Expresión', prompt='Introducir una expresión')
    # Se construye el arból y se guarda la raíz
    root = construct_expression_tree(expression)

    # Mostrar el árbol graficamente
    G = nx.Graph()
    node_id_map = {}
    buildGraph(G, root, node_id_map)
    pos = hierarchy_pos(G, id(root))
    labels = {node_id: node_value for node_id, node_value in node_id_map.items()}  # Etiquetas
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, node_color="lightgrey", font_size=10, font_weight="bold", edge_color="black")
    plt.show()
    # Generar mensaje
    mensaje = f'Notación polaca:\n{notacionPolaca(root)}\nRecorrido inorden:\n{inorder(root)}\nRecorrido posorden:\n{posorder(root)}'
    # Mostrar resultado
    messagebox.showinfo("Notación polaca", mensaje)