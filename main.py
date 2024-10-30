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

def isNumber(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validateValues(expression):
    for element in expression:
        if element not in ['-', '+', '/', '*', '^'] and not isNumber(element):
            messagebox.showwarning('Error', f'La expresión {expression} incluye variables, por lo que no se puede generar código ensambalor a partir de ella')
            return;
    return generateCode(expression);

def generateCode(expression):
    stack = []
    code = []
    temp_var_counter = 0

    # Generar el bloque .data
    code.append(".model small")
    code.append(".stack 100h")
    code.append(".data")
    
    # Función para crear nuevas variables temporales
    def new_temp_var():
        nonlocal temp_var_counter
        var_name = f"TEMP{temp_var_counter} DW ?"
        temp_var_counter += 1
        return var_name

    # Crear variables temporales para cada número en la expresión
    for _ in expression:
        code.append(new_temp_var())

    code.append(".code")
    code.append("main proc")

    # Reiniciar el contador de variables temporales para su uso
    temp_var_counter = 0

    for token in expression:
        if token.isdigit():
            # Si es un número, guardarlo en la última variable temporal disponible
            temp_var = f"TEMP{temp_var_counter}"
            code.append(f'MOV {temp_var}, {token}')
            stack.append(temp_var)
            temp_var_counter += 1
        else:
            # Si es un operador, sacar los dos últimos operandos
            if len(stack) >= 2:
                reg2 = stack.pop()
                reg1 = stack.pop()
                
                temp_var = f"TEMP{temp_var_counter}"
                temp_var_counter += 1

                if token == '+':
                    code.append(f'MOV AX, {reg1}')
                    code.append(f'ADD AX, {reg2}')
                    code.append(f'MOV {temp_var}, AX')

                elif token == '-':
                    code.append(f'MOV AX, {reg1}')
                    code.append(f'SUB AX, {reg2}')
                    code.append(f'MOV {temp_var}, AX')

                elif token == '*':
                    code.append(f'MOV AX, {reg1}')
                    code.append(f'IMUL {reg2}')
                    code.append(f'MOV {temp_var}, AX')

                elif token == '/':
                    code.append(f'MOV AX, {reg1}')
                    code.append(f'IDIV {reg2}')
                    code.append(f'MOV {temp_var}, AX')

                # Guardar el resultado temporal en el stack
                stack.append(temp_var)

    code.append('''
MOV BX, 10
XOR CX, CX
CONVERT:
    XOR DX, DX
    DIV BX
    ADD DL, '0'
    PUSH DX
    INC CX
    TEST AX, AX
    JNZ CONVERT

PRINT_DIGITS:
    POP DX
    MOV AH, 02h
    INT 21h
    LOOP PRINT_DIGITS

    MOV AH, 4Ch
    INT 21h''')
    
    code.append("main endp")
    code.append("end main")
    
    return code


# Función principal
if __name__ == "__main__":
    tknroot = tk.Tk()
    tknroot.withdraw()
    # Ingresar expresión desde dialogo de texto
    expression = simpledialog.askstring(title='Expresión', prompt='Introducir una expresión')
    if expression == '':
        messagebox.showinfo('Error', 'No se ha proporcionado una expresión')
        exit(0)
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
    messagebox.showinfo("Recorridos", mensaje)
    code = ''
    for line in validateValues(posorder(root).split()):
        code += line+'\n'
    # Generar NEWCODE.asm
    with open('C:/dos/masm/NEWCODE.asm', 'w') as f:
        f.write(code)
    messagebox.showinfo('Código Generado', 'El código ha sido generado y guardado en C:/dos/masm/NEWCODE.asm')
    # Pruebas
    # (a+b*c)+((d*e+f)*g)
    # 5*4+3*2-1
    # (6+2)*(5-3)
    # 7*(4+3)-2