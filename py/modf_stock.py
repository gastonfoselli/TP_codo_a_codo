import pymysql

def conectar_base_de_datos():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="stock"
    )
    return conn

def agregar_producto():
    try:
        conn = conectar_base_de_datos()
        with conn.cursor() as cursor:
            ProductName = input("Ingrese nombre del producto: ")
            categoryID = input("Ingrese categoría del producto: ")
            manufacturerID = input("Indique fabricante del producto: ")
            price = float(input("Ingrese precio del producto: "))
            stockQuantity = int(input("Ingrese la cantidad en stock del producto: "))
            description = input("Ingrese detalles del producto: ")
            image = input("Ingrese imagen del producto: ")

            sql = "INSERT INTO products (ProductName, categoryID, manufacturerID, price, stockQuantity, description, image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (ProductName, categoryID, manufacturerID, price, stockQuantity, description, image)
            cursor.execute(sql, values)

        conn.commit()
        print("El producto ha sido agregado con éxito.")
    except pymysql.Error as e:
        print(f"Error al agregar producto: {e}")
    finally:
        conn.close()

def modificar_producto():
    try:
        conn = conectar_base_de_datos()
        with conn.cursor() as cursor:
            ProductID = int(input("Ingrese el código del producto a modificar: "))
            ProductName = input("Ingrese el nuevo nombre del producto: ")
            categoryID = input("Ingrese la nueva categoría del producto: ")
            manufacturerID = input("Indique el nuevo fabricante del producto: ")
            price = float(input("Ingrese el nuevo precio del producto: "))
            stockQuantity = int(input("Ingrese la nueva cantidad en stock del producto: "))
            description = input("Ingrese los nuevos detalles del producto: ")
            image = input("Ingrese imagen del producto: ")

            sql = "UPDATE products SET ProductName=%s, categoryID=%s, manufacturerID=%s, price=%s, stockQuantity=%s, description=%s, image=%s WHERE ProductID=%s"
            values = (ProductName, categoryID, manufacturerID, price, stockQuantity, description, image, ProductID)
            cursor.execute(sql, values)

        conn.commit()
        print("El producto ha sido modificado con éxito.")
    except pymysql.Error as e:
        print(f"Error al modificar el producto: {e}")
    finally:
        conn.close()

def eliminar_producto():
    try:
        conn = conectar_base_de_datos()
        with conn.cursor() as cursor:
            ProductID = int(input("Ingrese el código del producto a eliminar: "))

            sql = "DELETE FROM products WHERE ProductID=%s"
            values = (ProductID,)
            cursor.execute(sql, values)

        conn.commit()
        if cursor.rowcount > 0:
            print("El producto ha sido eliminado satisfactoriamente.")
        else:
            print("El producto no se encuentra en la base de datos.")
    except pymysql.Error as e:
        print(f"Error al eliminar el producto: {e}")
    finally:
        conn.close()

def consultar_producto():
    try:
        conn = conectar_base_de_datos()
        with conn.cursor() as cursor:
            ProductID = int(input("Ingrese el código del producto a consultar: "))

            sql = "SELECT * FROM products WHERE ProductID = %s"
            values = (ProductID,)
            cursor.execute(sql, values)
            producto = cursor.fetchone()

            if producto:
                print("Información del producto:")
                print(f"Código: {producto[0]}")
                print(f"Nombre del producto: {producto[1]}")
                print(f"Categoría: {producto[2]}")
                print(f"ID Fabricante: {producto[3]}")
                print(f"Precio: {producto[4]}")
                print(f"Stock: {producto[5]}")
                print(f"Descripción: {producto[6]}")
            else:
                print("El producto no existe.")
    except pymysql.Error as e:
        print(f"Error al consultar el producto: {e}")
    finally:
        conn.close()

def mostrar_menu():
    print("\n\n--- MENÚ ---")
    print("1. Agregar producto")
    print("2. Modificar ítem/stock")
    print("3. Eliminar un producto")
    print("4. Consultar un producto")
    print("0. Salir\n")

def main():
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            modificar_producto()
        elif opcion == "3":
            eliminar_producto()
        elif opcion == "4":
            consultar_producto()
        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()