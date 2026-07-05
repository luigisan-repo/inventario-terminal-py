# Sistema de Inventario de Productos (Terminal)
Este repositorio contiene el proyecto final para el curso de **Iniciación a la Programación con Python** dictado por [TalentoTech](https://talentotech.bue.edu.ar/home#/trayectos/adultos).

---
# Consigna del Proyecto Final Python

Desarrollar un programa en Python que cumpla con las siguientes características

## Requerimientos:
  1. **Base de datos**: Crear una base de datos llamada `inventario.db` para almacenar los datos de los productos. La tabla `productos` debe contener las siguientes columnas:
    - `id`: Identificador único del producto (clave primaria, auto-incremental).
    - `nombre`: Nombre del producto (texto, no nulo).
    - `descripcion`: Breve descripción del producto (texto).
    - `cantidad`: Cantidad disponible del producto (entero, no nulo).
    - `precio`: Precio del producto (real, no nulo).
    - `categoria`: Categoría a la que pertenece el producto (texto).  

## Funcionalidades de la aplicación  

1. **La aplicación debe permitir:**
    - Registrar nuevos productos.
    - Visualizar datos de los productos registrados.
    - Actualizar datos de productos, mediante su ID.
    - Eliminación de productos, mediante su ID
    - Búsqueda de productos, mediante su ID. De manera opcional, se puede implementar la búsqueda por los campos nombre o categoría.
    - Reporte de productos que tengan una cantidad igual o inferior a un límite especificado por el usuario o usuaria.  

## Interfaz de usuario  

Implementar una interfaz de usuario básica, para interactuar con la base de datos a través de la terminal. La interfaz debe incluir un menú principal con las opciones necesarias para acceder a cada funcionalidad descrita anteriormente.  

**Opcional**: Utilizar el módulo `colorama` para mejorar la legibilidad y experiencia de usuario en la terminal, añadiendo colores a los mensajes y opciones.

## Requisitos técnicos  

- El código debe estar bien estructurado, utilizando funciones para modularizar la lógica de la aplicación.
- Los comentarios deben estar presentes en el código, explicando las partes clave del mismo.


---
### Estructura del Proyecto

El código está modularizado para separar la lógica de la interfaz y la base de datos:

``` text
/
├── main.py        # Punto de entrada de la app y menú principal
├── operaciones.py # Lógica de conexión a DB y funciones
└── inventario.db  # Base de datos SQLite (se genera automáticamente al ejecutar)
```