from prep_mensaje import hash_mensaje

def firmar(mensaje, llave_privada):
  #extraemos los valores de la llave privada
    d, n = llave_privada
    #convertimos el mensaje en un numero usando hash
    h = hash_mensaje(mensaje) % n
    #generamos la firma digital
    firma = pow(h, d, n)
    return firma