import os

def crear_clave_sesion():
    # 1 byte y [0] extraer primer byte como número entero 0-255
    clave_sesion = os.urandom(1)[0]
    
    # Por si sigue saliendo 0 no guardar ese dato
    while clave_sesion == 0:
        clave_sesion = os.urandom(1)[0]
        
    return clave_sesion 

def cifrar_mensaje(mensaje, clave):
    # Validamos que el valor sea un texto
    if not isinstance(mensaje, str) or not mensaje.strip():
      raise ValueError("El mensaje debe ser texto")
    
    # Lista guardar mensaje cifrado 
    mensaje_cifrado = []

    # Cada char
    for c in mensaje:
        # Char a ASCII
        ascii = ord(c)

        # XOR con clave
        ascii_cifrado = ascii ^ clave

        mensaje_cifrado.append(ascii_cifrado)


    return mensaje_cifrado

def descifrar_mensaje(mensaje_cifrado, clave):
    mensaje_descifrado = "" 

    # Cada número cifrado de la lista 
    for num in mensaje_cifrado:

        # Se revierte XOR
        ascii_descifrado = num ^ clave

        # Se va agregando caracter por caracter como char
        mensaje_descifrado += chr(ascii_descifrado)
    
    return mensaje_descifrado