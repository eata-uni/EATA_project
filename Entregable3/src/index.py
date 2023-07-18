# version que reduce a un solo proceso ejecutando
import requests
from flask import Flask, render_template, jsonify
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from datetime import timedelta

app = Flask(__name__)
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'eata-project.appspot.com'})

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/products')
def products():
    return render_template('products2.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/products/one')
def product_one():
    return render_template('product_one.html')

@app.route('/products/two')
def product_two():
    return render_template('product_two.html')

@app.route('/products/three')
def product_three():
    return render_template('product_three.html')

@app.route('/products/four')
def product_four():
    return render_template('product_four.html')


bot_token = '6133446393:AAFRHLcBFG6VQ4WIOnCPoJM0Qx65Eot-efs'
chat_id = '5175931855'



def obtener_mensajes():
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(url)
    data = response.json()

    if 'result' in data:
        mensajes = data['result']
        return mensajes
    else:
        return []
    
# obtener mensajes
@app.route('/get_messages1', methods=['GET'])
def get_messages1():
    mensajes = obtener_mensajes()
    mensajes_texto = ''
    tz = pytz.timezone('America/Lima') 

    for mensaje in mensajes:
        if 'message' in mensaje and 'chat' in mensaje['message']:
            chat = mensaje['message']['chat']
            message_time = datetime.fromtimestamp(mensaje['message']['date'], tz).strftime('%Y-%m-%d %H:%M:%S')
            if str(chat.get('id')) == chat_id:
                if 'text' in mensaje['message'] and mensaje['message']['text'].startswith('/type5'):
                    contenido = message_time + ": " + mensaje['message']['text'][7:] + "\n"
                    mensajes_texto += contenido
                    print(mensajes_texto)
                if 'text' in mensaje['message'] and mensaje['message']['text'].startswith('/delete5'):
                    mensajes_texto = ''   
    return mensajes_texto

@app.route('/get_messages2', methods=['GET'])
def get_messages2():
    mensajes = obtener_mensajes()
    mensajes_texto = ''
    tz = pytz.timezone('America/Lima') 

    for mensaje in mensajes:
        if 'message' in mensaje and 'chat' in mensaje['message']:
            chat = mensaje['message']['chat']
            message_time = datetime.fromtimestamp(mensaje['message']['date'], tz).strftime('%Y-%m-%d %H:%M:%S')
            if str(chat.get('id')) == chat_id:
                if 'text' in mensaje['message'] and mensaje['message']['text'].startswith('/type6'):
                    contenido = message_time + ": " + mensaje['message']['text'][7:] + "\n"
                    mensajes_texto += contenido
                    print(mensajes_texto)
                if 'text' in mensaje['message'] and mensaje['message']['text'].startswith('/delete6'):
                    mensajes_texto = ''   
    return mensajes_texto

@app.route('/get_messages3', methods=['GET'])
def get_messages3():
    mensajes = obtener_mensajes()
    mensajes_texto = ''
    tz = pytz.timezone('America/Lima') 

    for mensaje in mensajes:
        if 'message' in mensaje and 'chat' in mensaje['message']:
            chat = mensaje['message']['chat']
            message_time = datetime.fromtimestamp(mensaje['message']['date'], tz).strftime('%Y-%m-%d %H:%M:%S')
            if str(chat.get('id')) == chat_id:
                if 'text' in mensaje['message'] and mensaje['message']['text'].startswith('/type7'):
                    contenido = message_time + ": " + mensaje['message']['text'][7:] + "\n"
                    mensajes_texto += contenido
                    print(mensajes_texto)
                if 'text' in mensaje['message'] and mensaje['message']['text'].startswith('/delete7'):
                    mensajes_texto = ''   
    return mensajes_texto

@app.route('/get_messages4', methods=['GET'])
def get_messages4():
    mensajes = obtener_mensajes()
    mensajes_texto = ''
    tz = pytz.timezone('America/Lima') 

    for mensaje in mensajes:
        if 'message' in mensaje and 'chat' in mensaje['message']:
            chat = mensaje['message']['chat']
            message_time = datetime.fromtimestamp(mensaje['message']['date'], tz).strftime('%Y-%m-%d %H:%M:%S')
            if str(chat.get('id')) == chat_id:
                if 'text' in mensaje['message'] and mensaje['message']['text'].startswith('/type8'):
                    contenido = message_time + ": " + mensaje['message']['text'][7:] + "\n"
                    mensajes_texto += contenido
                    print(mensajes_texto)
                if 'text' in mensaje['message'] and mensaje['message']['text'].startswith('/delete8'):
                    mensajes_texto = ''   
    return mensajes_texto
    
# obtener imagenes
@app.route('/get_images1')
def get_images1():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/Type1')
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in images]
    return jsonify({'image_urls': image_urls})

@app.route('/get_images2')
def get_images2():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/Type2')
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in images]
    return jsonify({'image_urls': image_urls})

@app.route('/get_images3')
def get_images3():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/Type3')
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in images]
    return jsonify({'image_urls': image_urls})

@app.route('/get_images4')
def get_images4():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/Type4')
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in images]
    return jsonify({'image_urls': image_urls})

if __name__ == '__main__':
    app.run(debug=True)

