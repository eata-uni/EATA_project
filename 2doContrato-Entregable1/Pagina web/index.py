# version que reduce a un solo proceso ejecutando
import requests
from flask import Flask, render_template, jsonify
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage
from datetime import timedelta


app = Flask(__name__)
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://eata-project-default-rtdb.firebaseio.com/',
                                     'storageBucket': 'eata-project.appspot.com'})


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

# productos

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

@app.route('/products/five')
def product_five():
    return "falta colocar"

@app.route('/products/six')
def product_six():
    return "falta colocar"

@app.route('/products/seven')
def product_seven():
    return "falta colocar"

@app.route('/products/eight')
def product_eight():
    return "falta colocar"


# rutas de  departamenos
@app.route('/products/one/lima')
def product_one_lima():
    return render_template('product_one_lima.html')


# obtener comentarios de los productos

# Ruta para obtener el valor de 'producto_uno' desde Firebase
@app.route('/get_producto_uno', methods=['GET'])
def get_producto_uno():
    ref = db.reference('/comentarios/producto_uno')
    value = ref.get()
    return jsonify({'value': value})

# Ruta para obtener el valor de 'producto_dos' desde Firebase
@app.route('/get_producto_dos', methods=['GET'])
def get_producto_dos():
    ref = db.reference('/comentarios/producto_dos')
    value = ref.get()
    return jsonify({'value': value})

# Ruta para obtener el valor de 'producto_tres' desde Firebase
@app.route('/get_producto_tres', methods=['GET'])
def get_producto_tres():
    ref = db.reference('/comentarios/producto_tres')
    value = ref.get()
    return jsonify({'value': value})

# Ruta para obtener el valor de 'producto_cuatro' desde Firebase
@app.route('/get_producto_cuatro', methods=['GET'])
def get_producto_cuatro():
    ref = db.reference('/comentarios/producto_cuatro')
    value = ref.get()
    return jsonify({'value': value})
    
# obtener imagenes de los productos

@app.route('/get_images1')
def get_images1():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/Type1')
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in images]
    
    if len(image_urls) > 1:
        return jsonify({'image_urls': image_urls[1:]})
    else:
        return jsonify({'image_urls': []})

@app.route('/get_images2')
def get_images2():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/Type2')
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in images]

    if len(image_urls) > 1:
        return jsonify({'image_urls': image_urls[1:]})
    else:
        return jsonify({'image_urls': []})

@app.route('/get_images3')
def get_images3():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/Type3')
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in images]
    
    if len(image_urls) > 1:
        return jsonify({'image_urls': image_urls[1:]})
    else:
        return jsonify({'image_urls': []})

@app.route('/get_images4')
def get_images4():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/Type4')
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in images]
    if len(image_urls) > 1:
        return jsonify({'image_urls': image_urls[1:]})
    else:
        return jsonify({'image_urls': []})
   


# obtener comentarios de los departamentos
@app.route('/get_producto_uno_lima', methods=['GET'])
def get_producto_uno_lima():
    ref = db.reference('/comentarios/producto_uno_lima')
    value = ref.get()
    return jsonify({'value': value})
    
# obtener imagenes de los departamentos
@app.route('/get_images_lima')
def get_images_lima():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Lima/')
    existing_images = [image for image in images if image.exists()]
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in existing_images]
    if len(image_urls) > 1:
        return jsonify({'image_urls': image_urls[1:]})
    else:
        return jsonify({'image_urls': []})



if __name__ == '__main__':
    app.run(debug=True)
