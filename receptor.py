import json

from cifrados import descifrar_mensaje
from verificar import verificar

def recibir_paquete(ruta_json, llave_privada_receptor):
    # Leer el paquete JSON;
    try:
        with open(ruta_json, "r") as archivo:
            paquete = json.load(archivo)

    except FileNotFoundError:
        print("Error: archivo JSON no encontrado")
        return

    except json.JSONDecodeError:
        print("Error: el archivo JSON está mal formado")
        return
    
    campos_json = [
        "sender",
        "receiver",
        "encrypted_message",
        "encrypted_session_key",
        "signature",
        "sender_public_key"
    ]

    # Verificar que no falte ningun campo en el JSON 
    for campo in campos_json:
        if campo not in paquete:
            print(f"Error: falta el campo '{campo}' en el JSON")
            return
    
    # Extraer datos JSON a variables
    # Identificar al emisor y al receptor del JSON
    emisor = paquete["sender"]
    receptor = paquete["receiver"]
    mensaje_cifrado = paquete["encrypted_message"]
    clave_sesion_cifrada = paquete["encrypted_session_key"]
    firma = paquete["signature"]
    e = paquete["sender_public_key"]["e"]
    n = paquete["sender_public_key"]["n"]
    llave_publica_emisor = (e, n)

    # El receptor usa su llave privada RSA para recuperar la clave de sesión.
    # Recuperar la clave de sesión usando la llave privada del receptor
    d, n_receptor = llave_privada_receptor
    clave_sesion = pow(clave_sesion_cifrada, d, n_receptor)

    # El receptor usa la clave de sesión para descifrar el mensaje.
    mensaje_descifrado = descifrar_mensaje(mensaje_cifrado, clave_sesion)

    print("\nMENSAJE RECIBIDO")

    print("De:", emisor)

    print("Para:", receptor)

    print("Mensaje descifrado:", mensaje_descifrado)

    # Verificar la firma digital usando la llave pública del emisor;
    firma_valida = verificar(mensaje_descifrado, firma, llave_publica_emisor)

    # Indicar si el mensaje es válido o inválido y mostrar explicación del resultado 
    print("\nVERIFICACIÓN")
    if firma_valida:
        print("La firma es válida.")
        print("El mensaje no fue alterado y corresponde al emisor.")
    else:
        print("La firma NO es válida.")
        print("El mensaje pudo haber sido alterado o la llave pública es incorrecta.")