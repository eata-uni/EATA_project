# version que reduce a un solo proceso ejecutando
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage



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
@app.route('/products/one/amazonas')
def product_one_amazonas():
    return render_template('product_one_amazonas.html')

@app.route('/products/one/ancash')
def product_one_ancash():
    return render_template('product_one_ancash.html')

@app.route('/products/one/apurimac')
def product_one_apurimac():
    return render_template('product_one_apurimac.html')

@app.route('/products/one/arequipa')
def product_one_arequipa():
    return render_template('product_one_arequipa.html')

@app.route('/products/one/ayacucho')
def product_one_ayacucho():
    return render_template('product_one_ayacucho.html')

@app.route('/products/one/cajamarca')
def product_one_cajamarca():
    return render_template('product_one_cajamarca.html')

@app.route('/products/one/cusco')
def product_one_cusco():
    return render_template('product_one_cusco.html')

@app.route('/products/one/huancavelica')
def product_one_huancavelica():
    return render_template('product_one_huancavelica.html')

@app.route('/products/one/huanuco')
def product_one_huanuco():
    return render_template('product_one_huanuco.html')

@app.route('/products/one/ica')
def product_one_ica():
    return render_template('product_one_ica.html')

@app.route('/products/one/junin')
def product_one_junin():
    return render_template('product_one_junin.html')

@app.route('/products/one/lalibertad')
def product_one_lalibertad():
    return render_template('product_one_lalibertad.html')

@app.route('/products/one/lambayeque')
def product_one_lambayeque():
    return render_template('product_one_lambayeque.html')

@app.route('/products/one/lima')
def product_one_lima():
    return render_template('product_one_lima.html')

@app.route('/products/one/limametropolitana')
def product_one_limametropolitana():
    return render_template('product_one_limametropolitana.html')

@app.route('/products/one/loreto')
def product_one_loreto():
    return render_template('product_one_loreto.html')

@app.route('/products/one/madrededios')
def product_one_madrededios():
    return render_template('product_one_madrededios.html')

@app.route('/products/one/moquegua')
def product_one_moquegua():
    return render_template('product_one_moquegua.html')

@app.route('/products/one/pasco')
def product_one_pasco():
    return render_template('product_one_pasco.html')

@app.route('/products/one/piura')
def product_one_piura():
    return render_template('product_one_piura.html') 

@app.route('/products/one/puno')
def product_one_puno():
    return render_template('product_one_puno.html') 

@app.route('/products/one/sanmartin')
def product_one_sanmartin():
    return render_template('product_one_sanmartin.html') 

@app.route('/products/one/tacna')
def product_one_tacna():
    return render_template('product_one_tacna.html')  

@app.route('/products/one/tumbes')
def product_one_tumbes():
    return render_template('product_one_tumbes.html') 

@app.route('/products/one/ucayali')
def product_one_ucayali():
    return render_template('product_one_ucayali.html') 
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
@app.route('/get_producto_uno_amazonas', methods=['GET'])
def get_producto_uno_amazonas():
    ref = db.reference('/comentarios/producto_uno_Amazonas')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_ancash', methods=['GET'])
def get_producto_uno_ancash():
    ref = db.reference('/comentarios/producto_uno_Ancash')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_apurimac', methods=['GET'])
def get_producto_uno_apurimac():
    ref = db.reference('/comentarios/producto_uno_Apurimac')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_arequipa', methods=['GET'])
def get_producto_uno_arequipa():
    ref = db.reference('/comentarios/producto_uno_Arequipa')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_ayacucho', methods=['GET'])
def get_producto_uno_ayacucho():
    ref = db.reference('/comentarios/producto_uno_Ayacucho')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_cajamarca', methods=['GET'])
def get_producto_uno_cajamarca():
    ref = db.reference('/comentarios/producto_uno_Cajamarca')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_callao', methods=['GET'])
def get_producto_uno_callao():
    ref = db.reference('/comentarios/producto_uno_Callao')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_cusco', methods=['GET'])
def get_producto_uno_cusco():
    ref = db.reference('/comentarios/producto_uno_Cusco')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_huancavelica', methods=['GET'])
def get_producto_uno_huancavelica():
    ref = db.reference('/comentarios/producto_uno_Huancavelica')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_huanuco', methods=['GET'])
def get_producto_uno_huanuco():
    ref = db.reference('/comentarios/producto_uno_Huanuco')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_ica', methods=['GET'])
def get_producto_uno_ica():
    ref = db.reference('/comentarios/producto_uno_Ica')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_junin', methods=['GET'])
def get_producto_uno_junin():
    ref = db.reference('/comentarios/producto_uno_Junin')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_lalibertad', methods=['GET'])
def get_producto_uno_lalibertad():
    ref = db.reference('/comentarios/producto_uno_LaLibertad')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_lambayeque', methods=['GET'])
def get_producto_uno_lambayeque():
    ref = db.reference('/comentarios/producto_uno_Lambayeque')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_lima', methods=['GET'])
def get_producto_uno_lima():
    ref = db.reference('/comentarios/producto_uno_Lima')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_limametropolitana', methods=['GET'])
