# creación de la base de datos de productos, si no existe la base de datos, se crea.
# Cargamos las librerías globales necesarias para el programa archivo main.py
import sqlite3
import os

from colorama import init, Fore, Back, Style
# Inicializamos colorama (autoreset=True es clave para que el color no se "pegue" a la siguiente línea)
init(autoreset=True)

# Funcipon limpiar pantalla
def limpiar_pantalla():
    """Limpia la pantalla de la terminal según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

# ---------------------
# Conexión y creación de DB inventario.db y tabla productos
# ---------------------
def conectar_db():
    """
    Crea una tabla solo si no existe la tabla productos
    id INTEGER PRIMARY KEY AUTOINCREMENT, # INTEGER: Almacenará números enteros, PRIMARY KEY: Campo de valor único id , AUTOINCREMENT se incrementa de manera automática cada vez que se inserta un nuevo registro
        nombre TEXT NOT NULL, # TEXT: campo de tipo texto, NOT NULL: no puede ser null (vacío)
        descripcion TEXT, # Campo de tipo texto, puede permite null 
        cantidad INTEGER NOT NULL,  # campo de tipo entero, no permite null
        precio REAL NOT NULL, # REAL: campo de tipo decimal y no permite valor null
        categoria TEXT NOT NULL # campo de tipo texto y no permite valor null
    """
    # indicamos el directorio actual del archivo main.py para crear la base de datos en el mismo directorio
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_db = os.path.join(directorio_actual, "inventario.db")
    # sqlite3.connect: si el archivo inventario.db se conecta si no existe se crea.
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL
        )
    """)
    conexion.commit()
    # Cerramos la conexión para liberar el archivo la conexión de la base de datos solo se realiza dentro den esta función. 
    #conexion.close()
    #si tenemos conexion.close() no se utiliza el return conexión porque la conexión se cierra al finalizar la función.
    return conexion


# ---------------------
# función para agregar productos en la base de datos
# ---------------------
def agregar_producto(conexion):
    """Pide datos al usuario y los guarda en la base de datos."""
    limpiar_pantalla() # se llama la fucnión limpiar pantalla


    while True:
        print(f"{Back.BLUE}\n** Menu Ingreso de Productos **\n")

        print (f"{Fore.GREEN} \n Introduzca los datos del producto a registrar: ")
        while True:
            nombre = input(f"{Fore.CYAN}\t\t Nombre: {Style.RESET_ALL}").strip()
            if nombre:
                break
            print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}ERRO!! El campo nombre esta vacio, ingrese el nombre del producto")
        while True:
            descripcion = input(f"{Fore.CYAN}\t\t Descripción: {Style.RESET_ALL}").strip()
            if descripcion:
                break
            print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}ERRO!! El campo descripción esta vacio, ingrese la descripción del producto")

        while True:
            cantidad = (input(f"{Fore.CYAN}\t\t Cantidad: {Style.RESET_ALL}").strip())
            # vlidamos que el campo cantidad no este vacio
            if not cantidad: 
                print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}ERRO!! El campo cantidad esta vacio, ingrese la cantidad del producto")
                continue
            try: 
                cantidad = int(cantidad)
                if cantidad < 1:
                    print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}ERROR!! el campo contiene un valor menor a 1")
                    continue
                break
            except ValueError:
                print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}ERRO!! Ingresar un numero entero valido (ej: 1 2 3 )")

        while True:
            try:
                precio = float(input(f"{Fore.CYAN}\t\t Precio: $ {Style.RESET_ALL}").replace(",","."))
                if precio > 0:
                    break
                print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}ERRO!! El precio debe ser mayor a 0 ")
            except ValueError:
                print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}ERRO!! Ingresa un numero valido (ej: 1200.40)")

        while True:
                categoria = input(f"{Fore.CYAN}\t\t Categoría: {Style.RESET_ALL}").strip()
                if categoria:
                    break
                print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}ERRO!! El campo categoría esta vacio, ingrese la categoría del producto") 

        # tenemos cargado en memoria la conexión a la DB cuando llamamos a la fución conectar_db() en el menu principal
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO productos (nombre,descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?) ",(nombre,descripcion,cantidad,precio,categoria))
            conexion.commit()
            print(f"{Fore.GREEN} Producto {Style.RESET_ALL} '{nombre}' {Fore.GREEN}agregado correctamente.{Style.RESET_ALL}")
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}\n  ERROR !! al guardar: {e}")
        # submenu de salida 
        submenu = 0
        submenu = input(f"{Style.BRIGHT}\n¿Quiere salir? Presione S. Para cargar otro producto, presione Enter: {Style.RESET_ALL}").strip().title()
        if submenu == "S":
            break  # rompe el sub-bucle del menu



