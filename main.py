import json
from generar_llaves import generar_llaves
from emisor import crear_paquete
from receptor import recibir_paquete
from verificar import verificar
from firmar import firmar

if __name__ == "__main__":
    # IVANOVICH (EMISOR)
    # _, _, _, _, _, _, llave_publica_ivanovich, llave_privada_ivanovich = generar_llaves()
    p_i, q_i, n_i, phi_i, e_i, d_i, llave_publica_ivanovich, llave_privada_ivanovich = generar_llaves()
    
    # DANIEL (RECEPTOR)
    p_d, q_d, n_d, phi_d, e_d, d_d, llave_publica_daniel, llave_privada_daniel = generar_llaves()

    print("\n---- LLAVES GENERADAS Y MENSAJE ----")
    print("\nIVANOVICH")
    print(f"p (primo): {p_i}")
    print(f"q (primo): {q_i}")
    print(f"n = {n_i}")
    print(f"phi(n) = {phi_i}")
    print(f"e (exponente público): {e_i}")
    print(f"d (exponente privado): {d_i}")
    print("Llave pública:", llave_publica_ivanovich)
    print("Llave privada:", llave_privada_ivanovich)
    
    print("\nDANIEL")
    print(f"p (primo): {p_d}")
    print(f"q (primo): {q_d}")
    print(f"n = {n_d}")
    print(f"phi(n) = {phi_d}")
    print(f"e (exponente público): {e_d}")
    print(f"d (exponente privado): {d_d}")
    print("Llave pública:", llave_publica_daniel)
    print("Llave privada:", llave_privada_daniel)

    # mensaje original
    mensaje = "Hola Daniel, este es un mensaje original :)"
    
    print("\nMensaje original:", mensaje)

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
    with open("paquete_V4_firma_alterada.json", "w") as archivo:
        json.dump(paquete_alterado, archivo, indent=4)

    resultado_firma_alterada = recibir_paquete(
        "paquete_V4_firma_alterada.json",
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
    firma_valida = verificar(mensaje, firma, otra_pub)
    if firma_valida:
        print("Error: la firma fue validada con una llave incorrecta")
    else:
        print("La firma NO es válida.")
        print("La llave pública no corresponde al emisor.")
        
    # 6. Intento de descifrado con la llave privada de otro usuario
    print("\n6. Intento de descifrado con la llave privada de otro usuario")
    _, _, _, _, _, _, llave_publica_vanessa, llave_privada_vanessa = generar_llaves()

    # En receptor.py ayuda a imprimir error 
    recibir_paquete(
        "paquete.json",
        llave_privada_vanessa
    )

    # 7. Paquete JSON incompleto
    print("\n7. Paquete JSON incompleto")
    with open("paquete.json", "r") as archivo:
        paquete_incompleto = json.load(archivo)

    # Se elimina un campo del JSON y se guarda como nuevo 
    del paquete_incompleto["signature"]

    with open("paquete_V7_incompleto.json", "w") as archivo:
        json.dump(paquete_incompleto, archivo, indent=4)

    # Validacion en receptor.py ayuda en esta validación 
    recibir_paquete(
        "paquete_V7_incompleto.json",
        llave_privada_daniel
    )

    # 8. Paquete JSON con datos mal formados
    print("\n8. Paquete JSON con datos mal formados")
    
    # JSON no valido
    with open("paquete_V8_mal_formado.json", "w") as archivo:
        archivo.write(
            '{ "sender": "Ivanovich", "receiver": "Daniel", '
        )

    # Validacion en receptor.py ayuda en esta validación s
    recibir_paquete(
        "paquete_V8_mal_formado.json",
        llave_privada_daniel
    )

    # 9. Firma que no corresponde al mensaje recibido
    print("\n9. Firma que no corresponde al mensaje recibido")
    with open("paquete.json", "r") as archivo:
        paquete_inconsistente = json.load(archivo)
    
    # Que se modifica el primer numero del mensaje cifrado 
    paquete_inconsistente["encrypted_message"][0] += 1

    with open("paquete_V9_firma_no_corresponde.json", "w") as archivo:
        json.dump(paquete_inconsistente, archivo, indent=4)
    
    recibir_paquete(
        "paquete_V9_firma_no_corresponde.json",
        llave_privada_daniel
    )