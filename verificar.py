from prep_mensaje import hash_mensaje

def verificar(mensaje, firma, llave_publica):
  #extraemos los valores de la llave publica
    e, n = llave_publica
    #calculamos el hash del mensaje y lo reducimos a n
    h = hash_mensaje(mensaje) % n
    #deshacemos lo que se hizo al firmar
    h_verificado = pow(firma, e, n)
    return h == h_verificado
