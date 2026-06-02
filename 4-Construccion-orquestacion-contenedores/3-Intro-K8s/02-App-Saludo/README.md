## Lab 02 - Mis primeros manifiestos

En esta parte veremos como crear recursos del tipo *namespace* y *pod*.

Para eso, debemos estar seguros que estamos apuntando al cluster creado en el Lab 01.

### Build de la aplicación

Sobre el path */apps* se encuentra una aplicación muy simple que será la que desplegaremos. Se disponibiliza un *docker-compose* para hacer pruebas locales.
Una vez buildeada la imagen, puede hacer push sobre algún repo propio. Se recomienda que a estas alturas los repos estén *públicos* para no complicarla con la necesidad de autenticarse al mismo desde el cluster.


### Aplicar manifiestos

En general, para crear recursos de K8S utilizaremos manifiestos. Para ello, tengamos presentes los comandos:

- `kubectl apply -f <path-a-manifiesto>`
- `kubectl delete -f <path-a-manifiesto>`

Tip: Si leer los primeros manifiestos le resulta confuso entender en un principio que está creando, pruebe leerlos de "abajo hacia arriba".

### Declarativo vs imperativo.

A lo largo de la materia aplicaremos el enfoque _declarativo_ en lugar del _imperativo_. Puede leer mas al respecto en este [enlace](https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Kubernetes-Resources/Imperative-vs-Declarative/page), pero a modo de resumen, para definir el estado del cluster y sus recursos lo haremos principalmente mediante archivos de manifiestos en formato YAML en vez de administrarlos por comandos CLI.

Nota: En los manifestos encontrarán comentarios con la leyenda "DIPLO:". Estos comentarios invitan a explorar y jugar un poco con esos campos señalados.
