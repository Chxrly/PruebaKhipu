from flask import Flask, render_template, request, redirect, session, url_for
import requests

app = Flask(__name__)
app.secret_key = 'clave-segura'

PRODUCTOS = [
    {"id": 1, "nombre": "Lubricante 4 en 1 Chocolate Caliente", "precio": 1490, "imagen": "producto1.jpg"},
    {"id": 2, "nombre": "Lubricante efecto ICE sachet 5 ml", "precio": 1490, "imagen": "producto2.jpg"},
    {"id": 3, "nombre": "Lubricante 4 en 1 FrutiLub 5ml", "precio": 1490, "imagen": "producto3.jpg"},
    {"id": 4, "nombre": "Lubricante 4 en 1 Chocolate Caliente 30 ml", "precio": 6990, "imagen": "producto4.jpg"},
    {"id": 5, "nombre": "SensorPlus 5 ml", "precio": 1490, "imagen": "producto5.jpg"},
]

@app.route('/')
def index():
    return render_template('catalogo.html', productos=PRODUCTOS)

@app.route('/agregar/<int:producto_id>')
def agregar(producto_id):
    producto = next((p for p in PRODUCTOS if p['id'] == producto_id), None)
    if producto:
        if 'carrito' not in session:
            session['carrito'] = {}
        carrito = session['carrito']
        str_id = str(producto_id)
        carrito[str_id] = carrito.get(str_id, 0) + 1
        session['carrito'] = carrito
    return redirect(url_for('index'))

@app.route('/eliminar/<int:producto_id>')
def eliminar(producto_id):
    carrito = session.get('carrito', {})
    carrito.pop(str(producto_id), None)
    session['carrito'] = carrito
    return redirect(url_for('carrito'))

@app.route('/carrito')
def carrito():
    carrito_session = session.get('carrito', {})
    resumen = {}
    for str_id, cantidad in carrito_session.items():
        producto = next((p for p in PRODUCTOS if str(p['id']) == str_id), None)
        if producto:
            resumen[str_id] = {
                'producto': producto,
                'cantidad': cantidad
            }
    total = sum(item['producto']['precio'] * item['cantidad'] for item in resumen.values())
    return render_template("carrito.html", resumen=resumen, total=total)

@app.route('/actualizar-carrito', methods=['POST'])
def actualizar_carrito():
    cantidades = request.form.getlist('cantidad')
    ids = request.form.getlist('producto_id')
    
    nuevo_carrito = {}
    for pid, qty in zip(ids, cantidades):
        if qty.isdigit() and int(qty) > 0:
            nuevo_carrito[pid] = int(qty)

    session['carrito'] = nuevo_carrito
    return redirect(url_for('carrito'))

@app.route('/pagar', methods=['POST'])
def pagar():
    total = request.form.get('total')
    try:
        total = int(total)
        if total <= 0 or total > 5000:
            return "El monto debe ser mayor a $0 y no superar $5.000 CLP (entorno pruebas).", 400
    except:
        return "Monto invalido", 400

    payload = {
        "amount": total,
        "currency": "CLP",
        "subject": "Pago desde carrito XYRA"
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": "594608c0-d9c6-4489-ae65-891934d9f8a0"
    }

    response = requests.post("https://payment-api.khipu.com/v3/payments", json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return redirect(data['payment_url'])
    else:
        return "Error al procesar el pago", 500

if __name__ == '__main__':
    app.run(debug=True)