#------
# Modulo de listado de registros de la DB 
# -----

def ver_productos(conexion):
    """Muestra todos os productos en formato tabla."""
    limpiar_pantalla() ## llamamos a la función limpiar_pantalla()

    print(f"{Back.BLUE}\n\t\t** Listado de Productos Cargados **\n")

    # tenemos cargado en memoria la conexión a la DB cuando llamamos a la fución conectar_db() en el menu principal
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos ORDER BY id")
    filas = cursor.fetchall()

    if not filas:
        print(f"{Style.BRIGHT + Fore.WHITE + Back.RED}\n No hay en stock")
        input(f"{Style.BRIGHT}\nPresione Enter para volver al menú principal...{Style.RESET_ALL}")
        return

    print("\n" + "-" * 120)
    print(f"{Fore.GREEN}  {'ID':<5} {'NOMBRE':<20} {'DESCRIPCIÓN':<20} {'CANTIDAD':<10} {'CATEGORÍA':<15} {'PRECIO':>15}")
    print(f"{Fore.RED}{'-' * 120}")
    for id_, nombre, descripcion, cantidad, precio, categoria in filas:
        print(f"  {id_:<5} {nombre:<20} {descripcion:<20} {cantidad:<10} {categoria:<15} ${precio:>14,.2f}")
    print("-" * 120)
    print(f"  Total de productos: {Style.BRIGHT}{len(filas)}{Style.RESET_ALL}")
    input(f"{Style.BRIGHT}\nPresione Enter para continuar...{Style.RESET_ALL}")



#--------
# Modulo de actualización  de registros
# ---------

