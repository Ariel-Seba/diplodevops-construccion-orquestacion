## 03 - upgrade k8s
# Intro

En este practico se realizará la actualizacion de un k8s reduciendo al minimo posible el downtime de una aplicación.
Se pensará como un caso practico en que el tiempo que la aplicación no esté disponible será tiempo que perjudicará a los clientes.

## Setup

```
k3d cluster create diplodevops-lab14 --config 14-k3d-setup-lab.yaml --kubeconfig-switch-context
k3d kubeconfig write diplodevops-lab14

alias update-k8s-diplo-06='export KUBECONFIG=$HOME/.config/k3d/kubeconfig-diplodevops-lab14.yaml'
alias unset-k8s-diplo-06='unset KUBECONFIG'

```

```
k3d cluster delete diplodevops-lab14
```

## Uptime

Para este laboratorio será necesario crear una aplicación que ejecute una carga simple, y un script local que hará reportes del uptime de la aplicación.

pip install requests keyboard

Hacemos build de la imagen
docker build -t uptime-app:v1 .

Importamos la imagen a K3D:
k3d image import uptime-app:v1 -c diplodevops-lab14

Esto "inyecta" la imagen a un registry que k3d puede pullear. Se debe importar cada vez que se haga un cambio en la imagen
Podemos verificar que la imagen fué importada:
docker exec k3d-diplodevops-lab14-agent-0 ctr image ls

Nota: K3S usa containerd, por eso usamos el comando ctr y no docker dentro del nodo

Para este práctico se ha deshabilitado traefik y en su lugar se instalará nginx

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.0/deploy/static/provider/cloud/deploy.yaml
Podemos revisar los logs del pod para ver que esté todo en orden
kubectl get pods -n ingress-nginx

Luego, aplicamos los manifiestos para instalar la app en el cluster.
Verificamos ingresando a http://diplodevops.example:8080/uptime-app/health

## Proceso

1- Tomar nota primero de la cantidad de nodos que hay en control plane y data plane.

2- Verificar que no hayan aplicaciones con problema de compatibilidad. Para eso, validar la documentacion oficial.

3- De ser necesario, realizar backups

4- Investigar sobre "cordon" y "drain" de los nodos. ¿Que diferencias tienen y cuando se aplica cada uno?

5- Tomar nota de la versión final a la que se quiere llegar. Investigar para que diferencias de versiones entre control plane y workers kubernetes nos garantiza su funcionamiento. La versión final debe ser la úlitma disponible a la fecha de la realización de este trabajo.

6- Realizar un runbook con el procedimiento completo. Anotar posibles eventualidades y procesos de rollback.

7- Cuando se tenga todo listo, antes de iniciar ejecutar el script de estadísticas "uptime".


Nota: para actualizar no hay un comando que lea el yaml y aplique los cambios. sin embargo, una vez modificado el yaml, podemos ejecutar:

```
k3d node create nodo-futurista \
    --cluster diplodevops-lab14 \
    --role agent \
    --image rancher/k3s:v1.29.1-k3s1
```

```
k3d node create nodo-futurista-controlador \
    --cluster diplodevops-lab14 \
    --role server \
    --image rancher/k3s:v1.29.1-k3s1
```

Ver logs 
```
docker logs k3d-nodo-futurista-controlador-0
````

Esto trae errores por que el cluster no se creó en modo HA para el control plane.
Recrearlo con 2 o 3 nodos.
Crearlo con 2 primero y ver que recomendación da k3d en el warning

Luego probar nuevamente


## Tips

Puede probar agregar un node selector al deployment. De esta forma, fuerza a nivel deployment que los pods de la app siempre eligan un nodo actualizado.

Otro truquito puede ser implementar un "pod disruption budget". Esto fuerza a que siempre exista una cantidad mínima determinada y configurable de pods. De esta forma, mientras se está realizando el upgrade, se reducen posibles downtimes.


## Uso de IA

Este es un caso de uso en que la IA nos puede asistir muy bien. Como habran notado, debemos investigar las matrices de compatibilades para 
definir si es seguro actualizar, o si primero debemos hacer upgrade de alguna dependencia.
Como hay que revisar mucha documentacion y es facil perderse, se pueden crear asistentes con herramientas que investiguen y referencien la web
(como deepresearch en gemini). Le importamos un archivo de configuracion del cluster (ej, con todos los helms listados), le seteamos
los promtps necesarios y pedimos que nos haga un análisis y un plan de actualizacion, con procesos de rollback, posibles riesgos y
SIEMPRE, pero SIEMPRE pedirle que:
- No asuma, pregunte lo necesario
- Haga una nota al pie con la documentación que respalde sus afirmaciones
- Validar el output.