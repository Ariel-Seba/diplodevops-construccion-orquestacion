## Practico Podman

## Instalacion

https://podman.io/docs/installation

## Guia rapida

https://podman.io/docs

## Ejemplo sencillo

- podman run -dt -p 8080:80/tcp docker.io/library/httpd

## Paso a paso

### Configuracion de los registries

Archivo de configuración de registries:
/etc/containers/registries.conf

En vez de modificar el archivo global, podemos tener uno por usuario:
~/.config/containers/registries.conf

### Primeros comandos

Notará que los comandos son muy similares a los de Docker. Esto es por diseño, para permitir una transición mas sencilla.
Algunos usuarios crean un alias "docker=podman" al comenzar una migración de Docker a Podman.

Para buscar una imagen, usamos el comando 
podman search <image>
Esto utilizará los registries definidos en el archivo de configuración.

Podemos especificar un registry en particular. Por ejemplo:
- podman search docker.io/library/httpd

Habrá notado que en estos comandos no fué necesario ejecutar como "sudo"

## EJERCICIOS: 
- Agregue el registry "quay.io"
- ¿Como creé que podemos "pullear" una imagen"?
- ¿Como listamos imagenes descargadas?
- Una forma rápida de limpiar nuestro entorno que es de mi agrado es con "docker rm -f $(docker ps -aq)". ¿Como lo haría con podman?
- podman run -it -p 8080:80/tcp docker.io/library/httpd

### Construyendo imagenes

Podman es compatible con Dockerfile, por lo que todos los comandos de docker utilizados para construir una imagen son equivalentes.

NOTA: Como aclaración conceptual, Podman no es en sí el que construye las imágenes. El comando "podman build" utiliza por debajo código proveniente del proyecto "Buildah"

### Compartiendo imágenes

Similar al punto anterior, los comandos de Podman son similares a los de Docker en este aspecto:

- podman login <registry>
- podman build -t <username>/<image-name>
- podman push <username>/<image-name>

### Links relacionados:
- https://www.redhat.com/es/topics/containers/what-is-buildah
- https://docs.redhat.com/es/documentation/red_hat_enterprise_linux/8/html/building_running_and_managing_containers/index
- https://earthly.dev/blog/docker-vs-buildah-vs-kaniko/
- https://developers.redhat.com/blog/2018/02/22/container-terminology-practical-introduction#h.dqlu6589ootw
- https://www.youtube.com/watch?v=YXfA5O5Mr18
- https://docs.redhat.com/es/documentation/red_hat_enterprise_linux_atomic_host/7/html/managing_containers/finding_running_and_building_containers_with_podman_skopeo_and_buildah#overview

