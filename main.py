import networkx as nx
import matplotlib.pyplot as plt
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def get_precedence(op):
    precedences = {'-': 1, '+': 1, '/': 2, '*': 2, '^': 3}
    return precedences.get(op, 0)

def construct_expression_tree(expression):
    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        node = Node(operator)
        node.left = left
        node.right = right
        values.append(node)
    
    operators = []
    values = []
    i = 0
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        
        if expression[i] == '(':
            operators.append(expression[i])
        elif expression[i].isdigit():
            num = []
            while i < len(expression) and expression[i].isdigit():
                num.append(expression[i])
                i += 1
            values.append(Node(''.join(num)))
            continue
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()
        else:
            while (operators and operators[-1] != '(' and
                   get_precedence(operators[-1]) >= get_precedence(expression[i])):
                apply_operator(operators, values)
            operators.append(expression[i])
        
        i += 1
    
    while operators:
        apply_operator(operators, values)
    
    return values[0]


def print_tree(node, indent="", last='updown'):
    if node is not None:
        # Recursivamente imprime el subárbol derecho
        print_tree(node.right, indent + "     ", 'up')
        
        # Imprime el valor del nodo con formato gráfico
        updown = '┌── ' if last == 'up' else '└── ' if last == 'down' else '─── '
        print(indent + updown + str(node.value))
        
        # Recursivamente imprime el subárbol izquierdo
        print_tree(node.left, indent + "     ", 'down')

def buildGraph(graph, node, node_id_map):
    if node is not None:
        # Se crea un identificador para cada nodo y evitar que se repita
        node_id = id(node)
        node_id_map[node_id] = node.value
        # Si hay un nodo izquierdo, agregamos el borde y seguimos recursivamente
        if node.left is not None:
            left_id = id(node.left)
            graph.add_edge(node_id, left_id)
            buildGraph(graph, node.left, node_id_map)
        
        # Si hay un nodo derecho, agregamos el borde y seguimos recursivamente
        if node.right is not None:
            right_id = id(node.right)
            graph.add_edge(node_id, right_id)
            buildGraph(graph, node.right, node_id_map)

def hierarchy_pos(graph, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=None):
    if pos is None:
        pos = {}
    if parsed is None:
        parsed = set()
        
    # Asegurarse de que el nodo raíz no ha sido procesado antes
    if root not in parsed:
        parsed.add(root)
        neighbors = list(graph.neighbors(root))
        if parent is not None:  # eliminar al nodo padre de la lista de vecinos
            neighbors.remove(parent)
        if len(neighbors) != 0:
            dx = width / 2
            nextx = xcenter - width / 2 - dx / 2
            for neighbor in neighbors:
                nextx += dx
                pos = hierarchy_pos(graph, neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
        pos[root] = (xcenter, vert_loc)
    return pos

# Ejemplo de uso
# expression = "(1+2*3)+((4*5+6)*7)"
expression = input('Ingresar una expresión infija: ')
root = construct_expression_tree(expression)

# Mostrar el árbol en orden
G = nx.Graph()
node_id_map = {}
buildGraph(G, root, node_id_map)
pos = hierarchy_pos(G, id(root))
labels = {node_id: node_value for node_id, node_value in node_id_map.items()}  # Etiquetas
nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, node_color="lightgrey", font_size=10, font_weight="bold", edge_color="black")
plt.show()

print_tree(root)
