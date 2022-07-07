
Proyecto final para la formación en Tokio School.

Nos han solicitado una aplicación de escritorio la cual se utilizará para el manejo de una farmacia (administración, ventas y pagos) Esta debe contar con un inicio de sesión mediante el cual se podrá acceder, según el usuario, a distintas funcionalidades.

Usuario administrador

1.	Este usuario contará con la facultad de manejar los productos dentro del local. Podrá agregar, modificar y eliminar los artículos.
2.	Podrá crear, modificar y eliminar usuarios.

Usuario vendedor

1.	Generará tickets de venta con los productos seleccionados, donde se indicará la cantidad, descripción, precio por artículo, un total y un número de referencia del ticket. Este ultimo será utilizado por el cajero para hacer valida la compra. 
2.	Al usuario se le dará un aviso al momento de que un producto disponga de poco stock. Con esto así se pueda dar un aviso al administrador para una futura reposición. 

Usuario cajero
  
1. Este usuario acreditará las ventas utilizando el número de ticket generado por el usuario anterior (vendedor). Con el que se podrá ver si la venta fue pagada o no, además tendrá acceso a un resumen, donde se muestran los artículos adquiridos por el cliente. 
Todos los artículos deben ser almacenados en una base de datos, con sus respectivas referencias (código de producto, nombre o descripción, stock, precio de compra y precio de venta).
Por otra parte, los usuarios también serán almacenados en una base de datos con sus respectivos roles y contraseñas.
Por último, al igual que los datos anteriores, los tickets generados serán almacenados en una base de datos, donde podremos ver los productos adquiridos. Estos últimos deben ser descontados del stock general una vez la venta haya sido acreditada.



INICIO DE SESIÓN

Dispone de dos cuadros de entrada, uno para el usuario y el otro para ingresar la contraseña.  Según el rol que tenga el usuario se abrirá una ventana diferente (ADMINISTRADOR, VENDEDOR o CAJERO)
También indicará cuando el usuario que se ingrese no exista o la contraseña no sea la correcta. 
Cabe destacar que los usuarios están almacenados en una base de datos con su nombre de usuario, rol y contraseña.

