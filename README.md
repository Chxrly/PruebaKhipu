Prueba de Integración Khipu con Flask

Este proyecto demuestra la integración de pagos con Khipu usando su API en modo desarrollador. Se implementa una tienda básica con un **catálogo de productos**, 
**carrito de compras** y **procesamiento de pago** con un **límite de $5.000 CLP**, tal como lo exige el entorno de pruebas de Khipu.

Funcionalidades principales

- Visualización de productos con nombre, imagen y precio
- Agregar productos al carrito
- Editar cantidades directamente desde el carrito
- Eliminar productos del carrito
- Validación del monto máximo permitido para pruebas
- Redirección al flujo de pago oficial de Khipu

Estructura del código

- `app.py`: aplicación principal Flask con rutas para catálogo, carrito y pago
- `templates/`: incluye `catalogo.html`, `carrito.html`, y `layout.html` usando Jinja2
- `static/`: contiene imágenes de productos y estilos
