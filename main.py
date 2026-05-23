import json
from generar_llaves import generar_llaves
from emisor import crear_paquete
from receptor import recibir_paquete
from verificar import verificar
from firmar import firmar

if __name__ == "__main__":
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
    mensaje = "Hola Daniel, este es un mensaje original :)"

    print("\n---- CREANDO PAQUETE ----")
    paquete = crear_paquete(
        mensaje=mensaje,
        emisor="Ivanovich",
        receptor="Daniel",
        llave_privada_emisor=llave_privada_ivanovich,
        llave_publica_emisor=llave_publica_ivanovich,
        llave_publica_receptor=llave_publica_daniel
    )
    print("\nPaquete JSON generado correctamente.")

    print("\n---- RECEPCIÓN DEL MENSAJE ----")
    resultado_recepcion = recibir_paquete(
        "paquete.json",
        llave_privada_daniel
    )

    # Para hacer las validaciones en main 
    mensaje_descifrado, firma = resultado_recepcion
    
    print("\n---- VALIDACIONES ----")

    # Verificar la firma digital usando la llave pública del emisor;
    firma_valida = verificar(mensaje_descifrado, firma, llave_publica_ivanovich)
    
    # 1. Mensaje válido enviado del emisor al receptor;
    print("\n1. Caso mensaje válido")
    if firma_valida:
        print("La firma es válida.")
        print("El mensaje no fue alterado y corresponde al emisor.")
    else:
        print("La firma NO es válida.")
        print("El mensaje pudo haber sido alterado o la llave pública es incorrecta.")

    # 2. Mensaje vacío
    print("\n2. Caso mensaje vacío")
    try:
        firma_vacia = firmar("", llave_privada_ivanovich)
        print("Mensaje vacío firmado:", firma_vacia)
    except:
        print("Error con mensaje vacío")
    
    # 3. Mensaje alterado después de haber sido firmado
    print("\n3. Caso mensaje alterado después de haber sido firmado")
    
    mensaje_alterado = "Hola Daniel, este es un mensaje alterado"
    firma_valida = verificar(mensaje_alterado, firma, llave_publica_ivanovich)
    
    if firma_valida:
        # Por si no marca error, no deberia de ser validada de todos modos
        print("Error: La firma sigue siendo válida")
    else:
        print("La firma NO es válida.")
        print("El mensaje fue modificado después de ser firmado.")

    # 4. Firma alterada manualmente dentro del JSON
    print("\n4. Firma alterada manualmente dentro del JSON")
    
    # Abrir json 
    with open("paquete.json", "r") as archivo:
        paquete_alterado = json.load(archivo)

    paquete_alterado["signature"] += 1

    # Guardamos JSON alterado 
    with open("paquete_firma_alterada.json", "w") as archivo:
        json.dump(paquete_alterado, archivo, indent=4)

    resultado_firma_alterada = recibir_paquete(
        "paquete_firma_alterada.json",
        llave_privada_daniel
    )

    mensaje_descifrado_alterado, firma_alterada = resultado_firma_alterada
    firma_valida = verificar(mensaje_descifrado_alterado, firma_alterada, llave_publica_ivanovich)

    if firma_valida:
        print("Error: La firma alterada sigue siendo válida")
    else:
        print("La firma fue modificada manualmente dentro del JSON.")

    # 5. Intento de verificación con una llave pública incorrecta
    print("\n5. Intento de verificación con una llave pública incorrecta")

    _, _, _, _, _, _, otra_pub, otra_priv = generar_llaves()
    firma_valida = verificar(
        mensaje,
        firma,
        otra_pub
    )
    if firma_valida:
        print("Error: la firma fue validada con una llave incorrecta")
    else:
        print("La firma NO es válida.")
        print("La llave pública no corresponde al emisor.")
        
    # 6. Intento de descifrado con la llave privada de otro usuario
    print("\n6. Intento de descifrado con la llave privada de otro usuario")
    _, _, _, _, _, _, llave_publica_vanessa, llave_privada_vanessa = generar_llaves()

    recibir_paquete(
        "paquete.json",
        llave_privada_vanessa
    )

    # 7. Paquete JSON incompleto
    
    # 8. Paquete JSON con datos mal formados
    
    # 9. Firma que no corresponde al mensaje recibido

    """""
    # entrada inválida
    try:
        firmar(12345, llave_privada)
    except:
        print("error detectado en entrada inválida")

    # firma incorrecta
    firma_falsa = firma + 1
    print("firma falsa válida:", verificar(mensaje, firma_falsa, llave_publica))
    """""