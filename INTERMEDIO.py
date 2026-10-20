# ==============================
# PARCIAL INTERMEDIO
# Desarrollo de aplicaciones web con acceso a datos
# SEBASTIAN WEHDEKING
# CORPORACIÓN UNIVERSITARIA AMERICANA
# DOCENTE: EDUARDO PIMIENTA
# 20 / 10 / 2026
# ==============================

import sqlite3 as Base

# Conexión a la base de datos
conexion = Base.connect("Tecnologia.db")
cursor = conexion.cursor()

# Habilitar soporte de claves foráneas
cursor.execute("PRAGMA foreign_keys = ON;")

# Creación de la tabla Productos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Precio REAL NOT NULL,
        Unidades_Disponibles INTEGER NOT NULL
    )
""")

# Creación de la tabla Ventas con clave foránea
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        PRODUCTO_ID INTEGER NOT NULL,
        UNIDADES INTEGER NOT NULL,
        FECHA TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (PRODUCTO_ID) REFERENCES Productos (id) ON DELETE CASCADE
    )
""")

conexion.commit()

while True:
    print("\n|===== MENU DEL PROGRAMA =====|")
    print("|===========================================|")
    print(" 1). REGISTRAR PRODUCTO ")
    print(" 2). CONSULTAR LISTA DE TODOS LOS PRODUCTOS ")
    print(" 3). ACTUALIZAR PRODUCTO ")
    print(" 4). ELIMINAR PRODUCTO ")
    print(" 5). REGISTRAR VENTA ")
    print(" 6). MOSTRAR HISTORIAL DE VENTAS ")
    print(" 7). SALIR DEL PROGRAMA ")
    print("|===========================================|")

    Opcion = input(" Seleccione una opción: ")

    if Opcion == "1":  # Registrar producto
        print("\n=== Registro del Producto ===")
        Nombre = input(" DIGITE EL NOMBRE: ")
        try:
            Precio = float(input("DIGITE EL PRECIO DEL PRODUCTO: "))
            Unidades = int(input("DIGITE LA CANTIDAD DE UNIDADES DISPONIBLES: "))
            
            cursor.execute("""
                INSERT INTO Productos (Nombre, Precio, Unidades_Disponibles)
                VALUES (?, ?, ?)
            """, (Nombre, Precio, Unidades))
            conexion.commit()
            print("Producto registrado exitosamente.")
        except ValueError:
            print("Error: Ingrese valores numéricos válidos para precio y unidades.")
            
            
            
            

    elif Opcion == "2":  # Consultar lista de todos los productos
        print("\n|=== Lista de todos los productos ===|")
        cursor.execute("SELECT * FROM Productos")
        Productos = cursor.fetchall()
                
        if Productos:
            for prod in Productos:
                print(f" ID: {prod[0]} | Nombre: {prod[1]} | Precio: ${prod[2]:.2f} | Disponibles: {prod[3]}")
        else:
            print("==========================================")
            print("No hay productos registrados en la tabla")
            print("==========================================")





    elif Opcion == "3":  # Modificar precio o unidades disponibles
        print("\n--- ACTUALIZACIÓN DEL PRODUCTO ---")
        try:
            id_prod = int(input(" ID del Producto a actualizar: "))
            
            # Verificar si existe el producto
            cursor.execute("SELECT * FROM Productos WHERE id = ?", (id_prod,))
            prod = cursor.fetchone()
            
            if prod:
                New_Nombre = input(f" Nuevo Nombre (Actual: {prod[1]}): ") or prod[1]
                New_Precio = input(f" Nuevo Precio (Actual: {prod[2]}): ")
                New_Precio = float(New_Precio) if New_Precio else prod[2]
                
                New_Unidades = input(f" Nuevas Unidades (Actual: {prod[3]}): ")
                New_Unidades = int(New_Unidades) if New_Unidades else prod[3]

                cursor.execute("""
                    UPDATE Productos
                    SET Nombre = ?, Precio = ?, Unidades_Disponibles = ?
                    WHERE id = ?
                """, (New_Nombre, New_Precio, New_Unidades, id_prod))
                
                conexion.commit()
                print("Producto actualizado exitosamente.")
            else:
                print("NO se ha encontrado el producto con el ID ingresado.")
        except ValueError:
            print("Error: Ingrese datos numéricos válidos.")





    elif Opcion == "4":  # Eliminar producto
        print("\n|--- ELIMINAR PRODUCTO ---|")
        try:
            id_prod = int(input(" ID DEL PRODUCTO: "))
            cursor.execute("DELETE FROM Productos WHERE id = ?", (id_prod,))
            conexion.commit()
                    
            if cursor.rowcount > 0:
                print("Producto eliminado con éxito.")
            else:
                print("No se pudo encontrar ningún producto con el ID ingresado.")
        except ValueError:
            print("Error: El ID debe ser un número entero.")

    elif Opcion == "5":  # Registrar una venta (Parte 3: Transacciones y Validaciones)
        print("\n=== REGISTRAR VENTA ===")
        try:
            id_producto = int(input("Ingrese el ID del producto a vender: "))
            
            # 1. Verificar que el producto exista
            cursor.execute("SELECT Nombre, Unidades_Disponibles FROM Productos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()
            
            if not producto:
                print("ERROR: El producto con ese ID no existe.")
                continue

            nombre_prod, stock_actual = producto
            cant_vender = int(input(f"Ingrese la cantidad a vender (Stock actual: {stock_actual}): "))

            if cant_vender <= 0:
                print("ERROR: La cantidad debe ser mayor a 0.")
                continue

            # 2. Comprobar que haya suficientes unidades
            if cant_vender > stock_actual:
                print(f"ERROR: Stock insuficiente. Solo hay {stock_actual} unidades disponibles.")
                continue

            # Preguntar si desea simular el error de la Parte 3 (Reto obligatorio)
            simular_error = input("¿Desea simular un error controlado para probar el ROLLBACK? (s/n): ").strip().lower()

            try:
                # Iniciar transacción explícita desactivando auto-commit si se requiere
                # 3. Registrar la venta en la base de datos
                cursor.execute("""
                    INSERT INTO Ventas (PRODUCTO_ID, UNIDADES)
                    VALUES (?, ?)
                """, (id_producto, cant_vender))

                # Provocar error simulado si el usuario lo solicita
                if simular_error == 's':
                    print("\n[SIMULACIÓN] Provocando error antes de actualizar el inventario...")
                    raise Exception("Falla simulada del sistema entre la venta y el descuento de inventario.")

                # 4. Descontar las unidades vendidas del inventario
                cursor.execute("""
                    UPDATE Productos
                    SET Unidades_Disponibles = Unidades_Disponibles - ?
                    WHERE id = ?
                """, (cant_vender, id_producto))

                # 5. Confirmar ambas operaciones mediante commit()
                conexion.commit()
                print(f"¡Venta de {cant_vender} unidad(es) de '{nombre_prod}' registrada con éxito!")

            except Exception as e:
                # Reto obligatorio: Cancelar la operación completa si falla algo
                conexion.rollback()
                print(f"\n[ROLLBACK EJECUTADO] Se canceló la transacción. Razón: {e}")
                print("Los datos permanecen intactos en la base de datos.")

        except ValueError:
            print("Error: Debe ingresar un valor numérico válido.")

    elif Opcion == "6":  # Mostrar historial de ventas mediante JOIN
        print("\n|=== HISTORIAL DE VENTAS ===|")
        cursor.execute("""
            SELECT 
                Ventas.id, 
                Productos.Nombre, 
                Ventas.UNIDADES, 
                Productos.Precio,
                (Ventas.UNIDADES * Productos.Precio) AS Total,
                Ventas.FECHA
            FROM Ventas
            INNER JOIN Productos ON Ventas.PRODUCTO_ID = Productos.id
            ORDER BY Ventas.FECHA DESC
        """)
        ventas = cursor.fetchall()

        if ventas:
            for v in ventas:
                print(f"ID Venta: {v[0]} | Producto: {v[1]} | Cantidad: {v[2]} | Precio Unitario: ${v[3]:.2f} | Total: ${v[4]:.2f} | Fecha: {v[5]}")
        else:
            print("==========================================")
            print(" No hay ventas registradas aún.")
            print("==========================================")

    elif Opcion == "7":  # Salir del programa
        print("\nSaliendo del programa... ¡Hasta luego!")
        conexion.close()
        break

    else:
        # Validación en caso de que el usuario ingrese una opción fuera del menú
        print("\nLA OPCIÓN INGRESADA NO ES VÁLIDA EN EL PROGRAMA. Por favor inténtelo de nuevo.")