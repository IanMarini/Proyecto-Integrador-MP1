import aritmetica

def test_sumar():
    assert aritmetica.sumar(3.5, 2.2) == 5.7
    assert aritmetica.sumar(-1, 1) == 0.0
    assert aritmetica.sumar(0, 0) == 0.0

def test_restar():
    assert aritmetica.restar(10, 5) == 5.0
    assert aritmetica.restar(-1, -1) == 0.0
    assert aritmetica.restar(5, 10) == -5.0

def test_dividir():
    assert aritmetica.dividir(10, 2) == 5.0
    assert aritmetica.dividir(5, 2) == 2.5
    try:
        aritmetica.dividir(10, 0)
    except ValueError:
        assert True

def test_multiplicar():
    assert aritmetica.multiplicar(3, 2) == 6.0
    assert aritmetica.multiplicar(-1, 2) == -2.0
    assert aritmetica.multiplicar(0, 10) == 0.0

def test_sumar_n():
    assert aritmetica.sumar_n(1, 2, 3, 4) == 10.0
    assert aritmetica.sumar_n(0, 0, 0) == 0.0
    assert aritmetica.sumar_n(1.1, 2.2) == 3.3

def test_promedio_n():
    assert aritmetica.promedio_n(10, 20, 30) == 20.0
    assert aritmetica.promedio_n(1, 1, 1, 1) == 1.0
    try:
        aritmetica.promedio_n()
    except ValueError:
        assert True

if __name__ == "__main__":
    test_sumar()
    test_restar()
    test_dividir()
    test_multiplicar()
    test_sumar_n()
    test_promedio_n()
    print("Todos los tests pasaron correctamente.")