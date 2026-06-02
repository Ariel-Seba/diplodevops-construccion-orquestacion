## Volumenes

### Ejercicio 1

Levantar la app con el docker-compose provisto.

~~~
sudo docker compose up
~~~

Una vez levantada, abrir la app en un navegador y cargar los archivos que se encuentran en el directorio "recursos".

- ¿Que nota en la carpeta "app-volumen"?
- ¿Que tipo de montaje estamos utilizando?

Eliminar el contenedor, levantarlo nuevamente. Sin cargar los archivos, ingrese al contenedor y explore el path _/code/src/uploads_


### Challenge

Modificar el tipo de montaje a _volume_.

Explorar el directorio **/var/lib/docker/volumes**

Simular una situación de "recuperación" y migrar un backup utilizando volumenes


### Links de ayuda e interés

- https://www.geeksforgeeks.org/docker-volume-vs-bind-mount/
- https://docs.docker.com/storage/volumes/#back-up-restore-or-migrate-data-volumes
- https://kinsta.com/es/blog/volumenes-docker-compose/
- https://www.schutzwerk.com/en/blog/linux-container-namespaces02-mnt/
