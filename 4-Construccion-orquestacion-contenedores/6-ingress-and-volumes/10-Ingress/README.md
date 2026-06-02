## Ingress

Levantaremos dos aplicaciones bajo el mismo namespace, y accederemos a las mismas a travez de reglas de ingress.

Para ello, primero es necesario instalar un INGRESS CONTROLLER.
En el caso de minikube, podemos instalar un nginx ingress controller simplemente con el siguiente comando:
~~~
    minikube addons enable ingress
~~~

Para otras distribuciones, será necesario consultar su documentación. Aun que, tipicamente, es simplemente aplicar un chart.

Habiendo levantado el ingress controller, procedemos a instalar los 4 manifiestos bajo el directorio "manifests"
Debes agregar esa entrada en tu /etc/hosts apuntando a 127.0.0.1

Luego, puede ser necesario que haga el mapeo http://diplodevops.example:8080/ (Esto es por como k3d interactua con el S.O.)

## Tarea 1

Habiendo finalizado la sección de networking, implementar los services e ingresses necesarios para el trabajo final.

## Tarea 2


Instalar los manifiestos 1,2 y 3 de la clase.
Para nginx ingress:
Luego, se proveen dos manifiestos de ingress con errores
- challenge-ingress-1.yaml
- challenge-ingress-2.yaml
Instalar UNO a la vez, y realizar un proceso de troubleshooting hasta hacerlos funcionar.
Para la resolución, **NO** consulte el manifiesto utilizado en clase.

Para Traefik:
Completar el manifiesto 4-ingress-traefik.yaml para que soporte el app contador.