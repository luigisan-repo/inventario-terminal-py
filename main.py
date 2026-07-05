# Archivo principal del programa. 

# creación de la base de datos de productos, si no existe la base de datos, se crea.
# Cargamos las librerías globales necesarias para el programa archivo main.py
import sqlite3
import os

# Importamos las funciones del archivo modulos.py
from modulos import (conectar_db, 
    agregar_producto, 
    ver_productos, 
    update_productos, 
    eliminar_productos, 
    reporte_productos, 
    limpiar_pantalla
)

from colorama import init, Fore, Back, Style
# Inicializamos colorama (autoreset=True es clave para que el color no se "pegue" a la siguiente línea)
init(autoreset=True)



# Funcipon limpiar pantalla
def limpiar_pantalla():
    """Limpia la pantalla de la terminal según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

# +++++++++++++
# Inicio del programa 
#++++++++++++++
# se llama la función de creación y conexión de la DB
conexion = conectar_db()
menu ="0" # lo ponemos tipo srt porque el user puede colocar un caracter. 

# creamos siclo para la creación del menu interactivo utilizando match-case
while True: # El bucle sigue mientras no sea false
    limpiar_pantalla()
    print (f"\t\t{Back.YELLOW + Fore.BLACK} Sistema de Inventario de Productos")
    print (f"-"*120)
    print (f"{Back.BLUE}\n\t\t -- MENU PRINCIPAL --")
    print(f"{Fore.RED}{'-' * 120}")
    print (f"\t1. Registrar nuevos productos")
    print (f"\t2. Listado de todos los productos registrados")
    print (f"\t3. Actualizar datos de productos, mediante su ID")
    print (f"\t4. Eliminación de productos, mediante su ID")
    print (f"\t5. Reporte de productos, mediante su ID, Nombre, Categoría o Cantidad del producto")
    print (f"\t6. Salir")

    # var del menu es de tipo srt porque existe la posibilidad que de el usuario ponga un caracter
    menu = input(f"{Fore.CYAN}\nSeleccione una opción: {Style.RESET_ALL}") # input() SIEMPRE devuelve un texto (string) por defecto


    match menu:
        case "1":
           agregar_producto(conexion)

        case "2":
            ver_productos(conexion)
            
        case "3":
            update_productos(conexion)

        case "4":
            eliminar_productos(conexion)
        case "5":
            reporte_productos(conexion)
     
        case "6":
            print(f"\n¡Saliendo del sistema!")
            # Cerramos la conexión se abrió al inicio del programa
            conexion.close()
            break  # Rompe el bucle while salida del programa
        case "":
            print (f"{Style.BRIGHT + Fore.WHITE + Back.RED}\n!ERROR! : No selecciono ninguna opción.\n")
            input(f"{Style.BRIGHT}\nPresione Enter para volver al menú principal...{Style.RESET_ALL}")
        case _: # el else del match
            print (f"{Style.BRIGHT + Fore.WHITE + Back.RED}\n!ERROR! : Selecciono una opción no valida.\n")
            input(f"{Style.BRIGHT}\nPresione Enter para volver al menú principal...{Style.RESET_ALL}")