def update_productos(conexion):
    """Actualizar los datos de un producto mediante su ID."""
    # tenemos cargado en memoria la conexión a la DB cuando llamamos a la fución conectar_db() en el menu principal
    cursor = conexion.cursor()

    while True:
        limpiar_pantalla()
        print(f"{Back.BLUE}\n\t\t** Menu Actualizar Producto **\n")
        
        
        # Hacemos una consulta rápida para mostrar qué hay disponible
        cursor.execute("SELECT id, nombre, cantidad, precio FROM productos ORDER BY id")
        filas = cursor.fetchall()
        
        if not filas:
            print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED}\n No hay productos en el inventario para actualizar.{Style.RESET_ALL}")
            input(f"\n{Style.BRIGHT}Presione Enter para volver al menú principal...{Style.RESET_ALL}")
            return # Expulsa al usuario al menú principal porque no hay nada que hacer

        # tabla resumida de los datos cargados en la base de datos
        print(f"{Fore.GREEN}  {'ID':<5} {'NOMBRE':<20} {'CANT':<8} {'PRECIO':>12}")
        print(f"{Fore.RED}{'-' * 55}")
        for id_, nombre, cantidad, precio in filas:
            print(f"  {id_:<5} {nombre:<20} {cantidad:<8} ${precio:>11,.2f}")
        print("-" * 55)
        # ---------------------------------------------
        
        # validar el ID
        while True:
            id_producto = input(f"\n{Fore.CYAN}Ingresa el ID del producto a actualizar (o 0 para salir): {Style.RESET_ALL}").strip()
            
            if id_producto == "0":
                return # Salida rápida 
                
            if not id_producto:
                print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED} ERROR!! El ID no puede estar vacío.")
                continue
            try: 
                id_producto = int(id_producto)
                if id_producto < 1:
                    print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED} ERROR!! El campo contiene un valor inválido.")
                    continue
                break 
            except ValueError:
                print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED} ERROR!! Ingresar un número entero válido.")
        
        # se busca todos los datos actuales del ID indicado
        cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone() 

        if not producto:
            # Si pone un ID que no existe el bucle reiniciará
            print(f"{Style.BRIGHT}{Fore.YELLOW}\n No se encontró ningún producto con el ID {id_producto}. Intente de nuevo.{Style.RESET_ALL}")
            input(f"{Style.BRIGHT}\nPresione Enter para continuar...")
            continue 

        # Desempaquetamos los datos
        id_, nombre_actual, descripcion_actual, cantidad_actual, precio_actual, categoria_actual = producto

        # CÓDIGO DONDE SE EDITAN LOS DATOS DEL PRODUCTO
        print(f"{Style.BRIGHT}\n Editando: {Fore.GREEN}{nombre_actual}{Style.RESET_ALL}")
        print(f"\n\t Escriba los nuevos datos (Presione ENTER para conservar el valor actual):")

        # --- EDICIÓN ---
        nombre_nuevo = input(f"{Fore.CYAN}  Nombre {Style.RESET_ALL}[{nombre_actual}] {Fore.CYAN}-> : {Style.RESET_ALL}").strip()
        if not nombre_nuevo:
            nombre_nuevo = nombre_actual
            
        descripcion_nuevo = input(f"{Fore.CYAN}  Descripción {Style.RESET_ALL}[{descripcion_actual}] {Fore.CYAN}-> : {Style.RESET_ALL}").strip()
        if not descripcion_nuevo:
            descripcion_nuevo = descripcion_actual

        # Validación de Cantidad
        while True:
            entrada_cantidad = input(f"{Fore.CYAN}  Cantidad {Style.RESET_ALL}[{cantidad_actual}] {Fore.CYAN}-> : {Style.RESET_ALL}").strip()
            if not entrada_cantidad:
                cantidad_nuevo = cantidad_actual
                break
            try: 
                cantidad_nuevo = int(entrada_cantidad)
                if cantidad_nuevo < 1: 
                    print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED} ERROR!! La cantidad no puede ser menor a 1.")
                    continue
                break
            except ValueError:
                print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED} ERROR!! Ingresar un número entero válido.")

        # Validación de Precio
        while True:
            entrada_precio = input(f"{Fore.CYAN}  Precio {Style.RESET_ALL}[${precio_actual:,.2f}] {Fore.CYAN}-> $ : {Style.RESET_ALL}").strip().replace(",", ".")
            if not entrada_precio:
                precio_nuevo = precio_actual
                break 
            try:
                precio_nuevo = float(entrada_precio)
                if precio_nuevo <= 0:
                    print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED} ERROR!! El precio debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED} ERROR!! Ingresa un número válido.")

        categoria_nuevo = input(f"{Fore.CYAN}  Categoría {Style.RESET_ALL}[{categoria_actual}] {Fore.CYAN}-> : {Style.RESET_ALL}").strip()
        if not categoria_nuevo:
            categoria_nuevo = categoria_actual

        # UPDATE de la db
        try:
            cursor.execute("""
                UPDATE productos 
                SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? 
                WHERE id=?
            """, (nombre_nuevo, descripcion_nuevo, cantidad_nuevo, precio_nuevo, categoria_nuevo, id_producto))
            
            conexion.commit()
            print(f"\n {Fore.GREEN}Producto {Style.RESET_ALL}'{nombre_nuevo}' {Fore.GREEN}actualizado correctamente.{Style.RESET_ALL}")
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"{Style.BRIGHT}{Fore.WHITE}{Back.RED}\n  ERROR !! al actualizar: {e}")
            
        # Submenú de salida general
        submenu = input(f"{Style.BRIGHT}\n¿Quiere salir al menú principal? Presione S. Para modificar otro, presione Enter: {Style.RESET_ALL}").strip().upper()
        if submenu == "S":
            break


