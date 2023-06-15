import requests
from datetime import datetime

def get_updates():
    #bot_token = '6133446393:AAFRHLcBFG6VQ4WIOnCPoJM0Qx65Eot-efs'
    
    bot_token = '5773810421:AAHNbgQNX3_uZEeXeN1k7nehW0eJTHxwlHQ'
    get_updates_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'

    response = requests.get(get_updates_url)
    data = response.json()

    if 'result' in data:
        return data['result']
    else:
        return []

def get_all_messages(updates, chat_id):
    filtered_updates = [update for update in updates if 'message' in update and 'from' in update['message'] and 'id' in update['message']['from'] and update['message']['from']['id'] == chat_id]

    messages = ['', '', '', '']  # Inicializar las 4 cajas de texto con cadenas vacías

    for update in filtered_updates:
        message_text = update['message']['text']
        message_time = datetime.fromtimestamp(update['message']['date']).strftime('%H:%M:%S')
        if message_text == "/start":
            continue  # Ignorar el comando /start
        elif message_text.startswith("/posttype1"):
            product_info = message_text.replace("/posttype1", "").strip()
            message = f"{message_time}: {product_info}"
            messages[0] += f"{message}\n"  # Agregar el mensaje a la caja 1
        elif message_text == "/delete1":
            messages[0] = ""  # Limpiar el mensaje en la caja 1
        elif message_text.startswith("/posttype2"):
            product_info = message_text.replace("/posttype2", "").strip()
            message = f"{message_time}: {product_info}"
            messages[1] += f"{message}\n"  # Agregar el mensaje a la caja 2
        elif message_text == "/delete2":
            messages[1] = ""  # Limpiar el mensaje en la caja 2
        elif message_text.startswith("/posttype3"):
            product_info = message_text.replace("/posttype3", "").strip()
            message = f"{message_time}: {product_info}"
            messages[2] += f"{message}\n"  # Agregar el mensaje a la caja 3
        elif message_text == "/delete3":
            messages[2] = ""  # Limpiar el mensaje en la caja 3
        elif message_text.startswith("/posttype4"):
            product_info = message_text.replace("/posttype4", "").strip()
            message = f"{message_time}: {product_info}"
            messages[3] += f"{message}\n"  # Agregar el mensaje a la caja 4
        elif message_text == "/delete4":
            messages[3] = ""  # Limpiar el mensaje en la caja 4

    return messages

def get_last_id():
    try:
        chat_id = None  # Valor predeterminado para chat_id

        # Obtener las actualizaciones de mensajes
        updates = get_updates()

        # Mostrar el último mensaje recibido
        if updates:
            last_update = updates[-1]
            chat_id = last_update['message']['chat']['id']
            last_message_text = last_update['message']['text']
        else:
            print("No se han recibido mensajes aún")

        return chat_id
    except Exception as e:
        print(f"Ocurrió un error en get_last_id: {e}")
