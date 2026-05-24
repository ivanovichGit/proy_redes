import os


#con esta funcion validamos si un numero es o no primo
def es_primo(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

# Generamos un numero primo  100-3000 (en criptografia real se utilizaria un rango mucho mas grande)
def generar_primo():
    while True:
        bytes_aleatorios = os.urandom(2)
        num = int.from_bytes(bytes_aleatorios, "big")
        num = 100 + (num % 2901)

        if num % 2 == 0:
            num += 1
        if es_primo(num):
            return num

def mcd(a, b):
    while b:
        a, b = b, a % b
    return a

def inverso_modular(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d

def generar_llaves():
    p = generar_primo()
    q = generar_primo()
    while q == p:
        q = generar_primo()
    #es el mundo donde trabajan los numeros
    n = p * q
    # cantidad de números menores que n que son coprimos con n
    phi = (p - 1) * (q - 1)

    #exponente publico
    e = 3

    #mientras e y phi no sean comprimos seguimos cambiando e
    #su maximo comun divisor debe de ser 1
    while mcd(e, phi) != 1:
        e += 2
        
    # este es el que mantendremos privado
    d = inverso_modular(e, phi)

    return p, q, n, phi, e, d, (e, n), (d, n)

# generamos las llaves y obtenemos todos los datos correspondiente para autoexplicarnos lo que esta sucediendo
p, q, n, phi, e, d, llave_publica, llave_privada = generar_llaves()

"""""
Comentarios de explicación ahora no necesarios.
print("Generamos las llaves\n")

print(f"p (primo): {p}")
print(f"q (primo): {q}")

print("\n")
print(f"n = {n}")
print(f"phi(n) = {phi}")

print("\n")
print(f"e (exponente público): {e}")
print(f"d (exponente privado): {d}")

print("\n")
print("LLAVES")
print(f"Llave pblica: (e={e}, n={n})")
print("(Esta llave se puede compartir)\n")

print(f"Llave privada: (d={d}, n={n})")
print("(Esta llave debe mantenerse en secreto)\n")
"""