def get_producto_uno_limametropolitana():
    ref = db.reference('/comentarios/producto_uno_LimaMetropolitana')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_loreto', methods=['GET'])
def get_producto_uno_loreto():
    ref = db.reference('/comentarios/producto_uno_Loreto')
    value = ref.get()
    return jsonify({'value': value})

@app.route('/get_producto_uno_madrededios', methods=['GET'])
def get_producto_uno_madrededios():
    ref = db.reference('/comentarios/producto_uno_MadredeDios')
    value = ref.get()
    return jsonify({'value': value}) 

@app.route('/get_producto_uno_moquegua', methods=['GET'])
def get_producto_uno_moquegua():
    ref = db.reference('/comentarios/producto_uno_Moquegua')
    value = ref.get()
    return jsonify({'value': value}) 

@app.route('/get_producto_uno_pasco', methods=['GET'])
def get_producto_uno_pasco():
    ref = db.reference('/comentarios/producto_uno_Pasco')
    value = ref.get()
    return jsonify({'value': value}) 

@app.route('/get_producto_uno_piura', methods=['GET'])
def get_producto_uno_piura():
    ref = db.reference('/comentarios/producto_uno_Piura')
    value = ref.get()
    return jsonify({'value': value}) 

@app.route('/get_producto_uno_puno', methods=['GET'])
def get_producto_uno_puno():
    ref = db.reference('/comentarios/producto_uno_Puno')
    value = ref.get()
    return jsonify({'value': value}) 

@app.route('/get_producto_uno_sanmartin', methods=['GET'])
def get_producto_uno_sanmartin():
    ref = db.reference('/comentarios/producto_uno_SanMartin')
    value = ref.get()
    return jsonify({'value': value}) 

@app.route('/get_producto_uno_tacna', methods=['GET'])
def get_producto_uno_tacna():
    ref = db.reference('/comentarios/producto_uno_Tacna')
    value = ref.get()
    return jsonify({'value': value}) 

@app.route('/get_producto_uno_tumbes', methods=['GET'])
def get_producto_uno_tumbes():
    ref = db.reference('/comentarios/producto_uno_Tumbes')
    value = ref.get()
    return jsonify({'value': value}) 

@app.route('/get_producto_uno_ucayali', methods=['GET'])
def get_producto_uno_ucayali():
    ref = db.reference('/comentarios/producto_uno_Ucayali')
    value = ref.get()
    return jsonify({'value': value}) 

# obtener imagenes de los departamentos
@app.route('/get_images_t1amazonas')
def get_images_t1amazonas():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Amazonas/')
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

@app.route('/get_images_t1ancash')
def get_images_t1ancash():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Ancash/')
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

@app.route('/get_images_t1apurimac')
def get_images_t1apurimac():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Apurimac/')
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

@app.route('/get_images_t1arequipa')
def get_images_t1arequipa():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Arequipa/')
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

@app.route('/get_images_t1ayacucho')
def get_images_t1ayacucho():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Ayacucho/')
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

@app.route('/get_images_t1cajamarca')
def get_images_t1cajamarca():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Cajamarca/')
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

@app.route('/get_images_t1cusco')
def get_images_t1cusco():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Cusco/')
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

@app.route('/get_images_t1huancavelica')
def get_images_t1huancavelica():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Huancavelica/')
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

@app.route('/get_images_t1huanuco')
def get_images_t1huanuco():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Huanuco/')
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

@app.route('/get_images_t1ica')
def get_images_t1ica():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Ica/')
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

@app.route('/get_images_t1junin')
def get_images_t1junin():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Junin/')
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

@app.route('/get_images_t1lalibertad')
def get_images_t1lalibertad():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1LaLibertad/')
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

@app.route('/get_images_t1lambayeque')
def get_images_t1lambayeque():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Lambayeque/')
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

@app.route('/get_images_t1lima')
def get_images_t1lima():
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
    
@app.route('/get_images_t1limametropolitana')
def get_images_t1limametropolitana():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Lima2/')
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
    
@app.route('/get_images_t1loreto')
def get_images_t1loreto():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Loreto/')
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

@app.route('/get_images_t1madrededios')
def get_images_t1madrededios():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1MadredeDios/')
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

@app.route('/get_images_t1moquegua')
def get_images_t1moquegua():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Moquegua/')
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

@app.route('/get_images_t1pasco')
def get_images_t1pasco():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Pasco/')
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

@app.route('/get_images_t1piura')
def get_images_t1piura():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Piura/')
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

@app.route('/get_images_t1puno')
def get_images_t1puno():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Puno/')
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

@app.route('/get_images_t1sanmartin')
def get_images_t1sanmartin():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1SanMartin/')
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

@app.route('/get_images_t1tacna')
def get_images_t1tacna():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Tacna/')
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

@app.route('/get_images_t1tumbes')
def get_images_t1tumbes():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Tumbes/')
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

@app.route('/get_images_t1ucayali')
def get_images_t1ucayali():
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix='Images/T1Ucayali/')
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
