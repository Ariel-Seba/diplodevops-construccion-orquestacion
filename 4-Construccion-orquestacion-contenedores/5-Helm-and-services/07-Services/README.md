# Clase 5 - Services

En esta sección practica veremos los manifiestos de 3 tipos de services

### nodePort

Este es el tipo de service que utilizamos hasta el momento. Accedemos a la aplicacion mediante <IP nodo>:<puerto expuesto>
nota para Mac: Debido a que estamos haciendo un mapeo de puertos (30080), en vez de ip nodo debemos usar localhost
~~~
kubectl get nodes -o wide
kubectl get services -n intro-k8s
~~~

### ClusterIP

Al usar este tipo de service, la IP asignada es privada dentro del cluster. Solo se puede acceder mediante algun "intermediario" que se exponga (lo veremos la proxima clase). Sin embargo, a los fines de pruebas y ya que disponemos de conexion al cluster (recordemos kubeconfig), podemos utilizar la herramienta de "port forward"

~~~
kubectl port-forward service/app-saludo-service 9091:8081 -n intro-k8s
~~~

(El puerto 9091 es de nuestra maquina host, y en este ejemplo fué elegido al azar).

Luego, accedemos desde nuestro navegador mediante localhost:9091

Documentacion: https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/

### LoadBalancer

Este tipo de service NO lo mostramos en el práctico, ya que tipicamente se utiliza en aquellos clusteres k8s de proveedores de nube. Se requiere de alguna solución que provea capacidades de balanceo de carga. Sin embargo, para aquellos que les interese el tema, se presenta el siguiente challenge.


### Challenge

Implementar un service del tipo Load Balancer en su cluster local. Ej, con MetalLB
Link de ayuda: https://medium.com/@shoaib_masood/metallb-network-loadbalancer-minikube-335d846dfdbe


### Troubleshooting

Si no pueden acceder a IPNODO:PUERTO_NODO en nodePort, para que el navegador llegue al NodePort, el tráfico debe hacer:
Navegador (Host) -> Docker Desktop (VM) -> Contenedor K3D (Nodo) -> Service -> Pod.
Si no mapeaste el puerto del rango 30000 en el archivo de configuración de K3D, la puerta del "Host" está cerrada

