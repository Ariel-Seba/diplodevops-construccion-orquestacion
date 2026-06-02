### Scheduling


### node label
Para modificar labels en nodo ya existente:
~~~
 kubectl label nodes <nombre> arch=arm
~~~

Eliminar label

~~~
 kubectl label --overwrite nodes <nombre> <label-key>-
~~~

Listar labels:

~~~
kubectl get nodes --show-labels
~~~

### Taint
Agregar taint a nodo ya existente:
~~~
 kubectl taint nodes <nombre> arch=arm:NoSchedule
 kubectl taint nodes <nombre> gpu=true:NoSchedule
~~~

Eliminar taint

~~~
 kubectl taint nodes <nombre> <taint-key>-
~~~

### Challenge

- Implementar affinity/antiaffinity necesaria para que los pods de "app-saludo" tiendan a desplegarse "cerca entre ellos".
- Implementar affinity/antiaffinity necesaria para que los pods de "app-contador" se esparsan.

### Links extras
- https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes/
- https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity/
- https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/