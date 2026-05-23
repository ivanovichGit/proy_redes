import hashlib

def hash_mensaje(mensaje):
  #validamos que el valor sea un texto
  if not isinstance(mensaje, str) or not mensaje.strip():
      raise ValueError("El mensaje debe ser texto")
  # convertimos el texto a bytes y calculamos el sha256
  hash_obj = hashlib.sha256(mensaje.encode())
  #como el objeto hash no es un número directamente, lo convertimos a hexadecimal para poder transformarlo a un entero.
  #convertismo el hash a texto hex y despues de hex a entero
  return int(hash_obj.hexdigest(), 16)