#-------------------
# borrar registros de la DB
#-----------------
def eliminar_productos(conexion):
    """Elimina productos por su id en ese modulo el cliente elimina un producto y retorna al menu principal"""
    limpiar_pantalla()

    # Listamos todos los productos 
    ver_productos(conexion)

    # Solicitamos el ID del producto a eliminar
    print(f"\n\t\t\t{Back.BLUE}** Eliminación de Producto por ID **{Style.RESET_ALL}\n")
    try:
        id_eliminar = int(input(f"{Fore.CYAN}\n Ingresa el ID del producto a eliminar: {Style.RESET_ALL}").strip()) # 1
    except ValueError:
        input(f"{Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! el ID debe ser un número entero, Enter para retornará al menú principal{Style.RESET_ALL}")
        return
    
    # Buscamos la info
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM productos WHERE id = ? " , (id_eliminar,)) # id=1 nombre="coca-cola" cat="ada" precio=1231 -> ["1","coca-cola","categora",1231432]
    fila = cursor.fetchone()

    if not fila:
        input(f"{Style.BRIGHT + Fore.WHITE + Back.RED} No existe ningÚn producto con el id {id_eliminar}, Enter para retornará al menú principal{Style.RESET_ALL}")
        return

    nombre = fila[0]
    print(f"\n {Style.BRIGHT}Producto encontrado:{Style.RESET_ALL} {Fore.GREEN}{nombre}{Style.RESET_ALL}")
    respuesta = input(f"{Fore.CYAN} ¿ Quiere  eliminar  el producto {Style.RESET_ALL}  '{nombre}' {Fore.CYAN}(s/n): {Style.RESET_ALL}").strip().title().upper()
    if respuesta != 'S':
        respuesta = input(f'{Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! Escriba "S" para eliminar el producto, Enter para retornará al menú principal{Style.RESET_ALL}')
        return
    # ELiminamos la info de la DB
    try:
        cursor.execute("DELETE FROM productos WHERE id = ?",(id_eliminar,))
        conexion.commit()
        print(f"{Fore.CYAN} producto {Style.RESET_ALL}  '{nombre}' {Fore.CYAN} eliminado correctamente.{Style.RESET_ALL}")
    except sqlite3.Error as e:
        conexion.rollback()
        print(f"\n {Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! al eliminar: {e}")
    input(f"{Style.BRIGHT}\nPresione Enter para continuar retornará al menú principal...{Style.RESET_ALL}")





#----------
#  Reportes de productos con un filtro
# ---------

