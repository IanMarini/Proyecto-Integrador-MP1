def sumar(a: float, b: float) -> float:
    return round(a + b, 2)

def restar(a: float, b: float) -> float:
    return round(a - b, 2)

def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return round(a / b, 2)

def multiplicar(a: float, b: float) -> float:
    return round(a * b, 2)

def sumar_n(*args: float) -> float:
    return round(sum(args), 2)

def promedio_n(*args: float) -> float:
    if len(args) == 0:
        raise ValueError("Se necesita al menos un número para calcular el promedio")
    return round(sum(args) / len(args), 2)