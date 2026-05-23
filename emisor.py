import json
from firmar import firmar
from cifrados import crear_clave_sesion
from cifrados import cifrar_mensaje

def crear_paquete(mensaje, emisor, receptor, llave_privada_emisor, llave_publica_emisor, llave_publica_receptor):
    # La firma se genera con la llave privada del emisor
    firma = firmar(mensaje, llave_privada_emisor)

    # El emisor genera una clave de sesión
    clave_sesion = crear_clave_sesion()

    # El mensaje se cifra usando la clave de sesión
    mensaje_cifrado = cifrar_mensaje(mensaje, clave_sesion)
    
    print("\nMensaje cifrado:", mensaje_cifrado)

    e, n = llave_publica_receptor

    # La clave de sesión se cifra usando la llave pública RSA del receptor
    clave_sesion_cifrada = pow(clave_sesion, e, n)

    paquete = {
        "sender": emisor,
        "receiver": receptor,
        "encrypted_message": mensaje_cifrado,
        "encrypted_session_key": clave_sesion_cifrada,
        "signature": firma,
        "hash_algorithm": "SHA-256",
        "sender_public_key": {
            "e": llave_publica_emisor[0],
            "n": llave_publica_emisor[1]
        }
    }
    # Se abre
    with open("paquete.json", "w") as archivo:
        json.dump(paquete, archivo, indent=4)
    
    return paquete
