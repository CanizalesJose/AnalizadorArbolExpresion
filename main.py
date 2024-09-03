import re
# Peso de operadores
# ^ Derecha - Izquierda
# / * Izquierda - Derecha
# - + Izquierda - Derecha

def leerExpresion(expresion):
    print(f'Se analiza la expresión {expresion}')
    operando = ''
    operandos = []
    operadores = []
    for elemento in expresion:
        if elemento not in ['-', '+', '/', '*', '^']:
            operando += elemento
        else:
            operandos.append(operando)
            operando = ''
        if elemento in ['-', '+', '/', '*', '^']:
            operadores.append(elemento)
        
    print(operandos)
    print(operadores)


testExpressions = ['51*42/56+38/23*62-56*94']
for expresion in testExpressions:
    leerExpresion(expresion)