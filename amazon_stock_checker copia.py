import requests
from bs4 import BeautifulSoup
import time

# Configuración inicial
PRODUCT_URLS = [
    "https://www.amazon.es/dp/B0F2JCL3NZ",  # Producto 1
    "https://www.amazon.es/dp/B0F2J4SYJ2"   # Producto 2
]
CHECK_INTERVAL = 3600  # Tiempo en segundos (1 hora)


# Frases que indican disponibilidad o preventa
AVAILABLE_PHRASES = [
    "ahorros precio de preventa garantizado",
    "comprar ya",
    "Añadir a la cesta"
]

# Función para verificar la disponibilidad del producto
def check_availability(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error al acceder a la URL: {url}")
        return False

    soup = BeautifulSoup(response.content, "html.parser")

    # Extraer todo el texto de la página
    page_text = soup.get_text().lower()

    # Verificar si alguna de las frases de disponibilidad está presente
    for phrase in AVAILABLE_PHRASES:
        if phrase in page_text:
            return True
    return False

# Función para enviar notificaciones a Telegram
def send_telegram_message(product_url):
    message = f"¡Producto disponible!: {product_url}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Notificación enviada a Telegram.")
        else:
            print(f"Error al enviar mensaje a Telegram: {response.text}")
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

# Función principal
def main():
    while True:
        for url in PRODUCT_URLS:
            print(f"Verificando disponibilidad de: {url}")
            if check_availability(url):
                print(f"¡Producto disponible!: {url}")
                send_telegram_message(url)
            else:
                print("Producto no disponible.")
        print(f"Esperando {CHECK_INTERVAL / 60} minutos antes de la próxima verificación...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
