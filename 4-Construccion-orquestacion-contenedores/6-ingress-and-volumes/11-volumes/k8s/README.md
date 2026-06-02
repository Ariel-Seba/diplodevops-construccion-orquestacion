### Volumes

Para esta seccion utilizamos la misma aplicación de volumen que la vista en la clase "Contenedores-II"
Una vez instalados los manifiestos, cargar en la aplicacion las imagenes deseadas.

~~~
kubectl exec --stdin --tty <pod> -n intro-k8s -- /bin/sh 
~~~


Una vez dentro, listemos los archivos dentro de el directorio "/uploads"
Puede probar escalando, desescalando, reinicando, eliminando el deployment etc. Mientras no se elimine el volumen, los datos de ese directorio deben persistir.

## Tareas

Con lo visto respecto de volumenes, implementar persistencia de datos en la aplicación de bases de datos.


## Challenges

- Implementar provisinado dinámico mediante "storage classes".
- Realizar conexión con algún volumen remoto (Ej, NFS, cloud, etc.)
- Configurar un deployment con multi-volumes con distinto backend de almacenamiento.
