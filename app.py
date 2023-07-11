from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pymysql

app = Flask(__name__)
CORS(app)


class Producto:
    def __init__(self, codigo, nombreProducto, IDcategoria, IDfabricante, precio, cantidad, descripcion, imagen):
        self.codigo = codigo
        self.nombreProducto = nombreProducto
        self.IDcategoria = IDcategoria
        self.IDfabricante = IDfabricante
        self.precio = precio
        self.cantidad = cantidad
        self.descripcion = descripcion
        self.imagen = imagen

    def modificar(self, nueva_descripcion, nueva_cantidad, nuevo_precio):
        self.descripcion = nueva_descripcion
        self.cantidad = nueva_cantidad
        self.precio = nuevo_precio

class Inventario:
    def __init__(self):
        self.conexion = pymysql.connect(
            host='techdreamscac.mysql.pythonanywhere-services.com', 
            port=3306,
            user='techdreamscac', 
            password='TDCAC2023_', 
            database='techdreamscac$pccomcponentsstore')
        
        self.cursor = self.conexion.cursor()
    def agregar_producto(self, codigo, producto, IDcategoria, IDfabricante, precio, cantidad, descripcion, imagen):
        producto_existente = self.consultar_producto(codigo)
        if producto_existente:
            return jsonify({'message': 'Ya existe un producto con ese código.'}), 400
        nuevo_producto = Producto(codigo, descripcion, cantidad, precio)
        self.cursor.execute("INSERT INTO products (codigo, producto, IDcategoria, IDfabricante, precio, cantidad, descripcion, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (codigo, producto, IDcategoria, IDfabricante, precio, cantidad, descripcion, imagen))
        self.conexion.commit()
        return jsonify({'message': 'Producto agregado correctamente.'}), 200


    def consultar_producto(self, codigo):
        self.cursor.execute("SELECT * FROM products WHERE ProductID = %s", (int(codigo),))
        resultado = self.cursor.fetchone()
        if resultado:
            ProductID, ProductName, CategoryID, ManufacturerID, Price, StockQuantity, description, Image = resultado
            producto = Producto(ProductID, ProductName, CategoryID, ManufacturerID, Price, StockQuantity, description, Image)
            return producto
        return None

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        producto = self.consultar_producto(codigo)
        if producto:
            producto.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio, codigo)
            self.cursor.execute("UPDATE products SET description = %s, StockQuantity = %s, Price = %s WHERE ProductID = %s",
                                (nueva_descripcion, nueva_cantidad, nuevo_precio, codigo))
            self.conexion.commit()
            return jsonify({'message': 'Producto modificado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404

    def listar_productos(self):
        self.cursor.execute("SELECT ProductID, ProductName, CategoryID, StockQuantity, Price, description, Image FROM products")
        items = self.cursor.fetchall()
        productos = []
        for item in items:
            ProductID, ProductName, CategoryID, StockQuantity, Price, description, Image = item
            producto = {
                'codigo': ProductID,
                'nombreproducto': ProductName,
                'cantidad': StockQuantity,
                'precio': Price,
                'descripcion': description,
                'imagen': Image,
                'categoria': CategoryID
            }
            productos.append(producto)
        return jsonify(productos),200

    def eliminar_producto(self, codigo):
            self.cursor.execute("DELETE FROM products WHERE ProductID = %s", (codigo,))
            if self.cursor.rowcount > 0:
                self.conexion.commit()
                return jsonify({'message': 'Producto eliminado correctamente.'}), 200
            return jsonify({'message': 'Producto no encontrado.'}), 404


app = Flask(__name__)
CORS(app)
inventario = Inventario()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/obtener-productos', methods=['GET'])
def obtener_productos():
    productos = inventario.listar_productos()
    return render_template('consultar.html', productos=productos)

@app.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    productos = inventario.agregar_producto()
    return render_template('agregar.html', productos=productos)

@app.route('/modificar-producto/<int:codigo>', methods=['PUT'])
def modificar_producto():
    productos = inventario.modificar_producto()
    return render_template('modificaciones.html', productos=productos)

@app.route('/eliminar-producto/<int:codigo>', methods=['DELETE'])
def eliminar_productos():
    productos = inventario.eliminar_producto()
    return render_template('delete.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True, port=5500)
