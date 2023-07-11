import pymysql
from flask import Flask, jsonify, request
from flask_cors import CORS

# -------------------------------------------------------------------
# Definimos la clase "Producto"
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# Definimos la clase "Inventario"
# -------------------------------------------------------------------
class Inventario:
    def __init__(self):
        self.conexion = pymysql.connect(
            host='techdreamscac.mysql.pythonanywhere-services.com', 
            port=3306,
            user='techdreamscac', 
            password='TDCAC2023_', 
            database='techdreamscac$pccomcponentsstore')
        
        self.cursor = self.conexion.cursor()

    def agregar_categoria(self, codigo, categoria):
        try:
            self.cursor.execute("INSERT INTO categories (codigo, categoria) VALUES (%s, %s)",
                                (codigo, categoria))
            self.conexion.commit()
            return jsonify({"Categoria agregada correctamente."}), 200
        except pymysql.IntegrityError:
            return jsonify({"La categoria ya existe."}), 400

    def agregar_fabricante(self, codigo, fabricante):
        try:
            self.cursor.execute("INSERT INTO manufacturers (codigo, fabricante) VALUES (%s, %s)",
                                (codigo, fabricante))
            self.conexion.commit()
            jsonify({"Fabricante agregado correctamente."}), 200
        except pymysql.IntegrityError:
            jsonify({"El fabricante ya existe."}), 400

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


    def listar_productos2(self):
        print("-" * 30)
        self.cursor.execute("SELECT ProductID, description, StockQuantity, Price FROM products")
        rows = self.cursor.fetchall()
        for row in rows:
            ProductID, description, StockQuantity, Price = row
            print(f"Código: {ProductID}")
            print(f"Descripción: {description}")
            print(f"Cantidad: {StockQuantity}")
            print(f"Precio: {Price}")
            print("-" * 30)

    def eliminar_producto(self, codigo):
        self.cursor.execute("DELETE FROM products WHERE ProductID = %s", (codigo,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Producto eliminado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404


# -------------------------------------------------------------------
# Definimos la clase "Carrito"
# -------------------------------------------------------------------
class Carrito:
    def __init__(self):
        self.conexion = pymysql.connect(
            host='techdreamscac.mysql.pythonanywhere-services.com', 
            port=3306,
            user='techdreamscac', 
            password='TDCAC2023_', 
            database='techdreamscac$pccomcponentsstore')
        self.cursor = self.conexion.cursor()
        self.items = []

    def agregar(self, codigo, cantidad, inventario, customer):
        producto = inventario.consultar_producto(int(codigo))
        if producto is None:
            return jsonify({'message': 'El producto no existe.'}), 404
        if producto.cantidad < cantidad:
            return jsonify({'message': 'Cantidad en stock insuficiente.'}), 400

        for item in self.items:
            if item.codigo == int(codigo):
                item.cantidad += 1
                self.cursor.execute("UPDATE products SET StockQuantity = StockQuantity - %s WHERE ProductID = %s",
                                    (int(cantidad), int(codigo)))
                self.conexion.commit()
                return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200

        nuevo_item = Producto(codigo, producto.nombreProducto, producto.IDcategoria, producto.IDfabricante, producto.precio, cantidad, producto.descripcion, producto.imagen)
        self.items.append(nuevo_item)
        self.cursor.execute("INSERT INTO shoppingcart VALUES (%s, %s, %s, %s)", (0, int(customer), int(codigo), int(cantidad)))
        self.cursor.execute("UPDATE products SET StockQuantity = StockQuantity - %s WHERE ProductID = %s",
                            (int(cantidad), int(codigo)))
        self.conexion.commit()
        return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200
    
    def modificar_cantidad (self, codigo, cantidad):
        self.cursor.execute("UPDATE shoppingcart SET Quantity = %s WHERE OrderItemID = %s", (cantidad, codigo))
        self.conexion.commit()
        return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200

    def quitar(self, codigo, cantidad, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    return jsonify({'message': 'Cantidad a quitar mayor a la cantidad en el carrito.'}), 400
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                self.cursor.execute("UPDATE productos SET cantidad = cantidad + ? WHERE codigo = ?",
                                    (cantidad, codigo))
                self.conexion.commit()
                return jsonify({'message': 'Producto quitado del carrito correctamente.'}), 200

        return jsonify({'message': 'El producto no se encuentra en el carrito.'}), 404

    def mostrar(self):
        self.cursor.execute("SELECT sp.OrderItemID, sp.CustomerID, sp.ProductID, sp.Quantity, pr.ProductName, pr.Price, pr.Image FROM shoppingcart sp INNER JOIN products pr ON sp.ProductID = pr.ProductID")
        items = self.cursor.fetchall()
        productos_carrito = []
        for item in items:
            OrderItemID, CustomerID, ProductID, Quantity, ProductName, Price, Image  = item
            producto = {'codigo': OrderItemID, 'customer': CustomerID, 'productoID': ProductID,
                        'cantidad': Quantity, 'producto': ProductName, 'price': Price, 'image': Image}
            productos_carrito.append(producto)
        return jsonify(productos_carrito), 200
    
    def eliminar_producto_carrito(self, codigo):
        self.cursor.execute("DELETE FROM shoppingcart WHERE OrderItemID = %s", (codigo,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Producto eliminado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404



app = Flask(__name__)
CORS(app)
inventario = Inventario()
carrito = Carrito()

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return inventario.listar_productos()

@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    data=request.get_json()
    codigo = data['codigo']
    cantidad = data['cantidad']
    inventario = Inventario()
    customer = data['customer']
    return carrito.agregar(codigo, cantidad, inventario, customer)

# Ruta para quitar un producto del carrito
@app.route('/carrito', methods=['DELETE'])
def quitar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    return carrito.quitar(codigo, cantidad, inventario)

@app.route('/carrito/<int:codigo>', methods=['DELETE'])
def eliminar_producto(codigo):
    return carrito.eliminar_producto_carrito(codigo)

@app.route('/carrito/<int:codigo>', methods=['PUT'])
def modificar_cantidad_carrito (codigo):
    data=request.get_json()
    cantidad = data['cantidad']
    return carrito.modificar_cantidad(codigo, cantidad)

# Ruta para obtener el contenido del carrito
@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return carrito.mostrar()

if __name__ == '__main__':
    app.run()