def reporte_productos(conexion):
    """Menú Reporte de productos por su ID, nombre o categoría"""

    while True:
        limpiar_pantalla()
        # Menu de filtros para los reportes 
        print(f"{Back.BLUE}\n ** Menu Filtro de Reporte de Productos **\n")

        print ("\n Indique el filtro de la búsqueda del producto:")
        print (f"\t 1. Buscar por ID")
        print (f"\t 2. Buscar por Nombre")
        print (f"\t 3. Buscar por Categoría")
        print (f"\t 4. Cantidad de productos igual o inferior a un límite")
        print (f"\t 5. Salir al menú principal")
        filtro = input(f"{Fore.CYAN}\nIndique el filtro de la búsqueda del producto,  : {Style.RESET_ALL}").strip()
        if not filtro:
            input(f"{Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! no puede estar vacío, Entre para retornará al menú principal{Style.RESET_ALL}")
            return
        if filtro not in ["1", "2", "3", "4" ,"5"]:
            input(f"{Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! Opción de filtro no válida solo se aceptan 1, 2, 3 o 4, Entre para retornará al menú principal  {Style.RESET_ALL}")
            return
        # algunos filtro tienen un SELECT con un LIKE en el WHERE para buscar palabras claves y obtener el listado completo otros tienen consulta puntual o por rango
        elif filtro == "1":
            try:
                busqueda_filtro = int(input(f"{Fore.CYAN}\nIngresa el ID a buscar: {Style.RESET_ALL}").strip())
            except ValueError:
                input(f"{Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! el ID debe ser un número entero, Entre para retornará al menú principal{Style.RESET_ALL}")
                return
            cursor = conexion.cursor()
            cursor.execute("SELECT id,nombre,descripcion,cantidad,precio,categoria FROM productos WHERE id = ? ORDER BY id", (busqueda_filtro,))
            filas = cursor.fetchall()
        elif filtro == "2":
            busqueda_filtro = input(f"{Fore.CYAN}\nIngresa el nombre a buscar: {Style.RESET_ALL}").strip()
            if not busqueda_filtro:
                input(f"{Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! El nombre de búsqueda no puede estar vacío, Entre para retornará al menú principal{Style.RESET_ALL}")
                return
            cursor = conexion.cursor()
            # LIKE para buscar coincidencias en los campos 
            cursor.execute("SELECT id,nombre,descripcion,cantidad,precio,categoria FROM productos WHERE nombre LIKE ? ORDER BY id", (f"%{busqueda_filtro}%",) )
            filas = cursor.fetchall()
        elif filtro == "3":
            busqueda_filtro = input(f"{Fore.CYAN}\nIngresa la categoría a buscar: {Style.RESET_ALL}").strip()
            if not busqueda_filtro:
                input(f"{Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! La categoría de búsqueda no puede estar vacía, Entre para retornará al menú principal{Style.RESET_ALL}")
                return
            cursor = conexion.cursor()
            cursor.execute("SELECT id,nombre,descripcion,cantidad,precio,categoria FROM productos WHERE categoria LIKE ? ORDER BY id", (f"%{busqueda_filtro}%",) )
            filas = cursor.fetchall()
        elif filtro == "4":
            try:
                busqueda_filtro = int(input(f"{Fore.CYAN}\nIngresa la cantidad límite a buscar: {Style.RESET_ALL}").strip())
            except ValueError:
                input(f"{Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! la cantidad límite debe ser un número entero, Entre para retornará al menú principal{Style.RESET_ALL}")
                return
            cursor = conexion.cursor()
            cursor.execute("SELECT id,nombre,descripcion,cantidad,precio,categoria FROM productos WHERE cantidad <= ? ORDER BY id", (busqueda_filtro,))
            filas = cursor.fetchall()
        elif filtro == "5":
            break  # Salida al menú principal
        #else:
        #    input(f"{Style.BRIGHT + Fore.WHITE + Back.RED} ERROR !! Opción de filtro no válida , Entre para retornará al menú principal{Style.RESET_ALL}")
        #    return


        print(f"\n  Se encontraron {len(filas)} resultado(s):")
        print("\n" + "-" * 100)
        print(f"{Fore.GREEN}   {'ID':<5} {'NOMBRE':<20} {'DESCRIPCIÓN':<20} {'CANTIDAD':<10} {'PRECIO':<15} {'CATEGORÍA':<20}")
        print(f"{Fore.RED}{'-' * 100}")
        for id_, nombre, descripcion, cantidad, precio, categoria in filas:
            print(f"  {id_:<5} {nombre:<20} {descripcion:<20} {cantidad:<10} ${precio:<15,.2f} {categoria:<20}")
        print("-" * 100)
        # Submenú de salida
        submenu = input(f"{Style.BRIGHT}\n¿Quiere salir al menú principal? Presione S. Para modificar otro producto, presione Enter: {Style.RESET_ALL}").strip().upper()
        if submenu == "S":
            break  # Rompe el bucle principal



