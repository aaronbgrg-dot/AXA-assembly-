# En este documento, vamos a explicar los entresijos de nuestra base de datos MOBILIARIO.
Nuestra base de datos sirve para gestionar diferentes secciones de una tienda. Nos hemos enfocado en:
- Venta de muebles
- Diseño personalizado
- Comercio electrónico
- Gestión de pedidos
- Servicios adicionales
- Puntos de entrega y recogidas

Tenemos un total de 13 tablas. A continuación, una breve descripción sobre cada una de ellas:
+ Usuario: Gestión de la página web mediante roles.
+ Departamento: Áreas internas de secciones de trabajo de la empresa.
+ Trabajador: Los empleados de la empresa.
+ Proveedor: Empresas colaboradoras con nosotras y que nos proporcionan los materiales y productos correspondientes.
+ Mueble: Los productos a disposición del cliente.
+ Pedido: Cuantificador de pedidos por parte del cliente.
+ Detalle_pedido: Los productos seleccionados dentro de un mismo pedido. 
+ Diseño_personalizado: La función de proporcionar al cliente un sistema de personalización de productos.
+ Servicio: Servicios adicionales, especialmente enfocado al transporte. 
+ Pedido_servicio: Tabla intermedia entre servicio y pedido.
+ Oferta: Muestra de ofertas temporales aplicadas a algunos productos en venta de la página web.
+ Mueble_oferta: La relación entre el mueble y la oferta.
+ Cita: Registros de petición de entrega de producto y ubicación del mismo.

A continuación, explicamos las relaciones de cada tabla, además de la muestra visual:
+ Usuario:
* Un usuario solo puede pertenecer a un trabajador. Un trabajador no puede tener más de un usuario (1:1)
* Un usuario puede hacer más de un pedido. Un pedido solo puede ser realizado por un usuario. (1:N)
* Un usuario puede pedir más de un diseño personalizado pero este solo puede ser pedido por un usuario. (1:N)
* Un usuario puede pedir varias citas pero cada cita solo puede ser pedida por un usuario. (1:N)
+ Departamento:
* Un trabajador solo puede pertenecer a un departamento y en cada departamento puede haber más de un trabajador. (1:N)
+ Proveedor:
* Un proveedor puede dar varios muebles pero un mueble solo puede ser entregado por un proveedor. (1:N)
+ Mueble:
* Un mueble puede estar en más de un producto seleccionado, pero el producto solo puede contener ese mueble una vez. (1:N)
* Un mueble puede pedirse para más de un diseño pero ese diseño solo puede contener ese mueble una vez. (1:N)
* Un mueble puede tener varias ofertas y esa oferta puede tener varios muebles. (N:M)
+ Pedido:
* Puede haber más de un pedido en la cantidad total pero esa cantidad solo corresponde a un pedido total. (1:N)
* En un pedido, puede haber más de un servicio escogido y un servicio puede acaparar más de un pedido. (N:M)
* Una cita puede contener varios pedidos, pero un pedido solo puede estar en una cita concreta. (1:N)

Aquí dejo una imagen visual esquemática de la base de datos:

![Esquema](https://raw.githubusercontent.com/aaronbgrg-dot/AXA-assembly-/5f2c71e1adad6caea8a561404cf7cb22f8b89e5b/Imagen-Esquema-BD.png)



