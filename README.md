# Demo HashiCopr Vault
Generaracion de credenciales de conexión a base de datos bajo demanda.

![demo](/img/demo.png)

Esta demo pretende mostrar como funciona la creacion de credenciales de conexccion de forma dinamica con el administrador de secretos vault, mejorando la seguridad en una aplicacion sencilla de django.

Los beneficios de aplicar esta estrategia usando vault son los siguientes:
- No hay unas credenciales que usen las aplicaciones que tengan un tiempo de vida indefinido.
- Las aplicaciones no necesitan guardar en su configuración las credenciales.
- las credenciales se rotan de forma automática cada cierto tiempo 
- los permisos para obtenerlas se pueden revocar de forma centralizada con Vault esto con cualquier bases de datos que se utilicen

## Instalacion 
En este demo se realizo en un sistema windows utilizando WSL se realizo la instalamos Vault en ESL usando la siguiente guia [Guia de instalacion para Linux/Ubuntu](https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-install).

Ademas de lo anterior se debe tener docker en el equipo he instalar las dependencias necesarias para la ejecuion del server de django usando el siguiente comando 

    $ pip install -r requirements.txt

## Ejecucion

1 Arancar server de vault y obtenemos la llave y token de acceso 

    WSL | vault server -dev

![demo](/img/server%20vault.PNG)

2 Correr el container con la base de datos y creamos la base de datos app para probar el demo

    CMD | startDB.bat
          psql -U postgres
          CREATE DATABASE app;

![demo](/img/start%20db.PNG)

3 iniciar secion en el server de vault con el token de acceso obtenido en el paso 1 y configuramos la coneccion de vault con la base de datos y la creacion de roles dinamicos 

    WSL | start_vault.sh

![demo](/img/config%20vault.PNG)

4 crear variables de entono para el Unseal Key y Root Token del server de vault, estos valores se obtienen en el paso 1 

    CMD | environment.bat


5 aplicamos migraciones en la aplicacion de django la base de datos, arrancamos el manejador de credenciales y server de django.

    CMD |  py cred_handler.py

![demo](/img/server%20django.PNG)

Despues de un tiempo en ejecucion podemos ver que en la base de datos se han creado nuevos roles con una vida util definida de 10 min.

![demo](/img/created%20roles.PNG)

Eestos roles fueron renovados por vault y solicitados por la aplicacion de django cada que sus credenciales de coneccion de bsase de datos estaban por expirar. 

