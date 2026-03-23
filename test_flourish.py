import requests
import urllib3

# Desactivar advertencias de seguridad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Definimos la IP REAL de Flourish (la que nos respondió el ping)
# Si esta IP cambia, el script fallará, pero es nuestra única salida ahora.
FLOURISH_IP = "34.120.208.157"
API_KEY = "TU_KEY_REAL"
VIZ_ID = "TU_ID_REAL"

# 2. La URL usa la IP, no el nombre
url = f"https://{FLOURISH_IP}/v1/visualisation/{VIZ_ID}"

try:
    print(f"--- Intentando túnel directo a la IP {FLOURISH_IP} ---")

    # IMPORTANTE: Le decimos en el Header que el host es el dominio real
    # Esto engaña al servidor de Flourish para que acepte la conexión
    headers = {"Host": "api.flourish.studio"}

    response = requests.get(
        url,
        params={"api_key": API_KEY},
        headers=headers,
        verify=False,  # Saltamos la validación de nombre
        timeout=15
    )

    print(f"✅ ¡ESTADO!: {response.status_code}")
    print(f"Respuesta: {response.text[:100]}")

except Exception as e:
    print(f"🚨 Error incluso con IP directa: {e}")
