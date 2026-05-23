from generar_llaves import generar_llaves
from firmar import firmar
from verificar import verificar
from generar_llaves import generar_llaves
from emisor import crear_paquete
from receptor import recibir_paquete

if __name__ == "__main__":
    # generar llaves
    p, q, n, phi, e, d, llave_publica, llave_privada = generar_llaves()

    # IVANOVICH (EMISOR)
    _, _, _, _, _, _, llave_publica_ivanovich, llave_privada_ivanovich = generar_llaves()

    # DANIEL (RECEPTOR)
    _, _, _, _, _, _, llave_publica_daniel, llave_privada_daniel = generar_llaves()

    print("\n---- LLAVES GENERADAS ----")
    print("\nIVANOVICH")
    print("Llave pública:", llave_publica_ivanovich)
    print("Llave privada:", llave_privada_ivanovich)

    print("\nDANIEL")
    print("Llave pública:", llave_publica_daniel)
    print("Llave privada:", llave_privada_daniel)

    # mensaje original
    mensaje = "Hola Daniel, este es un mensaje original, ya casi nos graduamos :)"

    print("\n---- CREANDO PAQUETE ----")
    paquete = crear_paquete(
        mensaje=mensaje,
        emisor="Ivanovich",
        receptor="Daniel",
        llave_privada_emisor=llave_publica_ivanovich,
        llave_publica_emisor=llave_publica_ivanovich,
        llave_publica_receptor=llave_publica_daniel
    )
    print("\nPaquete JSON generado correctamente.")

    print("\n---- RECEPCIÓN DEL MENSAJE ----")
    recibir_paquete(
        "paquete.json",
        llave_privada_daniel
    )
    
    """""
    print("\nVALIDACIONES")

    # caso de mensaje vacío
    try:
        firma_vacia = firmar("", llave_privada)
        print("mensaje vacío firmado:", firma_vacia)
    except:
        print("error con mensaje vacío")

    # caso mensaje alterado
    mensaje2 = "esto es un mensaje alterado"
    print("firma válida con mensaje alterado:", verificar(mensaje2, firma, llave_publica))

    # llave incorrecta
    _, _, _, _, _, _, otra_pub, otra_priv = generar_llaves()
    print("firma válida con llave incorrecta:", verificar(mensaje, firma, otra_pub))

    # entrada inválida
    try:
        firmar(12345, llave_privada)
    except:
        print("error detectado en entrada inválida")

    # firma incorrecta
    firma_falsa = firma + 1
    print("firma falsa válida:", verificar(mensaje, firma_falsa, llave_publica))
    """