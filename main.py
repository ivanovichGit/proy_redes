from generar_llaves import generar_llaves
from firmar import firmar
from verificar import verificar

if __name__ == "__main__":
    # generar llaves
    p, q, n, phi, e, d, llave_publica, llave_privada = generar_llaves()

    print("LLAVES GENERADAS")
    print("Llave pública:", llave_publica)
    print("Llave privada:", llave_privada)

    # mensaje original
    mensaje = "este es un mensaje original"

    # firmar mensaje
    firma = firmar(mensaje, llave_privada)

    print("\nMENSAJE ORIGINAL")
    print("Mensaje:", mensaje)
    print("Firma:", firma)

    # verificar firma original
    print("\nVERIFICACIÓN ORIGINAL")
    print("Firma válida:", verificar(mensaje, firma, llave_publica))


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