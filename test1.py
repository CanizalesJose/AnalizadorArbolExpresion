class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def get_precedence(op):
    precedences = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
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

def inorder_traversal(node):
    if node is not None:
        inorder_traversal(node.left)
        print(node.value, end=' ')
        inorder_traversal(node.right)

# Ejemplo de uso
expression = "51*42/56+38/23*62-56*94"
root = construct_expression_tree(expression)

# Mostrar el árbol en orden
inorder_traversal(root)
