import os

def crear_clave_sesion():
    # 1 byte y [0] extraer primer byte como número entero 1-256
    clave_sesion = os.urandom(1)[0] + 1
        
    return clave_sesion 

def cifrar_mensaje(mensaje, clave_sesion):
    # Validamos que el valor sea un texto
    if not isinstance(mensaje, str) or not mensaje.strip():
      raise ValueError("El mensaje debe ser texto")
    
    # Lista guardar mensaje cifrado 
    mensaje_cifrado = []

    # Cada char
    for c in mensaje:
        # Char a ASCII
        ascii = ord(c)

        # XOR con clave de sesion
        ascii_cifrado = ascii ^ clave_sesion

        mensaje_cifrado.append(ascii_cifrado)


    return mensaje_cifrado

def descifrar_mensaje(mensaje_cifrado, clave_sesion):
    mensaje_descifrado = "" 

    # Cada número cifrado de la lista 
    for num in mensaje_cifrado:

        # Se revierte XOR con clave de sesión 
        ascii_descifrado = num ^ clave_sesion

        # Se va agregando caracter por caracter como char
        mensaje_descifrado += chr(ascii_descifrado)
    
    return mensaje_descifrado