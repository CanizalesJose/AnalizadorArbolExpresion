from pyparsing import (
    Word, alphas, nums, oneOf, Forward, Group, ZeroOrMore, infixNotation, opAssoc
)
import operator

# Definir operadores
expr_stack = []

def push_first(tokens):
    expr_stack.append(tokens[0])

def parse_expression(expr):
    expr_stack.clear()

    # Definir gramática
    operand = Word(alphas, exact=1) | Word(nums)
    operator = oneOf("+ - * / ^")
    expr = Forward()
    atom = operand | Group('(' + expr + ')')
    term = infixNotation(atom, [
        (oneOf("^"), 2, opAssoc.RIGHT, push_first),
        (oneOf("* /"), 2, opAssoc.LEFT, push_first),
        (oneOf("+ -"), 2, opAssoc.LEFT, push_first),
    ])
    expr <<= term

    parsed_expr = expr.parseString(expr, parseAll=True)
    return parsed_expr

# Generar el árbol de expresión
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_expression_tree():
    token = expr_stack.pop(0)
    node = Node(token)
    
    if token in "+-*/^":
        node.left = build_expression_tree()
        node.right = build_expression_tree()

    return node

# Función para imprimir el árbol de expresión
def print_expression_tree(node, level=0):
    if node is not None:
        print_expression_tree(node.right, level + 1)
        print(' ' * 4 * level + '->', node.value)
        print_expression_tree(node.left, level + 1)

# Ejemplo de expresiones
expressions = [
    "5*4/5+3/2*6-5",
    "(a+b*c)+((d*e+h)*g)"
]

# Parsear y construir el árbol para cada expresión
for expr in expressions:
    print(f"\nExpresión: {expr}")
    parse_expression(expr)
    tree = build_expression_tree()
    print("Árbol de expresión:")
    print_expression_tree(tree)
