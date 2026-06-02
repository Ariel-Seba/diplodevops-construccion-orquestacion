## Construccion y orquestación de contenedores - Clase 4


### Temas a ver
- Deployments
- ConfigMaps
- Secrets

### 1 - apps

En esta primera parte, levantaremos un docker compose con una aplicación sencilla que recibe una variable de entorno y un secret.
Una variable de entorno es un valor definido por el usuario que puede afectar como se ejecuta un proceso. En un ambiente Linux, cada proceso tiene su conjunto de variables de entorno, y hereda las de su proceso padre al momento de hacer un fork.

En el docker compose, entonces, vemos los siguientes campos nuevos:

- environment: Lista o mapa con las variables de entorno en formato <key>: <value>. -- [Link de ayuda](https://docs.docker.com/compose/environment-variables/set-environment-variables/) -- [Blogpost de interes](https://vsupalov.com/docker-arg-env-variable-guide/)

- secrets: Variables que tipicamente tienen información sensible (ej, credenciales de BD), por lo que se proveé un mecanismo para dificultar el acceso a usuarios no deseados. Es decir, toda información que no se debe publicar por el riesgo que conlleva. Docker monta los secretos bajo el path **/run/secrets/<secret_name>** -- [Link de ayuda](https://docs.docker.com/engine/swarm/secrets/)


### Ejercicio 1: Listar variables de entorno

Ejecutamos el docker compose provisto, e ingresamos a una shell del contenedor. Dentro del mismo, ejecutamos

`printenv | grep ENG_MSG`


### Ejercicio 2: Exploramos el secreto

Nuevamente desde el contenedor, exploramos el path `/run/secrets/`

Explore el código de la aplicación bajo el path `/secret`

### Ejercicio 3: Despliegue en K8S

Desplegar los manifiestos ubicados en el directorio "2-manifests" según el orden en que se presentan, del manifiesto 1 al 4.
Una vez explorado y entendido los conceptos, eliminar el manifiesto 2 y desplegar en su lugar el manifiesto 5.
Realize la misma investigación de variables de entorno y secrets que la realizada en el docker compose.

¡Mas comandos!

- `kubectl delete -f <manifest>`
- `kubectl get nodes -o wide`
- `kubectl get services -n <namespace>`
- `kubectl get pods -n <namespace>`
- `kubectl logs <pod> -n <namespace>`

### Tarea 1: Desplegamos app-saludo

Ya teniendo los recursos de K8S básicos, realize los despliegues necesarios para "app-saludo" teniendo en mente la consigna del trabajo final. Aproveche este ejercicio para definir el flujo de trabajo con su equipo, ramas, git, etc.
Por el momento, se recomienda que la imagen de aplicación se aloje en un repositorio de imagenes docker PÚBLICO.
Una vez desplegada y probada la aplicación, puede pasar dicho repositorio a PRIVADO, y estudiar como debe autenticarse para traer dicha imagen.


### Tarea 2: Desplegamos nuestra app

En esta segunda tarea se pide desplegar la "app-db" dada como tarea en la clase 1.
Se solicita utilizar ConfigMaps y/o Secrets para configurar parámetros. Ej: parametros de conexión a BD de la aplicación.

### Challenge: Opciones para debug

Conectarse al nodo de forma tal que pueda ejecutar comandos sobre la máquina. Si usa minikube, [`minikube ssh`](https://minikube.sigs.k8s.io/docs/commands/ssh/) les dá un acceso a consola. Si no puede acceder por SSH al nodo, pero tiene acceso por kubectl al cluster, puede utilizar un [pod de debug](https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/)

Una vez dentro, explore `/var/log`.
Realize lo mismo, pero explorando ese directorio dentro de un pod. 
- ¿Que nota?
- ¿Que ventaja puede dar el hecho de que las cosas sucedan de esa forma?
- ¿En que nos puede ayudar saber donde se guardan esos logs?
