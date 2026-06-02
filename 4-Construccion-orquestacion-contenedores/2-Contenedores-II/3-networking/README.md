### Challenge

Para este ejercicio deberá contar con el código de la aplicación que conecta a BD.
Luego, implementar una arquitectura similar a la siguiente:

~~~
host <----> nginx <-----> app <-----> DB
~~~

Consideraciones:

- El host NO puede tener conexión directa hacia la app ni DB
- NginX NO puede acceder directamente hacia la DB
- La app debe esperar a que la DB esté lista para aceptar conexiones. Implementar algún tipo de healthcheck
- Respaldar los datos de la BD (basicamente, implementar volumen)



### Links de ayuda e interés


- https://craftech.io/blog/the-ultimate-guide-to-containerize-php/
- https://blog.kubesimplify.com/docker-networking-demystified
- https://learn-docker.it-sziget.hu/en/latest/pages/advanced/kernel-namespaces-network.html
- https://spacelift.io/blog/docker-networking
- https://medium.com/@MetricFire/understanding-docker-networking-9f81244cf824
- https://www.docker.com/blog/docker-networking-design-philosophy/
- https://www.simplilearn.com/tutorials/docker-tutorial/docker-networking#container_network_model
- https://docs.docker.com/network/network-tutorial-standalone/
- https://docs.docker.com/network/network-tutorial-host/
- https://dev.to/pemcconnell/docker-networking-network-namespaces-docker-and-dns-19f1