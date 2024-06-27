# Proyecto venta de productos en la web
Este es el backend del software para ventas de productos de aseo en lineas, para la empresa Entregas Condor ltda.
El caso por el que se baso la creacion de este backend es el siguiente:
Entregas Cóndor Ltda; la empresa se dedica a la comercialización de productos para el aseo desde 
un punto central ubicado en Bogotá D.C. debido al confinamiento por el brote de COV-19 durante el año 2020, 
los clientes empezaron a escasear, y las ventas rápidamente empezaron a bajar, en busca de alternativas para poder superar
la falta de ventas, decidieron crear un espacio en el site de la empresa y activar la venta por catálogo, rápidamente las
ventas aumentaron, mediante el empleo de una estrategia de recomendados los pedidos de sus productos empezaron a ser
generados desde diferentes partes del país lo que generó un mayor volumen de ventas, nuevos clientes y la necesidad de
implementar un sistema de información mayor, además de generar alianzas con proveedores, distribuidores y requerir un
desarrollador backend que se encargue de toda la logica del web-site.

Para la creacion del proyecto se utilizo Fastapi como framework, psycopg como driver, postgresql como gestor de bases de datos,
sqlalchemy como orm, uvicorn como despliegue en la web de la aplicacion y pip como instalador de paquetes.

Este es el codigo para instalar todas librerias que yo use en el proyecto, estan almacenadas en el archivo
requirements.txt, deben usar pip para descargarlas todas de una vez con el archivo -r.
```
pip3 install -r requirements.txt
```

link del repositorio en GitHub del proyecto
```
git remote add origin "https://github.com/Edy1523/ventas-productos"
```