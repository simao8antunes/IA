import math

#Exercicio 4.1
impar = lambda a: a % 2 == 1 

#Exercicio 4.2
positivo = lambda a: a > 0 

#Exercicio 4.3
comparar_modulo = lambda x, y: abs(x) < abs(y) 

#Exercicio 4.4
cart2pol = lambda x, y: (math.hypot(x,y), math.atan2(y, x))

#Exercicio 4.5
ex5 = lambda f, g, h: lambda x,y,z: h(f (x, y), g(y, z)) 

#Exercicio 4.6
def quantificador_universal(lista, f):
    if lista == []:
        return True

    return f(lista[0]) and quantificador_universal(lista[1:], f) 

#Exercicio 4.8
def subconjunto(lista1, lista2):
    return quantificador_universal(lista1, lambda a1: a1 in lista2)

#Exercicio 4.9
def menor_ordem(lista, f):
    if lista == []:
        return None
    if len(lista) == 1:
        return lista[0]

    m = menor_ordem(lista[1:], f)

    if f(lista[0], m):
        return lista[0]
    return m


#Exercicio 4.10
def menor_e_resto_ordem(lista, f):
    if lista == []:
        return None, []
    if len(lista) == 1:
        return lista[0], []

    m, r = menor_e_resto_ordem(lista[1:], f)

    if f(lista[0], m):
        return lista[0], [m] + r
    return m, [lista[0]] + r



#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    pass
