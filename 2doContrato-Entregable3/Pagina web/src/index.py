from flask import Flask, render_template, jsonify
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage



app = Flask(__name__)
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://eata-project-default-rtdb.firebaseio.com/',
                                     'storageBucket': 'eata-project.appspot.com'})

# Definir las rutas de productos
numbertext_product = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight'
]
numerotexto_producto = [
    'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho'
]
departments = [
    'amazonas', 'ancash', 'apurimac', 'arequipa','ayacucho', 'cajamarca', 'cusco', 'huancavelica', 'huanuco','ica','junin','lalibertad','lambayeque','lima','limametropolitana','loreto','madrededios','moquegua','pasco','piura','puno','sanmartin','tacna','tumbes','ucayali'
]

title_department = [
    'Amazonas', 'Ancash', 'Apurimac', 'Arequipa','Ayacucho', 'Cajamarca', 'Cusco', 'Huancavelica', 'Huanuco','Ica','Junin','La Libertad','Lambayeque','Lima','Lima Metropolitana','Loreto','Madre de Dios','Moquegua','Pasco','Piura','Puno','San Martin','Tacna','Tumbes','Ucayali'
]

number_product = [
    '1', '2', '3', '4', '5', '6', '7', '8'
]

title_product = [
    'Estimador de precipitación', 'Incremento de vapor de agua', 'Altura de la base de la nube', 'Capas de nieve nubes', 'Máscara de nubes', 'Tasa de lluvia' , 'Agua precipitable total', 'Fase superior de nube'
]

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/about')
def about():
    return render_template('nosotros.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# productos

# Rutas de productos
@app.route('/products/<product_name>')
def product(product_name):
    if product_name in numbertext_product:
        if product_name == 'one':
            return render_template(f'product.html', product_number = number_product[0], numerotexto_producto=numerotexto_producto[0], title_product=title_product[0], numbertext_product=numbertext_product[0])
        elif product_name == 'two':
            return render_template(f'product.html', product_number = number_product[1], numerotexto_producto=numerotexto_producto[1], title_product=title_product[1], numbertext_product=numbertext_product[1])
        elif product_name == 'three':
            return render_template(f'product.html', product_number = number_product[2], numerotexto_producto=numerotexto_producto[2], title_product=title_product[2], numbertext_product=numbertext_product[2])
        elif product_name == 'four':
            return render_template(f'product.html', product_number = number_product[3], numerotexto_producto=numerotexto_producto[3], title_product=title_product[3], numbertext_product=numbertext_product[3])
        elif product_name == 'five':
            return render_template(f'product.html', product_number = number_product[4], numerotexto_producto=numerotexto_producto[4], title_product=title_product[4], numbertext_product=numbertext_product[4])
        elif product_name == 'six':
            return render_template(f'product.html', product_number = number_product[5], numerotexto_producto=numerotexto_producto[5], title_product=title_product[5], numbertext_product=numbertext_product[5])
        elif product_name == 'seven':
            return render_template(f'product.html', product_number = number_product[6], numerotexto_producto=numerotexto_producto[6], title_product=title_product[6], numbertext_product=numbertext_product[6])
        elif product_name == 'eight':
            return render_template(f'product.html', product_number = number_product[7], numerotexto_producto=numerotexto_producto[7], title_product=title_product[7], numbertext_product=numbertext_product[7])

    else:
        return f"El producto {product_name} no está disponible en este momento."

# rutas de  departamenos
@app.route('/products/<int:product_number>/<department_name>')
def product_department(product_number, department_name):
    if department_name in departments:
        if product_number == 1:
            return render_template('product_department.html', product_number=product_number, department_name=department_name, numerotexto_producto=numerotexto_producto[0], title_product=title_product[0], numbertext_product=numbertext_product[0])
        elif product_number == 2:
            return render_template('product_department.html', product_number=product_number, department_name=department_name, numerotexto_producto=numerotexto_producto[1], title_product=title_product[1], numbertext_product=numbertext_product[1])
        elif product_number == 3:
            return render_template('product_department.html', product_number=product_number, department_name=department_name, numerotexto_producto=numerotexto_producto[2], title_product=title_product[2], numbertext_product=numbertext_product[2])
        elif product_number == 4:
            return render_template('product_department.html', product_number=product_number, department_name=department_name, numerotexto_producto=numerotexto_producto[3], title_product=title_product[3], numbertext_product=numbertext_product[3])
        elif product_number == 5:
            return render_template('product_department.html', product_number=product_number, department_name=department_name, numerotexto_producto=numerotexto_producto[4], title_product=title_product[4], numbertext_product=numbertext_product[4])
        elif product_number == 6:
            return render_template('product_department.html', product_number=product_number, department_name=department_name, numerotexto_producto=numerotexto_producto[5], title_product=title_product[5], numbertext_product=numbertext_product[5])
        elif product_number == 7:
            return render_template('product_department.html', product_number=product_number, department_name=department_name, numerotexto_producto=numerotexto_producto[6], title_product=title_product[6], numbertext_product=numbertext_product[6])
        elif product_number == 8:
            return render_template('product_department.html', product_number=product_number, department_name=department_name, numerotexto_producto=numerotexto_producto[7], title_product=title_product[7], numbertext_product=numbertext_product[7])
    else:
        return f"El departamento {department_name} no está disponible en este momento."

# obtener comentarios de los productos

@app.route('/get_producto/<nombre_producto>', methods=['GET'])
def get_producto(nombre_producto):
    ref = db.reference(f'/comentarios/producto_{nombre_producto}')
    value = ref.get()
    return jsonify({'value': value})


def get_images_by_type(image_type):
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix=f'Images/{image_type}')
    image_urls = [image.generate_signed_url(
        version="v4",
        expiration=timedelta(days=7),
        method="GET"
    ) for image in images]

    return jsonify({'image_urls': image_urls[1:]}) if len(image_urls) > 1 else jsonify({'image_urls': []})

@app.route('/get_images/<int:image_type>', methods=['GET'])
def get_images(image_type):
    return get_images_by_type(f'Type{image_type}')
   

# producto uno comentarios
@app.route('/get_producto_uno/<departamento>', methods=['GET'])
def get_producto_uno(departamento):
    ref = db.reference(f'/comentarios/producto_uno_{departamento.capitalize()}')
    value = ref.get()
    return jsonify({'value': value})

# producto dos comentarios
@app.route('/get_producto_dos/<departamento>', methods=['GET'])
def get_producto_dos(departamento):
    ref = db.reference(f'/comentarios/producto_dos_{departamento.capitalize()}')
    value = ref.get()
    return jsonify({'value': value})

# producto tres comentarios
@app.route('/get_producto_tres/<departamento>', methods=['GET'])
def get_producto_tres(departamento):
    ref = db.reference(f'/comentarios/producto_tres_{departamento.capitalize()}')
    value = ref.get()
    return jsonify({'value': value})

def get_images_by_type_and_department(image_type, department):
    prefix = f'Images/T{image_type}{department.capitalize()}/'
    bucket = storage.bucket()
    images = bucket.list_blobs(prefix=prefix)
    existing_images = [image for image in images if image.exists()]
    image_urls = [image.generate_signed_url(
                version="v4",
                expiration=timedelta(days=7),
                method="GET"
            ) for image in existing_images]
    return jsonify({'image_urls': image_urls[1:]}) if len(image_urls) > 1 else jsonify({'image_urls': []})

@app.route('/get_images_t<int:image_type><string:department>', methods=['GET'])
def get_images_d(image_type, department):
    return get_images_by_type_and_department(image_type, department)

if __name__ == '__main__':
    app.run(debug=True)