![image](https://user-images.githubusercontent.com/108106098/175749265-5b877d69-d1fb-48a5-b298-b7fbbcd4b9d7.png)


VENTANA DEL ADMINISTRADOR

Esta ventana dispone de múltiples apartados, que se pueden visualizar en forma de tarjetas (tabs) en donde cada una contiene funcionalidades diferentes de la aplicación:

1.	LISTA DE PRODUCTOS

La tarjeta de lista de productos dispone de un apartado para el ingreso de productos a la base de datos dedicada. Podemos percibir una entrada para el código del artículo, una descripción, número de stock, precio de adquisición, y precio en que se venderá el elemento.  

Luego dispondremos de un listado con todos los productos ingresados con todas las características antes mencionadas.


![image](https://user-images.githubusercontent.com/108106098/175749443-4a31c1e0-84fc-4e32-a36b-9127d15f41e9.png)

2.	BUSQUEDA DE PRODUCTOS

En la tarjeta de búsqueda de productos, encontraremos una entrada para poder buscar un producto en especifico el cual será resaltado de la lista que se encuentra en la parte inferior. 

![image](https://user-images.githubusercontent.com/108106098/175749468-299b42d9-9eb2-4cf2-a9b9-3bab9383d517.png)

Una vez que se seleccione el elemento buscado, tendremos las opciones de editar o eliminar el producto. Solo hace falta clicar la opción deseada.

3.	EDITAR PRODUCTO

Esta tarjeta como se puede observar viene deshabilitada en un principio, solo se activará al momento de presionar el botón EDITAR de la tarjeta anterior (BUSQUEDA DE PRODUCTOS)

Aquí podremos modificar todas las características del producto, a excepción del código. 

![image](https://user-images.githubusercontent.com/108106098/175749495-2afe1c46-abd2-429c-9da5-16b236fd02fe.png)

Una vez que se hayan hecho las modificaciones pertinentes, se volverá a la tarjeta anterior, mostrándonos un mensaje que indica que el producto fue modificado con éxito.

![image](https://user-images.githubusercontent.com/108106098/175749506-a738cc60-15a0-4442-8686-eb279ff90ff1.png)

4.	CREAR USUARIOS

Esta tarjeta está dedicada para la creación de usuarios. En la primera parte podremos ingresar los parámetros de cada trabajador, nombre de usuario, rol del usuario (administrador, vendedor y cajero) y contraseña. Al igual que la tarjeta de LISTA DE PRODUCTOS una vez ingresada la información se podrán visualizar a los colaboradores en la lista de la parte inferior. Donde también podremos ver dos botones para modificar y eliminar usuarios.

![image](https://user-images.githubusercontent.com/108106098/175749537-7295b740-e266-4dbf-857a-6b0e517e1d5b.png)

EDITAR USUARIO

Para editar los parámetros del usuario deberemos seleccionar uno de la lista antes mencionada y presionar el botón para modificar. Posterior a esto emergerá una ventana donde podremos cambiar el nombre de usuario, rol y contraseña. 

Como medida de seguridad, al momento de querer modificar algo se solicita la contraseña actual del usuario.

![image](https://user-images.githubusercontent.com/108106098/175749563-7daba132-6951-451e-bc2b-2e958edd7555.png)

5.	CERRAR SESIÓN

En la parte superior izquierda se encuentra un apartado para cerrar la sesión y volver nuevamente al LOGIN de usuarios.

![image](https://user-images.githubusercontent.com/108106098/175749583-45bf1398-491f-4dc4-b874-78fad74b743a.png)

VENTANA DEL VENDEDOR

La ventana del vendedor podremos ingresar los productos que el cliente solicite. Esto mediante el código del artículo el cual le hace referencia. Además, podremos indicar la cantidad que se desea.
Disponemos de 3 botones en la parte derecha, que como sus nombres lo indican, podremos agregar el producto, eliminarlo y totalizar la cuenta de todos los elementos ingresados. 
Los productos ingresados se podrán visualizar en la lista que se encuentra en la parte inferior. Es aquí donde debemos seleccionar el ítem para hacer funcionar el botón de eliminar.

![image](https://user-images.githubusercontent.com/108106098/175749594-9bf95f52-ddb9-458b-9fb8-174d603d39d3.png)

Al momento de ingresar todos los artículos deseados deberemos presionar uno de los botones antes mencionados para totalizar la cuenta. En este momento visualizaremos el monto total a pagar a un costado de la etiqueta que dice TOTAL VENTA.

![image](https://user-images.githubusercontent.com/108106098/175749603-1685445e-4505-407f-8887-43dafadef2cf.png)

Una vez totalizada la cuenta tendremos dos opciones (botones) Una generar un ticket	venta o cancelarla eliminando todos los productos seleccionados.

En el ticket de venta, tendremos información del local, un resumen de la venta (cantidad, 	descripción y precio), el total y por último un código de barras con el número de referencia 	del ticket (este número será utilizado por el cajero para hacer valida la venta)

![image](https://user-images.githubusercontent.com/108106098/175749623-01cf6455-3ad1-40b1-8d90-57de55e11687.png)

Al momento de darle aceptar, el número de ticket generado es almacenado (primeros 12 números) en una base de datos junto con el código del producto, descripción, cantidad que solicitó el cliente, precio por unidad y precio totalizado según la cantidad anterior. 

![image](https://user-images.githubusercontent.com/108106098/175749651-bd6dc77d-1afd-43c0-9efe-0d182039124a.png)
![image](https://user-images.githubusercontent.com/108106098/175749659-38bc8b7c-0939-4d23-ac83-bcb8b54b036a.png)

VENTANA DEL CAJERO

En esta ventana podremos hacer efectivas la venta o consultar el estado de esta (PAGADO / NO PAGADO). Debemos ingresar el número de ticket generado por el vendedor (12 primeros números) y presionar en buscar ticket. Dándonos el estado y un resumen de la venta. 

![image](https://user-images.githubusercontent.com/108106098/175749696-a3f767aa-31c0-4140-ae4f-530853baa5bb.png)

Aquí podremos eliminar la búsqueda en el caso que solo estemos consultando o pagar la cuenta. Para ello deberemos ingresar con cuanto dinero pagará el cliente en el apartado PAGO CON y dar al botón PAGAR CUENTA. Luego de esto nos emergerá una venta con el mensaje de que el pagó fue realizado con éxito y en la parte inferior en el apartado de VUELTO la cantidad de dinero que se debe devolver al cliente.

![image](https://user-images.githubusercontent.com/108106098/175749706-026c13ce-6ca8-4880-88b6-a1459638cc0a.png)

Ahora si consultamos nuevamente por el ticket antes validado, podremos ver que el estado de este ha cambiado a PAGADO.

![image](https://user-images.githubusercontent.com/108106098/175749714-2fb1c1ac-730a-4145-956a-86a9a5b77b22.png)

EXTRAS

Una vez que el estado del ticket ha cambiado a PAGADO, las cantidades solicitadas se descontarán automáticamente del stock general.

STOCK ANTES DE LA VENTA

![image](https://user-images.githubusercontent.com/108106098/175749741-f02c28b3-67ca-4c18-b7bb-1133e4c6d599.png)

STOCK DESPUES DE LA VENTA

![image](https://user-images.githubusercontent.com/108106098/175749748-f908742e-3024-4782-9602-08fc93c7dfb9.png)

Al momento que se esté realizando una venta (VENTANA DEL VENDEDOR) En el caso de que un articulo disponga de poco stock (menor o igual a 5), la aplicación avisará al usuario con un mensaje emergente. 

![image](https://user-images.githubusercontent.com/108106098/175749765-5e3f95f2-c926-4f9d-9cb8-e3c6ebdcca14.png)

















